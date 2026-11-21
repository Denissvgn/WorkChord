"""Preserve a proved assignment context across an iteration end-date extension."""

from __future__ import annotations

import hashlib
import json

from sqlalchemy import select
from app.agent_contract import EXECUTION_PLANNING_WINDOW_FEATURE

from app.models.agent import (
    AgentActor,
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


async def authority_stamp(db, task, assignment, *, lock=False, as_of=None):
    """Fingerprint the actual scope, roster and bindings of both assignment principals."""
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
            if historical_digest != member.runtime_acknowledgement_digest:
                # A runtime can acknowledge the newly advertised optional command
                # after upgrading. Reconstruct the exact previous acknowledged
                # bytes. Every field other than that one capability must match.
                from app.services.agent_team_setup_service import _digest

                encoded = await db.scalar(
                    select(AgentTeamTopologyMember.runtime_acknowledgement_payload).where(
                        AgentTeamTopologyMember.actor_id == member.id
                    )
                )
                try:
                    current = json.loads(encoded)
                    features = current["server_features"]
                    if (
                        not isinstance(features, list)
                        or features.count(EXECUTION_PLANNING_WINDOW_FEATURE) != 1
                        or _digest(current) != member.runtime_acknowledgement_digest
                        or _digest(
                            {
                                **current,
                                "server_features": [
                                    v for v in features if v != EXECUTION_PLANNING_WINDOW_FEATURE
                                ],
                            }
                        )
                        != historical_digest
                    ):
                        return None
                except (ValueError, TypeError, KeyError):
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
    return digest(
        {
            "project": task.project_id,
            "strict": policy,
            "capacity": tuple(capacity),
            "links": [tuple(row) for row in links],
            "permissions": [tuple(row) for row in permissions],
            "members": [tuple(row) for row in members],
            "bindings": [tuple(row) for row in bindings],
        }
    )


async def window_authority_matches(db, task, assignment, *, lock=False):
    if assignment.task_version == task.version:
        return True
    if not assignment_matches(task, assignment):
        return False
    expected = current_window(task).get("authority", {}).get(str(assignment.id))
    return bool(expected and await authority_stamp(db, task, assignment, lock=lock) == expected)


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


async def seal_authority(db, task, window, assignments, *, prior=None, lock=False, as_of=None):
    from app.services.planning_window_reconciliation import _ownership
    from app.utils.time import utc_now

    stamps = {}
    for row in assignments:
        key = str(row.id)
        if key not in window["assignments"]:
            continue
        if as_of is None and not await _ownership(db, task, row, utc_now()):
            continue
        stamp = await authority_stamp(db, task, row, lock=lock, as_of=as_of)
        if stamp and (
            row.task_version == task.version - 1 or prior and prior.get("authority", {}).get(key) == stamp
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
            AgentTaskAssignment.task_id.in_(task_ids), AgentTaskAssignment.state.in_(("queued", "accepted"))
        )
        .order_by(AgentTaskAssignment.task_id, AgentTaskAssignment.id)
    )
    rows = await db.scalars(query.with_for_update() if lock else query)
    for row in rows:
        assignments.setdefault(row.task_id, []).append(row)
    return assignments
