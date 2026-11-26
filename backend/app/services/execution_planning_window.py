"""Preserve a proved assignment context across an iteration end-date extension."""

from __future__ import annotations

import hashlib
import itertools
import json

from sqlalchemy import select
from app.agent_contract import EXECUTION_PLANNING_WINDOW_FEATURE

from app.models.agent import (
    AgentActor,
    AgentIdempotencyRecord,
    AgentRun,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentTaskAssignment,
    AgentTeamTopology,
    AgentTeamTopologyMember,
)
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.external_link import ExternalLink
from app.models.identity import Principal, ProjectMembership, WorkspaceMembership
from app.models.team_member import TeamMember

LIVE_ASSIGNMENT_STATES = ("queued", "accepted")
LIVE_RUN_STATE = "running"


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode()
    ).hexdigest()


def task_context(task):
    # Revisions, assignment scope and actual work state are included. The
    # secret claim is independently checked by the normal worker command.
    fields = (
        "id",
        "iteration_id",
        "project_id",
        "parent_id",
        "assignee_id",
        "owner_profile_id",
        "status",
        "execution_mode",
        "brief_revision",
        "artifact_revision",
        "brief",
        "progress",
        "description",
        "title",
        "priority",
        "source",
        "source_url",
        "milestone_id",
        "external_key",
        "effort_hours",
        "start_date",
        "end_date",
        "min_start_date",
        "max_end_date",
        "claimed_by",
        "claim_generation",
        "blocked_reason",
        "canceled_at",
        "is_deferred",
    )
    return digest({name: getattr(task, name) for name in fields})


def assignment_context(assignment):
    fields = (
        "id",
        "actor_id",
        "assigned_by_actor_id",
        "task_id",
        "team_member_id",
        "purpose",
        "queue_class",
        "state",
        "task_version",
        "model_binding_id",
        "model_binding_revision",
        "reviewer_profile_id",
        "review_selection",
        "routing_snapshot",
        "not_before",
    )
    return digest({name: getattr(assignment, name) for name in fields})


def current_window(task):
    window = getattr(task, "execution_planning_window", None)
    if (
        isinstance(window, dict)
        and window.get("kind") == "iteration_end_extension"
        and window.get("through") == task.version
        and type(window.get("from")) is int
        and 0 < window["from"] < task.version
        and window.get("task_context") == task_context(task)
        and isinstance(window.get("assignments"), dict)
    ):
        return window
    return None


def assignment_matches(task, assignment):
    if assignment.task_version == task.version:
        return True
    window = current_window(task)
    return bool(
        window
        and window["from"] <= assignment.task_version < task.version
        and window["assignments"].get(str(assignment.id)) == assignment_context(assignment)
    )


def candidate_version(task):
    window = current_window(task)
    return window["from"] if window else task.version


async def earlier_acknowledgements(db, member):
    """Return digests of the acknowledgement as it was before a runtime adopted newer fields.

    A runtime can re-acknowledge after an upgrade solely to adopt
    ``EXECUTION_PLANNING_WINDOW_FEATURE`` or the runtime instance identity (the
    identity feature and ``runtime_instance_id``). The stored bytes must
    reproduce the current digest. Removing what was adopted reproduces the
    previous acknowledgement only when every other field is identical, so every
    combination of removals is returned and the caller compares against it.
    Any other result is an empty tuple.
    """
    from app.agent_contract import RUNTIME_INSTANCE_IDENTITY_FEATURE
    from app.services.agent_team_setup_service import _digest

    encoded = await db.scalar(
        select(AgentTeamTopologyMember.runtime_acknowledgement_payload).where(
            AgentTeamTopologyMember.actor_id == member.id,
            AgentTeamTopologyMember.topology_id == member.team_id,
        )
    )
    try:
        current = json.loads(encoded)
        features = current["server_features"]
        if not isinstance(features, list) or _digest(current) != member.runtime_acknowledgement_digest:
            return ()
        window = features.count(EXECUTION_PLANNING_WINDOW_FEATURE)
        identity = features.count(RUNTIME_INSTANCE_IDENTITY_FEATURE)
        if window > 1 or identity > 1:
            return ()
        adoptable = []
        if window:
            adoptable.append("window")
        if identity or "runtime_instance_id" in current:
            adoptable.append("identity")
        digests = []
        for size in range(1, len(adoptable) + 1):
            for removed in itertools.combinations(adoptable, size):
                earlier = dict(current)
                earlier["server_features"] = [
                    value
                    for value in features
                    if not (
                        ("window" in removed and value == EXECUTION_PLANNING_WINDOW_FEATURE)
                        or ("identity" in removed and value == RUNTIME_INSTANCE_IDENTITY_FEATURE)
                    )
                ]
                if "identity" in removed:
                    earlier.pop("runtime_instance_id", None)
                digests.append(_digest(earlier))
        return tuple(digests)
    except (ValueError, TypeError, KeyError):
        return ()


async def authority_stamp(db, task, assignment, *, lock=False, as_of=None):
    """Fingerprint the actual scope, roster and bindings of both assignment principals."""
    basis = await _authority_basis(db, task, assignment, lock=lock, as_of=as_of)
    return digest(basis[0]) if basis else None


async def authority_matches(db, task, assignment, expected, *, lock=False):
    """Compare a sealed stamp with current authority.

    The only tolerated difference is a member that has since re-acknowledged
    solely to add the planning-window feature or its runtime instance identity. Every other roster, topology
    revision, permission, binding, link or policy change still mismatches.
    """
    if not expected:
        return False
    basis = await _authority_basis(db, task, assignment, lock=lock)
    if basis is None:
        return False
    fields, members = basis
    if digest(fields) == expected:
        return True
    slot = members[0]._fields.index("runtime_acknowledgement_digest")
    choices = []
    for member in members:
        choices.append((member[slot], *await earlier_acknowledgements(db, member)))
    for combination in itertools.product(*choices):
        rows = [
            (*tuple(member)[:slot], value, *tuple(member)[slot + 1 :])
            for member, value in zip(members, combination)
        ]
        if digest({**fields, "members": rows}) == expected:
            return True
    return False


async def _authority_basis(db, task, assignment, *, lock=False, as_of=None):
    from app.models.agent import TaskEvent

    def fenced(query):
        return query.with_for_update(read=True) if lock else query

    actors = {assignment.actor_id, assignment.assigned_by_actor_id}
    selection = assignment.review_selection or {}
    if not isinstance(selection, dict) or not isinstance(selection.get("contributors", []), list):
        return None
    actors.update(row.get("actor_id") for row in selection.get("contributors", ()) if isinstance(row, dict))
    if (
        not actors
        or any(type(actor) is not int for actor in actors)
        or not task.project_id
        or assignment.team_member_id != task.assignee_id
    ):
        return None
    policy = await db.scalar(
        fenced(select(Project.require_different_review_publisher).where(Project.id == task.project_id))
    )
    if policy is None:
        return None
    capacity = (
        await db.execute(
            fenced(
                select(TeamMember.id, TeamMember.profile_id, TeamMember.iteration_id).where(
                    TeamMember.id == task.assignee_id
                )
            )
        )
    ).one_or_none()
    if capacity is None or capacity.iteration_id != task.iteration_id:
        return None
    members = (
        await db.execute(
            fenced(
                select(
                    AgentActor.id,
                    AgentActor.profile_id,
                    AgentActor.role,
                    AgentActor.enabled,
                    AgentActor.scopes,
                    AgentTeamTopologyMember.actor_key,
                    AgentTeamTopologyMember.lifecycle_state,
                    AgentTeamTopologyMember.runtime_acknowledgement_digest,
                    AgentTeamTopology.id.label("team_id"),
                    AgentTeamTopology.topology_key,
                    AgentTeamTopology.revision,
                    AgentTeamTopology.primary_actor_id,
                )
                .select_from(AgentActor)
                .join(AgentTeamTopologyMember, AgentTeamTopologyMember.actor_id == AgentActor.id)
                .join(AgentTeamTopology, AgentTeamTopology.id == AgentTeamTopologyMember.topology_id)
                .where(AgentActor.id.in_(actors), AgentTeamTopology.state != "disabled")
                .order_by(AgentActor.id)
            )
        )
    ).all()
    if (
        {row.id for row in members} != actors
        or len({row.team_id for row in members}) != 1
        or any(
            not row.enabled
            or row.lifecycle_state != "runtime_ready"
            or not row.runtime_acknowledgement_digest
            for row in members
        )
    ):
        return None
    if assignment.purpose == "execution" and not any(
        row.id == assignment.actor_id and row.profile_id == capacity.profile_id for row in members
    ):
        return None
    from app.authority import internal_authority
    from app.config import get_settings

    if get_settings().workchord_auth_mode == "managed":
        # A worker need not read another principal's grants. Only the hash of
        # grants on the authenticated assignment's project is used here.
        with internal_authority(db):
            permissions = (
                await db.execute(
                    fenced(
                        select(
                            Principal.agent_actor_id,
                            Principal.enabled,
                            WorkspaceMembership.role,
                            ProjectMembership.role,
                        )
                        .select_from(Principal)
                        .join(WorkspaceMembership, WorkspaceMembership.principal_id == Principal.id)
                        .join(ProjectMembership, ProjectMembership.principal_id == Principal.id)
                        .where(
                            Principal.agent_actor_id.in_(actors),
                            ProjectMembership.project_id == task.project_id,
                        )
                        .order_by(Principal.agent_actor_id)
                    )
                )
            ).all()
        roles = {row.id: row.role for row in members}
        allowed = {
            "pm": {"manager"},
            "worker": {"editor", "executor", "manager"},
            "verifier": {"reviewer", "manager"},
        }
        if {item[0] for item in permissions} != actors or any(
            not item[1] or item[3] not in allowed.get(roles[item[0]], set()) for item in permissions
        ):
            return None
    else:
        permissions = []
    if as_of is not None:
        for member in members:
            prior = await db.scalar(
                select(TaskEvent.payload)
                .where(
                    TaskEvent.actor_id == member.id,
                    TaskEvent.event_type == "agent.team_runtime_acknowledged",
                    TaskEvent.created_at <= as_of,
                )
                .order_by(TaskEvent.created_at.desc(), TaskEvent.id.desc())
                .limit(1)
            )
            try:
                ack = json.loads(prior)
            except (TypeError, ValueError):
                return None
            if not isinstance(ack, dict) or (
                ack.get("actor_id"),
                ack.get("actor_key"),
                ack.get("topology_key"),
                ack.get("topology_revision"),
                ack.get("runtime_ready"),
            ) != (member.id, member.actor_key, member.topology_key, member.revision, True):
                return None
            historical_digest = ack.get("acknowledgement_digest")
            if historical_digest != member.runtime_acknowledgement_digest and (
                historical_digest not in await earlier_acknowledgements(db, member)
            ):
                return None
    bindings = (
        await db.execute(
            fenced(
                select(
                    AgentModelBinding.actor_id,
                    AgentModelBinding.id,
                    AgentModelBinding.revision,
                    AgentModelBinding.is_default,
                    AgentModelCatalogEntry.id,
                    AgentModelCatalogEntry.revision,
                    AgentModelCatalogEntry.key,
                    AgentModelCatalogEntry.configured_model_alias,
                    AgentModelCatalogEntry.publisher_key,
                )
                .select_from(AgentModelBinding)
                .join(AgentModelCatalogEntry, AgentModelCatalogEntry.id == AgentModelBinding.model_catalog_id)
                .where(
                    AgentModelBinding.actor_id.in_(actors),
                    AgentModelBinding.enabled.is_(True),
                    AgentModelCatalogEntry.enabled.is_(True),
                )
                .order_by(AgentModelBinding.id)
            )
        )
    ).all()
    if {row[0] for row in bindings} != actors:
        return None
    links = (
        await db.execute(
            fenced(
                select(ExternalLink.id, ExternalLink.provider, ExternalLink.external_key, ExternalLink.url)
                .where(ExternalLink.entity_type == "task", ExternalLink.entity_id == task.id)
                .order_by(ExternalLink.id)
            )
        )
    ).all()
    return (
        {
            "project": task.project_id,
            "strict": policy,
            "capacity": tuple(capacity),
            "links": [tuple(row) for row in links],
            "permissions": [tuple(row) for row in permissions],
            "members": [tuple(row) for row in members],
            "bindings": [tuple(row) for row in bindings],
        },
        members,
    )


async def window_authority_matches(db, task, assignment, *, lock=False):
    if assignment.task_version == task.version:
        return True
    if not assignment_matches(task, assignment):
        return False
    expected = current_window(task).get("authority", {}).get(str(assignment.id))
    return await authority_matches(db, task, assignment, expected, lock=lock)


async def require_window_authority(db, task, assignment):
    from app.services.agent_service import AgentConflictError

    if not await window_authority_matches(db, task, assignment, lock=True):
        raise AgentConflictError(
            "The planning-only execution fence no longer matches current ownership, team, policy or model bindings."
        )


def make_window(task, old_version, assignments, *, prior=None, evidence):
    eligible = {
        str(row.id): assignment_context(row)
        for row in assignments
        if row.task_id == task.id
        and row.state in {"accepted", "queued"}
        and (
            row.task_version == old_version
            or prior
            and prior["assignments"].get(str(row.id)) == assignment_context(row)
        )
    }
    if not eligible or task.version != old_version + 1:
        return None
    return {
        "kind": "iteration_end_extension",
        "from": prior["from"] if prior else old_version,
        "through": task.version,
        "task_context": task_context(task),
        "assignments": eligible,
        "evidence": evidence,
    }


async def original_ownership(db, task, row, before):
    """Verify one current assignment against its original, authenticated worker, PM or reviewer receipt."""
    from app.services.execution_reconciliation import _json_value
    from app.services.review_provenance import actor_provenance, rework_binding_identity

    records = select(AgentIdempotencyRecord).where(AgentIdempotencyRecord.created_at < before)
    if row.state == "accepted" and row.purpose == "execution":
        runs = (
            await db.scalars(
                select(AgentRun)
                .where(
                    AgentRun.assignment_id == row.id,
                    AgentRun.task_id == task.id,
                    AgentRun.actor_id == row.actor_id,
                    AgentRun.status == LIVE_RUN_STATE,
                )
                .limit(2)
            )
        ).all()
        receipt = await db.scalar(
            records.where(
                AgentIdempotencyRecord.actor_id == row.actor_id,
                AgentIdempotencyRecord.target_type == "assignment",
                AgentIdempotencyRecord.target_id == row.id,
                AgentIdempotencyRecord.operation.in_(("work.begin", "work.renew")),
            )
            .order_by(AgentIdempotencyRecord.id.desc())
            .limit(1)
        )
        if len(runs) != 1 or not receipt or not task.claim_id or task.claimed_by != row.actor_id:
            return None
        run = runs[0]
        try:
            raw = json.loads(receipt.response_payload)
            observed = raw["response_without_claim_id"]
            prior_run = observed["run"]
            prior_task = observed["task"]
            if (
                raw.get("claim_sha256") != hashlib.sha256(task.claim_id.encode()).hexdigest()
                or (
                    prior_run["id"],
                    prior_run["assignment_id"],
                    prior_run["actor_id"],
                    prior_run["task_id"],
                    prior_run["status"],
                )
                != (run.id, row.id, row.actor_id, task.id, LIVE_RUN_STATE)
                or observed["assignment"]["id"] != row.id
                or observed["assignment"]["task_version"] != row.task_version
                or observed["claim_generation"] != task.claim_generation
                or run.claim_generation != task.claim_generation
                or (
                    prior_task["id"],
                    prior_task["version"],
                    prior_task["brief_revision"],
                    prior_task["artifact_revision"],
                )
                != (task.id, row.task_version, task.brief_revision, task.artifact_revision)
            ):
                return None
            previous = prior_run["execution_provenance"]
            stored = run.execution_provenance or {}
            actor = await db.get(AgentActor, row.actor_id)
            bound = await actor_provenance(db, actor, binding_id=previous["binding_id"])
            policy = await db.scalar(
                select(Project.require_different_review_publisher).where(Project.id == task.project_id)
            )
            if (
                not previous["publisher_key"]
                or previous["source"] != "authenticated_work_begin"
                or previous["different_publisher_required"] != policy
                or rework_binding_identity(bound) != rework_binding_identity(previous)
                or rework_binding_identity(previous) != rework_binding_identity(stored)
            ):
                return None
            captured_links = {
                (link["id"], link["provider"], link.get("external_key"), link.get("url"))
                for link in prior_task.get("external_links", ())
                if link.get("id") is not None
            }
            actual_links = (
                await db.execute(
                    select(
                        ExternalLink.id, ExternalLink.provider, ExternalLink.external_key, ExternalLink.url
                    ).where(ExternalLink.entity_type == "task", ExternalLink.entity_id == task.id)
                )
            ).all()
            if captured_links != {tuple(link) for link in actual_links}:
                return None
        except (KeyError, TypeError, ValueError):
            return None
        return {"receipt": receipt.id, "run": run.id, "generation": run.claim_generation}
    if row.state != "queued":
        return None
    if row.purpose == "verification" or row.purpose == "execution" and row.queue_class == "normal":
        query = records.where(
            AgentIdempotencyRecord.actor_id == row.assigned_by_actor_id,
            AgentIdempotencyRecord.operation == "assignment.create",
            AgentIdempotencyRecord.target_type == "task",
            AgentIdempotencyRecord.target_id == task.id,
            _json_value(db, AgentIdempotencyRecord.response_payload, "response", "id", integer=True)
            == row.id,
        )
        field = None
    elif row.purpose == "execution" and row.queue_class == "recovery":
        query = records.where(
            AgentIdempotencyRecord.actor_id == row.assigned_by_actor_id,
            AgentIdempotencyRecord.operation == "recovery.requeue",
            AgentIdempotencyRecord.target_type == "task",
            AgentIdempotencyRecord.target_id == task.id,
            _json_value(
                db, AgentIdempotencyRecord.response_payload, "response", "assignment", "id", integer=True
            )
            == row.id,
        )
        field = "assignment"
    elif row.purpose == "execution" and row.queue_class == "rework":
        query = records.where(
            AgentIdempotencyRecord.actor_id == row.assigned_by_actor_id,
            AgentIdempotencyRecord.operation == "verification.verdict",
            AgentIdempotencyRecord.target_type == "assignment",
            _json_value(
                db,
                AgentIdempotencyRecord.response_payload,
                "response",
                "rework_assignment",
                "id",
                integer=True,
            )
            == row.id,
        )
        field = "rework_assignment"
    else:
        return None
    records = (await db.scalars(query.limit(2))).all()
    if len(records) != 1:
        return None
    try:
        original = json.loads(records[0].response_payload)["response"]
        captured = original[field] if field else original
        if (
            captured["id"],
            captured["task_id"],
            captured["actor_id"],
            captured["purpose"],
            captured["task_version"],
            captured["team_member_id"],
            captured["reviewer_profile_id"],
            captured.get("review_selection"),
        ) != (
            row.id,
            task.id,
            row.actor_id,
            row.purpose,
            row.task_version,
            row.team_member_id,
            row.reviewer_profile_id,
            row.review_selection,
        ):
            return None
        snapshot = json.loads(row.routing_snapshot or "{}")
        if (captured.get("routing_snapshot") or {}) != snapshot:
            return None
        if row.purpose == "execution" and row.queue_class in {"normal", "recovery"}:
            return {"receipt": records[0].id}
        if field:
            candidate = original["review_assignment"]["review_selection"]["candidate"]
        else:
            candidate = row.review_selection["candidate"]
        if (candidate["task_id"], candidate["brief_revision"], candidate["artifact_revision"]) != (
            task.id,
            task.brief_revision,
            task.artifact_revision,
        ):
            return None
        if not await db.scalar(
            select(Project.require_different_review_publisher).where(Project.id == task.project_id)
        ):
            return None
    except (TypeError, ValueError, KeyError):
        return None
    return {"receipt": records[0].id, "candidate_digest": candidate["digest"]}


async def seal_authority(db, task, window, assignments, *, prior=None, lock=False, as_of=None):
    from app.utils.time import utc_now

    stamps = {}
    for row in assignments:
        key = str(row.id)
        if key not in window["assignments"]:
            continue
        if as_of is None and not await original_ownership(db, task, row, utc_now()):
            continue
        stamp = await authority_stamp(db, task, row, lock=lock, as_of=as_of)
        sealed = prior.get("authority", {}).get(key) if prior else None
        if stamp and (
            row.task_version == task.version - 1
            or sealed == stamp
            or sealed
            and as_of is None
            and await authority_matches(db, task, row, sealed, lock=lock)
        ):
            stamps[key] = stamp
    window["assignments"] = {key: value for key, value in window["assignments"].items() if key in stamps}
    window["authority"] = stamps
    return window if stamps else None


async def extension_input(db, values, iterations):
    """Only an explicit date-only extension may preserve issued execution state."""
    data = values.get("data")
    iteration_id = values.get("iteration_id")
    if (
        data is None
        or set(getattr(data, "model_fields_set", ())) - {"expected_revisions"} != {"end_date"}
        or not data.end_date
    ):
        return None
    if len(iterations) != 1 or iteration_id not in iterations:
        return None
    old = await db.scalar(select(Iteration.end_date).where(Iteration.id == iteration_id))
    if old is None or data.end_date <= old:
        return None
    return {
        "iteration_id": iteration_id,
        "previous_end": old.isoformat(),
        "new_end": data.end_date.isoformat(),
    }


async def live_assignments(db, task_ids, *, lock=False):
    assignments = {}
    if not task_ids:
        return assignments
    query = (
        select(AgentTaskAssignment)
        .where(
            AgentTaskAssignment.task_id.in_(task_ids), AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES)
        )
        .order_by(AgentTaskAssignment.task_id, AgentTaskAssignment.id)
    )
    rows = await db.scalars(query.with_for_update() if lock else query)
    for row in rows:
        assignments.setdefault(row.task_id, []).append(row)
    return assignments
