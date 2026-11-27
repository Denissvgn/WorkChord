"""Postponed work returns to its lifecycle by itself once every recorded requirement holds."""

import asyncio
import json
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from sqlalchemy import func, select, update

from app.authority import Authority, AuthorityError
from app.main import app
from app.models.agent import TaskEvent
from app.models.outbound_webhook import OutboundWebhookEvent
from app.models.project import Project
from app.models.task import Task
from app.models.task_postponement import TaskPostponement, TaskReactivationRequirement
from app.models.task_status_log import TaskStatusLog
from app.models.triage import TriageItem
from app.schemas.task_brief import TaskReviewWrite
from app.schemas.task_domain import TaskActionRequest
from app.schemas.task_postponement import OwnerDecisionRequest, TaskPostponeRequest
from app.schemas.triage import TriageActionRequest
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_postponement_service import TaskPostponementService
from app.services.task_reactivation_service import ReactivationService
from app.services.triage_service import TriageService
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_postponement import _client, _evidenced_task, _later, _postpone

__all__ = ["delivery_store"]


def _owner(principal_id=None):
    return Authority(principal_id, "human", workspace_role="owner")


async def _resolved_task(factory, scenario):
    """Evidenced resolved work in the first project, with the reviewer who can accept it."""
    async with factory() as db:
        task, worker, reviewer_id = await _evidenced_task(db, scenario, resolve=True)
        return task.id, worker, reviewer_id


async def _accept(factory, scenario, reviewer_id, task_id):
    async with factory() as db:
        db.info["authority"] = Authority(reviewer_id, "human", workspace_role="member", projects={scenario.projects[0]: "reviewer"})
        task = await db.get(Task, task_id)
        return await TaskBriefService(db).review(task_id, TaskReviewWrite(
            expected_version=task.version, brief_revision=task.brief_revision, artifact_revision=task.artifact_revision,
            verdict="accept", reason="Confirmed independently"))


async def _postpone_task(factory, task_id, *requirements, authority=None):
    async with factory() as db:
        db.info["authority"] = authority or _owner()
        task = await db.get(Task, task_id)
        return await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(task.version, *requirements)))


async def _state(factory, task_id):
    async with factory() as db:
        task = await db.get(Task, task_id)
        postponement = await db.scalar(select(TaskPostponement).where(TaskPostponement.task_id == task_id)
                                       .order_by(TaskPostponement.id.desc()).limit(1))
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == task_id, TaskEvent.event_type == "task_reactivated"))).all()
        return task, postponement, events


async def _requirement_states(client, task_id):
    detail = await client.get(f"/api/tasks/{task_id}/detail")
    assert detail.status_code == 200, detail.text
    record = detail.json()["postponement"]
    return None if record is None else [(item["kind"], item["met"], item["met_at"] is not None) for item in record["requirements"]]


async def test_accepting_the_named_predecessor_reactivates_once_across_projects(delivery_store):
    factory, scenario, _ = delivery_store
    predecessor_id, _, reviewer_id = await _resolved_task(factory, scenario)
    # The postponed task is in another project the reviewer cannot even read.
    waiting_id = scenario.tasks["other_project"]
    await _postpone_task(factory, waiting_id, {"kind": "predecessor_accepted", "task_id": predecessor_id})
    async with _client() as client:
        assert await _requirement_states(client, waiting_id) == [("predecessor_accepted", False, False)]
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "postponed" and postponement.reactivated_at is None and not events
    accepted = await _accept(factory, scenario, reviewer_id, predecessor_id)
    assert accepted.status == "closed"
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "planned"
    assert postponement.reactivated_to_status == "planned" and postponement.reactivation_trigger == "requirements_met"
    assert postponement.reactivated_by_principal_id is None and postponement.reactivated_by_actor_id is None
    assert f"task {predecessor_id} was accepted" in postponement.reactivation_reason
    assert len(events) == 1
    payload = json.loads(events[0].payload)
    assert payload["trigger"] == "requirements_met" and payload["to_status"] == "planned"
    assert [item["kind"] for item in payload["completed_by"]] == ["predecessor_accepted"]
    assert payload["completed_by"][0]["task_id"] == predecessor_id
    assert events[0].actor_type == "auto"
    async with factory() as db:
        log = await db.scalar(select(TaskStatusLog).where(TaskStatusLog.task_id == waiting_id, TaskStatusLog.to_status == "planned"))
        assert log.from_status == "postponed" and log.triggered_by == "system"
        event = await db.scalar(select(OutboundWebhookEvent).where(OutboundWebhookEvent.event_type == "task.reactivated"))
        assert event.entity_id == waiting_id and event.payload_json["completed_by"][0]["task_id"] == predecessor_id
    async with _client() as client:
        # No postponement is open once the work is back, and the timeline names the requirement.
        assert await _requirement_states(client, waiting_id) is None
        timeline = await client.get(f"/api/tasks/{waiting_id}/timeline")
        assert timeline.status_code == 200, timeline.text
        assert any(item["title"] == "task_reactivated" for item in timeline.json()["items"])
    # Repeating the evaluation changes nothing.
    async with factory() as db:
        assert await ReactivationService(db).run_date_check() == []
    _, _, events = await _state(factory, waiting_id)
    assert len(events) == 1


@pytest.mark.parametrize("closing", ["accept", "decline"])
async def test_a_linked_triage_item_resolved_returns_resolved_work_to_resolved(delivery_store, closing):
    factory, scenario, _ = delivery_store
    waiting_id, _, _ = await _resolved_task(factory, scenario)
    async with factory() as db:
        triage = TriageItem(title="Vendor answer", project_hint_id=scenario.projects[0])
        snoozed = TriageItem(title="Later", project_hint_id=scenario.projects[0])
        db.add_all([triage, snoozed])
        await db.commit()
        triage_id, snoozed_id = triage.id, snoozed.id
    await _postpone_task(factory, waiting_id, {"kind": "linked_resolved", "triage_item_id": triage_id})
    async with factory() as db:
        # Snoozing leaves an item in the inbox, so it resolves nothing; another item is unrelated.
        await TriageService(db).accept(snoozed_id)
        assert (await db.get(Task, waiting_id)).status == "postponed"
    async with factory() as db:
        service = TriageService(db)
        if closing == "accept":
            await service.accept(triage_id, TriageActionRequest(reason="Answered"))
        else:
            await service.decline(triage_id, TriageActionRequest(reason="Not needed"))
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "resolved"
    assert postponement.reactivated_to_status == "resolved" and f"triage item {triage_id} was resolved" in postponement.reactivation_reason
    assert len(events) == 1
    async with factory() as db:
        # An accepted item moving on to another resolved state does not reactivate anything again.
        await TriageService(db).decline(triage_id, TriageActionRequest(reason="Closed"))
    assert len((await _state(factory, waiting_id))[2]) == 1


async def test_snoozed_triage_item_keeps_work_postponed_and_a_duplicate_resolves_it(delivery_store):
    from app.schemas.triage import TriageDuplicateRequest, TriageSnoozeRequest
    factory, scenario, _ = delivery_store
    async with factory() as db:
        first = TriageItem(title="Original", project_hint_id=scenario.projects[0])
        second = TriageItem(title="Repeat", project_hint_id=scenario.projects[0])
        db.add_all([first, second])
        await db.commit()
        first_id, second_id = first.id, second.id
    waiting_id = scenario.tasks["planned"]
    await _postpone_task(factory, waiting_id, {"kind": "linked_resolved", "triage_item_id": second_id})
    async with factory() as db:
        await TriageService(db).snooze(second_id, TriageSnoozeRequest(snoozed_until=utc_now() + timedelta(days=3)))
    assert (await _state(factory, waiting_id))[0].status == "postponed"
    async with factory() as db:
        await TriageService(db).mark_duplicate(second_id, TriageDuplicateRequest(duplicate_of_id=first_id))
    assert (await _state(factory, waiting_id))[0].status == "planned"


async def test_a_linked_task_resolved_without_acceptance_is_enough(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        linked, worker, _ = await _evidenced_task(db, scenario, resolve=False)
        linked_id, linked_version = linked.id, linked.version
    waiting_id = scenario.tasks["planned"]
    await _postpone_task(factory, waiting_id, {"kind": "linked_resolved", "task_id": linked_id})
    async with factory() as db:
        db.info["authority"] = worker
        await TaskDomainService(db).command(linked_id, TaskActionRequest(action="resolve_manual", expected_version=linked_version, reason="Done"))
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "planned" and f"linked task {linked_id} was resolved" in postponement.reactivation_reason
    assert len(events) == 1


async def test_a_date_requirement_reactivates_on_its_date_in_the_project_time_zone(delivery_store):
    factory, scenario, _ = delivery_store
    day = utc_now().date() + timedelta(days=30)
    orchard, harbor = scenario.tasks["planned"], scenario.tasks["other_project"]
    for task_id in (orchard, harbor):
        await _postpone_task(factory, task_id, {"kind": "date", "on_date": day.isoformat()})
    async with factory() as db:
        # The first project works 14 hours ahead of UTC, the second 11 hours behind.
        await db.execute(update(Project).where(Project.id == scenario.projects[0]).values(timezone="Pacific/Kiritimati"))
        await db.execute(update(Project).where(Project.id == scenario.projects[1]).values(timezone="Pacific/Pago_Pago"))
        await db.commit()
    midday_before = datetime(day.year, day.month, day.day, 12, tzinfo=timezone.utc) - timedelta(days=1)
    async with factory() as db:
        assert await ReactivationService(db).run_date_check(now=midday_before - timedelta(days=1)) == []
    async with factory() as db:
        # It is already the day in Kiritimati, still the day before in Pago Pago.
        assert await ReactivationService(db).run_date_check(now=midday_before) == [orchard]
    assert (await _state(factory, orchard))[0].status == "planned" and (await _state(factory, harbor))[0].status == "postponed"
    async with factory() as db:
        assert await ReactivationService(db).run_date_check(now=midday_before + timedelta(hours=22)) == []
    async with factory() as db:
        assert await ReactivationService(db).run_date_check(now=midday_before + timedelta(hours=24)) == [harbor]
    _, postponement, events = await _state(factory, harbor)
    assert f"the date {day.isoformat()} was reached" in postponement.reactivation_reason and len(events) == 1
    async with factory() as db:
        assert await ReactivationService(db).run_date_check(now=midday_before + timedelta(days=5)) == []


async def test_an_owner_decision_requirement_waits_for_the_owner_alone(delivery_store):
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["planned"]
    await _postpone_task(factory, task_id, {"kind": "owner_decision", "description": "Keep the Android scope?"})
    async with factory() as db:
        requirement = await db.scalar(select(TaskReactivationRequirement).where(TaskReactivationRequirement.task_id == task_id))
        requirement_id = requirement.id
        task = await db.get(Task, task_id)
        version = task.version
    # Nothing else can satisfy it: not the date check, not another trigger.
    far_future = datetime.now(timezone.utc) + timedelta(days=4000)
    async with factory() as db:
        assert await ReactivationService(db).run_date_check(now=far_future) == []
    request = OwnerDecisionRequest(expected_version=version, decision="Drop Android for this release")
    for authority in (
        Authority(1, "human", workspace_role="member", projects={scenario.projects[0]: "manager"}),
        Authority(None, "agent", actor_id=scenario.actors[0], actor_role="pm", projects={scenario.projects[0]: "manager"},
                  scopes=frozenset({"tasks:read", "planning:read", "planning:write"})),
        Authority(1, "human", workspace_role="operator"),
    ):
        async with factory() as db:
            db.info["authority"] = authority
            with pytest.raises(AuthorityError) as caught:
                await ReactivationService(db).record_owner_decision(task_id, requirement_id, request)
            assert caught.value.code == "owner_decision_required"
    assert (await _state(factory, task_id))[0].status == "postponed"
    async with factory() as db:
        db.info["authority"] = _owner(7)
        with pytest.raises(LookupError):
            await ReactivationService(db).record_owner_decision(task_id, requirement_id + 100, request)
        stale = OwnerDecisionRequest(expected_version=version + 5, decision="Too late")
        with pytest.raises(Exception, match="changed|version"):
            await ReactivationService(db).record_owner_decision(task_id, requirement_id, stale)
    async with factory() as db:
        db.info["authority"] = _owner(7)
        result = await ReactivationService(db).record_owner_decision(task_id, requirement_id, request)
        assert result["task"].status == "planned" and not result["postponement"]["open"]
        assert result["postponement"]["reactivation_trigger"] == "requirements_met"
        assert [item["met"] for item in result["postponement"]["requirements"]] == [True]
    async with factory() as db:
        decided = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == task_id, TaskEvent.event_type == "owner_decision_recorded"))).all()
        assert len(decided) == 1 and json.loads(decided[0].payload)["decision"] == "Drop Android for this release"
    # Recording it again on work that has moved on is refused, never a second reactivation.
    async with factory() as db:
        db.info["authority"] = _owner(7)
        with pytest.raises(Exception):
            await ReactivationService(db).record_owner_decision(task_id, requirement_id, request)
    assert len((await _state(factory, task_id))[2]) == 1


async def test_the_owner_decision_command_over_http(delivery_store):
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["active"]
    await _postpone_task(factory, task_id, {"kind": "owner_decision", "description": "Approve the vendor"})
    async with factory() as db:
        requirement_id = await db.scalar(select(TaskReactivationRequirement.id).where(TaskReactivationRequirement.task_id == task_id))
        version = (await db.get(Task, task_id)).version
    async with _client() as client:
        assert await _requirement_states(client, task_id) == [("owner_decision", False, False)]
        response = await client.post(f"/api/tasks/{task_id}/postponement/requirements/{requirement_id}/decision",
                                     json={"expected_version": version, "decision": "Approved"})
        assert response.status_code == 200, response.text
        assert response.json()["task"]["status"] == "planned" and response.json()["postponement"]["requirements"][0]["met"] is True
        again = await client.post(f"/api/tasks/{task_id}/postponement/requirements/{requirement_id}/decision",
                                  json={"expected_version": version, "decision": "Approved"})
        assert again.status_code == 409, again.text


async def test_all_four_kinds_reactivate_only_when_the_last_is_met(delivery_store):
    factory, scenario, _ = delivery_store
    predecessor_id, _, reviewer_id = await _resolved_task(factory, scenario)
    async with factory() as db:
        triage = TriageItem(title="Contract answer", project_hint_id=scenario.projects[0])
        db.add(triage)
        await db.commit()
        triage_id = triage.id
    waiting_id = scenario.tasks["planned"]
    day = utc_now().date() + timedelta(days=30)
    result = await _postpone_task(factory, waiting_id,
                                  {"kind": "predecessor_accepted", "task_id": predecessor_id},
                                  {"kind": "linked_resolved", "triage_item_id": triage_id},
                                  {"kind": "date", "on_date": day.isoformat()},
                                  {"kind": "owner_decision", "description": "Go or no go"})
    requirement_id = next(item["id"] for item in result["postponement"]["requirements"] if item["kind"] == "owner_decision")
    version = result["task"].version
    kinds = ["predecessor_accepted", "linked_resolved", "date", "owner_decision"]
    async with _client() as client:
        async def states():
            return await _requirement_states(client, waiting_id)
        assert await states() == [(kind, False, False) for kind in kinds]
        await _accept(factory, scenario, reviewer_id, predecessor_id)
        assert await states() == [("predecessor_accepted", True, True), ("linked_resolved", False, False),
                                  ("date", False, False), ("owner_decision", False, False)]
        async with factory() as db:
            await TriageService(db).decline(triage_id, TriageActionRequest(reason="Not needed"))
        assert (await states())[1] == ("linked_resolved", True, True)
        async with factory() as db:
            assert await ReactivationService(db).run_date_check(now=datetime.now(timezone.utc) + timedelta(days=31)) == []
        assert await states() == [(kind, kind != "owner_decision", kind != "owner_decision") for kind in kinds]
        assert (await _state(factory, waiting_id))[0].status == "postponed"
        async with factory() as db:
            db.info["authority"] = _owner(3)
            await ReactivationService(db).record_owner_decision(
                waiting_id, requirement_id, OwnerDecisionRequest(expected_version=version, decision="Go"))
        assert await states() is None
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "planned" and len(events) == 1
    payload = json.loads(events[0].payload)
    # The last requirement met is the one the timeline names; every requirement is listed with when it was met.
    assert [item["kind"] for item in payload["completed_by"]] == ["owner_decision"]
    assert [item["kind"] for item in payload["requirements"]] == kinds
    assert "the owner decided: Go or no go" in postponement.reactivation_reason


async def test_a_later_postponement_waits_for_its_own_requirements(delivery_store):
    factory, scenario, _ = delivery_store
    predecessor_id, _, reviewer_id = await _resolved_task(factory, scenario)
    waiting_id = scenario.tasks["planned"]
    await _postpone_task(factory, waiting_id, {"kind": "predecessor_accepted", "task_id": predecessor_id})
    await _accept(factory, scenario, reviewer_id, predecessor_id)
    assert (await _state(factory, waiting_id))[0].status == "planned"
    await _postpone_task(factory, waiting_id, {"kind": "date", "on_date": _later()})
    async with factory() as db:
        assert await ReactivationService(db).run_date_check() == []
    task, postponement, _ = await _state(factory, waiting_id)
    assert task.status == "postponed" and postponement.reactivated_at is None
    async with factory() as db:
        assert await db.scalar(select(func.count()).select_from(TaskPostponement).where(TaskPostponement.task_id == waiting_id)) == 2


async def test_two_triggers_arriving_together_reactivate_the_task_once(delivery_store):
    factory, scenario, _ = delivery_store
    if factory.kw["bind"].dialect.name != "postgresql":
        pytest.skip("Concurrent transactions need PostgreSQL")
    first_id, _, first_reviewer = await _resolved_task(factory, scenario)
    second_id, _, second_reviewer = await _resolved_task(factory, scenario)
    async with factory() as db:
        triage = TriageItem(title="Vendor answer", project_hint_id=scenario.projects[0])
        db.add(triage)
        await db.commit()
        triage_id = triage.id
    waiting_id = scenario.tasks["planned"]
    day = utc_now().date() + timedelta(days=30)
    await _postpone_task(factory, waiting_id,
                         {"kind": "predecessor_accepted", "task_id": first_id},
                         {"kind": "predecessor_accepted", "task_id": second_id},
                         {"kind": "linked_resolved", "triage_item_id": triage_id},
                         {"kind": "date", "on_date": day.isoformat()})
    # The date has come; the date check, a triage resolution and two acceptances all arrive together,
    # and none of them is the last one to commit.
    async def resolve_triage():
        async with factory() as db:
            await TriageService(db).accept(triage_id)

    async def date_check():
        async with factory() as db:
            return await ReactivationService(db).run_date_check(now=datetime.now(timezone.utc) + timedelta(days=31))

    outcomes = await asyncio.gather(
        _accept(factory, scenario, first_reviewer, first_id), _accept(factory, scenario, second_reviewer, second_id),
        resolve_triage(), date_check(), return_exceptions=True)
    assert not [item for item in outcomes if isinstance(item, BaseException)], outcomes
    # A concurrent date check can finish before the last requirement is met; the next one settles it.
    async with factory() as db:
        await ReactivationService(db).run_date_check(now=datetime.now(timezone.utc) + timedelta(days=31))
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "planned" and postponement.reactivated_at is not None
    assert len(events) == 1
    async with factory() as db:
        logs = (await db.scalars(select(TaskStatusLog).where(TaskStatusLog.task_id == waiting_id, TaskStatusLog.from_status == "postponed"))).all()
        assert len(logs) == 1
        assert await db.scalar(select(func.count()).select_from(OutboundWebhookEvent).where(
            OutboundWebhookEvent.event_type == "task.reactivated", OutboundWebhookEvent.entity_id == waiting_id)) == 1
        assert task.version == (await db.get(Task, waiting_id)).version


async def test_two_final_triggers_race_and_exactly_one_reactivates(delivery_store):
    factory, scenario, _ = delivery_store
    if factory.kw["bind"].dialect.name != "postgresql":
        pytest.skip("Concurrent transactions need PostgreSQL")
    for _ in range(3):
        first_id, _, first_reviewer = await _resolved_task(factory, scenario)
        second_id, _, second_reviewer = await _resolved_task(factory, scenario)
        waiting_id = scenario.tasks["other_project"]
        await _postpone_task(factory, waiting_id,
                             {"kind": "predecessor_accepted", "task_id": first_id},
                             {"kind": "predecessor_accepted", "task_id": second_id})
        outcomes = await asyncio.gather(_accept(factory, scenario, first_reviewer, first_id),
                                        _accept(factory, scenario, second_reviewer, second_id), return_exceptions=True)
        assert not [item for item in outcomes if isinstance(item, BaseException)], outcomes
        task, postponement, events = await _state(factory, waiting_id)
        assert task.status == "planned" and postponement.reactivated_at is not None
        assert len([event for event in events if json.loads(event.payload)["postponement_id"] == postponement.id]) == 1
        async with factory() as db:
            assert await db.scalar(select(func.count()).select_from(TaskReactivationRequirement).where(
                TaskReactivationRequirement.postponement_id == postponement.id, TaskReactivationRequirement.met_at.is_not(None))) == 2


async def _backlog_task(factory, project_id, title="Backlog item"):
    from app.schemas.task import TaskCreate
    from app.services.task_service import TaskService
    async with factory() as db:
        db.info["authority"] = _owner()
        task = await TaskService(db).create(None, TaskCreate(title=title, project_id=project_id))
        assert task.iteration_id is None
        return task.id


async def test_backlog_work_in_a_project_the_caller_cannot_read_reactivates(delivery_store):
    factory, scenario, _ = delivery_store
    predecessor_id, _, reviewer_id = await _resolved_task(factory, scenario)
    waiting_id = await _backlog_task(factory, scenario.projects[1])
    await _postpone_task(factory, waiting_id, {"kind": "predecessor_accepted", "task_id": predecessor_id})
    await _accept(factory, scenario, reviewer_id, predecessor_id)
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "planned" and postponement.reactivated_at is not None and len(events) == 1


async def test_the_date_check_reactivates_backlog_work_in_managed_mode(delivery_store, monkeypatch):
    from app.config import get_settings
    factory, scenario, _ = delivery_store
    waiting_id = await _backlog_task(factory, scenario.projects[1])
    day = utc_now().date() + timedelta(days=30)
    await _postpone_task(factory, waiting_id, {"kind": "date", "on_date": day.isoformat()})
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    try:
        async with factory() as db:
            assert await ReactivationService(db).run_date_check(now=datetime.now(timezone.utc) + timedelta(days=31)) == [waiting_id]
    finally:
        monkeypatch.undo()
        get_settings.cache_clear()
    assert (await _state(factory, waiting_id))[0].status == "planned"


async def test_a_closed_summary_counts_as_an_accepted_predecessor(delivery_store):
    factory, scenario, _ = delivery_store
    summary_id, waiting_id = scenario.tasks["parent"], scenario.tasks["planned"]
    async with factory() as db:
        await db.execute(update(Task).where(Task.id == summary_id).values(is_summary=True))
        await db.commit()
    await _postpone_task(factory, waiting_id, {"kind": "predecessor_accepted", "task_id": summary_id})
    async with factory() as db:
        assert await ReactivationService(db).run_date_check() == []
        # The roll-up closes the summary without recording an acceptance of its own.
        await db.execute(update(Task).where(Task.id == summary_id).values(status="closed", accepted_at=None))
        await db.commit()
    async with factory() as db:
        assert await ReactivationService(db).run_date_check() == [waiting_id]
    other_id = scenario.tasks["active"]
    async with factory() as db:
        db.info["authority"] = _owner()
        version = (await db.get(Task, other_id)).version
        with pytest.raises(ValueError, match="already accepted"):
            await TaskPostponementService(db).postpone(other_id, TaskPostponeRequest(**_postpone(
                version, {"kind": "predecessor_accepted", "task_id": summary_id})))


async def test_reactivating_to_resolved_with_the_command_wakes_work_waiting_for_it(delivery_store):
    from app.schemas.task_postponement import TaskReactivateRequest
    factory, scenario, _ = delivery_store
    resolved_id, _, _ = await _resolved_task(factory, scenario)
    waiting_id = scenario.tasks["planned"]
    await _postpone_task(factory, resolved_id, {"kind": "date", "on_date": _later()})
    await _postpone_task(factory, waiting_id, {"kind": "linked_resolved", "task_id": resolved_id})
    async with factory() as db:
        db.info["authority"] = _owner()
        version = (await db.get(Task, resolved_id)).version
        await TaskPostponementService(db).reactivate(resolved_id, TaskReactivateRequest(expected_version=version, reason="Resume"))
    assert (await _state(factory, resolved_id))[0].status == "resolved"
    task, postponement, events = await _state(factory, waiting_id)
    assert task.status == "planned" and f"linked task {resolved_id} was resolved" in postponement.reactivation_reason


async def test_a_sweep_that_finds_nothing_leaves_the_planning_revision_alone(delivery_store):
    from app.models.capacity import PlanningState
    factory, scenario, _ = delivery_store
    await _postpone_task(factory, scenario.tasks["planned"], {"kind": "date", "on_date": _later()})
    await _postpone_task(factory, scenario.tasks["active"], {"kind": "owner_decision", "description": "Decide"})
    async with factory() as db:
        before = await db.scalar(select(PlanningState.revision))
    for _ in range(3):
        async with factory() as db:
            assert await ReactivationService(db).run_date_check() == []
    async with factory() as db:
        assert await db.scalar(select(PlanningState.revision)) == before


@pytest.mark.parametrize("failure", [RuntimeError("boom"), TypeError("odd")])
async def test_a_failed_evaluation_never_blocks_the_trigger_and_is_retried(delivery_store, monkeypatch, failure):
    factory, scenario, _ = delivery_store
    predecessor_id, _, reviewer_id = await _resolved_task(factory, scenario)
    waiting_id = scenario.tasks["planned"]
    await _postpone_task(factory, waiting_id, {"kind": "predecessor_accepted", "task_id": predecessor_id})
    original = TaskPostponementService.resume

    async def failing(self, *args, **kwargs):
        raise failure

    monkeypatch.setattr(TaskPostponementService, "resume", failing)
    accepted = await _accept(factory, scenario, reviewer_id, predecessor_id)
    assert accepted.status == "closed"
    task, postponement, _ = await _state(factory, waiting_id)
    assert task.status == "postponed" and postponement.reactivated_at is None
    async with factory() as db:
        requirement = await db.scalar(select(TaskReactivationRequirement).where(TaskReactivationRequirement.task_id == waiting_id))
        assert requirement.met_at is None
    monkeypatch.setattr(TaskPostponementService, "resume", original)
    async with factory() as db:
        assert await ReactivationService(db).run_date_check() == [waiting_id]


async def test_the_owner_decision_also_counts_a_date_that_came_due(delivery_store):
    factory, scenario, _ = delivery_store
    task_id = scenario.tasks["planned"]
    await _postpone_task(factory, task_id, {"kind": "date", "on_date": _later()}, {"kind": "owner_decision", "description": "Go?"})
    async with factory() as db:
        await db.execute(update(TaskReactivationRequirement).where(
            TaskReactivationRequirement.task_id == task_id, TaskReactivationRequirement.kind == "date")
            .values(on_date=utc_now().date() - timedelta(days=1)))
        requirement_id = await db.scalar(select(TaskReactivationRequirement.id).where(
            TaskReactivationRequirement.task_id == task_id, TaskReactivationRequirement.kind == "owner_decision"))
        version = (await db.get(Task, task_id)).version
        await db.commit()
    async with factory() as db:
        db.info["authority"] = _owner(5)
        result = await ReactivationService(db).record_owner_decision(
            task_id, requirement_id, OwnerDecisionRequest(expected_version=version, decision="Go"))
        assert result["task"].status == "planned"
        assert [item["met"] for item in result["postponement"]["requirements"]] == [True, True]
