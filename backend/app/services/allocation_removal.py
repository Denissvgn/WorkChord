"""Check whether removing a capacity allocation changes planning alone."""

import json
from dataclasses import dataclass
from functools import lru_cache

from pydantic import TypeAdapter

from sqlalchemy import String, cast, inspect, or_, select, text

from app.authority import internal_authority
from app.commands import PlanningConflict, current_command
from app.database import Base
from app.models.capacity import PlanningState
from app.schemas.agent_routing import RoutingDecisionSnapshot
from app.services.agent_routing_policy import (
    MAX_ROUTING_SNAPSHOT_BYTES,
    ROUTING_DECISION_AUTHORITY,
    ROUTING_DECISION_LINEAGE_FIELDS,
    ROUTING_LINEAGE_AUTHORITY,
    ROUTING_POLICY_VERSION,
)
from app.services.execution_planning_window import LIVE_ASSIGNMENT_STATES, LIVE_RUN_STATE
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.task import Task
from app.models.team_member import TeamMember


def foreign_keys_to_members(connection):
    """Return the physical allocation references, including extensions absent from the ORM."""
    if connection.dialect.name == "postgresql":
        rows = connection.execute(
            text("""
            SELECT CASE WHEN ns.nspname=current_schema() THEN rel.relname
                        ELSE ns.nspname||'.'||rel.relname END, a.attname
            FROM pg_constraint c JOIN pg_class rel ON rel.oid=c.conrelid
            JOIN pg_namespace ns ON ns.oid=rel.relnamespace
            JOIN pg_attribute a ON a.attrelid=c.conrelid AND a.attnum=ANY(c.conkey)
            WHERE c.contype='f' AND c.confrelid='team_members'::regclass
        """)
        )
        return {tuple(row) for row in rows}
    if connection.dialect.name == "sqlite":
        rows = connection.execute(
            text("""
            SELECT lower(m.name), lower(f."from") FROM main.sqlite_master m, pragma_foreign_key_list(m.name) f
            WHERE m.type='table' AND lower(f."table")='team_members'
        """)
        )
        return {tuple(row) for row in rows}
    return {
        (table, column)
        for (_, table), keys in inspect(connection).get_multi_foreign_keys().items()
        for key in keys
        if key["referred_table"] == "team_members"
        for column in key["constrained_columns"]
    }


def _history_statement(dialect):
    # Traverse only canonical task nodes, including nested children and project
    # backlog snapshots. Listing an otherwise unused allocation in an iteration's
    # team inventory is expected and keeps that recovery point restorable.
    if dialect == "sqlite":
        roots = """SELECT CASE WHEN e.type='object' THEN e.value ELSE '{}' END
            FROM application_snapshots s, json_each(CASE WHEN json_type(s.payload,'$.tasks')='array'
                THEN json_extract(s.payload,'$.tasks') ELSE '[{}]' END) e"""
        children = """SELECT CASE WHEN e.type='object' THEN e.value ELSE '{}' END
            FROM saved, json_each(CASE WHEN json_type(node,'$.children') IS NULL THEN '[]'
                WHEN json_type(node,'$.children')='array' THEN json_extract(node,'$.children') ELSE '[{}]' END) e"""
        referenced = """json_type(node,'$.assignee_id') IS NULL
            OR json_type(node,'$.assignee_id') NOT IN ('null','integer')
            OR json_extract(node,'$.assignee_id') <= 0
            OR CAST(json_extract(node,'$.assignee_id') AS TEXT)=:member"""
    elif dialect == "postgresql":
        roots = """SELECT CASE WHEN jsonb_typeof(e.value)='object' THEN e.value ELSE '{}'::jsonb END FROM application_snapshots s,
            jsonb_array_elements(CASE WHEN jsonb_typeof(s.payload::jsonb->'tasks')='array'
                THEN s.payload::jsonb->'tasks' ELSE '[{}]'::jsonb END) e"""
        children = """SELECT CASE WHEN jsonb_typeof(e.value)='object' THEN e.value ELSE '{}'::jsonb END FROM saved,
            jsonb_array_elements(CASE WHEN node->'children' IS NULL THEN '[]'::jsonb
                WHEN jsonb_typeof(node->'children')='array' THEN node->'children' ELSE '[{}]'::jsonb END) e"""
        referenced = """NOT (node ? 'assignee_id')
            OR jsonb_typeof(node->'assignee_id') NOT IN ('null','number')
            OR (jsonb_typeof(node->'assignee_id')='number' AND node->>'assignee_id' !~ '^[1-9][0-9]*$')
            OR node->>'assignee_id'=:member"""
    else:
        return None
    return text(
        f"WITH RECURSIVE saved(node) AS ({roots} UNION ALL {children}) "
        f"SELECT EXISTS (SELECT 1 FROM saved WHERE {referenced})"
    )


async def _historical_task_reference(db, member_id):
    statement = _history_statement(db.get_bind().dialect.name)
    return statement is None or bool(await db.scalar(statement, {"member": str(member_id)}))


_GROUPS = {
    "review_floor": {"review_mode", "reviewer_profile_ids", "independence_must_be_revalidated"},
    "cause": {"category", "reason"},
    "model_tier_change": {
        "eligible",
        "comparison_available",
        "previous_reasoning_tier",
        "previous_context_tier",
        "selected_reasoning_tier",
        "selected_context_tier",
        "applied",
        "reason",
    },
    "selection_result": {"completed_by_snapshot", "assignment_id"},
}
_SCALARS = {
    "schema_version",
    "authority",
    "source_authority",
    "policy_version",
    "selection_pending",
    "task_id",
    "task_version",
    "purpose",
    "queue_class",
    "provisional_actor_id",
    "supervised_actor_id",
}


@lru_cache(maxsize=64)
def _decision_field(name):
    return TypeAdapter(RoutingDecisionSnapshot.model_fields[name].rebuild_annotation())


def _positive_ids(values):
    return isinstance(values, list) and all(type(value) is int and value > 0 for value in values)


def _lineage_ids(value):
    """Classify the current pending and completed lineage formats and their compact prior decisions."""
    if not (
        isinstance(value, dict)
        and value.get("schema_version") == "routing-lineage-snapshot-v1"
        and value.get("authority") == ROUTING_LINEAGE_AUTHORITY
        and value.get("policy_version") == ROUTING_POLICY_VERSION
        and value.get("selection_pending") is True
        and value.get("purpose") == "execution"
        and value.get("queue_class") in ("rework", "recovery")
        and all(
            type(value.get(k)) is int and value[k] > 0
            for k in ("task_id", "task_version", "provisional_actor_id")
        )
        and all(k in value for k in ("review_floor", "cause", "model_tier_change"))
        and value.get("source_authority", "verified") == "verified"
        and _positive_ids(value.get("source_assignment_ids"))
        and isinstance(value.get("prior_decisions"), list)
        and not set(value) - _SCALARS - _GROUPS.keys() - {"source_assignment_ids", "prior_decisions"}
    ):
        return None
    if "supervised_actor_id" in value and (
        value["queue_class"] != "recovery"
        or type(value["supervised_actor_id"]) is not int
        or value["supervised_actor_id"] != value["provisional_actor_id"]
    ):
        return None
    if any(isinstance(value[k], (dict, list)) for k in value.keys() & _SCALARS):
        return None
    for group, fields in _GROUPS.items():
        if group not in value:
            continue
        section = value[group]
        if not isinstance(section, dict) or set(section) - fields:
            return None
        for name, item in section.items():
            if name == "reviewer_profile_ids":
                if not _positive_ids(item):
                    return None
            elif isinstance(item, (dict, list)):
                return None
    owners = set()
    for decision in value["prior_decisions"]:
        if not (
            isinstance(decision, dict)
            and decision.get("schema_version") == "routing-decision-snapshot-v1"
            and decision.get("authority") == ROUTING_DECISION_AUTHORITY
            and "capacity_owner_id" in decision
            and set(decision) <= set(ROUTING_DECISION_LINEAGE_FIELDS)
        ):
            return None
        for name, item in decision.items():
            if name in RoutingDecisionSnapshot.model_fields:
                _decision_field(name).validate_python(item)
            elif name == "source_assignment_id" and (type(item) is not int or item < 1):
                return None
            elif name == "snapshot_sha256" and not (
                isinstance(item, str) and len(item) == 64 and all(c in "0123456789abcdef" for c in item)
            ):
                return None
        if decision["capacity_owner_id"] is not None:
            owners.add(decision["capacity_owner_id"])
    return owners


@lru_cache(maxsize=256)
def _routing_ids(raw):
    """Cache verified owners by the exact bounded source bytes; None denotes unclassified history."""
    try:
        saved = json.loads(raw)
        if saved == {}:
            return frozenset()
        if not isinstance(saved, dict):
            return None
        if saved.get("schema_version") == "workchord-runner-supervised-dispatch-v1":
            # This bounded runner format stores a model selection and an assessment
            # reference. Classifying those fields confers no producer authority.
            if (
                set(saved) == {"schema_version", "model_catalog_key", "assessment_id"}
                and type(saved["assessment_id"]) is int
                and saved["assessment_id"] > 0
                and _decision_field("model_catalog_key").validate_python(saved["model_catalog_key"])
                == saved["model_catalog_key"]
            ):
                return frozenset()
            return None
        if saved.get("schema_version") == "routing-decision-snapshot-v1":
            model = RoutingDecisionSnapshot.model_validate(saved)
            result = _lineage_ids(model.prior_lineage) if model.prior_lineage is not None else set()
            if result is not None and model.capacity_owner_id is not None:
                result.add(model.capacity_owner_id)
        else:
            result = _lineage_ids(saved)
        return frozenset(result) if result is not None else None
    except (TypeError, ValueError, RecursionError):
        return None


@dataclass(frozen=True)
class AllocationHistory:
    revision: int
    unused: bool | None


def _mapped_references():
    return {
        (table.name, key.parent.name): key.parent
        for table in Base.metadata.tables.values()
        for key in table.foreign_keys
        if key.target_fullname == "team_members.id"
    }


def mapped_allocation_references(db):
    names = set(_mapped_references())
    if db.get_bind().dialect.name == "sqlite":
        return {(table.lower(), column.lower()) for table, column in names}
    return names


async def _direct_reference(db, member_id):
    queries = [
        select(column).where(column == member_id).exists() for column in _mapped_references().values()
    ]
    return bool(await db.scalar(select(or_(*queries))))


async def inspect_allocation_history(db, member_id):
    """Read history before the planning writer is reserved; return only its revision and a boolean."""
    with db.no_autoflush, internal_authority(db):
        state = current_command(db)
        revision = (
            state.planning_revision
            if state and state.planning_revision is not None
            else (await db.scalar(select(PlanningState.revision).where(PlanningState.id == 1)) or 0)
        )
        # A deliberately referenced allocation normally takes the legacy path.
        # Recheck this inexpensive hint under the member lock before making the decision.
        if await _direct_reference(db, member_id):
            return AllocationHistory(revision, None)
        statements = (
            select(AgentTaskAssignment.routing_snapshot)
            .where(AgentTaskAssignment.routing_snapshot != "{}")
            .execution_options(yield_per=64)
        )
        snapshots = await db.stream_scalars(statements)
        try:
            async for raw in snapshots:
                if not isinstance(raw, str) or len(raw.encode("utf-8")) > MAX_ROUTING_SNAPSHOT_BYTES:
                    return AllocationHistory(revision, False)
                owners = _routing_ids(raw)
                if owners is None or member_id in owners:
                    return AllocationHistory(revision, False)
        finally:
            await snapshots.close()
        return AllocationHistory(revision, not await _historical_task_reference(db, member_id))


async def is_unused_allocation(db, member_id, history, *, unused_only):
    """Called after authorization and the global planning and affected iteration locks."""
    row = (
        await db.execute(
            select(TeamMember.id, TeamMember.iteration_id, TeamMember.profile_id)
            .where(TeamMember.id == member_id)
            .with_for_update()
        )
    ).one_or_none()
    if row is None:
        return False
    if history.unused is False:
        return False
    # Restrict this internal read to a boolean. Hidden reference rows, IDs and
    # historical content must neither disappear from the proof nor reach the caller.
    with db.no_autoflush, internal_authority(db):
        actual = await (await db.connection()).run_sync(foreign_keys_to_members)
        if mapped_allocation_references(db) != actual:
            return False
        if await _direct_reference(db, member_id):
            return False
        if history.unused is None:
            # A direct reference existed at observation time. History was not read.
            return False
        if row.profile_id is not None and row.iteration_id is not None:
            issued = (
                select(AgentTaskAssignment.id)
                .join(Task, Task.id == AgentTaskAssignment.task_id)
                .join(AgentActor, AgentActor.id == AgentTaskAssignment.actor_id)
                .where(
                    Task.iteration_id == row.iteration_id,
                    AgentTaskAssignment.state.in_(LIVE_ASSIGNMENT_STATES),
                    or_(
                        AgentActor.profile_id == row.profile_id,
                        AgentTaskAssignment.reviewer_profile_id == row.profile_id,
                        cast(
                            AgentTaskAssignment.review_selection["reviewer"]["profile_id"].as_string(),
                            String,
                        )
                        == str(row.profile_id),
                    ),
                )
                .limit(1)
            )
            if await db.scalar(issued) is not None:
                return False
            running = (
                select(AgentRun.id)
                .join(Task, Task.id == AgentRun.task_id)
                .join(AgentActor, AgentActor.id == AgentRun.actor_id)
                .where(
                    AgentRun.status == LIVE_RUN_STATE,
                    Task.iteration_id == row.iteration_id,
                    or_(
                        AgentActor.profile_id == row.profile_id,
                        cast(AgentRun.execution_provenance["profile_id"].as_string(), String)
                        == str(row.profile_id),
                    ),
                )
                .limit(1)
            )
            if await db.scalar(running) is not None:
                return False
            owner_task = (
                select(Task.id)
                .where(
                    Task.iteration_id == row.iteration_id,
                    Task.status != "closed",
                    Task.owner_profile_id == row.profile_id,
                )
                .limit(1)
            )
            if await db.scalar(owner_task) is not None:
                return False
    if current_command(db).planning_revision != history.revision:
        if unused_only:
            raise PlanningConflict(
                "planning_scope_changed",
                "Planning inputs changed while checking allocation history. Reload the member context.",
            )
        # The ordinary caller still has the original referenced-row operation.
        return False
    return True
