"""Reconcile existing ownership only from an authenticated date-only command and its preimage."""

from contextlib import nullcontext
from datetime import date
import hashlib
import json
import secrets

from sqlalchemy import select, update

from app.authority import AuthorityError, require_operator
from app.commands import command_transaction
from app.models.agent import AgentIdempotencyRecord, TaskEvent
from app.models.identity import CommandAudit, Principal
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task
from app.schemas.agent_planning import AgentPlanningCommandContext, AgentPlanningReceipt
from app.services.agent_model_catalog_service import AgentModelConflictError
from app.services.agent_planning_service import AgentPlanningService
from app.services.agent_service import actor_has_scope, is_admin_key_principal, validate_idempotency_key
from app.services import execution_planning_window
from app.services.execution_planning_window import digest, live_assignments, make_window, original_ownership
from app.services.snapshot_service import SnapshotService
from app.services.task_service import TaskService


ACTION = "agent.planning_window_reconciled"


async def source_receipt_id(db, operation, target_type, target_id, *, receipt_id, actor_id, command_key):
    """Resolve an exact ordinary PM receipt using identifiers returned by its public command."""
    if receipt_id is not None:
        if type(receipt_id) is not int or receipt_id < 1 or actor_id is not None or command_key is not None:
            raise ValueError(
                "Use either the receipt ID or the source command's actor ID and idempotency key."
            )
        return receipt_id
    if type(actor_id) is not int or actor_id < 1 or not command_key:
        raise ValueError("Supply the source command's actor ID and idempotency key.")
    validate_idempotency_key(command_key, required=True)
    return await db.scalar(
        select(AgentIdempotencyRecord.id).where(
            AgentIdempotencyRecord.actor_id == actor_id,
            AgentIdempotencyRecord.operation == operation,
            AgentIdempotencyRecord.target_type == target_type,
            AgentIdempotencyRecord.target_id == target_id,
            AgentIdempotencyRecord.idempotency_key == command_key,
        )
    )


def _saved_tasks(roots, task_id):
    pending = list(roots)
    matches = []
    while pending:
        current = pending.pop()
        if current["id"] == task_id:
            matches.append(current)
        pending.extend(current.get("children", ()))
    return matches


async def _planning_proof(db, task, receipt_id, *, after_recovery=False):
    if not receipt_id:
        return None, "planning_receipt"
    issued = await db.get(AgentIdempotencyRecord, receipt_id)
    if (
        not issued
        or issued.operation != "planning.iteration.update"
        or issued.target_type != "iteration"
        or issued.target_id != task.iteration_id
    ):
        return None, "planning_receipt"
    try:
        recorded = AgentPlanningReceipt.model_validate(json.loads(issued.response_payload)["response"])
        result = recorded.result
        revision = result["revision"] - 1
        next_end = date.fromisoformat(result["end_date"])
        if (
            recorded.operation,
            recorded.target_type,
            recorded.target_id,
            recorded.actor_id,
            recorded.idempotency_key,
        ) != (
            issued.operation,
            issued.target_type,
            task.iteration_id,
            issued.actor_id,
            issued.idempotency_key,
        ):
            return None, "planning_receipt"
        expected = {str(task.iteration_id): revision}
        request = {
            "command": {"rationale": recorded.rationale, "correlation_id": recorded.correlation_id},
            "payload": {"end_date": next_end.isoformat(), "expected_revisions": expected},
        }
        possibilities = (request, {**request, "expected_revisions": expected})
        if not any(
            secrets.compare_digest(issued.request_hash, AgentPlanningService._request_hash(data))
            for data in possibilities
        ):
            return None, "end_date_only_request"
    except (TypeError, ValueError, KeyError):
        return None, "planning_receipt"
    principal = await db.scalar(select(Principal.id).where(Principal.agent_actor_id == issued.actor_id))
    matches = (
        await db.scalars(
            select(ApplicationSnapshot)
            .where(
                ApplicationSnapshot.iteration_id == task.iteration_id,
                ApplicationSnapshot.input_revision == revision,
                ApplicationSnapshot.provenance == "command",
                ApplicationSnapshot.schema_version == 2,
                ApplicationSnapshot.created_by_principal_id == principal,
                ApplicationSnapshot.created_at <= issued.created_at,
            )
            .limit(2)
        )
    ).all()
    if not principal or len(matches) != 1:
        return None, "unique_server_snapshot"
    snapshot = matches[0]
    payload = snapshot.payload
    iteration = await db.get(Iteration, task.iteration_id)
    try:
        if (
            hashlib.sha256(SnapshotService._encode(payload)).hexdigest() != snapshot.checksum
            or payload["snapshot_info"]["reason"] != "before_planning_input_change"
            or not date.fromisoformat(payload["iteration"]["end_date"]) < next_end
            or iteration.end_date != next_end
            or result["id"] != iteration.id
            or result["project_id"] != task.project_id
            or iteration.project_id != task.project_id
        ):
            return None, "matching_iteration_cutoff"
        for key in ("id", "project_id", "calendar_id", "name", "manager_email", "start_date"):
            value = getattr(iteration, key)
            current = value.isoformat() if isinstance(value, date) else value
            if payload["iteration"].get(key) != current or result.get(key) != current:
                return None, "matching_iteration_scope"
        rows = _saved_tasks(payload["tasks"], task.id)
        if (
            len(rows) != 1
            or rows[0]["status"] == "closed"
            or rows[0]["version"] + (2 if after_recovery else 1) != task.version
        ):
            return None, "one_task_reservation"
        current = SnapshotService(db)._task_to_export(task)
        if current != {**rows[0], "version": task.version} or current["children"]:
            return None, "unchanged_saved_task"
    except (KeyError, TypeError, ValueError):
        return None, "valid_before_image"
    return (issued, snapshot, rows[0]["version"]), None


async def reconcile_window(
    db,
    actor,
    task_id,
    receipt_id=None,
    *,
    planning_actor_id=None,
    planning_command_key=None,
    apply=False,
    expected_evidence_digest=None,
    idempotency_key=None,
    rationale=None,
    correlation_id=None,
):
    require_operator(db)
    principal = db.info["authority"]
    if (
        principal.read_only
        or principal.principal_id is None
        or not (
            is_admin_key_principal(actor)
            and principal.kind == "system"
            or actor.id > 0
            and actor.id == principal.actor_id
            and actor_has_scope(actor, "admin")
        )
    ):
        raise AuthorityError("operator_required", "An authenticated workspace operator is required.")
    command = None
    if apply:
        command = AgentPlanningCommandContext(
            idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id
        )
        if not expected_evidence_digest:
            raise ValueError("Apply requires the digest of a current reviewable preview.")
    async with command_transaction(db) if apply else nullcontext():
        iteration_id = await db.scalar(select(Task.iteration_id).where(Task.id == task_id))
        if not iteration_id:
            raise LookupError("Iteration task not found")
        receipt_id = await source_receipt_id(
            db,
            "planning.iteration.update",
            "iteration",
            iteration_id,
            receipt_id=receipt_id,
            actor_id=planning_actor_id,
            command_key=planning_command_key,
        )
        if apply:
            if db.get_bind().dialect.name == "sqlite":
                await db.execute(update(Task).where(Task.id == task_id).values(id=Task.id))
            else:
                await db.scalar(
                    select(Iteration.id)
                    .join(Task, Task.iteration_id == Iteration.id)
                    .where(Task.id == task_id)
                    .with_for_update(of=Iteration)
                )
            await db.scalar(select(Task.id).where(Task.id == task_id).with_for_update())
            request_hash = digest(
                {
                    "task": task_id,
                    "receipt": receipt_id,
                    "expected": expected_evidence_digest,
                    "command": command.model_dump(mode="json"),
                }
            )
            previous = await db.scalar(
                select(CommandAudit).where(
                    CommandAudit.action == ACTION,
                    CommandAudit.principal_id == principal.principal_id,
                    CommandAudit.details["task_id"].as_integer() == task_id,
                    CommandAudit.details["idempotency_key"].as_string() == idempotency_key,
                )
            )
            if previous:
                if previous.details["request_hash"] != request_hash:
                    raise AgentModelConflictError(
                        "reconciliation_idempotency_conflict",
                        "The command key is bound to a different request.",
                    )
                return previous.details["response"]
        task = await TaskService(db).get_by_id(task_id)
        if task is None:
            raise LookupError("Task not found")
        proof, missing = await _planning_proof(db, task, receipt_id)
        window = None
        sources = {}
        if not missing:
            issued, snapshot, old = proof
            assignments = (await live_assignments(db, [task.id], lock=apply)).get(task.id, [])
            evidence = {
                "planning_receipt_id": issued.id,
                "snapshot_id": snapshot.id,
                "snapshot_sha256": snapshot.checksum,
                "input_revision": snapshot.input_revision,
                "previous_end": snapshot.payload["iteration"]["end_date"],
                "new_end": json.loads(issued.response_payload)["response"]["result"]["end_date"],
            }
            for assignment in assignments:
                if assignment.task_version == old:
                    source = await original_ownership(db, task, assignment, snapshot.created_at)
                    if source:
                        sources[str(assignment.id)] = source
            if sources and len(sources) == len(assignments):
                window = make_window(task, old, assignments, evidence={**evidence, "ownership": sources})
                if window:
                    window = await execution_planning_window.seal_authority(
                        db, task, window, assignments, lock=apply, as_of=snapshot.created_at
                    )
            if not window or set(window["assignments"]) != set(sources):
                missing = "current_authority_and_original_ownership"
                window = None
        result = {
            "task_id": task.id,
            "task_version": task.version,
            "planning_receipt_id": receipt_id,
            "assignment_ids": sorted(map(int, sources)),
            "source_receipts": sources,
            "missing": [missing] if missing else [],
            "applied": False,
            "evidence_digest": digest(
                {
                    "task": task.id,
                    "version": task.version,
                    "window": window,
                    "receipt": receipt_id,
                    "missing": missing,
                }
            ),
        }
        if not apply:
            return result
        if result["missing"] or not secrets.compare_digest(
            result["evidence_digest"], expected_evidence_digest
        ):
            raise AgentModelConflictError(
                "planning_window_evidence_unavailable",
                "Refresh the preview and provide matching complete evidence.",
            )
        result["applied"] = task.execution_planning_window != window
        task.execution_planning_window = window
        event = TaskEvent(
            task_id=task.id,
            actor_type="operator",
            actor_id=principal.actor_id,
            event_type=ACTION,
            correlation_id=command.correlation_id,
            idempotency_key=idempotency_key,
            payload=json.dumps({**result, "principal_id": principal.principal_id}),
        )
        db.add(event)
        await db.flush()
        result.update(event_id=event.id, principal_id=principal.principal_id)
        db.add(
            CommandAudit(
                principal_id=principal.principal_id,
                project_id=task.project_id,
                action=ACTION,
                source=principal.source,
                correlation_id=command.correlation_id[:128],
                reason=command.rationale,
                details={
                    "task_id": task.id,
                    "idempotency_key": idempotency_key,
                    "request_hash": request_hash,
                    "response": result,
                },
            )
        )
        return result
