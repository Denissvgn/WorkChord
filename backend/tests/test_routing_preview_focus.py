"""A focused routing preview keeps a named team actor's rows inside the bounded response."""

import json

import pytest
from pydantic import ValidationError

from app.config import get_settings
from app.models.agent import AgentActor, AgentModelBinding, AgentModelCatalogEntry, AgentRun, AgentTaskAssignment
from app.models.iteration import Iteration
from app.schemas.agent import ModelAwareAgentTaskAssignmentCreate
from app.schemas.agent_routing import AgentRoutingPreviewCreate
from app.services import agent_routing_service
from app.services.agent_routing_policy import (
    MAX_ROUTING_EXCLUSIONS,
    MAX_ROUTING_PACKET_BYTES,
    canonical_routing_json_bytes,
)
from app.services.agent_routing_service import AgentRoutingConflictError, AgentRoutingService
from app.services.agent_work_service import AgentWorkService
from app.services.task_service import TaskService
from app.utils.time import utc_now
from tests.support.transactions import reload_session_fixture
from tests.test_agent_routing_service import _command_context
from tests.test_agent_routing_wave6_qualification import _assessment_command, _dispatch
from tests.test_agent_team_setup_qualification import (
    acknowledge_all,
    default_candidate,
    provision_ready_topology,
    routing_base,
)
from tests.test_review_provenance import database_engines
from tests.test_scoped_review_evidence import through
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory

# More of the team's own excluded rows than one bounded response can hold.
TEAM_FILLER_ROWS = MAX_ROUTING_EXCLUSIONS + 5
# A runtime acknowledges at most 16 enabled bindings: its default and these.
WORKER_ALTERNATIVES = 15
# The longest model alias, in multibyte characters, and extra declared tools,
# so that the worker's eligible rows alone overflow the response packet.
LONG_ALIAS = "\u754c" * 255
EXTRA_TOOL_TAGS = [f"declared-tool-{index:02d}-of-the-alternative" for index in range(8)]


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


def size(value):
    return len(canonical_routing_json_bytes(value))


def find(items, actor_id, binding_id):
    return [row for row in items if (row["actor_id"], row.get("model_binding_id")) == (actor_id, binding_id)]


def totals(preview):
    return (
        len(preview["eligible_candidates"]) + preview["eligible_candidates_omitted"],
        len(preview["exclusions"]) + preview["exclusions_omitted"],
    )


def catalog_entry(key, *, alias=None):
    return AgentModelCatalogEntry(
        key=key,
        provider="test-provider",
        configured_model_alias=alias or f"runtime-{key}",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="balanced",
        enabled=True,
        revision=1,
    )


async def bind_fillers(db, actor, prefix, count, *, enabled, alias=None, tool_tags=()):
    entries = [catalog_entry(f"{prefix}-{index}", alias=alias) for index in range(count)]
    db.add_all(entries)
    await db.flush()
    db.add_all(
        AgentModelBinding(
            actor_id=actor.id, model_catalog_id=entry.id, enabled=enabled, tool_tags=list(tool_tags), revision=1
        )
        for entry in entries
    )


async def occupy(db, actor, iteration, task_factory, title):
    """Give the actor accepted work elsewhere with a running run."""

    other = await task_factory(iteration=iteration, title=title)
    assignment = AgentTaskAssignment(
        task_id=other.id, actor_id=actor.id, task_version=other.version, state="accepted"
    )
    db.add(assignment)
    await db.flush()
    run = AgentRun(task_id=other.id, actor_id=actor.id, assignment_id=assignment.id, status="running")
    db.add(run)
    await db.commit()
    return assignment, run


def preview_reader(db_session_factory, monkeypatch, task_id, base_body):
    async def read(key, **focus):
        body = {**base_body, **focus}
        rest = await through(
            "rest",
            db_session_factory,
            monkeypatch,
            "agent_preview_task_routing",
            f"/api/agent/tasks/{task_id}/routing-preview",
            key,
            body,
            task_id=task_id,
        )
        mcp = await through(
            "mcp",
            db_session_factory,
            monkeypatch,
            "agent_preview_task_routing",
            f"/api/agent/tasks/{task_id}/routing-preview",
            key,
            body,
            task_id=task_id,
        )
        assert rest == mcp
        assert size(rest) <= MAX_ROUTING_PACKET_BYTES
        return rest

    return read


@pytest.mark.sqlite
def test_focused_binding_requires_its_actor():
    with pytest.raises(ValidationError, match="focus_actor_id"):
        AgentRoutingPreviewCreate(
            purpose="execution", assessment_id=1, expected_task_version=1, focus_model_binding_id=2
        )
    unfocused = AgentRoutingPreviewCreate(purpose="execution", assessment_id=1, expected_task_version=1)
    assert "focus_actor_id" not in unfocused.model_dump()
    assert "focus_model_binding_id" not in unfocused.model_dump()


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_focus_returns_named_worker_blockers_and_selection_on_rest_and_mcp(
    db_session,
    db_session_factory,
    actor_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    team = await provision_ready_topology(db)
    worker = team.actors["operations-worker"]
    teammate = team.actors[team.manifest.workers[0].actor_key]
    assert teammate.id < worker.id
    base = await routing_base(
        db,
        topology=team,
        actor_key="operations-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Prepare the bounded release package",
        skill_key="security-review",
    )
    task, pm = base.task, base.pm
    iteration = await db.get(Iteration, task.iteration_id)
    named = default_candidate(worker).binding
    named_pair = (worker.id, named.id)

    # The teammate's disabled bindings sort ahead of the worker's rows and fill
    # the exclusions. The worker's cheaper alternatives outrank its named
    # binding and, with long aliases, fill the response packet.
    await bind_fillers(db, teammate, "teammate-filler", TEAM_FILLER_ROWS, enabled=False)
    await bind_fillers(
        db,
        worker,
        "worker-alternative",
        WORKER_ALTERNATIVES,
        enabled=True,
        alias=LONG_ALIAS,
        tool_tags=EXTRA_TOOL_TAGS,
    )
    await db.commit()
    # The runtimes acknowledge their current bindings, so the team stays ready.
    await acknowledge_all(team.service, team.manifest, team.sink.keys)
    outsider = await actor_factory(name="outside-team-worker", display_name="Outside Team Worker")
    outside_catalog = catalog_entry("outside-team-runtime")
    db.add(outside_catalog)
    await db.flush()
    outside_binding = AgentModelBinding(
        actor_id=outsider.id, model_catalog_id=outside_catalog.id, is_default=True, enabled=True, revision=1
    )
    db.add(outside_binding)
    await db.commit()
    outsider_id, outside_binding_id, pm_id = outsider.id, outside_binding.id, pm.id

    assessment = (
        await AgentRoutingService(db).create_assessment(
            task.id,
            pm,
            _assessment_command(task_version=task.version, required_skill_levels={"security-review": 3}),
            _command_context("assess-focus"),
        )
    ).assessment
    now = utc_now().replace(microsecond=0)
    monkeypatch.setattr(agent_routing_service, "utc_now", lambda: now)
    read = preview_reader(
        db_session_factory,
        monkeypatch,
        task.id,
        {"purpose": "execution", "assessment_id": assessment.id, "expected_task_version": task.version},
    )
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    team_ids = {actor.id for actor in team.actors.values()}

    # Occupied: the worker owns an active run, so every one of its rows is
    # excluded, and its own team's rows push them out of the response.
    busy, run = await occupy(db, worker, iteration, task_factory, "The worker's current release")
    busy_id, run_id = busy.id, run.id
    plain = await read(pm_key)
    assert plain["recommended_candidate"] is None
    assert "no_eligible_candidate" in plain["hard_blocker_codes"]
    assert plain["exclusions_omitted"] > 0
    assert not find([*plain["eligible_candidates"], *plain["exclusions"]], *named_pair)

    focused = await read(pm_key, focus_actor_id=worker.id, focus_model_binding_id=named.id)
    (row,) = find(focused["exclusions"], *named_pair)
    assert "current_work_conflict" in row["hard_blocker_codes"]
    assert row["running_runs"] == 1 and row["accepted_assignments"] == 1
    assert focused["preview_id"] == plain["preview_id"]
    assert focused["input_digest"] == plain["input_digest"]
    assert focused["preview_digest"] != plain["preview_digest"]
    assert focused["hard_blocker_codes"] == plain["hard_blocker_codes"]
    assert totals(focused) == totals(plain)
    assert {item["actor_id"] for item in focused["exclusions"]} <= team_ids
    # Rows stay in their sorted order; the named row replaced a tail row.
    keys = [(item["actor_id"], item["model_binding_id"] or 0) for item in focused["exclusions"]]
    assert keys == sorted(keys)

    # Without a binding the focus keeps the worker's rows that fit.
    whole = await read(pm_key, focus_actor_id=worker.id)
    assert find(whole["exclusions"], *named_pair)
    assert all(
        "current_work_conflict" in item["hard_blocker_codes"]
        for item in whole["exclusions"]
        if item["actor_id"] == worker.id
    )
    assert totals(whole) == totals(plain)

    # Selection still recomputes the preview, and now names the real blockers.
    selection = ModelAwareAgentTaskAssignmentCreate(
        task_id=task.id,
        actor_id=worker.id,
        expected_task_version=task.version,
        purpose="execution",
        assessment_id=assessment.id,
        model_binding_id=named.id,
        model_binding_revision=named.revision,
        routing_preview_id=focused["preview_id"],
        routing_preview_digest=focused["preview_digest"],
        reason="Select the named worker and model.",
    )
    await reload_session_fixture(db)
    with pytest.raises(AgentRoutingConflictError) as occupied:
        await AgentRoutingService(db).validate_assignment_selection(
            task=await TaskService(db).get_by_id(task.id),
            selected_actor=await db.get(AgentActor, worker.id),
            data=selection,
        )
    assert occupied.value.code == "routing_selection_ineligible"
    assert occupied.value.context["hard_blocker_codes"] == row["hard_blocker_codes"]
    await db.rollback()

    # An actor outside the team, or no actor at all, changes nothing.
    for focus in (
        {"focus_actor_id": outsider_id},
        {"focus_actor_id": outsider_id, "focus_model_binding_id": outside_binding_id},
        {"focus_actor_id": outsider_id + 10_000},
    ):
        ignored = await read(pm_key, **focus)
        assert ignored == plain
        assert "outside-team" not in json.dumps(ignored)

    # Free: the worker's named binding is eligible but ranked past the bound.
    (await db.get(AgentTaskAssignment, busy_id)).state = "cancelled"
    (await db.get(AgentRun, run_id)).status = "succeeded"
    await db.commit()
    plain = await read(pm_key)
    assert plain["recommended_candidate"]["actor_id"] == named_pair[0]
    assert plain["eligible_candidates_omitted"] > 0
    assert not find([*plain["eligible_candidates"], *plain["exclusions"]], *named_pair)

    focused = await read(pm_key, focus_actor_id=named_pair[0], focus_model_binding_id=named_pair[1])
    (candidate,) = find(focused["eligible_candidates"], *named_pair)
    assert candidate["hard_blocker_codes"] == [] and candidate["eligible"] is True
    assert candidate["rank"] == totals(plain)[0] == WORKER_ALTERNATIVES + 1
    assert focused["recommended_candidate"] == plain["recommended_candidate"]
    assert totals(focused) == totals(plain)
    ranks = [item["rank"] for item in focused["eligible_candidates"]]
    assert ranks == sorted(ranks)
    assert focused["preview_id"] == plain["preview_id"]

    # The focused preview selects the named binding; the snapshot records
    # exactly the response the PM read.
    selection = selection.model_copy(
        update={
            "routing_preview_id": focused["preview_id"],
            "routing_preview_digest": focused["preview_digest"],
        }
    )
    await reload_session_fixture(db)
    assignment = await AgentWorkService(db).create_assignment(
        await db.get(AgentActor, pm_id),
        selection,
        idempotency_key="focus-named-worker",
        rationale="Dispatch the named worker and model.",
        correlation_id="focus-named-worker",
    )
    snapshot = (await db.get(AgentTaskAssignment, assignment.id)).routing_snapshot
    snapshot = json.loads(snapshot) if isinstance(snapshot, str) else snapshot
    assert (snapshot["actor_id"], snapshot["model_binding_id"]) == named_pair
    assert snapshot["selected_rank"] == candidate["rank"]
    assert snapshot["routing_preview_digest"] == focused["preview_digest"]
    assert snapshot["eligible_candidates_omitted"] == focused["eligible_candidates_omitted"]
    assert snapshot["exclusions_omitted"] == focused["exclusions_omitted"]


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_focus_returns_named_reviewer_blockers_on_rest_and_mcp(
    db_session,
    db_session_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    team = await provision_ready_topology(db)
    worker = team.actors["operations-worker"]
    reviewer = team.actors["independent-verifier"]
    teammate = team.actors[team.manifest.workers[0].actor_key]
    assert teammate.id < reviewer.id
    base = await routing_base(
        db,
        topology=team,
        actor_key="operations-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Review the bounded security change",
        skill_key="security-review",
    )
    task, pm = base.task, base.pm
    iteration = await db.get(Iteration, task.iteration_id)
    await team_member_factory(profile=reviewer.profile, iteration=iteration)
    reviewer_binding = default_candidate(reviewer).binding
    reviewer_pair = (reviewer.id, reviewer_binding.id)
    await bind_fillers(db, teammate, "teammate-filler", TEAM_FILLER_ROWS, enabled=False)
    await db.commit()
    await acknowledge_all(team.service, team.manifest, team.sink.keys)

    request = _assessment_command(
        task_version=task.version,
        required_skill_levels={"security-review": 3},
        minimum_reasoning_tier=3,
        minimum_context_tier="large",
        axes={"reasoning": 3, "ambiguity": 2, "context_breadth": 2, "risk": 3, "verification_burden": 3},
        reason_codes=("security", "specialist-verification"),
    )
    service = AgentRoutingService(db)
    assessment = (await service.create_assessment(task.id, pm, request, _command_context("assess-focus-review"))).assessment
    execution_preview = await service.preview_task_routing(
        task.id,
        pm,
        AgentRoutingPreviewCreate(purpose="execution", assessment_id=assessment.id, expected_task_version=task.version),
    )
    execution = await _dispatch(
        db,
        base=base,
        assessment=assessment,
        preview=execution_preview,
        candidate=default_candidate(worker),
        key="focus-review-execution",
    )
    (await db.get(AgentTaskAssignment, execution.id)).state = "fulfilled"
    task.status = "resolved"
    await db.commit()
    busy, run = await occupy(db, reviewer, iteration, task_factory, "The reviewer's current review")
    now = utc_now().replace(microsecond=0)
    monkeypatch.setattr(agent_routing_service, "utc_now", lambda: now)
    read = preview_reader(
        db_session_factory,
        monkeypatch,
        task.id,
        {
            "purpose": "verification",
            "assessment_id": assessment.id,
            "expected_task_version": task.version,
            "reviewer_profile_id": reviewer.profile_id,
        },
    )
    pm_key = team.sink.keys[team.manifest.controller.actor_key]

    # Occupied reviewer: its own team's rows crowd it out unless named.
    plain = await read(pm_key)
    assert plain["recommended_candidate"] is None and plain["exclusions_omitted"] > 0
    assert not find(plain["exclusions"], *reviewer_pair)
    focused = await read(pm_key, focus_actor_id=reviewer.id, focus_model_binding_id=reviewer_binding.id)
    (row,) = find(focused["exclusions"], *reviewer_pair)
    assert "current_work_conflict" in row["hard_blocker_codes"]
    assert row["running_runs"] == 1
    assert totals(focused) == totals(plain)
    assert focused["preview_id"] == plain["preview_id"]

    # Free reviewer: it is the recommended candidate, so the focus changes
    # nothing and the unfocused and focused previews are the same response.
    (await db.get(AgentTaskAssignment, busy.id)).state = "cancelled"
    (await db.get(AgentRun, run.id)).status = "succeeded"
    await db.commit()
    plain = await read(pm_key)
    assert (plain["recommended_candidate"]["actor_id"], plain["recommended_candidate"]["model_binding_id"]) == (
        reviewer_pair
    )
    assert plain["exclusions_omitted"] > 0
    assert await read(pm_key, focus_actor_id=reviewer.id, focus_model_binding_id=reviewer_binding.id) == plain
