"""Reconcile existing ownership only from an authenticated date-only command and its preimage."""

from contextlib import nullcontext
from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, datetime
import hashlib
import json
import secrets
from threading import Lock

from sqlalchemy import Text, cast, func, literal, literal_column, select, update
from app.config import get_settings

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
_SCOPE_FIELDS = ("id", "project_id", "calendar_id", "name", "manager_email", "start_date")


@dataclass(frozen=True)
class SnapshotIdentity:
    id: int
    checksum: str
    input_revision: int
    created_at: datetime
    previous_end: str


@dataclass(frozen=True)
class _SavedTask:
    version: int
    context_digest: str
    iteration_digest: str
    previous_end: str


# Each entry is content-bound and retains only dates, versions and digests.
# No task text, snapshot payload or authority decision is kept in this cache.
_SNAPSHOT_CACHE: OrderedDict[tuple, OrderedDict[int, _SavedTask]] = OrderedDict()
_CACHE_LOCK = Lock()
_MAX_SNAPSHOTS = 16
_MAX_TASKS_PER_SNAPSHOT = 32


def _cached_task(key, task_id):
    with _CACHE_LOCK:
        tasks = _SNAPSHOT_CACHE.get(key)
        if tasks is None:
            return False, None
        _SNAPSHOT_CACHE.move_to_end(key)
        return True, tasks.get(task_id)


def _remember_task(key, task_id, view):
    with _CACHE_LOCK:
        tasks = _SNAPSHOT_CACHE.setdefault(key, OrderedDict())
        _SNAPSHOT_CACHE.move_to_end(key)
        tasks[task_id] = view
        if len(tasks) > _MAX_TASKS_PER_SNAPSHOT:
            tasks.popitem(last=False)
        if len(_SNAPSHOT_CACHE) > _MAX_SNAPSHOTS:
            _SNAPSHOT_CACHE.popitem(last=False)


def _canonical_snapshot_checksum(payload):
    return hashlib.sha256(SnapshotService._encode(payload)).hexdigest()


def _snapshot_task(
    snapshot,
    task_id,
    expected_version,
    expected_context,
    expected_scope,
    next_end,
    *,
    cache_reads,
    source_text=None,
):
    # CAST(... AS TEXT) supplies the actual bytes represented by the current
    # row on either engine. A changed payload paired with an old stored
    # checksum thus cannot hit a prior cache entry.
    raw = source_text if source_text is not None else snapshot.raw_payload
    encoded = raw.encode("utf-8") if isinstance(raw, str) else None
    if encoded is not None and len(encoded) > get_settings().snapshot_max_bytes * 6 + 1024:
        return None, "valid_before_image"
    native_fingerprint = getattr(snapshot, "raw_fingerprint", None)
    fingerprint = bytes(native_fingerprint) if native_fingerprint is not None else None
    if encoded is not None and (cache_reads or fingerprint is not None):
        fetched = hashlib.sha256(encoded).digest()
        if fingerprint is not None and fetched != fingerprint:
            return None, "matching_iteration_cutoff"
        fingerprint = fetched
    key = (snapshot.id, snapshot.checksum, fingerprint) if cache_reads and fingerprint is not None else None
    verified, view = _cached_task(key, task_id) if key else (False, None)
    try:
        if view is None:
            if encoded is None:
                return None, "snapshot_payload_required"
            payload = json.loads(encoded)
            scope = payload["iteration"]
            if payload["snapshot_info"]["reason"] != "before_planning_input_change":
                return None, "matching_iteration_cutoff"
            rows = _saved_tasks(payload["tasks"], task_id)
            if len(rows) != 1 or rows[0]["status"] == "closed":
                return None, "one_task_reservation"
            view = _SavedTask(
                rows[0]["version"],
                digest({k: v for k, v in rows[0].items() if k != "version"}),
                digest({field: scope.get(field) for field in _SCOPE_FIELDS}),
                scope["end_date"],
            )
        if type(view.version) is not int or view.version != expected_version:
            return None, "one_task_reservation"
        if view.context_digest != expected_context:
            return None, "unchanged_saved_task"
        if view.iteration_digest != expected_scope:
            return None, "matching_iteration_scope"
        if not date.fromisoformat(view.previous_end) < next_end:
            return None, "matching_iteration_cutoff"
        if not verified and _canonical_snapshot_checksum(payload) != snapshot.checksum:
            return None, "matching_iteration_cutoff"
    except (TypeError, ValueError, KeyError):
        return None, "valid_before_image"
    if key:
        _remember_task(key, task_id, view)
    return view, None


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


async def _planning_proof(db, task, receipt_id, *, after_recovery=False, cache_reads=False, lock=False):
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
    iteration = await db.get(Iteration, task.iteration_id)
    if (
        not iteration
        or iteration.end_date != next_end
        or result.get("id") != iteration.id
        or result.get("project_id") != task.project_id
        or iteration.project_id != task.project_id
    ):
        return None, "matching_iteration_cutoff"
    current_scope = {}
    for field in _SCOPE_FIELDS:
        value = getattr(iteration, field)
        current_scope[field] = value.isoformat() if isinstance(value, date) else value
    if any(result.get(field) != value for field, value in current_scope.items()):
        return None, "matching_iteration_scope"
    if task.status == "closed" or task.children:
        return None, "unchanged_saved_task"
    current = SnapshotService(db)._task_to_export(task)
    current_context = digest({field: value for field, value in current.items() if field != "version"})
    principal = await db.scalar(select(Principal.id).where(Principal.agent_actor_id == issued.actor_id))
    raw_column = cast(ApplicationSnapshot.payload, Text)
    database_fingerprint = cache_reads and not lock and db.get_bind().dialect.name == "postgresql"
    query = (
        select(
            ApplicationSnapshot.id,
            ApplicationSnapshot.checksum,
            ApplicationSnapshot.input_revision,
            ApplicationSnapshot.created_at,
            (literal(None) if database_fingerprint else raw_column).label("raw_payload"),
            (
                func.sha256(func.convert_to(raw_column, literal_column("'UTF8'")))
                if database_fingerprint
                else literal(None)
            ).label("raw_fingerprint"),
        )
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
    matches = (await db.execute(query.with_for_update(read=True) if lock else query)).all()
    if not principal or len(matches) != 1:
        return None, "unique_server_snapshot"
    row = matches[0]
    arguments = (
        row,
        task.id,
        task.version - (2 if after_recovery else 1),
        current_context,
        digest(current_scope),
        next_end,
    )
    view, missing = _snapshot_task(*arguments, cache_reads=cache_reads and not lock)
    if database_fingerprint and missing == "snapshot_payload_required":
        # PostgreSQL can check row content without sending the full snapshot to
        # the API on a warm poll. Recheck the bytes after a cold two-query read
        # so an intervening update or retention cleanup cannot populate the cache.
        raw = await db.scalar(
            select(raw_column).where(
                ApplicationSnapshot.id == row.id, ApplicationSnapshot.checksum == row.checksum
            )
        )
        if raw is None:
            return None, "unique_server_snapshot"
        view, missing = _snapshot_task(*arguments, cache_reads=True, source_text=raw)
    if missing:
        return None, missing
    identity = SnapshotIdentity(row.id, row.checksum, row.input_revision, row.created_at, view.previous_end)
    return (issued, identity, view.version), None


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
        proof, missing = await _planning_proof(db, task, receipt_id, lock=apply)
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
                "previous_end": snapshot.previous_end,
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
