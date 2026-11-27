"""Reconcile a terminal run using authenticated, contemporaneous server records."""

from __future__ import annotations

import json
import re
from contextlib import nullcontext

from sqlalchemy import JSON, cast, func, select, update

from app.authority import AuthorityError, require_operator
from app.commands import command_transaction
from app.models.agent import AgentIdempotencyRecord, AgentRun, AgentTeamTopologyMember, TaskEvent
from app.models.identity import CommandAudit
from app.models.task import Task
from app.query_limits import MAX_BOUNDED_LIST_ITEMS
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_team_setup import AgentTeamRuntimeAcknowledgement
from app.services.agent_model_catalog_service import AgentModelConflictError
from app.services.agent_routing_policy import ROUTING_DECISION_AUTHORITY
from app.services.agent_service import actor_has_scope, is_admin_key_principal
from app.services.agent_team_setup_service import _digest
from app.utils.time import as_utc


ACTION = "agent.execution_provenance_reconciled"
HISTORY_EVENT = "agent.model_configuration_changed"


def _object(encoded):
    try:
        value = json.loads(encoded)
    except (TypeError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _json_value(db, column, *path, integer=False):
    """Task event payloads are historical text on both supported databases."""
    if db.get_bind().dialect.name == "sqlite":
        return func.json_extract(column, "$." + ".".join(path))
    value = cast(column, JSON)
    for key in path:
        value = value[key]
    return value.as_integer() if integer else value.as_string()


async def _ack_at_begin(db, run, supplied):
    event = await db.scalar(
        select(TaskEvent)
        .where(
            TaskEvent.task_id.is_(None),
            TaskEvent.actor_id == run.actor_id,
            TaskEvent.actor_type == "agent",
            TaskEvent.event_type == "agent.team_runtime_acknowledged",
            TaskEvent.created_at <= run.started_at,
        )
        .order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc())
        .limit(1)
    )
    if event is None or as_utc(event.created_at) == as_utc(run.started_at):
        return None, None
    anchor = _object(event.payload)
    if anchor.get("actor_id") != run.actor_id or anchor.get("runtime_ready") is not True:
        return None, None
    if supplied is None:
        member = await db.scalar(
            select(AgentTeamTopologyMember).where(
                AgentTeamTopologyMember.actor_id == run.actor_id,
                AgentTeamTopologyMember.actor_key == anchor.get("actor_key"),
            )
        )
        archived = _object(member.runtime_acknowledgement_payload) if member else {}
    else:
        archived = supplied
    if (
        not isinstance(archived, dict)
        or _digest(archived) != anchor.get("acknowledgement_digest")
        or any(
            archived.get(key) != anchor.get(key) for key in ("actor_key", "topology_key", "topology_revision")
        )
    ):
        return None, None
    return archived, event.id


async def _latest_configuration(db, run, kind, target_id):
    """An operator-only mutation without a full historic record fences off older evidence."""
    payload = TaskEvent.payload
    event = await db.scalar(
        select(TaskEvent)
        .where(
            TaskEvent.task_id.is_(None),
            TaskEvent.event_type == HISTORY_EVENT,
            TaskEvent.created_at <= run.started_at,
            _json_value(db, payload, "target_type") == kind,
            _json_value(db, payload, "target_id", integer=True) == target_id,
        )
        .order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc())
        .limit(1)
    )
    if event is None or as_utc(event.created_at) == as_utc(run.started_at):
        return {}, {}
    anchor = _object(event.payload)
    if anchor.get("operation") not in {kind + ".create", kind + ".update", kind + ".disable"}:
        return {}, {}
    sources = {kind + "_event": event.id}
    configuration = anchor.get("configuration")
    if configuration is None and event.actor_id is not None:
        record = await db.scalar(
            select(AgentIdempotencyRecord)
            .where(
                AgentIdempotencyRecord.actor_id == event.actor_id,
                AgentIdempotencyRecord.operation == anchor["operation"],
                AgentIdempotencyRecord.target_type == kind,
                AgentIdempotencyRecord.idempotency_key == event.idempotency_key,
                AgentIdempotencyRecord.created_at <= run.started_at,
                _json_value(
                    db, AgentIdempotencyRecord.response_payload, "response", "target_id", integer=True
                )
                == target_id,
            )
            .limit(1)
        )
        receipt = _object(record.response_payload).get("response", {}) if record else {}
        if (
            isinstance(receipt, dict)
            and event.id in receipt.get("audit_event_ids", [])
            and receipt.get("authoritative_revision") == anchor.get("authoritative_revision")
        ):
            configuration = receipt.get("result")
            sources[kind] = record.id
    if (
        not isinstance(configuration, dict)
        or configuration.get("id") != target_id
        or configuration.get("revision") != anchor.get("authoritative_revision")
    ):
        return {}, sources
    return configuration, sources


async def _actor_binding_ids(db, run):
    payload = TaskEvent.payload
    event_id = _json_value(db, payload, "target_id", integer=True)
    events = (
        await db.scalars(
            select(event_id)
            .distinct()
            .where(
                TaskEvent.task_id.is_(None),
                TaskEvent.event_type == HISTORY_EVENT,
                TaskEvent.created_at <= run.started_at,
                _json_value(db, payload, "target_type") == "model_binding",
                _json_value(db, payload, "configuration", "actor_id", integer=True) == run.actor_id,
            )
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
    ).all()
    receipt = AgentIdempotencyRecord.response_payload
    resource_id = _json_value(db, receipt, "response", "target_id", integer=True)
    records = (
        await db.scalars(
            select(resource_id)
            .distinct()
            .where(
                AgentIdempotencyRecord.operation.in_(
                    ("model_binding.create", "model_binding.update", "model_binding.disable")
                ),
                AgentIdempotencyRecord.target_type == "model_binding",
                AgentIdempotencyRecord.created_at <= run.started_at,
                _json_value(db, receipt, "response", "result", "actor_id", integer=True) == run.actor_id,
            )
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
    ).all()
    ids = {value for value in (*events, *records) if type(value) is int and value > 0}
    if len(ids) > MAX_BOUNDED_LIST_ITEMS:
        return [], "receipt_history_exceeds_bound"
    return sorted(ids), None


async def _model_at_begin(db, run, original, governed, ack):
    observed = original.get("resolved_model_id") or original.get("model")
    if not observed:
        return {}, {}, []
    if governed:
        ids = [governed.get("model_binding_id")]
    else:
        revisions = (ack or {}).get("model_binding_revisions")
        if not isinstance(revisions, dict) or not revisions:
            return {}, {}, []
        ids, gap = await _actor_binding_ids(db, run)
        if gap:
            return {}, {}, [gap]
    matches, gaps = [], []
    for binding_id in ids:
        if type(binding_id) is not int:
            continue
        binding, sources = await _latest_configuration(db, run, "model_binding", binding_id)
        if binding.get("actor_id") != run.actor_id or binding.get("enabled") is not True:
            continue
        embedded = binding.get("model_catalog") or {}
        if observed not in (embedded.get("key"), embedded.get("configured_model_alias")):
            continue
        catalog, catalog_sources = await _latest_configuration(db, run, "model_catalog", embedded.get("id"))
        if (
            not catalog
            or catalog.get("revision") != embedded.get("revision")
            or governed
            and governed.get("model_catalog_revision") != catalog.get("revision")
        ):
            gaps.append("catalog_revision_at_start")
            continue
        if governed:
            if (
                original.get("model_binding_id") != binding_id
                or original.get("model_binding_revision") != governed.get("model_binding_revision")
                or governed.get("model_binding_revision") != binding.get("revision")
                or governed.get("model_catalog_id") != embedded.get("id")
            ):
                continue
        elif revisions.get(embedded.get("key")) != binding.get("revision"):
            continue
        if (
            catalog.get("enabled") is True
            and catalog.get("publisher_key")
            and all(
                catalog.get(k) == embedded.get(k)
                for k in ("id", "key", "configured_model_alias", "publisher_key")
            )
        ):
            matches.append(
                (
                    {
                        "binding_id": binding_id,
                        "binding_revision": binding["revision"],
                        "catalog_id": catalog["id"],
                        "catalog_revision": catalog["revision"],
                        "catalog_key": catalog["key"],
                        "configured_model_alias": catalog["configured_model_alias"],
                        "publisher_key": catalog["publisher_key"],
                    },
                    {**sources, **catalog_sources},
                )
            )
    if len(matches) == 1 and not gaps:
        return *matches[0], []
    if len(matches) > 1:
        gaps.append("ambiguous_model_binding")
    return {}, {}, sorted(set(gaps))


async def _observations(db, run, archived_ack):
    result = {
        "run_id": run.id,
        "model_trust_state": run.model_trust_state,
        "source_receipts": {},
        "missing": [],
        "applied": False,
    }
    stored = run.execution_provenance or {}
    evidence = dict(stored)
    result["provenance"] = evidence
    if run.status == "running" or run.assignment_id is None or run.claim_generation is None:
        result["missing"].append("terminal_assigned_execution")
        return result
    begin = await db.scalar(
        select(AgentIdempotencyRecord)
        .where(
            AgentIdempotencyRecord.actor_id == run.actor_id,
            AgentIdempotencyRecord.operation == "work.begin",
            AgentIdempotencyRecord.target_type == "assignment",
            AgentIdempotencyRecord.target_id == run.assignment_id,
            _json_value(
                db,
                AgentIdempotencyRecord.response_payload,
                "response_without_claim_id",
                "run",
                "id",
                integer=True,
            )
            == run.id,
        )
        .order_by(AgentIdempotencyRecord.id)
        .limit(1)
    )
    snapshot = _object(begin.response_payload).get("response_without_claim_id", {}) if begin else {}
    original, assignment = snapshot.get("run", {}), snapshot.get("assignment", {})
    if (
        original.get("id") != run.id
        or original.get("actor_id") != run.actor_id
        or original.get("task_id") != run.task_id
        or original.get("assignment_id") != run.assignment_id
        or original.get("claim_generation") != run.claim_generation
        or assignment.get("actor_id") != run.actor_id
        or assignment.get("id") != run.assignment_id
        or assignment.get("purpose") != "execution"
    ):
        result["missing"].append("authenticated_begin_receipt")
        return result
    result["source_receipts"]["begin"] = begin.id
    recovered = {k: v for k, v in (original.get("execution_provenance") or {}).items() if v is not None}
    recovered["actor_id"] = run.actor_id
    decision = assignment.get("routing_snapshot") or {}
    governed = (
        decision
        if (
            decision.get("schema_version") == "routing-decision-snapshot-v1"
            and decision.get("authority") == ROUTING_DECISION_AUTHORITY
            and decision.get("actor_id") == run.actor_id
            and decision.get("task_id") == run.task_id
            and decision.get("purpose") == "execution"
        )
        else {}
    )
    ack, ack_id = await _ack_at_begin(db, run, archived_ack) if not governed else (None, None)
    if governed:
        recovered.update(
            profile_id=governed.get("profile_id"), profile_revision=governed.get("profile_revision")
        )
    elif ack:
        profile = re.fullmatch(r"p([1-9][0-9]*)-[0-9a-f]{24}", str(ack.get("profile_revision")))
        if profile:
            recovered.update(profile_id=int(profile[1]), profile_revision=ack["profile_revision"])
        result["source_receipts"]["runtime_ack_event"] = ack_id
    if not (stored.get("publisher_key") or recovered.get("publisher_key")):
        model, sources, gaps = await _model_at_begin(db, run, original, governed, ack)
        recovered.update(model)
        result["source_receipts"].update(sources)
        result["missing"].extend(gaps)
    for key, value in recovered.items():
        if value is None:
            continue
        if evidence.get(key) is None:
            evidence[key] = value
        elif evidence[key] != value:
            result["missing"].append("conflicting_stored_evidence")
            break
    terminal = evidence.get("terminal_model") or {}
    if terminal.get("source") == "server_interruption" and not terminal.get("publisher_key"):
        from app.services.review_provenance import recover_terminal_observation

        observation, sources = await recover_terminal_observation(db, run)
        if observation:
            evidence["terminal_model"] = observation
            result["source_receipts"].update(sources)
        else:
            result["missing"].append("terminal_model")
    result["missing"].extend(
        k for k in ("profile_id", "profile_revision", "publisher_key") if not evidence.get(k)
    )
    return result


async def reconcile_execution(
    db, run_id, *, apply=False, archived_ack=None, expected_evidence_digest=None, command=None
):
    require_operator(db)
    principal = db.info["authority"]
    if principal.read_only or principal.principal_id is None:
        raise AuthorityError("operator_required", "An authenticated workspace operator is required.")
    if apply and (not isinstance(command, AgentPlanningCommandContext) or not expected_evidence_digest):
        raise ValueError("Apply requires command metadata and the preview evidence digest")
    async with command_transaction(db) if apply else nullcontext():
        if apply and db.get_bind().dialect.name == "sqlite":
            # SQLite ignores SELECT FOR UPDATE. Reserve only this target before reading its receipt.
            await db.execute(update(AgentRun).where(AgentRun.id == run_id).values(id=AgentRun.id))
        query = select(AgentRun).where(AgentRun.id == run_id).execution_options(populate_existing=True)
        run = await db.scalar(query.with_for_update() if apply else query)
        if run is None:
            raise LookupError("Run not found")
        if apply:
            request_hash = _digest(
                {
                    "run_id": run.id,
                    "expected_evidence_digest": expected_evidence_digest,
                    "acknowledgement_digest": _digest(archived_ack) if archived_ack is not None else None,
                    "command": command.model_dump(mode="json"),
                }
            )
            previous = await db.scalar(
                select(CommandAudit).where(
                    CommandAudit.action == ACTION,
                    CommandAudit.principal_id == principal.principal_id,
                    CommandAudit.details["run_id"].as_integer() == run.id,
                    CommandAudit.details["idempotency_key"].as_string() == command.idempotency_key,
                )
            )
            if previous:
                if previous.details["request_hash"] != request_hash:
                    raise AgentModelConflictError(
                        "reconciliation_idempotency_conflict",
                        "The command key was used with a different request",
                    )
                return previous.details["response"]
        result = await _observations(db, run, archived_ack)
        stored = run.execution_provenance or {}
        result["evidence_digest"] = _digest({"stored": stored, "observed": result})
        if not apply:
            return result
        if result["evidence_digest"] != expected_evidence_digest:
            raise AgentModelConflictError(
                "reconciliation_evidence_stale", "Inspect the current evidence before applying"
            )
        evidence = result["provenance"]
        if (
            (evidence.get("profile_id") or result["source_receipts"].get("renew"))
            and evidence != stored
            and "conflicting_stored_evidence" not in result["missing"]
        ):
            run.execution_provenance = evidence
            result["applied"] = True
        project_id = await db.scalar(select(Task.project_id).where(Task.id == run.task_id))
        event = TaskEvent(
            task_id=run.task_id,
            actor_type="operator",
            event_type=ACTION,
            correlation_id=command.correlation_id,
            idempotency_key=command.idempotency_key,
            payload=json.dumps(
                {
                    "run_id": run.id,
                    "principal_id": principal.principal_id,
                    "operator_actor_id": principal.actor_id,
                    "applied": result["applied"],
                    "source_receipts": result["source_receipts"],
                    "missing": result["missing"],
                    "model_trust_state": run.model_trust_state,
                }
            ),
        )
        db.add(event)
        await db.flush()
        result["event_id"] = event.id
        result["principal_id"] = principal.principal_id
        db.add(
            CommandAudit(
                principal_id=principal.principal_id,
                project_id=project_id,
                action=ACTION,
                source=principal.source,
                correlation_id=command.correlation_id[:128],
                reason=command.rationale,
                details={
                    "run_id": run.id,
                    "idempotency_key": command.idempotency_key,
                    "request_hash": request_hash,
                    "response": result,
                },
            )
        )
        return result


async def reconcile_execution_request(
    db,
    actor,
    run_id,
    *,
    apply=False,
    expected_evidence_digest=None,
    archived_acknowledgement=None,
    idempotency_key=None,
    rationale=None,
    correlation_id=None,
):
    require_operator(db)
    authority = db.info["authority"]
    if not (
        is_admin_key_principal(actor)
        and authority.kind == "system"
        or actor.id > 0
        and authority.actor_id == actor.id
        and actor_has_scope(actor, "admin")
    ):
        raise AuthorityError(
            "operator_required", "The credential must identify the authenticated workspace operator."
        )
    command = None
    if apply or any(value is not None for value in (idempotency_key, rationale, correlation_id)):
        command = AgentPlanningCommandContext(
            idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id
        )
    archived = None
    if archived_acknowledgement is not None:
        archived = AgentTeamRuntimeAcknowledgement.model_validate(archived_acknowledgement).stored_content()
    return await reconcile_execution(
        db,
        run_id,
        apply=apply,
        expected_evidence_digest=expected_evidence_digest,
        archived_ack=archived,
        command=command,
    )
