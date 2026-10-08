"""Initial shared-input observations are complete, bounded and side-effect free."""

from datetime import date

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.authority import Authority, AuthorityError
from app.commands import AggregateVersionConflict, PlanningConflict
from app.config import get_settings
from app.main import app
from app.models.calendar import Calendar
from app.models.capacity import ProfileAvailability
from app.models.identity import CommandAudit
from app.models.iteration import Iteration
from app.models.outbound_webhook import OutboundWebhookEvent
from app.models.recovery import ApplicationSnapshot
from app.models.team_member import TeamMember, Vacation
from app.schemas.calendar import CalendarCreate, CalendarUpdate
from app.schemas.planning_inputs import PlanningInputRevisions
from app.services.calendar_service import CalendarService
from app.services.capacity_service import CapacityService
from app.services.planning_input_context import observe_planning_input
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import managed_store


async def test_initial_resource_and_revision_read_does_not_advance_or_emit(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
        models = [ApplicationSnapshot, OutboundWebhookEvent, CommandAudit]
        counts = [await db.scalar(select(func.count()).select_from(model)) for model in models]
        before = dict((await db.execute(select(Iteration.id, Iteration.revision))).all())
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        read = await client.get(f"/api/tasks/planning-inputs/calendar/{calendar_id}/context")
        assert read.status_code == 200, read.text
        body = read.json()
        assert body["complete"] is True and body["resource"]["id"] == calendar_id
        assert {int(key): value for key, value in body["expected_revisions"].items()} == before
    async with factory() as db:
        assert dict((await db.execute(select(Iteration.id, Iteration.revision))).all()) == before
        assert [await db.scalar(select(func.count()).select_from(model)) for model in models] == counts


async def test_supplied_empty_scope_detects_new_allocation_in_compatibility_mode(delivery_store, monkeypatch):
    factory, scenario, _ = delivery_store
    monkeypatch.setenv("STRICT_MUTATION_VERSIONS", "false"); get_settings.cache_clear()
    try:
        async with factory() as db:
            calendar = await CalendarService(db).create(CalendarCreate(name="Unused calendar", year=2026))
            calendar_id = calendar.id
            initial = await observe_planning_input(db, "calendar", calendar_id)
            assert initial["expected_revisions"] == {}
            db.add(Iteration(name="New affected plan", calendar_id=calendar_id, project_id=scenario.projects[0],
                start_date=date(2026, 1, 1), end_date=date(2026, 1, 31)))
            await db.commit()
            with pytest.raises(PlanningConflict, match="scope changed"):
                await CalendarService(db).update(calendar_id, CalendarUpdate(name="Stale edit", expected_revisions={}))
        async with factory() as db:
            assert (await db.get(Calendar, calendar_id)).name == "Unused calendar"
    finally:
        get_settings.cache_clear()


async def test_empty_scope_remains_valid_for_unused_input_in_strict_mode(delivery_store, monkeypatch):
    factory, _, _ = delivery_store
    monkeypatch.setenv("STRICT_MUTATION_VERSIONS", "true"); get_settings.cache_clear()
    try:
        async with factory() as db:
            calendar = await CalendarService(db).create(CalendarCreate(name="Unused strict calendar", year=2026))
            updated = await CalendarService(db).update(calendar.id, CalendarUpdate(name="Observed empty scope", expected_revisions={}))
            assert updated.name == "Observed empty scope"
    finally:
        get_settings.cache_clear()


async def test_stale_and_contradictory_contexts_roll_back_shared_input(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
        context = await observe_planning_input(db, "calendar", calendar_id)
        await CalendarService(db).update(calendar_id, CalendarUpdate(name="Current name", expected_revisions=context["expected_revisions"]))
        with pytest.raises(AggregateVersionConflict):
            await CalendarService(db).update(calendar_id, CalendarUpdate(name="Stale name", expected_revisions=context["expected_revisions"]))
    async with factory() as db:
        context = await observe_planning_input(db, "calendar", calendar_id)
        db.info["request_expected_revisions"] = {key: value + 1 for key, value in context["expected_revisions"].items()}
        with pytest.raises(PlanningConflict, match="disagree"):
            await CalendarService(db).update(calendar_id, CalendarUpdate(name="Contradictory name", expected_revisions=context["expected_revisions"]))
    async with factory() as db:
        assert (await db.get(Calendar, calendar_id)).name == "Current name"


async def test_scope_overflow_is_explicit_instead_of_partial_context(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
        db.add_all([Iteration(name=f"Affected plan {index}", calendar_id=calendar_id, project_id=scenario.projects[0],
            start_date=date(2026, 1, 1), end_date=date(2026, 1, 31)) for index in range(500)])
        await db.commit()
        with pytest.raises(PlanningConflict, match="limit"):
            await observe_planning_input(db, "calendar", calendar_id)


async def test_unprivileged_context_read_does_not_disclose_hidden_scope(managed_store):
    factory, scenario, _, principals = managed_store
    async with factory() as db:
        calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
        db.info["authority"] = Authority(principals[0], "human", projects={scenario.projects[0]: "editor"})
        with pytest.raises(AuthorityError, match="operator"):
            await observe_planning_input(db, "calendar", calendar_id)


async def test_profile_local_version_contract_ignores_iteration_header_context(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        calendar_id = (await db.get(Iteration, scenario.iterations[0])).calendar_id
        db.info["request_expected_revisions"] = {scenario.iterations[1]: 999}
        saved = await CapacityService(db).set_calendar(scenario.profile, calendar_id, 0)
        assert saved["version"] == 1
        assert "expected_revisions" not in saved
        with pytest.raises(PlanningConflict, match="Availability changed"):
            await CapacityService(db).set_calendar(scenario.profile, calendar_id, 0)


def test_body_context_limits_and_positive_keys_match_header_contract():
    with pytest.raises(ValidationError):
        PlanningInputRevisions(expected_revisions={-1: 1})
    with pytest.raises(ValidationError):
        PlanningInputRevisions(expected_revisions={index + 1: 1 for index in range(501)})


async def test_context_covers_each_shared_resource_and_new_member_target(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        member = await db.scalar(select(TeamMember).where(TeamMember.iteration_id == scenario.iterations[0]))
        vacation = Vacation(team_member_id=member.id, start_date=date(2026, 1, 22), end_date=date(2026, 1, 23))
        db.add(vacation)
        await db.commit()
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        for kind, identifier in [('project', scenario.projects[0]), ('iteration', scenario.iterations[0]),
                                 ('member', member.id), ('vacation', vacation.id)]:
            observed = await observe_planning_input(db, kind, identifier)
            assert observed['resource']['id'] == identifier
            expected_ids = scenario.iterations if kind in {'member', 'vacation'} else [scenario.iterations[0]]
            assert observed['expected_revisions'] == {identifier: (await db.get(Iteration, identifier)).revision for identifier in expected_ids}
        profile = await observe_planning_input(db, 'profile', scenario.profile)
        assert set(profile['expected_revisions']) == set(scenario.iterations)
        target = await observe_planning_input(db, 'member', scenario.iterations[0], creating_member=True)
        assert target['resource']['id'] == scenario.iterations[0]
        assert target['expected_revisions'] == {scenario.iterations[0]: revision}
