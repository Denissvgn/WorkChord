"""Attribute an interrupted, checkpointed output without altering its historical lease or terminal result."""

from __future__ import annotations

import hashlib
import json
import secrets

from sqlalchemy import select

from app.authority import internal_authority
from app.commands import command_transaction
from app.models.agent import AgentIdempotencyRecord, AgentRun, AgentRunEvent, TaskEvent
from app.schemas.agent import AgentRecoveryRequeueResponse, AgentRetainedOutputAttestation, TaskEventCreate
from app.services.agent_service import (
    AgentConflictError,
    AgentPermissionError,
    AgentService,
    require_scope,
    validate_idempotency_key,
)
from app.services.execution_planning_window import authority_stamp
from app.services.planning_window_reconciliation import _planning_proof, source_receipt_id
from app.services.review_provenance import actor_provenance, rework_binding_identity
from app.utils.github_links import parse_github_url
from app.utils.time import as_utc, utc_now


OPERATION = "work.attest_retained_planning_output"


def _unverified(reason):
    raise AgentConflictError(
        "The original planning change, expired fence, worker checkpoint and retained output must all match ("
        + reason
        + ")."
    )


async def _authenticate_checkpoint(db, actor, run, task, data, before_version):
    event = await db.get(TaskEvent, data.checkpoint_id)
    if (
        not event
        or event.actor_type != "agent"
        or event.actor_id != actor.id
        or event.task_id != task.id
        or event.event_type != "agent.checkpoint"
        or not event.idempotency_key
    ):
        _unverified("checkpoint_identity")
    receipt = await db.scalar(
        select(AgentIdempotencyRecord).where(
            AgentIdempotencyRecord.actor_id == actor.id,
            AgentIdempotencyRecord.operation == "task.event.append",
            AgentIdempotencyRecord.target_type == "task",
            AgentIdempotencyRecord.target_id == task.id,
            AgentIdempotencyRecord.idempotency_key == event.idempotency_key,
        )
    )
    content = json.loads(event.payload)
    commit = parse_github_url(data.commit_url)
    pull = parse_github_url(data.pr_url)
    if (
        not receipt
        or json.loads(receipt.response_payload).get("event_id") != event.id
        or commit.github_type != "commit"
        or pull.github_type != "pull_request"
        or commit.repo_full_name.casefold() != pull.repo_full_name.casefold()
        or as_utc(event.created_at) < as_utc(run.started_at)
        or as_utc(event.created_at) > as_utc(run.ended_at)
    ):
        _unverified("checkpoint_receipt_or_repository")
    facts = {
        "run_id": run.id,
        "assignment_id": run.assignment_id,
        "observed_model": data.observed_model,
        "model_publisher": run.execution_provenance["publisher_key"],
        "output_state": "retained",
        "candidate": commit.sha,
        "git_tree": data.git_tree,
        "pr_url": data.pr_url,
        "terminal_native_turn": data.terminal_native_turn,
        "brief_revision": task.brief_revision,
        "artifact_revision": task.artifact_revision,
        "stale_assignment_version": before_version,
        "observed_task_version": before_version + 1,
    }
    if any(content.get(key) != value for key, value in facts.items()):
        _unverified("checkpoint_artifact")
    authored = {
        key: value
        for key, value in content.items()
        if key not in {"principal_id", "source", "local_profile_id"}
    }
    if not any(
        secrets.compare_digest(
            receipt.request_hash,
            AgentService._command_request_hash(
                TaskEventCreate(
                    event_type=event.event_type,
                    payload=authored,
                    claim_id=data.claim_id,
                    claim_generation=data.claim_generation,
                    trace_id=event.trace_id,
                    span_id=event.span_id,
                    correlation_id=correlation,
                ).model_dump(mode="json")
            ),
        )
        for correlation in (None, event.correlation_id)
    ):
        _unverified("checkpoint_request_digest")
    later_task = await db.scalar(
        select(TaskEvent.id)
        .where(
            TaskEvent.task_id == task.id,
            TaskEvent.actor_id == actor.id,
            TaskEvent.event_type.in_(("agent.progress", "agent.checkpoint", "agent.blocker")),
            TaskEvent.id > event.id,
            TaskEvent.created_at <= run.ended_at,
        )
        .limit(1)
    )
    later_run = await db.scalar(
        select(AgentRunEvent.id)
        .where(AgentRunEvent.run_id == run.id, AgentRunEvent.created_at >= event.created_at)
        .limit(1)
    )
    if later_task or later_run:
        _unverified("later_worker_evidence")
    return event, receipt


async def attest_retained_output(db, actor, run_id, data: AgentRetainedOutputAttestation, *, idempotency_key):
    from app.services.agent_work_service import AgentWorkService

    require_scope(actor, "work:execute")
    key = validate_idempotency_key(idempotency_key, required=True)
    values = data.model_dump(mode="json")
    async with command_transaction(db):
        hint = await db.scalar(
            select(AgentRun.task_id).where(AgentRun.id == run_id, AgentRun.actor_id == actor.id)
        )
        if not hint:
            raise AgentPermissionError(
                "Only the original authenticated worker can attest its retained output."
            )
        service = AgentWorkService(db)
        task = await service._lock_task(hint)
        actor = (await service._lock_actors([actor.id]))[actor.id]
        assignments = await service._lock_task_assignments(hint)
        (run,) = await service._lock_task_runs(hint, run_ids=(run_id,))
        replay = await service._idempotent_replay(actor, OPERATION, "run", run_id, key, values)
        if replay:
            return replay["response"]
        existing = await db.scalar(
            select(AgentIdempotencyRecord.id)
            .where(
                AgentIdempotencyRecord.actor_id == actor.id,
                AgentIdempotencyRecord.target_type == "run",
                AgentIdempotencyRecord.target_id == run_id,
                AgentIdempotencyRecord.operation == OPERATION,
            )
            .limit(1)
        )
        if existing:
            raise AgentConflictError(
                "Retained output is already attested. Replay the original idempotency key."
            )
        original = next((row for row in assignments if row.id == data.assignment_id), None)
        initial = run.execution_provenance or {}
        terminal = initial.get("terminal_model") or {}
        if (
            not task
            or not original
            or original.actor_id != actor.id
            or original.state != "cancelled"
            or run.assignment_id != original.id
            or run.claim_generation != data.claim_generation
            or run.status != "canceled"
            or not run.ended_at
            or not actor.enabled
            or initial.get("source") != "authenticated_work_begin"
            or not initial.get("different_publisher_required")
            or not initial.get("publisher_key")
            or terminal.get("source") != "server_interruption"
            or terminal.get("publisher_key")
            or terminal.get("output_state") != "unknown"
            or data.observed_model not in {initial.get("catalog_key"), initial.get("configured_model_alias")}
        ):
            _unverified("interrupted_owner")
        recovery_id = await source_receipt_id(
            db,
            "recovery.requeue",
            "task",
            task.id,
            receipt_id=data.recovery_receipt_id,
            actor_id=data.recovery_actor_id,
            command_key=data.recovery_command_key,
        )
        planning_id = await source_receipt_id(
            db,
            "planning.iteration.update",
            "iteration",
            task.iteration_id,
            receipt_id=data.planning_receipt_id,
            actor_id=data.planning_actor_id,
            command_key=data.planning_command_key,
        )
        recovery = await db.get(AgentIdempotencyRecord, recovery_id) if recovery_id else None
        if not recovery or (recovery.operation, recovery.target_type, recovery.target_id) != (
            "recovery.requeue",
            "task",
            hint,
        ):
            _unverified("pm_recovery_receipt")
        restored = AgentRecoveryRequeueResponse.model_validate(
            json.loads(recovery.response_payload)["response"]
        )
        replacement = next((row for row in assignments if row.id == restored.assignment.id), None)
        if (
            restored.cancelled_run_ids != [run_id]
            or restored.cancelled_assignment_ids != [original.id]
            or not replacement
            or replacement.state != "queued"
            or replacement.purpose != "execution"
            or replacement.queue_class != "recovery"
            or replacement.actor_id != actor.id
            or replacement.assigned_by_actor_id != recovery.actor_id
            or restored.task.id != task.id
            or restored.task.version != task.version
            or replacement.task_version != task.version
            or restored.assignment.actor_id != actor.id
            or restored.assignment.routing_snapshot != json.loads(replacement.routing_snapshot)
        ):
            _unverified("unchanged_replacement")
        proof, missing = await _planning_proof(db, task, planning_id, after_recovery=True)
        if missing:
            _unverified("planning_" + missing)
        plan, snapshot, old = proof
        # Team acknowledgement events have no project ID. The original-owner,
        # task, canceled run and actual PM replacement were already proved.
        # Only a matched digest of their own roster facts leaves this lookup.
        with internal_authority(db):
            team_proof = await authority_stamp(db, task, replacement, lock=True, as_of=snapshot.created_at)
        if not team_proof:
            _unverified("historical_team")
        current = await actor_provenance(db, actor, binding_id=initial["binding_id"], lock=True)
        if rework_binding_identity(current) != rework_binding_identity(initial):
            _unverified("current_binding")
        event, checkpoint = await _authenticate_checkpoint(db, actor, run, task, data, old)
        fence = await db.scalar(
            select(AgentIdempotencyRecord)
            .where(
                AgentIdempotencyRecord.actor_id == actor.id,
                AgentIdempotencyRecord.operation.in_(("work.begin", "work.renew")),
                AgentIdempotencyRecord.target_type == "assignment",
                AgentIdempotencyRecord.target_id == original.id,
                AgentIdempotencyRecord.created_at <= event.created_at,
            )
            .order_by(AgentIdempotencyRecord.id.desc())
            .limit(1)
        )
        stored = json.loads(fence.response_payload) if fence else {}
        captured = stored.get("response_without_claim_id") or {}
        try:
            from datetime import datetime

            expiry = as_utc(datetime.fromisoformat(captured["claim_expires_at"].replace("Z", "+00:00")))
            correct = (
                secrets.compare_digest(
                    stored["claim_sha256"], hashlib.sha256(data.claim_id.encode()).hexdigest()
                )
                and captured["run"]["id"] == run_id
                and captured["assignment"]["id"] == original.id
                and captured["task"]["version"] == old
                and captured["claim_generation"] == data.claim_generation
                and as_utc(plan.created_at) <= as_utc(event.created_at) < expiry <= as_utc(run.ended_at)
                and as_utc(run.ended_at) <= as_utc(recovery.created_at)
            )
        except (KeyError, TypeError, ValueError):
            correct = False
        if not correct:
            _unverified("original_fence_time")
        result = {
            "run_id": run_id,
            "actor_id": actor.id,
            "assignment_id": original.id,
            "task_id": task.id,
            "claim_generation": run.claim_generation,
            "source": "authenticated_post_interruption_attestation",
            "publisher_key": initial["publisher_key"],
            "observed_model": data.observed_model,
            "output_state": "retained",
            "commit_urls": [data.commit_url],
            "git_tree": data.git_tree,
            "pr_url": data.pr_url,
            "checkpoint_id": event.id,
            "worker_checkpoint_receipt_id": checkpoint.id,
            "planning_receipt_id": plan.id,
            "recovery_receipt_id": recovery.id,
            "original_fence_receipt_id": fence.id,
            "attested_at": utc_now().isoformat(),
        }
        note = await service.task_service.record_task_event(
            task.id,
            "agent.retained_interruption_attested",
            {"attestation": result},
            actor_type="agent",
            actor_id=actor.id,
            idempotency_key=key,
        )
        await db.flush()
        result["event_id"] = note.id
        await service._record_idempotency(actor, OPERATION, "run", run_id, key, values, {"response": result})
        return result


async def retained_attestations(db, task_id, runs):
    """Read exact paired worker receipts and server-owned events, once per review history."""
    by_id = {
        run.id: run
        for run in runs
        if run.status == "canceled"
        and ((run.execution_provenance or {}).get("terminal_model") or {}).get("source")
        == "server_interruption"
    }
    if not by_id:
        return {}
    receipts = (
        await db.scalars(
            select(AgentIdempotencyRecord)
            .where(
                AgentIdempotencyRecord.operation == OPERATION,
                AgentIdempotencyRecord.target_type == "run",
                AgentIdempotencyRecord.target_id.in_(by_id),
            )
            .limit(len(by_id) + 1)
        )
    ).all()
    if len(receipts) > len(by_id):
        return {}
    pairs = {}
    for receipt in receipts:
        try:
            result = json.loads(receipt.response_payload)["response"]
            run = by_id[receipt.target_id]
            if (
                result["task_id"],
                result["run_id"],
                result["assignment_id"],
                result["claim_generation"],
                result["actor_id"],
                result["source"],
                result["output_state"],
                receipt.actor_id,
                result["publisher_key"],
            ) != (
                task_id,
                run.id,
                run.assignment_id,
                run.claim_generation,
                run.actor_id,
                "authenticated_post_interruption_attestation",
                "retained",
                run.actor_id,
                run.execution_provenance["publisher_key"],
            ):
                continue
            pairs[result["event_id"]] = (result, receipt)
        except (KeyError, TypeError, ValueError):
            continue
    if not pairs:
        return {}
    events = await db.scalars(
        select(TaskEvent).where(
            TaskEvent.id.in_(pairs),
            TaskEvent.task_id == task_id,
            TaskEvent.event_type == "agent.retained_interruption_attested",
            TaskEvent.actor_type == "agent",
        )
    )
    verified = {}
    for event in events:
        result, receipt = pairs[event.id]
        try:
            saved = json.loads(event.payload)
        except (TypeError, ValueError):
            continue
        if (
            event.actor_id == receipt.actor_id
            and event.idempotency_key == receipt.idempotency_key
            and isinstance(saved, dict)
            and saved.get("attestation") == {key: value for key, value in result.items() if key != "event_id"}
        ):
            verified[result["run_id"]] = result
    return verified
