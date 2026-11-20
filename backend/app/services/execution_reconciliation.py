"""Recover immutable run evidence from authenticated, contemporaneous server receipts."""

from __future__ import annotations

import json
import re

from sqlalchemy import select

from app.authority import require_operator
from app.models.agent import AgentIdempotencyRecord, AgentRun, AgentTeamTopologyMember, TaskEvent
from app.query_limits import MAX_BOUNDED_LIST_ITEMS
from app.services.agent_routing_policy import ROUTING_DECISION_AUTHORITY
from app.services.agent_team_setup_service import _digest
from app.utils.time import as_utc


async def _ack_at_begin(db, run, supplied):
    event = await db.scalar(select(TaskEvent).where(TaskEvent.task_id.is_(None), TaskEvent.actor_id == run.actor_id,
        TaskEvent.actor_type == "agent", TaskEvent.event_type == "agent.team_runtime_acknowledged",
        TaskEvent.created_at <= run.started_at).order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc()).limit(1))
    if event is None:
        return None, None
    anchor = json.loads(event.payload)
    member = await db.scalar(select(AgentTeamTopologyMember).where(
        AgentTeamTopologyMember.actor_id == run.actor_id, AgentTeamTopologyMember.created_at <= run.started_at))
    if (member is None or member.updated_at is None or as_utc(member.updated_at) > as_utc(run.started_at)
            or anchor.get("actor_id") != run.actor_id or not anchor.get("runtime_ready")):
        return None, None
    archived = supplied or json.loads(member.runtime_acknowledgement_payload or "{}")
    if (_digest(archived) != anchor.get("acknowledgement_digest")
            or archived.get("actor_key") != anchor.get("actor_key")
            or archived.get("topology_key") != anchor.get("topology_key")
            or archived.get("topology_revision") != anchor.get("topology_revision")):
        return None, None
    return archived, event.id


async def _archived_bindings(db, run):
    """Only server-owned operator/admin receipts, at or before the actual start."""
    records = (await db.scalars(select(AgentIdempotencyRecord).where(
        AgentIdempotencyRecord.target_type == "model_binding",
        AgentIdempotencyRecord.operation.in_(("model_binding.create", "model_binding.update")),
        AgentIdempotencyRecord.created_at <= run.started_at,
    ).order_by(AgentIdempotencyRecord.created_at.desc()).limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
    if len(records) > MAX_BOUNDED_LIST_ITEMS:
        return []
    result = []
    for record in records:
        receipt = json.loads(record.response_payload).get("response", {})
        binding = receipt.get("result", {})
        if (binding.get("actor_id") == run.actor_id and binding.get("enabled")
                and binding.get("id") == receipt.get("target_id")
                and binding.get("revision") == receipt.get("authoritative_revision")):
            result.append((record.id, binding))
    return result


async def reconcile_execution(db, run_id, *, apply=False, archived_ack=None):
    """An operator may supply an archived acknowledgement only as a preimage of the server's original digest."""
    require_operator(db)
    query = select(AgentRun).where(AgentRun.id == run_id)
    run = await db.scalar(query.with_for_update() if apply else query)
    if run is None:
        raise ValueError("Run not found")
    result = {"run_id": run.id, "model_trust_state": run.model_trust_state, "source_receipts": {},
              "missing": [], "applied": False}
    if run.status == "running" or run.assignment_id is None or run.claim_generation is None:
        result["missing"].append("terminal_assigned_execution")
        return result
    begin = await db.scalar(select(AgentIdempotencyRecord).where(AgentIdempotencyRecord.actor_id == run.actor_id,
        AgentIdempotencyRecord.operation == "work.begin", AgentIdempotencyRecord.target_type == "assignment",
        AgentIdempotencyRecord.target_id == run.assignment_id))
    snapshot = json.loads(begin.response_payload).get("response_without_claim_id", {}) if begin else {}
    original, assignment = snapshot.get("run", {}), snapshot.get("assignment", {})
    if (original.get("id") != run.id or original.get("actor_id") != run.actor_id
            or original.get("task_id") != run.task_id or original.get("assignment_id") != run.assignment_id
            or original.get("claim_generation") != run.claim_generation or assignment.get("actor_id") != run.actor_id
            or assignment.get("id") != run.assignment_id or assignment.get("purpose") != "execution"):
        result["missing"].append("authenticated_begin_receipt")
        return result
    result["source_receipts"]["begin"] = begin.id
    stored = run.execution_provenance or {}
    evidence = dict(original.get("execution_provenance") or stored)
    evidence["actor_id"] = run.actor_id
    decision = assignment.get("routing_snapshot") or {}
    governed = (decision.get("schema_version") == "routing-decision-snapshot-v1"
                and decision.get("authority") == ROUTING_DECISION_AUTHORITY and decision.get("actor_id") == run.actor_id
                and decision.get("task_id") == run.task_id and decision.get("purpose") == "execution")
    ack, ack_id = await _ack_at_begin(db, run, archived_ack)
    if governed:
        evidence.setdefault("profile_id", decision.get("profile_id"))
        evidence.setdefault("profile_revision", decision.get("profile_revision"))
    elif ack:
        profile = re.fullmatch(r"p([1-9][0-9]*)-[0-9a-f]{24}", str(ack.get("profile_revision")))
        if profile:
            evidence.setdefault("profile_id", int(profile[1]))
            evidence.setdefault("profile_revision", ack["profile_revision"])
        result["source_receipts"]["runtime_ack_event"] = ack_id
    observed = original.get("resolved_model_id") or original.get("model")
    if not evidence.get("publisher_key") and observed:
        matches = {}
        for source_id, binding in await _archived_bindings(db, run):
            catalog = binding.get("model_catalog") or binding.get("catalog") or {}
            if (not catalog.get("publisher_key") or not catalog.get("enabled")
                    or observed not in {catalog.get("key"), catalog.get("configured_model_alias")}):
                continue
            if governed:
                exact = (original.get("model_binding_id") == decision.get("model_binding_id") == binding["id"]
                         and original.get("model_binding_revision") == decision.get("model_binding_revision") == binding["revision"]
                         and catalog.get("id") == decision.get("model_catalog_id")
                         and catalog.get("revision") == decision.get("model_catalog_revision"))
            else:
                exact = bool(ack and ack["model_binding_revisions"].get(catalog["key"]) == binding["revision"])
            if exact:
                matches[(binding["id"], binding["revision"], catalog["id"], catalog["revision"])] = (source_id, binding, catalog)
        if len(matches) == 1:
            source_id, binding, catalog = next(iter(matches.values()))
            evidence.update(binding_id=binding["id"], binding_revision=binding["revision"], catalog_id=catalog["id"],
                            catalog_revision=catalog["revision"], catalog_key=catalog["key"],
                            configured_model_alias=catalog["configured_model_alias"], publisher_key=catalog["publisher_key"])
            result["source_receipts"]["model_binding"] = source_id
    for field in ("profile_id", "profile_revision", "publisher_key"):
        if not evidence.get(field):
            result["missing"].append(field)
    result["provenance"] = evidence
    if (apply and evidence.get("profile_id") and evidence != stored
            and all(value is None or evidence.get(field) == value for field, value in stored.items())):
        run.execution_provenance = evidence
        db.add(TaskEvent(task_id=run.task_id, event_type="agent.execution_provenance_reconciled", actor_type="operator",
            payload=json.dumps({"run_id": run.id, "source_receipts": result["source_receipts"],
                                "missing": result["missing"], "model_trust_state": run.model_trust_state})))
        await db.flush()
        result["applied"] = True
    return result
