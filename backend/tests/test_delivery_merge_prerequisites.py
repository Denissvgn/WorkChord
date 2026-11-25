"""A delivery prerequisite can require accepted code merged on a named branch; the hold names who acts next."""

import json

import pytest
from sqlalchemy import select

from app.config import get_settings
from app.models.agent import AgentActor, AgentRun, TaskEvent
from app.models.identity import Principal
from app.models.task import Task
from app.schemas.request_source import RequestSourceCreate, RequestSourceLinkCreateRequest
from app.schemas.task_brief import BriefWrite, TaskBrief
from app.services.delivery_dependency_service import DeliveryDependencyService
from app.services.external_link_service import ExternalLinkService
from app.services.github_reconciliation_service import GitHubReconciliationService
from app.services.github_webhook_service import GitHubWebhookService
from app.services.request_source_service import RequestSourceService
from app.services.task_brief_service import TaskBriefService
from app.utils.time import utc_now
from tests.test_delivery_dependencies import pair
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_github_reconciliation import github  # noqa: F401

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


async def test_merged_without_a_merge_commit_on_the_target_is_not_confirmed(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        await observe(db, first, 45, status="merged", merge=False)
        await accept(db, first)
        await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert item["merge"]["state"] == "merge_branch_unknown" and not item["ready"]
        assert item["hold"]["next_owner"] == "pm" and "catch-up" in item["hold"]["next_action"]
        assert "other than" not in item["hold"]["next_action"]


async def test_canceled_prerequisite_is_replaced_by_the_pm(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first, second = await pair(db, scenario)
        await observe(db, first, 46, status="merged")
        await accept(db, first)
        first.canceled_at = utc_now()
        await db.commit()
        await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "main")
        item = await hold(db, second.id)
        assert item["hold"]["next_owner"] == "pm" and "replacement" in item["hold"]["next_action"]


async def test_closed_prerequisite_with_stale_acceptance_is_reopened_by_the_pm(delivery_store):
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
        assert item["hold"]["next_owner"] == "pm" and "Reopen" in item["hold"]["next_action"]


SUBMITTED = "a" * 40
PUSHED_AFTER_ACCEPTANCE = "b" * 40


async def accepted_with_pull_request(db, scenario):
    """An accepted, closed prerequisite whose run submitted a commit for its one pull request."""
    first, second = await pair(db, scenario)
    await ExternalLinkService(db).create_task_github_link(first.id, f"{REPO}/pull/39", commit=False)
    actor = AgentActor(name=f"worker-{first.id}", display_name="Worker", api_key_hash=f"hash-{first.id}")
    db.add(actor)
    await db.flush()
    db.add(AgentRun(task_id=first.id, actor_id=actor.id, status="succeeded",
                    commit_url=f"{REPO}/commit/{SUBMITTED}", pr_url=f"{REPO}/pull/39"))
    await db.commit()
    await accept(db, first)
    await DeliveryDependencyService(db).add(second.id, "task", first.id, second.version, "main")
    return first.id, second.id


async def record_merge(db, observer, github, task_id, head):
    github.pull = github.payload(head, "2026-11-24T12:00:00Z", state="closed", merged_at="2026-11-24T12:00:00Z")
    if observer == "catch_up":
        await GitHubReconciliationService(db).catch_up(task_id)
        return
    settings = get_settings().model_copy(update={"github_webhook_secret": "s"})
    response = await GitHubWebhookService(db, settings_override=settings).process("pull_request", "merge-1", {
        "action": "closed", "pull_request": github.pull, "repository": {"full_name": "example/project"},
        "sender": {"login": "octo"}})
    assert response.matched and response.ignored_reason is None


async def preserved_events(db, task_id):
    return (await db.scalars(select(TaskEvent).where(
        TaskEvent.task_id == task_id, TaskEvent.event_type == "acceptance_preserved_after_observation"))).all()


@pytest.mark.parametrize("observer", ["catch_up", "webhook"])
async def test_an_observed_merge_keeps_acceptance_and_releases_the_dependent(delivery_store, github, observer):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first_id, second_id = await accepted_with_pull_request(db, scenario)
        accepted_version = (await db.get(Task, first_id)).version
        await record_merge(db, observer, github, first_id, SUBMITTED)
    async with factory() as db:
        first = await db.get(Task, first_id)
        assert first.version > accepted_version and first.accepted_version == first.version
        (event,) = await preserved_events(db, first_id)
        payload = json.loads(event.payload)
        assert (payload["previous_version"], payload["current_version"]) == (accepted_version, first.version)
        assert payload["action"] == ("github_status_refresh" if observer == "catch_up" else "github_webhook_update")
        item = await hold(db, second_id)
        assert item["merge"]["state"] == "merged_on_target" and item["merge"]["verified"]
        assert item["ready"] and item["hold"] is None
        assert (await GitHubReconciliationService(db).view(first_id))["accepted"]


@pytest.mark.parametrize("observer", ["catch_up", "webhook"])
async def test_a_head_pushed_after_acceptance_makes_acceptance_stale(delivery_store, github, observer):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first_id, second_id = await accepted_with_pull_request(db, scenario)
        await record_merge(db, observer, github, first_id, PUSHED_AFTER_ACCEPTANCE)
    async with factory() as db:
        first = await db.get(Task, first_id)
        assert first.accepted_version != first.version and await preserved_events(db, first_id) == []
        item = await hold(db, second_id)
        assert item["merge"]["verified"] and not item["ready"] and item["hold"]["case"] == "not_accepted"
        pull = (await GitHubReconciliationService(db).view(first_id))["pull_requests"][0]
        assert "head_differs_from_submission" in pull["differences"]


@pytest.mark.parametrize("change", ["github_link", "request_source"])
async def test_other_context_changes_still_make_acceptance_stale(delivery_store, change):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first_id, second_id = await accepted_with_pull_request(db, scenario)
        if change == "github_link":
            await ExternalLinkService(db).create_task_github_link(first_id, f"{REPO}/pull/40", commit=False)
        else:
            await RequestSourceService(db).create_link(RequestSourceLinkCreateRequest(
                target_type="task", target_id=first_id,
                request_source=RequestSourceCreate(title="Customer request", source_type="customer")), commit=False)
        await db.commit()
    async with factory() as db:
        first = await db.get(Task, first_id)
        assert first.accepted_version != first.version and await preserved_events(db, first_id) == []
        assert (await hold(db, second_id))["hold"]["case"] == "not_accepted"


async def test_a_brief_change_still_makes_acceptance_stale(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first_id, second_id = await accepted_with_pull_request(db, scenario)
        first = await db.get(Task, first_id)
        await TaskBriefService(db).write(first_id, BriefWrite(expected_version=first.version,
                                                               brief=TaskBrief(goal="A different goal")))
    async with factory() as db:
        first = await db.get(Task, first_id)
        assert first.accepted_version != first.version and await preserved_events(db, first_id) == []
        assert not (await hold(db, second_id))["ready"]
