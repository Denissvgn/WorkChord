"""Attribute task execution and bind independent review to its submitted candidate."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from urllib.parse import urlsplit
import httpx

from sqlalchemy import select
from sqlalchemy.orm import contains_eager, selectinload

from app.models.agent import (
    AgentActor, AgentIdempotencyRecord, AgentModelBinding, AgentModelCatalogEntry, AgentRun, AgentRunEvent,
    AgentTaskAssignment, AgentTeamTopology, AgentTeamTopologyMember, TaskEvent,
)
from app.models.external_link import ExternalLink
from app.models.identity import Principal
from app.models.project import Project
from app.models.task_brief import TaskProgressRecord
from app.models.team_member import TeamMember, TeamMemberProfile
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.services.agent_routing_policy import ROUTING_DECISION_AUTHORITY, ROUTING_LINEAGE_AUTHORITY, canonical_routing_json_bytes
from app.services.execution_planning_window import assignment_matches, candidate_version
from app.utils.github_links import GitHubLinkError, parse_github_url
from app.utils.url_policy import normalize_stored_display_url


def _conflict(code, message, **details):
    from app.services.agent_routing_service import AgentRoutingConflictError
    raise AgentRoutingConflictError(code, message, **details)


def digest(value):
    return hashlib.sha256(canonical_routing_json_bytes(value)).hexdigest()


_BINDING_IDENTITY = ("actor_id", "profile_id", "profile_revision", "binding_id", "binding_revision",
                     "catalog_id", "catalog_revision", "catalog_key", "configured_model_alias", "publisher_key")


def rework_binding_identity(provenance):
    """Compare the complete operator binding captured at each authenticated boundary."""
    return {key: provenance.get(key) for key in _BINDING_IDENTITY}


@dataclass
class ReworkReadCache:
    """Ephemeral evidence for one queue/context request or one locked begin transaction."""
    assignments: dict = field(default_factory=dict)
    projects: dict = field(default_factory=dict)
    teams: dict = field(default_factory=dict)
    bindings: dict = field(default_factory=dict)
    modes: dict = field(default_factory=dict)
    retained_outputs: dict = field(default_factory=dict)


async def _rework_verdict(db, task, assignment, sources, lineage):
    """Find the unique immutable verifier receipt that issued this exact queued assignment."""
    from app.schemas.agent import AgentReviewVerdictResponse

    query = select(AgentIdempotencyRecord).join(
        AgentTaskAssignment, AgentTaskAssignment.id == AgentIdempotencyRecord.target_id,
    ).where(
        AgentIdempotencyRecord.operation == "verification.verdict",
        AgentIdempotencyRecord.target_type == "assignment",
        AgentIdempotencyRecord.actor_id == assignment.assigned_by_actor_id,
        AgentTaskAssignment.id.in_(sources),
        AgentTaskAssignment.task_id == task.id,
        AgentTaskAssignment.actor_id == assignment.assigned_by_actor_id,
        AgentTaskAssignment.purpose == "verification",
        AgentTaskAssignment.state == "fulfilled",
        AgentTaskAssignment.task_version == assignment.task_version,
        ~select(AgentRun.id).where(AgentRun.assignment_id == assignment.id).exists(),
    )
    receipts = (await db.scalars(query.limit(2))).all()
    if len(receipts) != 1:
        return None
    receipt = receipts[0]
    try:
        verdict = AgentReviewVerdictResponse.model_validate(json.loads(receipt.response_payload)["response"])
    except (KeyError, TypeError, ValueError):
        return None
    review, issued = verdict.review_assignment, verdict.rework_assignment
    if (issued is None or issued.id != assignment.id or issued.task_id != task.id
            or issued.actor_id != assignment.actor_id or issued.task_version != assignment.task_version
            or issued.assigned_by_actor_id != receipt.actor_id or issued.team_member_id != task.assignee_id
            or issued.routing_snapshot != lineage or issued.queue_class != "rework" or issued.state != "queued"
            or review.id != receipt.target_id or review.actor_id != receipt.actor_id or review.task_id != task.id
            or review.model_binding_id is not None or verdict.task.id != task.id or verdict.task.status != "active"
            or verdict.task.brief_revision != task.brief_revision or verdict.task.artifact_revision != task.artifact_revision):
        return None
    events = (await db.execute(select(TaskEvent.id, TaskEvent.payload).where(
        TaskEvent.task_id == task.id, TaskEvent.actor_type == "agent", TaskEvent.actor_id == receipt.actor_id,
        TaskEvent.event_type == "agent.verification_verdict", TaskEvent.idempotency_key == receipt.idempotency_key,
    ).limit(2))).all()
    if len(events) != 1:
        return None
    event_id, raw = events[0]
    try:
        event = json.loads(raw)
    except (TypeError, ValueError):
        return None
    selection = review.review_selection or {}
    reviewer = selection.get("reviewer")
    candidate = selection.get("candidate")
    if (not isinstance(event, dict) or not isinstance(reviewer, dict) or not isinstance(candidate, dict)
            or event.get("verdict") != "reject" or event.get("assignment_id") != review.id
            or event.get("rework_assignment_id") != assignment.id or event.get("task_version") != assignment.task_version
            or event.get("review_selection") != selection or event.get("routing_lineage_digest") != digest(lineage)
            or event.get("observed_model") not in (reviewer.get("catalog_key"), reviewer.get("configured_model_alias"))
            or event.get("reviewed_candidate_digest") not in (None, candidate.get("digest"))):
        return None
    return receipt, review, event_id


async def _rejected_execution(db, task, worker, sources, candidate):
    """Cross-bind the selected candidate to its original worker's normal submit receipt."""
    from app.schemas.agent import AgentWorkTerminalResponse

    query = select(AgentRun, AgentTaskAssignment, AgentIdempotencyRecord).join(
        AgentTaskAssignment, AgentTaskAssignment.id == AgentRun.assignment_id,
    ).join(
        AgentIdempotencyRecord, AgentIdempotencyRecord.target_id == AgentTaskAssignment.id,
    ).where(
        AgentRun.id == candidate["run_id"], AgentRun.task_id == task.id, AgentRun.actor_id == worker.id,
        AgentRun.status == "succeeded", AgentRun.model_binding_id.is_(None),
        AgentTaskAssignment.id.in_(sources), AgentTaskAssignment.task_id == task.id,
        AgentTaskAssignment.actor_id == worker.id, AgentTaskAssignment.team_member_id == task.assignee_id,
        AgentTaskAssignment.purpose == "execution", AgentTaskAssignment.state == "fulfilled",
        AgentTaskAssignment.model_binding_id.is_(None),
        AgentIdempotencyRecord.actor_id == worker.id, AgentIdempotencyRecord.operation == "work.submit",
        AgentIdempotencyRecord.target_type == "assignment", AgentIdempotencyRecord.request_hash == candidate["submission_sha256"],
    )
    matches = (await db.execute(query.limit(2))).all()
    if len(matches) != 1:
        return None
    run, source, receipt = matches[0]
    try:
        submission = AgentWorkTerminalResponse.model_validate(json.loads(receipt.response_payload)["response"])
    except (KeyError, TypeError, ValueError):
        return None
    trusted = submission.run.execution_provenance or {}
    if (submission.run.id != run.id or submission.run.actor_id != worker.id or submission.run.status != "succeeded"
            or submission.run.assignment_id != source.id or submission.assignment.id != source.id
            or submission.assignment.task_version != source.task_version or submission.task.version != source.task_version
            or submission.task.id != task.id or submission.task.artifact_revision != task.artifact_revision
            or submission.task.brief_revision != task.brief_revision or run.execution_provenance != trusted
            or trusted.get("source") != "authenticated_work_begin" or not trusted.get("binding_id")
            or not trusted.get("publisher_key") or trusted.get("profile_id") != worker.profile_id):
        return None
    terminal = trusted.get("terminal_model")
    if (not isinstance(terminal, dict) or terminal.get("source") != "authenticated_terminal"
            or terminal.get("publisher_key") != trusted["publisher_key"]):
        return None
    return run, source, trusted, receipt.id


async def _supervised_recovery_origin(db, source, submit_receipt_id, manager_id, reviewer_profile_id):
    """Authenticate the already selected PM recovery that produced the rejected submission."""
    from app.schemas.agent import AgentRecoveryRequeueResponse

    if source.assigned_by_actor_id != manager_id or source.reviewer_profile_id not in (None, reviewer_profile_id):
        return None
    receipt = await db.scalar(select(AgentIdempotencyRecord).where(
        AgentIdempotencyRecord.actor_id == manager_id, AgentIdempotencyRecord.operation == "recovery.requeue",
        AgentIdempotencyRecord.target_type == "task", AgentIdempotencyRecord.target_id == source.task_id,
        AgentIdempotencyRecord.id < submit_receipt_id,
    ).order_by(AgentIdempotencyRecord.id.desc()).limit(1))
    if receipt is None:
        return None
    try:
        response = AgentRecoveryRequeueResponse.model_validate(json.loads(receipt.response_payload)["response"])
        lineage = json.loads(source.routing_snapshot)
    except (TypeError, ValueError, KeyError):
        return None
    issued = response.assignment
    if (not isinstance(lineage, dict) or lineage != issued.routing_snapshot
            or lineage.get("schema_version") != "routing-lineage-snapshot-v1" or lineage.get("authority") != ROUTING_LINEAGE_AUTHORITY
            or lineage.get("queue_class") != "recovery" or lineage.get("selection_pending") is not True
            or lineage.get("supervised_actor_id") != source.actor_id or lineage.get("provisional_actor_id") != source.actor_id
            or lineage.get("task_version") != issued.task_version or lineage.get("task_id") != source.task_id or issued.id != source.id
            or issued.actor_id != source.actor_id or issued.assigned_by_actor_id != manager_id
            or issued.task_id != source.task_id or issued.state != "queued" or issued.purpose != "execution" or issued.queue_class != "recovery"
            or issued.team_member_id != source.team_member_id or response.task.id != source.task_id or response.task.status != "active"
            or response.task.version != issued.task_version or issued.task_version >= source.task_version
            or issued.model_binding_id is not None or issued.reviewer_profile_id != source.reviewer_profile_id):
        return None
    events = (await db.execute(select(TaskEvent.id, TaskEvent.payload).where(
        TaskEvent.task_id == source.task_id, TaskEvent.actor_type == "agent", TaskEvent.actor_id == manager_id,
        TaskEvent.event_type == "agent.recovery_requeued", TaskEvent.idempotency_key == receipt.idempotency_key,
    ).limit(2))).all()
    if len(events) != 1:
        return None
    event_id, raw = events[0]
    try:
        event = json.loads(raw)
    except (TypeError, ValueError):
        return None
    original_hash = digest(lineage)
    if (not isinstance(event, dict) or event.get("assignment_id") != source.id or event.get("actor_id") != source.actor_id
            or event.get("task_version") != issued.task_version or event.get("routing_selection_pending") is not False
            or event.get("routing_lineage_digest") != original_hash):
        return None
    return {"receipt_id": receipt.id, "event_id": event_id, "assignment_id": source.id, "lineage_digest": original_hash,
            "issued_task_version": issued.task_version, "submitted_task_version": source.task_version}


async def _lock_handback_team(db, worker_id, actor_ids):
    """Fence the roster and its contributing members until an exact begin commits."""
    topology_id = await db.scalar(select(AgentTeamTopologyMember.topology_id).where(AgentTeamTopologyMember.actor_id == worker_id))
    if topology_id is None:
        return None
    version = await db.scalar(select(AgentTeamTopology.revision).where(AgentTeamTopology.id == topology_id,
        AgentTeamTopology.state != "disabled").with_for_update(read=True))
    if version is None:
        return None
    members = (await db.scalars(select(AgentTeamTopologyMember.actor_id).where(
        AgentTeamTopologyMember.topology_id == topology_id, AgentTeamTopologyMember.actor_id.in_(actor_ids),
        AgentTeamTopologyMember.lifecycle_state != "disabled",
    ).order_by(AgentTeamTopologyMember.id).with_for_update(read=True))).all()
    return (topology_id, version) if set(members) == actor_ids else None


async def supervised_rework_evidence(db, task, assignment, worker, lineage, *, lock=False, cache=None):
    """Identify a strict shadow handback to the original actor, including previously issued rows."""
    from app.services.agent_team_setup_service import AgentTeamSetupService

    sources = lineage.get("source_assignment_ids")
    if (assignment.state != "queued" or assignment.purpose != "execution" or assignment.queue_class != "rework"
            or assignment.model_binding_id is not None or assignment.actor_id != worker.id or worker.profile_id is None
            or assignment.task_id != task.id or not assignment_matches(task, assignment) or task.status != "active"
            or assignment.team_member_id != task.assignee_id
            or lineage.get("schema_version") != "routing-lineage-snapshot-v1" or lineage.get("authority") != ROUTING_LINEAGE_AUTHORITY
            or (lineage.get("task_id"), lineage.get("task_version"), lineage.get("provisional_actor_id")) != (task.id, assignment.task_version, worker.id)
            or lineage.get("selection_pending") is not True or lineage.get("prior_decisions") != []
            or not isinstance(sources, list) or not 1 <= len(sources) <= 20 or not all(type(value) is int for value in sources)):
        return None
    # A mutable command always performs fresh locking reads. Queue computations may
    # share current team and catalog facts only within their own request.
    scoped = ReworkReadCache() if lock or cache is None else cache
    if task.project_id not in scoped.projects:
        scoped.projects[task.project_id] = await different_publisher_required(db, task.project_id, lock=lock)
    if not scoped.projects[task.project_id]:
        return None
    rejection = await _rework_verdict(db, task, assignment, sources, lineage)
    if rejection is None:
        return None
    verdict_receipt, review, verdict_event_id = rejection
    selection = review.review_selection or {}
    candidate, reviewer, contributors = (selection.get(field) for field in ("candidate", "reviewer", "contributors"))
    if (not isinstance(candidate, dict) or not isinstance(reviewer, dict) or not isinstance(contributors, list)
            or not contributors or selection.get("acceptance_blockers") != [] or selection.get("manual_execution")
            or type(candidate.get("run_id")) is not int or not isinstance(candidate.get("submission_sha256"), str)
            or type(review.assigned_by_actor_id) is not int
            or candidate.get("task_id") != task.id or candidate.get("brief_revision") != task.brief_revision
            or candidate.get("artifact_revision") != task.artifact_revision
            or candidate.get("digest") != digest({key: value for key, value in candidate.items() if key != "digest"})
            or reviewer.get("actor_id") != review.actor_id or not reviewer.get("profile_id") or not reviewer.get("publisher_key")
            or any(not isinstance(c, dict) or type(c.get("actor_id")) is not int or not c.get("profile_id") or not c.get("publisher_key")
                   or c["profile_id"] == reviewer["profile_id"] or c["publisher_key"] == reviewer["publisher_key"]
                   for c in contributors)):
        return None
    floor = lineage.get("review_floor")
    tier_change = lineage.get("model_tier_change")
    if (not isinstance(floor, dict) or floor.get("review_mode") not in {"none", "standard", "independent"}
            or floor.get("reviewer_profile_ids") not in ([], [reviewer["profile_id"]])
            or not isinstance(tier_change, dict) or tier_change.get("eligible") is not False):
        return None
    origin = await _rejected_execution(db, task, worker, sources, candidate)
    if origin is None:
        return None
    run, source, proof, submit_receipt_id = origin
    if not any((c.get("run_id"), c.get("actor_id"), c["profile_id"], c["publisher_key"]) ==
               (run.id, worker.id, worker.profile_id, proof["publisher_key"]) for c in contributors):
        return None
    if source.queue_class == "rework":
        prior_handoff = proof.get("supervised_rework")
        if (not isinstance(prior_handoff, dict) or prior_handoff.get("rework_assignment_id") != source.id
                or prior_handoff.get("worker_binding") != rework_binding_identity(proof)
                or prior_handoff.get("reviewer_profile_id") != reviewer["profile_id"]):
            return None
    members = {worker.id, review.actor_id, review.assigned_by_actor_id, *(c.get("actor_id") for c in contributors)}
    locked_team = await _lock_handback_team(db, worker.id, members) if lock else None
    if lock and locked_team is None:
        return None
    if worker.id not in scoped.teams:
        scoped.teams[worker.id] = await AgentTeamSetupService(db).membership_boundary(worker.id)
    team = scoped.teams[worker.id]
    capacity = select(TeamMember.profile_id).where(TeamMember.id == task.assignee_id)
    capacity_profile = await db.scalar(capacity.with_for_update(read=True) if lock else capacity)
    if (team is None or team.primary_actor_id is None or review.assigned_by_actor_id != team.primary_actor_id
            or (lock and (team.topology_id, team.topology_revision) != locked_team)
            or not {worker.id, review.actor_id}.issubset(team.runtime_ready_actor_ids)
            or (source.queue_class == "normal" and source.assigned_by_actor_id != team.primary_actor_id)
            or source.queue_class not in {"normal", "rework", "recovery"}
            or not members.issubset(team.member_actor_ids) or capacity_profile != worker.profile_id):
        return None
    recovery_origin = None
    if source.queue_class == "recovery":
        recovery_origin = await _supervised_recovery_origin(db, source, submit_receipt_id, team.primary_actor_id, reviewer["profile_id"])
        if recovery_origin is None:
            return None
    verifier_query = select(AgentActor).where(AgentActor.id == review.actor_id).execution_options(populate_existing=True)
    verifier = await db.scalar(verifier_query.with_for_update(read=True) if lock else verifier_query)
    if verifier is None or not verifier.enabled or verifier.role != "verifier" or verifier.id == worker.id or verifier.profile_id == worker.profile_id:
        return None
    for actor, recorded in ((worker, proof), (verifier, reviewer)):
        if not recorded.get("binding_id"):
            return None
        key = (actor.id, recorded["binding_id"])
        if key not in scoped.bindings:
            scoped.bindings[key] = await actor_provenance(db, actor, binding_id=recorded["binding_id"], lock=lock)
        if rework_binding_identity(scoped.bindings[key]) != rework_binding_identity(recorded):
            return None
    evidence = {"rework_assignment_id": assignment.id, "rework_task_version": assignment.task_version,
            "rejected_run_id": run.id, "execution_assignment_id": source.id,
            "review_assignment_id": review.id,
            "verdict_receipt_id": verdict_receipt.id, "verdict_event_id": verdict_event_id,
            "reviewed_candidate_digest": candidate["digest"],
            "reviewer_profile_id": reviewer["profile_id"], "reviewer_publisher_key": reviewer["publisher_key"],
            "worker_binding": rework_binding_identity(proof),
            "topology_id": team.topology_id, "topology_revision": team.topology_revision,
            "contributor_count": len(contributors), "contributors_digest": digest(contributors),
            "review_floor": {**floor, "review_mode": "independent", "reviewer_profile_ids": [reviewer["profile_id"]],
                             "independence_must_be_revalidated": True},
            "lineage_digest": digest(lineage)}
    if recovery_origin is not None:
        evidence["source_recovery"] = recovery_origin
    return evidence


async def different_publisher_required(db, project_id, *, lock=False):
    if project_id is None:
        return False
    from app.commands import current_command
    query = select(Project.require_different_review_publisher).where(Project.id == project_id,
                                                                    Project.require_different_review_publisher.is_(True))
    if lock or ((command := current_command(db)) is not None and command.mode == "apply"):
        query = query.with_for_update(read=True)
    return bool(await db.scalar(query))


def historical_profile(assignment):
    """Only an exact server-owned selection can supply a legacy assignment's profile."""
    try:
        snapshot = json.loads(assignment.routing_snapshot or "{}")
    except (TypeError, ValueError):
        return None
    if not isinstance(snapshot, dict):
        return None
    if (snapshot.get("schema_version") == "routing-decision-snapshot-v1"
            and snapshot.get("authority") == ROUTING_DECISION_AUTHORITY):
        value = snapshot.get("profile_id")
        if type(value) is int and value > 0:
            return value
    return None


def _begin_profile(run):
    """The authenticated begin receipt, or its audited reconciliation, names the run's own profile."""
    receipt = run.execution_provenance
    if not isinstance(receipt, dict) or receipt.get("actor_id") != run.actor_id:
        return None
    value, revision = receipt.get("profile_id"), receipt.get("profile_revision")
    # The begin receipt captures the profile's revision; one without it is not evidence.
    if type(value) is not int or value <= 0 or not isinstance(revision, str) or not revision.startswith(f"p{value}-"):
        return None
    return value


def _server_ended(run):
    """The server, not the worker's terminal command, ended this run."""
    terminal = (run.execution_provenance or {}).get("terminal_model") or {}
    return run.status in {"canceled", "cancelled"} or terminal.get("source") == "server_interruption"


async def record_server_end_profile(db, run):
    """When the server ends a run, record the actor's profile as the terminal command would."""
    if not run.execution_provenance:
        return
    profile_id = await db.scalar(select(AgentActor.profile_id).where(AgentActor.id == run.actor_id))
    run.execution_provenance = {**run.execution_provenance, "terminal_profile_id": profile_id}


def _run_profile_rows(assignment_id, run, begun):
    """The begin profile of one run and, when it differs or is unknown, its terminal profile."""
    rows = [{"assignment_id": assignment_id, "run_id": run.id, "actor_id": run.actor_id,
             "profile_id": begun, "source": "run_begin" if begun else "unavailable"}]
    receipt = run.execution_provenance or {}
    if begun and "terminal_profile_id" not in receipt and _server_ended(run):
        terminal = None
    else:
        terminal = receipt.get("terminal_profile_id", begun) if begun else begun
    if terminal != begun:
        rows.append({"assignment_id": assignment_id, "run_id": run.id, "actor_id": run.actor_id,
                     "profile_id": terminal if type(terminal) is int and terminal > 0 else None,
                     "source": "run_terminal"})
    return rows


# Bounds on the walk through earlier replacements. A bound that is hit fails closed.
MAX_CARRIED_REPLACEMENT_DEPTH = 32
MAX_CARRIED_HISTORY_RUNS = MAX_BOUNDED_LIST_ITEMS


def carried_history_truncated(original_task_id, reason):
    """An unknown row that ends a carried walk early; every independence check treats it as unprovable."""
    return {"assignment_id": None, "run_id": None, "actor_id": None, "profile_id": None,
            "source": "unavailable", "carried_from_task_id": original_task_id, "truncated": reason}


async def carried_profile_history(db, task_id):
    """Actors and profiles of the original runs a replacement carries, through every earlier replacement.

    The walk is bounded by MAX_CARRIED_REPLACEMENT_DEPTH links, MAX_CARRIED_HISTORY_RUNS carried runs,
    and a visited set of task ids. A bound that is hit, or a cycle, ends the history with a
    ``truncated`` row, which fails closed: the history cannot prove independence.
    """
    from app.authority import internal_authority
    from app.services.task_replacement_service import replacing
    rows, visited, loaded, current = [], {task_id}, 0, task_id
    while True:
        relation = await replacing(db, current)
        if relation is None or not relation.carried_run_ids:
            return rows
        original_id = relation.original_task_id
        if len(visited) > MAX_CARRIED_REPLACEMENT_DEPTH:
            return rows + [carried_history_truncated(original_id, "carried_history_depth")]
        if original_id in visited:
            return rows + [carried_history_truncated(original_id, "carried_history_cycle")]
        loaded += len(relation.carried_run_ids)
        if loaded > MAX_CARRIED_HISTORY_RUNS:
            return rows + [carried_history_truncated(original_id, "carried_history_runs")]
        visited.add(original_id)
        with internal_authority(db):
            runs = (await db.scalars(select(AgentRun).where(AgentRun.id.in_(relation.carried_run_ids))
                                     .order_by(AgentRun.id))).all()
            assignments = {item.id: item for item in (await db.scalars(select(AgentTaskAssignment).where(
                AgentTaskAssignment.id.in_([run.assignment_id for run in runs if run.assignment_id])))).all()}
        for run in runs:
            assignment = assignments.get(run.assignment_id)
            begun = _begin_profile(run)
            if begun is None and assignment is not None and assignment.actor_id == run.actor_id:
                begun = historical_profile(assignment)
            rows.extend({**row, "carried_from_task_id": original_id}
                        for row in _run_profile_rows(run.assignment_id, run, begun))
        for run_id in sorted(set(relation.carried_run_ids) - {run.id for run in runs}):
            rows.append({"assignment_id": None, "run_id": run_id, "actor_id": None, "profile_id": None,
                         "source": "unavailable", "carried_from_task_id": original_id})
        # A carried run of a replacement may itself build on the earlier original's carried work.
        current = original_id


async def execution_profile_history(db, assignments, *, task_id=None):
    """Name each fulfilled execution's actor and profile from server-owned records only.

    A server-owned routing decision supplies the profile. Without one, as for a
    compatibility dispatch, every run of that assignment supplies the profile its
    authenticated begin recorded. A profile change before the terminal command
    adds the terminal profile. A run the server ended without recording its
    terminal profile may have changed profile mid-run, so that profile is unknown.
    Anything else stays unknown; current membership is never consulted. With
    ``task_id``, a replacement also names each original run it carries.
    """
    fulfilled = sorted((item for item in assignments if item.purpose == "execution" and item.state == "fulfilled"),
                       key=lambda item: item.id)
    rows, pending = [], {}
    for assignment in fulfilled:
        profile_id = historical_profile(assignment)
        if profile_id is None:
            pending[assignment.id] = assignment
            continue
        rows.append({"assignment_id": assignment.id, "run_id": None, "actor_id": assignment.actor_id,
                     "profile_id": profile_id, "source": "routing_decision"})
    runs = []
    if pending:
        query = (select(AgentRun).where(AgentRun.assignment_id.in_(list(pending))).order_by(AgentRun.id)
                 .limit(MAX_BOUNDED_LIST_ITEMS + 1))
        runs = (await db.scalars(query)).all()
        if len(runs) > MAX_BOUNDED_LIST_ITEMS:
            runs = []
    by_assignment = {}
    for run in runs:
        by_assignment.setdefault(run.assignment_id, []).append(run)
    for assignment in pending.values():
        attempts = by_assignment.get(assignment.id)
        if not attempts:
            rows.append({"assignment_id": assignment.id, "run_id": None, "actor_id": assignment.actor_id,
                         "profile_id": None, "source": "unavailable"})
            continue
        for run in attempts:
            begun = (_begin_profile(run) if run.actor_id == assignment.actor_id and run.task_id == assignment.task_id
                     else None)
            rows.extend(_run_profile_rows(assignment.id, run, begun))
    rows = sorted(rows, key=lambda row: (row["assignment_id"], row["run_id"] or 0, row["source"]))
    return rows + (await carried_profile_history(db, task_id) if task_id is not None else [])


async def require_independent_profile(db, assignments, reviewer, reviewer_profile_id=None, *, task_id=None):
    """Refuse a reviewer whose actor or profile is known to have executed this task or work it carries."""
    history = await execution_profile_history(db, assignments, task_id=task_id)
    if any(row.get("truncated") for row in history):
        _conflict("verification_independence_unverifiable", "The carried replacement history is too long or cyclic to prove independence.")
    if any(row.get("carried_from_task_id") and row["actor_id"] == reviewer.id for row in history):
        _conflict("verification_actor_not_independent", "An actor whose run this replacement carries cannot verify it.")
    profiles = {reviewer.profile_id, reviewer_profile_id} - {None}
    if any(row["profile_id"] in profiles for row in history):
        _conflict("verification_profile_not_independent", "The review profile contributed to this task.")


async def actor_provenance(db, actor, *, observed_model=None, binding_id=None, lock=False):
    """Capture the authenticated actor's profile and exact operator-declared model at this instant."""
    from app.services.agent_routing_service import AgentRoutingService

    profile_query = select(TeamMemberProfile).where(TeamMemberProfile.id == actor.profile_id).options(
        selectinload(TeamMemberProfile.skills)).execution_options(populate_existing=True)
    query = (select(AgentModelBinding, AgentModelCatalogEntry).join(AgentModelBinding.model_catalog)
             .options(contains_eager(AgentModelBinding.model_catalog))
             .where(AgentModelBinding.actor_id == actor.id, AgentModelBinding.enabled.is_(True),
                    AgentModelCatalogEntry.enabled.is_(True))
             .execution_options(populate_existing=True))
    if lock:
        profile_query = profile_query.with_for_update(read=True)
        query = query.with_for_update(read=True)
    profile = await db.scalar(profile_query) if actor.profile_id is not None else None
    if binding_id is not None:
        query = query.where(AgentModelBinding.id == binding_id)
    elif observed_model is None:
        query = query.where(AgentModelBinding.is_default.is_(True))
    matches = []
    for binding, catalog in await db.execute(query):
        if observed_model is None or observed_model in {catalog.key, catalog.configured_model_alias}:
            matches.append((binding, catalog))
    receipt = {"actor_id": actor.id, "profile_id": actor.profile_id,
               "profile_revision": AgentRoutingService._profile_revision(profile),
               "binding_id": None, "binding_revision": None, "catalog_id": None, "catalog_revision": None,
               "catalog_key": None, "configured_model_alias": None, "publisher_key": None}
    if len(matches) == 1:
        binding, catalog = matches[0]
        receipt.update(binding_id=binding.id, binding_revision=binding.revision,
                       catalog_id=catalog.id, catalog_revision=catalog.revision, catalog_key=catalog.key,
                       configured_model_alias=catalog.configured_model_alias, publisher_key=catalog.publisher_key)
    return receipt


_OUTPUT_KEYS = {"artifact", "artifacts", "artifact_links", "commit", "commit_url", "commit_urls", "commit_sha",
                "retained_commits", "head_sha", "pr_url", "pull_request"}


def _has_output(value):
    if isinstance(value, dict):
        return any((key in _OUTPUT_KEYS and bool(child)) or _has_output(child) for key, child in value.items())
    if isinstance(value, list):
        return any(_has_output(child) for child in value)
    return False


async def no_output_corroborated(db, run, reported_evidence=None):
    """A sealed worker statement cannot discard artifacts already recorded on the same run."""
    if (run.commit_url or run.pr_url or json.loads(run.artifact_links or "[]") or _has_output(reported_evidence)
            or (run.execution_provenance or {}).get("submitted_commit_urls")):
        return False
    run_events = select(AgentRunEvent.payload).where(AgentRunEvent.run_id == run.id)
    task_events = select(TaskEvent.payload).where(TaskEvent.task_id == run.task_id, TaskEvent.actor_id == run.actor_id,
        TaskEvent.event_type.in_(("agent.progress", "agent.checkpoint", "agent.blocker")), TaskEvent.created_at >= run.started_at)
    if run.ended_at is not None:
        task_events = task_events.where(TaskEvent.created_at <= run.ended_at)
    for query in (run_events, task_events):
        rows = (await db.scalars(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
        if len(rows) > MAX_BOUNDED_LIST_ITEMS:
            return False
        for payload in rows:
            try:
                if _has_output(json.loads(payload or "{}")):
                    return False
            except (TypeError, ValueError):
                return False
    return True


async def record_terminal_observation(db, actor, run, observed_model, *, submitting, output_state=None,
                                      commit_urls=(), evidence=None, checkpoint=False):
    """Preserve a second contributing model on an interrupted or switched execution."""
    initial = run.execution_provenance or {}
    expected = {initial.get("catalog_key"), initial.get("configured_model_alias")}
    if not observed_model:
        _conflict("execution_publisher_unverifiable", "Provide the observed model on this terminal command.",
                  missing=[{"run_id": run.id, "facts": ["observed_model"]}])
    if output_state == "no_output" and (commit_urls or not await no_output_corroborated(db, run, evidence)):
        _conflict("execution_output_conflict", "Recorded artifacts contradict a no-output declaration.")
    current = await actor_provenance(db, actor, observed_model=observed_model,
                                    binding_id=initial.get("binding_id") if submitting else None, lock=True)
    publisher = current["publisher_key"]
    identity_fields = ("profile_id", "binding_id", "binding_revision", "catalog_id", "catalog_revision", "publisher_key")
    if submitting and (observed_model not in expected or not publisher
                       or any(current[key] != initial.get(key) for key in identity_fields)):
        _conflict("execution_publisher_unverifiable", "The model binding changed during execution. Report the interruption and retained work.")
    field = "interruption_checkpoint" if checkpoint else "terminal_model"
    observation = {"reported_model": observed_model, "publisher_key": publisher,
                   "source": "sealed_worker_checkpoint" if checkpoint else "authenticated_terminal",
                   "output_state": output_state or ("retained" if submitting or commit_urls else "unknown"),
                   "commit_urls": list(commit_urls), "run_id": run.id, "actor_id": actor.id,
                   "assignment_id": run.assignment_id, "claim_generation": run.claim_generation}
    sealed = initial.get("interruption_checkpoint")
    if sealed and (submitting or any(sealed.get(key) != observation[key] for key in
                                    ("reported_model", "output_state", "commit_urls", "publisher_key"))):
        _conflict("execution_output_conflict", "The worker already sealed its final output for this fence.")
    run.execution_provenance = {**initial, field: observation}


async def recover_terminal_observation(db, run):
    """Resolve only the server-bound receipt for a worker's final sealed checkpoint on this exact fence."""
    stored = run.execution_provenance or {}
    seal = stored.get("interruption_checkpoint")
    query = select(AgentIdempotencyRecord).where(AgentIdempotencyRecord.actor_id == run.actor_id,
        AgentIdempotencyRecord.operation == "work.renew", AgentIdempotencyRecord.target_type == "assignment",
        AgentIdempotencyRecord.target_id == run.assignment_id, AgentIdempotencyRecord.created_at >= run.started_at)
    if run.ended_at is not None:
        query = query.where(AgentIdempotencyRecord.created_at <= run.ended_at)
    if seal is not None:
        if not isinstance(seal, dict) or not isinstance(seal.get("renew_key"), str):
            return None, {}
        query = query.where(AgentIdempotencyRecord.idempotency_key == seal["renew_key"])
    receipts = (await db.scalars(query.limit(MAX_BOUNDED_LIST_ITEMS + 1))).all()
    if len(receipts) > MAX_BOUNDED_LIST_ITEMS:
        return None, {}
    matched = []
    identity = (run.id, run.actor_id, run.assignment_id, run.claim_generation)
    for receipt in receipts:
        try:
            packet = json.loads(receipt.response_payload)["response_without_claim_id"]
            captured = (packet["run"].get("execution_provenance") or {}).get("interruption_checkpoint")
            if not captured or captured.get("renew_key") != receipt.idempotency_key:
                continue
            if ((seal is not None and captured != seal) or captured.get("source") != "sealed_worker_checkpoint"
                    or tuple(captured.get(k) for k in ("run_id", "actor_id", "assignment_id", "claim_generation")) != identity
                    or tuple(packet["run"].get(k) for k in ("id", "actor_id", "assignment_id", "claim_generation")) != identity
                    or packet["task"]["id"] != run.task_id or packet["assignment"]["purpose"] != "execution"
                    or packet["assignment"]["id"] != run.assignment_id or packet["assignment"]["actor_id"] != run.actor_id
                    or captured.get("output_state") not in {"no_output", "retained"}):
                return None, {}
            matched.append((captured, receipt.id))
        except (AttributeError, KeyError, TypeError, ValueError):
            return None, {}
    if len(matched) != 1:
        return None, {}
    captured, receipt_id = matched[0]
    if captured["output_state"] == "no_output" and not await no_output_corroborated(db, run):
        return None, {}
    return captured, {"renew": receipt_id}


async def mark_server_interruption(db, run):
    provenance = run.execution_provenance or {}
    terminal, sources = await recover_terminal_observation(db, run)
    run.execution_provenance = {**provenance, "terminal_model": terminal or {
        "source": "server_interruption", "reported_model": None, "publisher_key": None, "output_state": "unknown"},
        "interruption_source_receipts": sources}


@dataclass
class ReviewHistory:
    contributors: list[dict]
    candidate: dict | None
    manual_execution: dict | None = None
    missing_manual_fact: str | None = None
    required_reviewer_profiles: tuple[int, ...] | None = None

    def permits_profile(self, profile_id):
        return self.required_reviewer_profiles is None or profile_id in self.required_reviewer_profiles

    def publisher_blockers(self, publisher):
        if (not self.contributors and self.manual_execution is None or not publisher
                or any(not row.get("publisher_key") for row in self.contributors)):
            return ["verification_publisher_unverifiable"]
        if any(row["publisher_key"] == publisher for row in self.contributors):
            return ["verification_publisher_not_independent"]
        return []


def _submitted_review_floor(provenance, assignment_id, actor_id):
    """An absent handback is unrestricted; a contradictory handback admits no verifier."""
    if not isinstance(provenance, dict) or "supervised_rework" not in provenance:
        return None
    handback = provenance["supervised_rework"]
    if not isinstance(handback, dict) or handback.get("rework_assignment_id") != assignment_id:
        return ()
    floor = handback.get("review_floor")
    profile = handback.get("reviewer_profile_id")
    identity = handback.get("worker_binding")
    if (type(profile) is not int or profile <= 0 or not isinstance(identity, dict) or identity.get("actor_id") != actor_id
            or not isinstance(floor, dict) or floor.get("review_mode") != "independent"
            or floor.get("independence_must_be_revalidated") is not True or floor.get("reviewer_profile_ids") != [profile]):
        return ()
    return (profile,)


async def _manual_history(db, task):
    """Verify an actual human executor and immutable evidence, independently of the planned owner."""
    principal_id = task.executed_by_principal_id
    if task.status != "resolved" or task.execution_mode != "manual" or not principal_id:
        return ReviewHistory([], None, missing_manual_fact="authenticated_manual_execution")
    human = await db.scalar(select(Principal.id).where(Principal.id == principal_id, Principal.kind == "human",
                                                       Principal.agent_actor_id.is_(None)))
    if human is None:
        return ReviewHistory([], None, missing_manual_fact="authenticated_human_executor")
    prior_agent = await db.scalar(select(TaskEvent.id).where(TaskEvent.task_id == task.id,
        TaskEvent.event_type.in_(("agent.work_began", "agent.work_renewed", "agent.work_submitted",
                                  "agent.work_recovery_required", "agent.run_created", "agent.run_finished"))).limit(1))
    if prior_agent is not None:
        return ReviewHistory([], None, missing_manual_fact="prior_agent_execution")
    events = {}
    for kind in ("task_start_manual", "task_resolve_manual", "status_changed"):
        event = await db.scalar(select(TaskEvent).where(TaskEvent.task_id == task.id, TaskEvent.event_type == kind)
                                .order_by(TaskEvent.id.desc()).limit(1))
        if event is None or event.actor_type != "user" or event.actor_id is not None:
            return ReviewHistory([], None, missing_manual_fact=kind)
        try:
            payload = json.loads(event.payload or "{}")
        except (TypeError, ValueError):
            return ReviewHistory([], None, missing_manual_fact=kind)
        if (not isinstance(payload, dict) or payload.get("principal_id") != principal_id
                or type(payload.get("version")) is not int):
            return ReviewHistory([], None, missing_manual_fact=kind)
        events[kind] = (event.id, payload)
    start_id, start = events["task_start_manual"]
    resolve_id, resolved = events["task_resolve_manual"]
    status_id, status = events["status_changed"]
    if (not start_id < status_id < resolve_id or status.get("from_status") != "active"
            or status.get("to_status") != "resolved" or status["version"] != resolved["version"]
            or not start["version"] < resolved["version"] <= task.version):
        return ReviewHistory([], None, missing_manual_fact="authenticated_manual_resolution")
    record = await db.scalar(select(TaskProgressRecord).where(TaskProgressRecord.task_id == task.id,
        TaskProgressRecord.original_task_id == task.id, TaskProgressRecord.artifact_revision == task.artifact_revision))
    if (record is None or record.principal_id != principal_id or record.brief_revision != task.brief_revision
            or not start["version"] < record.task_version <= resolved["version"]
            or not isinstance(record.payload, dict) or record.payload != task.progress
            or not record.payload.get("artifacts")):
        return ReviewHistory([], None, missing_manual_fact="current_human_artifact")
    artifacts = record.payload["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) > 50 or not all(isinstance(url, str) and url.strip() for url in artifacts):
        return ReviewHistory([], None, missing_manual_fact="current_human_artifact")
    commits, comparisons = [], []
    for url in artifacts:
        try:
            normalize_stored_display_url(url)
            parsed = urlsplit(url)
            hostname = parsed.hostname
        except ValueError:
            return ReviewHistory([], None, missing_manual_fact="current_human_artifact")
        if hostname in {"github.com", "www.github.com"} and "/compare/" in parsed.path:
            comparisons.append(parsed)
        try:
            link = parse_github_url(url)
        except GitHubLinkError:
            continue
        if link.github_type == "commit":
            commits.append(link.url)
    profile_ids = sorted({entry["executor_profile_id"] for entry in (start, resolved)
                          if type(entry.get("executor_profile_id")) is int and entry["executor_profile_id"] > 0})
    proof = {"principal_id": principal_id, "profile_ids": profile_ids, "start_event_id": start_id, "resolution_event_id": resolve_id,
             "progress_record_id": record.id, "commit_urls": commits}
    source = {"manual_progress_record_id": record.id, "submission_sha256": digest({"identity": proof, "progress": record.payload})}
    submitted = {"artifact_links": artifacts, "commit_url": commits[0] if commits else None}
    if comparisons:
        match = re.fullmatch(r"/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)/compare/([0-9a-f]{40}|[0-9a-f]{64})\.\.\.([0-9a-f]{40}|[0-9a-f]{64})/?", comparisons[0].path)
        if (len(comparisons) != 1 or not match or comparisons[0].scheme != "https"
                or comparisons[0].query or comparisons[0].fragment):
            return ReviewHistory([], None, manual_execution=proof)
        prefix = f"https://github.com/{match[1]}/{match[2]}/commit/"
        if prefix + match[4] not in commits:
            return ReviewHistory([], None, manual_execution=proof)
        submitted.update(commit_url=prefix + match[4], execution_provenance={"submitted_base_commit_url": prefix + match[3]})
    return ReviewHistory([], await _submission_candidate(db, task, submitted, source), manual_execution=proof)


async def _recorded_history(db, task):
    """An owner's or PM's recorded provenance for work that never ran through recorded runs.

    A human executor is reviewed like authenticated manual execution; an agent executor is an
    ordinary contributor with the profile and publisher captured when the record was made.
    """
    from app.services.manual_provenance_service import recorded_provenance, submitted_candidate
    found = await recorded_provenance(db, task)
    if found is None:
        return None
    event, record = found
    executor = record["executor"]
    commits = list(record["commit_urls"])
    source = {"manual_provenance_event_id": event.id, "submission_sha256": digest(record)}
    candidate = await _submission_candidate(db, task, submitted_candidate(record), source)
    if executor.get("kind") == "human" and type(executor.get("principal_id")) is int:
        proof = {"principal_id": executor["principal_id"], "profile_ids": list(executor.get("profile_ids") or ()),
                 "provenance_event_id": event.id, "commit_urls": commits}
        return ReviewHistory([], candidate, manual_execution=proof)
    if executor.get("kind") == "agent" and type(executor.get("actor_id")) is int:
        return ReviewHistory([{"run_id": None, "actor_id": executor["actor_id"], "profile_id": executor.get("profile_id"),
                               "publisher_key": executor.get("publisher_key"), "commit_urls": commits,
                               "provenance_event_id": event.id}], candidate)
    return None


async def review_history(db, task, assignments, *, strict, include_carried=True):
    """A failed or recovered run can have produced retained work. Include every actual attempt.

    A clean replacement also counts each original run whose commits it carries.
    """
    history = await _attempt_history(db, task, assignments, strict=strict)
    if strict and include_carried:
        from app.services.task_replacement_service import carried_contributors
        history.contributors.extend(await carried_contributors(db, task))
    return history


async def _attempt_history(db, task, assignments, *, strict):
    executions = {item.id: item for item in assignments if item.purpose == "execution"}
    query = select(AgentRun).where(AgentRun.task_id == task.id).order_by(AgentRun.id).limit(MAX_BOUNDED_LIST_ITEMS + 1)
    runs = (await db.scalars(query)).all()
    if len(runs) > MAX_BOUNDED_LIST_ITEMS:
        raise CollectionLimitExceededError("task execution provenance", MAX_BOUNDED_LIST_ITEMS)
    if strict and not runs and not any(item.state == "fulfilled" for item in executions.values()):
        recorded = await _recorded_history(db, task)
        if recorded is not None:
            return recorded
    if strict and not runs and not executions:
        return await _manual_history(db, task)
    from app.services.retained_planning_output import retained_attestations
    attestations = await retained_attestations(db, task.id, runs) if strict else {}
    contributors = []
    represented = set()
    for run in runs:
        assignment = executions.get(run.assignment_id)
        verification_run = any(item.id == run.assignment_id and item.actor_id == run.actor_id and
                               item.purpose == "verification" for item in assignments)
        if verification_run:
            continue
        if strict and assignment is None:
            contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": None,
                                 "publisher_key": None, "missing": ["execution_assignment", "profile_id", "publisher_key"]})
            continue
        if not strict and (assignment is None or assignment.state != "fulfilled"):
            continue
        receipt = run.execution_provenance or {}
        terminal = receipt.get("terminal_model") or {}
        interrupted = run.status in {"failed", "canceled", "cancelled"}
        if (strict and interrupted and terminal.get("source") in {"authenticated_terminal", "sealed_worker_checkpoint"}
                and terminal.get("output_state") == "no_output" and await no_output_corroborated(db, run)):
            represented.add(run.assignment_id)
            continue
        profile_id = receipt.get("profile_id")
        if profile_id is None and assignment is not None and run.actor_id == assignment.actor_id:
            profile_id = historical_profile(assignment)
        commits = set(receipt.get("submitted_commit_urls") or ())
        commits.update(terminal.get("commit_urls") or ())
        supplement = attestations.get(run.id)
        if supplement:
            commits.update(supplement["commit_urls"])
        if run.commit_url:
            commits.add(run.commit_url)
        contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": profile_id,
                             "publisher_key": receipt.get("publisher_key"),
                             "commit_urls": sorted(commits)})
        if supplement:
            contributors[-1]["retained_output_attestation"] = {
                key: supplement[key] for key in ("source", "event_id", "checkpoint_id", "attested_at")}
        if strict and (terminal or interrupted):
            last_publisher = terminal.get("publisher_key") or (supplement or {}).get("publisher_key")
            if last_publisher != receipt.get("publisher_key") or not last_publisher:
                contributors.append({"run_id": run.id, "actor_id": run.actor_id, "profile_id": profile_id,
                                     "publisher_key": last_publisher,
                                     "missing": [] if last_publisher else ["terminal_model"]})
        represented.add(run.assignment_id)
    for assignment in executions.values():
        if assignment.state == "fulfilled" and assignment.id not in represented:
            contributors.append({"run_id": None, "actor_id": assignment.actor_id,
                                 "profile_id": historical_profile(assignment), "publisher_key": None})
    if not strict:
        return ReviewHistory(contributors, None)

    submitted = [run for run in runs if run.status == "succeeded" and run.assignment_id in executions
                 and executions[run.assignment_id].state == "fulfilled" and run.ended_at is not None]
    if not submitted:
        return ReviewHistory(contributors, None)
    latest = max(submitted, key=lambda run: (run.ended_at, run.id))
    floor = _submitted_review_floor(latest.execution_provenance, latest.assignment_id, latest.actor_id)
    unavailable = ReviewHistory(contributors, None, required_reviewer_profiles=() if floor is not None else None)
    receipts = (await db.scalars(select(AgentIdempotencyRecord).where(
        AgentIdempotencyRecord.actor_id == latest.actor_id, AgentIdempotencyRecord.operation == "work.submit",
        AgentIdempotencyRecord.target_type == "assignment", AgentIdempotencyRecord.target_id == latest.assignment_id,
    ).limit(2))).all()
    if len(receipts) != 1:
        return unavailable
    try:
        response = json.loads(receipts[0].response_payload)["response"]
        if (response["run"]["id"] != latest.id or response["task"]["id"] != task.id
                or response["assignment"]["id"] != latest.assignment_id
                or response["run"]["actor_id"] != latest.actor_id or response["run"]["status"] != "succeeded"
                or response["task"].get("artifact_revision", 0) != task.artifact_revision
                or response["task"].get("brief_revision", 0) != task.brief_revision):
            return unavailable
    except (KeyError, TypeError, ValueError):
        return unavailable
    captured = _submitted_review_floor(response["run"].get("execution_provenance"), latest.assignment_id, latest.actor_id)
    if captured != floor:
        floor = ()
    candidate = await _submission_candidate(db, task, response["run"], {"run_id": latest.id, "submission_sha256": receipts[0].request_hash})
    return ReviewHistory(contributors, candidate, required_reviewer_profiles=floor)


async def _submission_candidate(db, task, submitted_run, source):
    """Use identical repository and revision checks for authenticated worker or human artifact records."""
    try:
        pr = parse_github_url(submitted_run["pr_url"]) if submitted_run.get("pr_url") else None
        commit = parse_github_url(submitted_run["commit_url"]) if submitted_run.get("commit_url") else None
        base_url = (submitted_run.get("execution_provenance") or {}).get("submitted_base_commit_url")
        base = parse_github_url(base_url) if base_url else None
        submitted_links = set(submitted_run.get("artifact_links") or [])
        submitted_links.update((submitted_run.get("execution_provenance") or {}).get("submitted_commit_urls", ()))
        artifact_commits, artifact_prs = set(), set()
        repository_artifact = False
        for url in submitted_links:
            try:
                link = parse_github_url(url)
            except GitHubLinkError:
                continue
            repository_artifact |= link.github_type in {"commit", "pull_request", "branch", "tag"}
            if link.github_type == "commit":
                artifact_commits.add(link.url)
            elif link.github_type == "pull_request":
                artifact_prs.add(link.url)
        if commit is None and len(artifact_commits) == 1:
            commit = parse_github_url(artifact_commits.pop())
        if pr is None:
            if not artifact_prs:
                linked_urls = await db.scalars(select(ExternalLink.url).where(
                    ExternalLink.entity_type == "task", ExternalLink.entity_id == task.id, ExternalLink.provider == "github"))
                for url in linked_urls:
                    try:
                        link = parse_github_url(url)
                    except GitHubLinkError:
                        continue
                    if link.github_type == "pull_request":
                        artifact_prs.add(link.url)
            if len(artifact_prs) > 1:
                return None
            if artifact_prs:
                pr = parse_github_url(artifact_prs.pop())
        if repository_artifact and commit is None:
            return None
        if ((commit and commit.github_type != "commit") or (pr and (pr.github_type != "pull_request" or not commit))
                or (base and (not commit or base.github_type != "commit" or base.repo_full_name.casefold() != commit.repo_full_name.casefold()))
                or (commit and not pr and not base)):
            return None
    except (KeyError, TypeError, ValueError, GitHubLinkError):
        return None
    basis = {"task_id": task.id, "task_version": candidate_version(task), "brief_revision": task.brief_revision,
             "artifact_revision": task.artifact_revision, **source,
             "commit_url": commit.url if commit else None, "pr_url": pr.url if pr else None,
             "base_commit_url": base.url if base else None}
    return {**basis, "digest": digest(basis)}


async def select_reviewer(db, task, assignments, reviewer, *, binding_id=None, reviewer_profile_id=None, review_evidence_id=None):
    if not await different_publisher_required(db, task.project_id):
        if review_evidence_id is not None:
            _conflict("verification_evidence_unavailable", "Scoped evidence requires independent verification.")
        return None
    history = await review_history(db, task, assignments, strict=True)
    from app.services.task_replacement_service import attributed
    held = sorted({row["run_id"] for row in history.contributors
                   if row.get("carried_from_task_id") and not attributed(row) and row.get("run_id")})
    if held:
        _conflict("replacement_contribution_unattributed",
                  "This replacement carries commits from an unattributed run and stays held.",
                  missing=[{"run_id": run_id, "facts": ["carried_contribution_attribution"]} for run_id in held])
    receipt = await actor_provenance(db, reviewer, binding_id=binding_id, lock=True)
    if not receipt["profile_id"] or any(row["profile_id"] is None for row in history.contributors):
        _conflict("verification_independence_unverifiable", "An implementation or verifier profile lacks historical evidence.",
                 missing=[{"run_id": r["run_id"], "facts": r.get("missing", ["profile_id"])} for r in history.contributors if r["profile_id"] is None])
    if reviewer_profile_id is not None and receipt["profile_id"] != reviewer_profile_id:
        _conflict("reviewer_profile_mismatch", "The selected reviewer must hold the requested profile.")
    if not history.permits_profile(receipt["profile_id"]):
        _conflict("reviewer_profile_mismatch", "The submitted rework requires its recorded independent reviewer profile.",
                  required_reviewer_profile_ids=list(history.required_reviewer_profiles))
    if history.manual_execution:
        profile = (await db.execute(select(TeamMemberProfile.profile_kind, TeamMemberProfile.automation_enabled,
            TeamMemberProfile.assignment_modes).where(TeamMemberProfile.id == receipt["profile_id"]))).one_or_none()
        if (profile is None or profile.profile_kind not in {"agent", "hybrid"} or not profile.automation_enabled
                or "verification" not in (profile.assignment_modes or ()) or receipt["profile_id"] in history.manual_execution["profile_ids"]):
            _conflict("verification_profile_not_independent", "Assign a separate automation-enabled verifier profile for the human submission.")
    if any(row["actor_id"] == reviewer.id for row in history.contributors):
        _conflict("verification_actor_not_independent", "An implementation actor cannot verify this candidate.")
    if any(row["profile_id"] == receipt["profile_id"] for row in history.contributors):
        _conflict("verification_profile_not_independent", "The review profile contributed to this task.")
    blockers = history.publisher_blockers(receipt["publisher_key"])
    if blockers:
        if history.missing_manual_fact:
            from app.services.manual_provenance_service import remedy
            _conflict(blockers[0], "An authenticated human must record manual execution and its current artifact, or an agent must supply "
                      "attributable execution evidence. For work resolved outside recorded runs, a project owner or PM records "
                      "its executor, commits or pull request and artifact revision as manual provenance.",
                      missing=[{"task_id": task.id, "facts": [history.missing_manual_fact, "manual_provenance"]}],
                      remedy=remedy(task.id))
        _conflict(blockers[0], "Review requires a known publisher distinct from every contributing publisher.",
                 missing=[{"run_id": r["run_id"], "facts": r.get("missing", ["publisher_key"])}
                          for r in history.contributors if not r.get("publisher_key")])
    selection = {"reviewer": receipt, "candidate": history.candidate, "contributors": history.contributors,
                 "acceptance_blockers": [] if history.candidate else ["verification_candidate_unverifiable"]}
    if history.manual_execution:
        selection["manual_execution"] = history.manual_execution
    if review_evidence_id is not None:
        from app.services.review_evidence import resolve
        selection["review_evidence"] = await resolve(db, task, review_evidence_id, history, reviewer=receipt)
    return selection


def require_verifiable_candidate(task, selection):
    """Refuse a new verification assignment that is already known never to be able to pass.

    The answer names the missing provenance. Work without recorded runs can get it from a
    manual provenance record.
    """
    if selection is None or selection.get("candidate"):
        return
    from app.services.manual_provenance_service import remedy
    recorded_runs = any(row.get("run_id") for row in selection.get("contributors") or ())
    fact = "current_human_artifact" if selection.get("manual_execution") else "submitted_candidate"
    context = {"missing": [{"task_id": task.id, "facts": [fact] if recorded_runs else [fact, "manual_provenance"]}]}
    message = "This task has no exact submitted candidate, so an independent review could never accept it."
    if not recorded_runs:
        context["remedy"] = remedy(task.id)
        message += (" A project owner or PM can record its executor, commits or pull request and artifact revision"
                    " as manual provenance first.")
    else:
        message += " Its recorded runs must supply a submitted repository candidate."
    _conflict("verification_candidate_unverifiable", message, **context)


async def observe_review_candidate(db, assignment_id, actor_id):
    """Resolve remote PR evidence before taking the task, actor and assignment locks."""
    from app.models.agent import AgentTaskAssignment
    from app.services.github_status_service import GitHubStatusService

    selection = await db.scalar(select(AgentTaskAssignment.review_selection).where(
        AgentTaskAssignment.id == assignment_id, AgentTaskAssignment.actor_id == actor_id,
        AgentTaskAssignment.purpose == "verification", AgentTaskAssignment.state.in_(("queued", "accepted"))))
    if not selection or not selection.get("candidate") or not selection["candidate"]["commit_url"]:
        return None
    candidate = selection["candidate"]
    commit = parse_github_url(candidate["commit_url"])
    failure_context = {}
    try:
        github = await GitHubStatusService.from_runtime(db)
        attributed = {}
        human = selection.get("manual_execution")
        if human:
            for url in human["commit_urls"]:
                source = parse_github_url(url)
                if source.github_type == "commit" and source.repo_full_name.casefold() == commit.repo_full_name.casefold():
                    attributed.setdefault(source.sha, set()).add(("human", human["principal_id"]))
        for row in selection["contributors"]:
            urls = row.get("commit_urls", ())
            for url in urls:
                source = parse_github_url(url)
                if source.github_type == "commit" and source.repo_full_name.casefold() == commit.repo_full_name.casefold():
                    attributed.setdefault(source.sha, set()).add(row["actor_id"])
        if candidate["pr_url"]:
            blocker = await github.verify_review_head(parse_github_url(candidate["pr_url"]), commit.sha, attributed,
                                                      expected_repository=commit.repo_full_name, failure_context=failure_context)
        else:
            blocker = await github.verify_review_range(parse_github_url(candidate["base_commit_url"]), commit, attributed,
                                                       failure_context=failure_context)
    except (httpx.HTTPError, ValueError, KeyError, TypeError, AttributeError):
        blocker = "verification_candidate_unverifiable"
    return candidate["digest"], blocker, failure_context


async def verify_verdict(db, task, assignments, assignment, actor, data, observed_candidate):
    from app.commands import current_command

    if assignment.actor_id != actor.id or not assignment.review_selection:
        _conflict("verification_independence_unverifiable", "The assigned reviewer must submit its own observed model.")
    stored = assignment.review_selection
    evidence = stored.get("review_evidence")
    if (evidence or data.reviewed_packet_sha256 is not None) and (
        not evidence or data.reviewed_packet_sha256 != evidence["packet_sha256"]
    ):
        _conflict("verification_evidence_unavailable", "A scoped verdict must acknowledge the exact reviewed evidence packet.")
    current = await select_reviewer(db, task, assignments, actor, binding_id=stored["reviewer"]["binding_id"],
                                    reviewer_profile_id=assignment.reviewer_profile_id, review_evidence_id=evidence["id"] if evidence else None)
    if current["reviewer"] != stored["reviewer"]:
        _conflict("verification_publisher_unverifiable", "Refresh the assignment after a change to the reviewer's binding or profile.")
    if data.verdict == "pass" and not current["candidate"]:
        _conflict("verification_candidate_unverifiable", "An exact submitted candidate is required for acceptance.")
    if data.verdict == "pass" and (current != stored or data.reviewed_candidate_digest != current["candidate"]["digest"]):
        _conflict("verification_candidate_stale", "Refresh the review assignment and review its exact candidate.")
    if data.observed_model not in {current["reviewer"]["catalog_key"], current["reviewer"]["configured_model_alias"]}:
        _conflict("verification_publisher_unverifiable", "The authenticated reviewer's observed model must match its selected binding.")
    if data.verdict == "pass" and current["candidate"]["commit_url"]:
        if not observed_candidate or observed_candidate[0] != current["candidate"]["digest"]:
            _conflict("verification_candidate_stale", "The selected PR candidate changed during review.")
        if observed_candidate[1] is not None:
            _conflict(observed_candidate[1], "The candidate head and all contributing authors must be verifiable for this review.",
                      **observed_candidate[2])
    command = current_command(db)
    assert command is not None
    command.verified_publishers.add((task.id, task.version, task.brief_revision, task.artifact_revision))
