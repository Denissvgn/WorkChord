"""A delivery prerequisite can require accepted code merged on a named branch; the hold names who acts next."""

import pytest

from app.models.identity import Principal
from app.services.delivery_dependency_service import DeliveryDependencyService
from app.services.external_link_service import ExternalLinkService
from app.utils.time import utc_now
from tests.test_delivery_dependencies import pair
from tests.test_delivery_scenarios import delivery_store  # noqa: F401

REPO = "https://github.com/example/project"
MERGE = "c" * 40


async def observe(db, task, number, *, status, base="main", merge=True):
    link = await ExternalLinkService(db).create_task_github_link(task.id, f"{REPO}/pull/{number}", commit=False)
    link.status = status
    link.metadata_json = {**link.metadata_json, "base_ref": base, "merge_commit_sha": MERGE if merge else None,
                          "observed_at": "2026-11-24T10:00:00Z"}
    await db.commit()
    return link


async def accept(db, task):
    reviewer = Principal(kind="human", display_name="Independent reviewer")
    db.add(reviewer)
    await db.flush()
    task.status, task.accepted_at, task.accepted_version = "closed", utc_now(), task.version
    task.accepted_by_principal_id = reviewer.id
    await db.commit()


async def hold(db, task_id):
    (item,) = await DeliveryDependencyService(db).projection(task_id)
    return item


async def test_implemented_prerequisite_with_open_pull_request_holds_with_reviewer(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        first.status = "resolved"
        await db.commit()
        await observe(db, first, 41, status="open", merge=False)
        await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "refs/heads/main")
        item = await hold(db, second.id)
        assert item["target_branch"] == "main" and not item["ready"]
        assert item["reason"] == "prerequisite_acceptance_required"
        assert item["merge"]["state"] == "open_pull_request"
        assert item["hold"]["case"] == "open_pull_request" and item["hold"]["next_owner"] == "reviewer"
        assert "main" in item["hold"]["next_action"]
        assert [h["id"] for h in await DeliveryDependencyService(db).holds(second.id)] == [item["id"]]


async def test_accepted_prerequisite_absent_from_target_holds_with_pm(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        link = await observe(db, first, 42, status=None, merge=False)
        await accept(db, first)
        service = DeliveryDependencyService(db)
        await service.add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert item["reason"] == "prerequisite_merge_not_observed" and item["merge"]["state"] == "not_observed"
        assert item["hold"]["next_owner"] == "pm" and "catch-up" in item["hold"]["next_action"]
        link.status = "open"
        await db.commit()
        item = await hold(db, second.id)
        assert item["hold"]["case"] == "open_pull_request" and item["hold"]["next_owner"] == "pm"
        link.status = "merged"
        link.metadata_json = {**link.metadata_json, "base_ref": "release", "merge_commit_sha": MERGE}
        await db.commit()
        item = await hold(db, second.id)
        assert item["merge"]["state"] == "merged_on_other_branch" and not item["ready"]


async def test_verified_merge_on_target_releases_the_hold_and_ordinary_edges_are_unchanged(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        await observe(db, first, 43, status="merged", base="main")
        await accept(db, first)
        service = DeliveryDependencyService(db)
        await service.add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert item["ready"] and item["hold"] is None and item["merge"]["verified"]
        assert await service.holds(second.id) == []
        # Retargeting an existing edge to another branch holds again; no target keeps the plain Accepted gate.
        await db.refresh(second)
        await service.add(second.id, "task", first.id, second.version, "release")
        assert not (await hold(db, second.id))["ready"]
        await db.refresh(second)
        await service.add(second.id, "task", first.id, second.version, None)
        item = await hold(db, second.id)
        assert item["ready"] and item["target_branch"] is None and item["merge"] is None


async def test_merge_without_acceptance_never_releases_and_branch_is_validated(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        await observe(db, first, 44, status="merged", base="main")
        service = DeliveryDependencyService(db)
        with pytest.raises(ValueError, match="branch"):
            await service.add(second.id, "task", first.id, second.version, "bad branch")
        with pytest.raises(ValueError, match="only to a task"):
            await service.add(second.id, "milestone", 1, second.version, "main")
        await service.add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert not item["ready"] and item["reason"] == "prerequisite_acceptance_required"
        assert item["hold"]["next_owner"] == "worker" and item["merge"]["verified"]
        assert not await service.ready(second.id)


async def test_pipeline_shows_the_hold_on_the_waiting_task(delivery_store):
    from app.services.agent_service import AgentService

    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        await accept(db, first)
        await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "main")
        pipeline = await AgentService(db).get_pipeline()
        shown = [task for tasks in pipeline.values() for task in tasks if task.id == second.id]
        assert len(shown) == 1
        (entry,) = shown[0].delivery_holds
        assert entry["hold"]["next_owner"] == "pm" and entry["reason"] == "prerequisite_merge_not_observed"
        assert not [task for task in pipeline["start_ready"] if task.id == second.id]


async def test_merged_pull_request_without_a_recorded_base_branch_asks_for_catch_up(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        link = await observe(db, first, 43, status="merged", base=None)
        await accept(db, first)
        await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert item["merge"]["state"] == "merge_branch_unknown" and not item["ready"]
        assert item["hold"]["case"] == "merge_branch_unknown" and item["hold"]["next_owner"] == "pm"
        assert "catch-up" in item["hold"]["next_action"] and "other than" not in item["hold"]["next_action"]
        link.metadata_json = {**link.metadata_json, "base_ref": "main"}
        await db.commit()
        assert (await hold(db, second.id))["ready"]


async def test_closed_prerequisite_with_stale_acceptance_asks_the_reviewer_not_the_worker(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        await observe(db, first, 44, status="merged")
        await accept(db, first)
        first.version += 1
        await db.commit()
        await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert item["reason"] == "prerequisite_acceptance_required" and item["hold"]["case"] == "not_accepted"
        assert item["hold"]["next_owner"] == "reviewer" and "Accept" in item["hold"]["next_action"]
