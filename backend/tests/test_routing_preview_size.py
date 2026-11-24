"""The routed decision, its wire defaults, and its digest share one exact byte budget."""

import json

import pytest

from app.config import get_settings
from app.models.agent import AgentModelBinding, AgentModelCatalogEntry, AgentTaskAssignment
from app.models.iteration import Iteration
from app.schemas import agent_routing
from app.schemas.agent_routing import AgentRoutingPreviewResponse
from app.services import agent_routing_service
from app.services.agent_routing_policy import MAX_ROUTING_PACKET_BYTES, canonical_routing_json_bytes
from app.services.agent_routing_service import AgentRoutingService
from app.services.agent_service import hash_api_key
from app.utils.time import utc_now
from tests.test_agent_routing_service import _assessment_command, _command_context
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance import database_engines
from tests.test_scoped_review_evidence import through
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


@database_engines
@pytest.mark.parametrize("primary", ["rest", "mcp"])
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_preview_bounds_final_rest_and_mcp_decisions(
    db_session,
    db_session_factory,
    team_member_factory,
    task_factory,
    actor_factory,
    monkeypatch,
    record_property,
    primary,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    team = await provision_ready_topology(db, two_workers=False)
    member = team.manifest.workers[0]
    subject = await routing_base(
        db,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Prepare the package",
    )
    task, worker, pm = subject.task, team.actors[member.actor_key], subject.pm
    request = _assessment_command(task_version=task.version)
    assessment = await AgentRoutingService(db).create_assessment(
        task.id, pm, request, _command_context("assess-package")
    )
    body = {
        "purpose": "execution",
        "assessment_id": assessment.assessment.id,
        "expected_task_version": task.version,
    }
    # A team-bound PM only receives its own team's rows. An operator without a
    # team boundary receives every actor's row, so it exercises the byte bound.
    key = "routing-size-operator"
    await actor_factory(role="pm", scopes=json.dumps(["admin"]), api_key_hash=hash_api_key(key))
    now = utc_now().replace(microsecond=0)
    monkeypatch.setattr(agent_routing_service, "utc_now", lambda: now)

    async def read(transport):
        return await through(
            transport,
            db_session_factory,
            monkeypatch,
            "agent_preview_task_routing",
            f"/api/agent/tasks/{task.id}/routing-preview",
            key,
            body,
            task_id=task.id,
        )

    source = AgentModelCatalogEntry(
        key="other-runtime",
        provider="test-provider",
        configured_model_alias="x",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="balanced",
        enabled=True,
        revision=1,
    )
    db.add(source)
    await db.flush()

    async def add_excluded():
        actor = await actor_factory()
        db.add(
            AgentModelBinding(
                actor_id=actor.id, model_catalog_id=source.id, is_default=True, enabled=True, revision=1
            )
        )

    await add_excluded()
    await db.commit()
    first = await read("rest")
    assert first["recommended_candidate"]["actor_id"] == worker.id and not first["exclusions_omitted"]
    (sample,) = [r for r in first["exclusions"] if r["model_catalog_id"] == source.id]
    size = lambda value: len(canonical_routing_json_bytes(value))
    # The ordinary inputs remain comfortably below the limit before applying a
    # valid multibyte model alias. Leave enough room for one alias in each row.
    extra = (MAX_ROUTING_PACKET_BYTES - 2200 - size(first)) // (size(sample) + 3)
    assert 1 <= extra < 46
    for _ in range(extra):
        await add_excluded()
    await db.commit()
    ordinary = await read("rest")
    assert ordinary == await read("mcp") and not ordinary["exclusions_omitted"]
    peers = [r for r in ordinary["exclusions"] if r["model_catalog_id"] == source.id]
    n = len(peers)
    increase = (MAX_ROUTING_PACKET_BYTES + 12 - size(ordinary) + n - 1) // n
    repeat, remaining = divmod(increase, 3)
    source.configured_model_alias = "x" + "界" * repeat + "x" * remaining
    assert len(source.configured_model_alias) <= 255
    await db.commit()
    measured = []
    validate = agent_routing.validate_routing_packet_size

    def observe(value, **kwargs):
        if isinstance(value, AgentRoutingPreviewResponse):
            measured.append(len(canonical_routing_json_bytes(value)))
        return validate(value, **kwargs)

    monkeypatch.setattr(agent_routing, "validate_routing_packet_size", observe)
    for busy in (False, True):
        if busy:
            other = await task_factory(
                iteration=await db.get(Iteration, task.iteration_id), title="Existing package work"
            )
            db.add(
                AgentTaskAssignment(
                    task_id=other.id, actor_id=worker.id, task_version=other.version, state="accepted"
                )
            )
            await db.commit()
        rest = await read(primary)
        secondary = "mcp" if primary == "rest" else "rest"
        assert rest == await read(secondary) == await read(primary)
        assert rest == AgentRoutingPreviewResponse.model_validate(rest).model_dump(mode="json")
        assert size(rest) <= MAX_ROUTING_PACKET_BYTES
        assert all(row["hard_blocker_codes"] for row in rest["exclusions"])
        assert len(rest["exclusions"]) + rest["exclusions_omitted"] == len(ordinary["exclusions"]) + int(
            busy
        )
        if busy:
            assert rest["recommended_candidate"] is None and not rest["eligible_candidates"]
            assert any(
                row["actor_id"] == worker.id and "current_work_conflict" in row["hard_blocker_codes"]
                for row in rest["exclusions"]
            )
        else:
            assert rest["recommended_candidate"] == rest["eligible_candidates"][0]
            assert (
                rest["recommended_candidate"]["actor_id"] == worker.id and rest["exclusions_omitted"] == 1
            )
            assert all(
                row["actor_id"] == prior["actor_id"]
                for row, prior in zip(rest["exclusions"], ordinary["exclusions"])
            )
            # All pre-bound row sizes were measured through the actual validated response.
            assert (
                MAX_ROUTING_PACKET_BYTES < size(ordinary) + increase * n <= MAX_ROUTING_PACKET_BYTES + 64
            )
        record_property("busy_bytes" if busy else "eligible_bytes", size(rest))
    assert max(measured) > MAX_ROUTING_PACKET_BYTES
    record_property("largest_validated_trial_bytes", max(measured))
