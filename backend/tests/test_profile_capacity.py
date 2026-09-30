"""Shared person capacity, calendar arithmetic and private availability boundaries."""

from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.database import Base

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberProfile, Vacation
from app.services.team_service import TeamService
from app.services.capacity_service import CapacityService
from app.commands import PlanningConflict
from app.models.capacity import PlanningState, ProfileAbsence
from app.schemas.team import VacationCreate, VacationUpdate
from sqlalchemy import select


def test_partial_absence_update_cannot_clear_required_dates():
    from pydantic import ValidationError
    with pytest.raises(ValidationError, match="cannot be null"):
        VacationUpdate(start_date=None)
    assert VacationUpdate().model_dump(exclude_unset=True) == {}


@pytest_asyncio.fixture(params=[pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])])
async def db_session(request, sqlite_engine):
    engine = sqlite_engine
    if request.param == "postgresql":
        engine = create_async_engine(request.getfixturevalue("postgres_database").url)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine, expire_on_commit=False)() as db:
        yield db
    if engine is not sqlite_engine:
        await engine.dispose()


async def allocation(db, *, hours=6, profile=None):
    calendar = Calendar(name="Local working week", year=2026, nominal_day_hours=hours,
                        holidays=[], weekend_days=[5, 6], short_days=["2026-10-02"])
    iteration = Iteration(name="Delivery", start_date=date(2026, 9, 28),
                          end_date=date(2026, 10, 2), calendar=calendar)
    member = TeamMember(name="Sam", position="Developer", iteration=iteration,
                        profile=profile, availability_percent=100,
                        operational_utilization=20, professionalism_coefficient=1.25)
    db.add(member)
    await db.flush()
    return member


@pytest.mark.asyncio
async def test_capacity_counts_union_of_absences_and_actual_calendar_hours(db_session):
    member = await allocation(db_session)
    db_session.add_all([
        Vacation(team_member_id=member.id, start_date=date(2026, 9, 28), end_date=date(2026, 9, 29)),
        Vacation(team_member_id=member.id, start_date=date(2026, 9, 29), end_date=date(2026, 9, 30)),
    ])
    await db_session.flush()
    capacity = await TeamService(db_session).calculate_capacity(member.id)
    assert capacity.vacation_days == 3
    assert capacity.available_days == 2
    assert capacity.hours == 11  # (6 + 5) × .8 × 1.25, shortened Friday included.


@pytest.mark.asyncio
async def test_profile_absence_applies_to_other_allocations(db_session):
    profile = TeamMemberProfile(display_name="Sam")
    first = await allocation(db_session, profile=profile)
    second = await allocation(db_session, profile=profile)
    db_session.add(Vacation(team_member_id=first.id, start_date=date(2026, 9, 28),
                            end_date=date(2026, 9, 28)))
    await db_session.flush()
    capacity = await TeamService(db_session).calculate_capacity(second.id)
    assert capacity.vacation_days == 1
    assert capacity.hours == 23


@pytest.mark.asyncio
async def test_shared_absence_revisions_legacy_adapter_and_stale_write(db_session):
    profile = TeamMemberProfile(display_name="Sam")
    first = await allocation(db_session, profile=profile)
    second = await allocation(db_session, profile=profile)
    await db_session.commit()
    service = TeamService(db_session)
    vacation = await service.add_vacation(first.id, VacationCreate(start_date=date(2026, 9, 28), end_date=date(2026, 9, 28)))
    absence_id, vacation_id = vacation.profile_absence_id, vacation.id
    assert (await service.calculate_capacity(second.id)).vacation_days == 1
    assert second.iteration.revision == 2
    await service.update_vacation(vacation_id, VacationUpdate(end_date=date(2026, 9, 29)))
    detail = await CapacityService(db_session).detail(profile.id)
    assert detail["absences"][0]["version"] == 2
    assert len(detail["absences"][0]["provenance"]) == 3
    assert detail["absences"][0]["provenance"][1] == {"legacy_vacation_ids": [vacation_id]}
    profile_id = profile.id
    with pytest.raises(PlanningConflict, match="Absence changed"):
        await CapacityService(db_session).save_absence(profile_id, date(2026, 9, 28), date(2026, 9, 30),
                                                     absence_id=absence_id, expected_version=1)
    await service.delete_vacation(vacation_id)
    assert (await db_session.get(ProfileAbsence, absence_id)).deleted
    assert (await service.calculate_capacity(second.id)).vacation_days == 0


@pytest.mark.asyncio
async def test_absence_owner_permission_and_projection_redaction(db_session):
    from app.authority import Authority, AuthorityError
    from app.models.project import Project
    from app.models.identity import Principal
    person = Principal(kind="human", display_name="Sam")
    profile = TeamMemberProfile(display_name="Sam")
    first = await allocation(db_session, profile=profile)
    second = await allocation(db_session, profile=profile)
    second.iteration.calendar = first.iteration.calendar
    private = Project(name="Private project")
    second.iteration.project = private
    db_session.add(person)
    await db_session.commit()
    profile_id = profile.id
    db_session.info["authority"] = Authority(principal_id=person.id, kind="human", workspace_role="member")
    service = CapacityService(db_session)
    with pytest.raises(AuthorityError, match="Only this person"):
        await service.detail(profile_id)
    projection = await service.projection(profile_id, date(2026, 9, 28), date(2026, 9, 28))
    assert projection["days"][0]["private_busy_hours"] == 6
    assert projection["days"][0]["overallocated_hours"] == 6
    assert "Private project" not in str(projection)
    assert (await db_session.scalars(select(ProfileAbsence))).all() == []


@pytest.mark.asyncio
async def test_preview_absence_rolls_back_planning_and_absence(db_session):
    from app.commands import command_transaction
    profile = TeamMemberProfile(display_name="Sam")
    member = await allocation(db_session, profile=profile)
    await db_session.commit()
    profile_id = profile.id
    async with command_transaction(db_session, mode="preview"):
        await CapacityService(db_session).save_absence(profile_id, date(2026, 9, 28), date(2026, 9, 28))
    assert (await db_session.scalars(select(ProfileAbsence))).all() == []
    assert await db_session.get(PlanningState, 1) is None


@pytest.mark.asyncio
async def test_concurrent_absence_edits_have_one_winner(db_session):
    import asyncio
    profile = TeamMemberProfile(display_name="Sam")
    await allocation(db_session, profile=profile)
    await db_session.commit()
    profile_id = profile.id
    absence = await CapacityService(db_session).save_absence(profile_id, date(2026, 9, 28), date(2026, 9, 28))
    absence_id = absence.id
    factory = async_sessionmaker(db_session.bind, expire_on_commit=False)

    async def edit(end):
        async with factory() as db:
            try:
                await CapacityService(db).save_absence(profile_id, date(2026, 9, 28), end,
                    absence_id=absence_id, expected_version=1)
                return "saved"
            except PlanningConflict:
                return "conflict"

    results = await asyncio.wait_for(asyncio.gather(edit(date(2026, 9, 29)), edit(date(2026, 9, 30))), 15)
    assert sorted(results) == ["conflict", "saved"]


@pytest.mark.asyncio
async def test_canonical_calendar_and_fractional_capacity_preserve_unknown_work(db_session):
    from app.models.task import Task
    profile = TeamMemberProfile(display_name="Sam")
    member = await allocation(db_session, profile=profile, hours=6)
    member.availability_percent = 50
    member.operational_utilization = 20
    member.professionalism_coefficient = 1.25
    db_session.add_all([
        Task(title="Small commitment", iteration=member.iteration, assignee=member,
             effort_hours=1.5, baseline_start_date=date(2026, 9, 28), baseline_end_date=date(2026, 9, 29)),
        Task(title="Unknown commitment", iteration=member.iteration, assignee=member,
             effort_hours=None, baseline_start_date=date(2026, 9, 28), baseline_end_date=date(2026, 9, 28)),
    ])
    await db_session.commit()
    service = CapacityService(db_session)
    await service.set_calendar(profile.id, member.iteration.calendar_id, 0)
    result = await service.projection(profile.id, date(2026, 9, 28), date(2026, 9, 28))
    day = result["days"][0]
    assert day["allocated_hours"] == 3
    assert day["productive_hours"] == 3
    assert day["committed_effort_hours"] == .75
    assert day["has_unknown_commitment"] and result["has_unknown_effort"]


def test_short_workday_and_overflow_are_reserved_for_the_person():
    from app.services.scheduler_service import MemberSchedule
    friday, monday = date(2026, 10, 2), date(2026, 10, 5)
    schedule = MemberSchedule(member_id=1, member_name="Sam", capacity_days=2,
        working_dates=[friday], nominal_day_hours=6, short_dates={friday})
    assert schedule.allocate(friday, 1, 10, required_hours=6) == (friday, monday)
    assert schedule.allocate(friday, 1, 11, required_hours=1) == (date(2026, 10, 6), date(2026, 10, 6))


@pytest.mark.asyncio
async def test_schedule_preview_is_pure_and_rejects_changed_shared_inputs(db_session):
    from app.commands import command_transaction
    from app.services.scheduler_service import SchedulerService
    profile = TeamMemberProfile(display_name="Sam")
    member = await allocation(db_session, profile=profile)
    await db_session.commit()
    profile_id, iteration_id = profile.id, member.iteration_id
    async with command_transaction(db_session, mode="preview"):
        result = await SchedulerService(db_session).schedule_iteration(iteration_id, commit=False)
        observed = result.planning_revision
    assert await db_session.get(PlanningState, 1) is None
    await CapacityService(db_session).save_absence(profile_id, date(2026, 9, 28), date(2026, 9, 28))
    with pytest.raises(PlanningConflict, match="Shared availability changed"):
        await SchedulerService(db_session).schedule_iteration(iteration_id, expected_planning_revision=observed)


@pytest.mark.asyncio
async def test_overallocated_person_can_preview_but_cannot_commit(db_session):
    from app.commands import command_transaction
    from app.services.scheduler_service import SchedulerService
    profile = TeamMemberProfile(display_name="Sam")
    first = await allocation(db_session, profile=profile)
    await allocation(db_session, profile=profile)
    await db_session.commit()
    iteration_id = first.iteration_id
    async with command_transaction(db_session, mode="preview"):
        result = await SchedulerService(db_session).schedule_iteration(iteration_id, commit=False)
        assert result.capacity_issues[0]["code"] == "shared_capacity_overallocated"
    with pytest.raises(PlanningConflict, match="Reduce overlapping"):
        await SchedulerService(db_session).schedule_iteration(iteration_id, commit_baseline=True)


@pytest.mark.asyncio
async def test_two_planners_cannot_commit_the_same_shared_revision(db_session):
    import asyncio
    from app.models.task import Task
    from app.services.scheduler_service import SchedulerService
    profile = TeamMemberProfile(display_name="Sam")
    first = await allocation(db_session, profile=profile)
    second = await allocation(db_session, profile=profile)
    first.availability_percent = second.availability_percent = 50
    db_session.add_all([Task(title="First delivery", iteration=first.iteration, assignee=first, effort_hours=3),
                        Task(title="Second delivery", iteration=second.iteration, assignee=second, effort_hours=3)])
    await db_session.commit()
    ids = [first.iteration_id, second.iteration_id]
    factory = async_sessionmaker(db_session.bind, expire_on_commit=False)

    async def commit_plan(iteration_id):
        async with factory() as db:
            try:
                await SchedulerService(db).schedule_iteration(iteration_id, commit_baseline=True, expected_planning_revision=0)
                return "committed"
            except PlanningConflict:
                return "conflict"

    assert sorted(await asyncio.wait_for(asyncio.gather(*(commit_plan(item) for item in ids)), 15)) == ["committed", "conflict"]
    tasks = (await db_session.scalars(select(Task))).all()
    assert sum(task.baseline_revision for task in tasks) == 1


@pytest.mark.asyncio
async def test_iteration_restore_preserves_current_shared_absence(db_session):
    from app.services.snapshot_service import SnapshotService
    profile = TeamMemberProfile(display_name="Sam")
    first = await allocation(db_session, profile=profile)
    second = await allocation(db_session, profile=profile)
    await db_session.commit()
    first_id, second_id, profile_id, iteration_id = first.id, second.id, profile.id, first.iteration_id
    vacation = await TeamService(db_session).add_vacation(first_id, VacationCreate(start_date=date(2026, 9, 28), end_date=date(2026, 9, 28)))
    snapshot = await SnapshotService(db_session).create_snapshot(iteration_id, "before_absence_edit")
    await CapacityService(db_session).save_absence(profile_id, date(2026, 10, 1), date(2026, 10, 2), absence_id=vacation.profile_absence_id, expected_version=1)
    await SnapshotService(db_session).restore(iteration_id, snapshot)
    detail = await CapacityService(db_session).detail(profile_id)
    assert detail["absences"][0]["start_date"] == date(2026, 10, 1)
    assert (await TeamService(db_session).calculate_capacity(second_id)).vacation_days == 2


@pytest.mark.asyncio
async def test_reassigning_allocation_does_not_transfer_private_absence(db_session):
    from app.schemas.team import TeamMemberUpdate
    profile = TeamMemberProfile(display_name="Sam")
    member = await allocation(db_session, profile=profile)
    another = TeamMemberProfile(display_name="Taylor")
    db_session.add(another)
    await db_session.commit()
    service = TeamService(db_session)
    vacation = await service.add_vacation(member.id, VacationCreate(start_date=date(2026, 9, 28), end_date=date(2026, 9, 28)))
    original_absence = vacation.profile_absence_id
    await service.update(member.id, TeamMemberUpdate(profile_id=another.id))
    assert member.vacations == []
    assert (await db_session.get(ProfileAbsence, original_absence)).profile_id == profile.id
    assert (await service.calculate_capacity(member.id)).vacation_days == 0


@pytest.mark.asyncio
async def test_person_calendar_cannot_be_deleted_while_selected(db_session):
    from app.services.calendar_service import CalendarService
    profile = TeamMemberProfile(display_name="Sam")
    await allocation(db_session, profile=profile)
    calendar = Calendar(name="Person calendar", year=2026, holidays=[], weekend_days=[5, 6], short_days=[])
    db_session.add(calendar)
    await db_session.commit()
    calendar_id = calendar.id
    await CapacityService(db_session).set_calendar(profile.id, calendar_id, 0)
    with pytest.raises(PlanningConflict, match="availability calendar"):
        await CalendarService(db_session).delete(calendar_id)
    assert await db_session.get(Calendar, calendar_id) is not None


@pytest.mark.asyncio
async def test_overflow_forecast_cannot_commit_outside_allocation_dates(db_session):
    from app.models.task import Task
    from app.commands import command_transaction
    from app.services.scheduler_service import SchedulerService
    profile = TeamMemberProfile(display_name="Sam")
    member = await allocation(db_session, profile=profile)
    task = Task(title="Work beyond this allocation", iteration=member.iteration, assignee=member, effort_hours=90)
    db_session.add(task)
    await db_session.commit()
    iteration_id, task_id = member.iteration_id, task.id
    async with command_transaction(db_session, mode="preview"):
        await SchedulerService(db_session).schedule_iteration(iteration_id, commit=False)
        assert task.end_date > member.iteration.end_date
    with pytest.raises(PlanningConflict, match="allocation dates"):
        await SchedulerService(db_session).schedule_iteration(iteration_id, commit_baseline=True)
    restored = await db_session.get(Task, task_id)
    assert restored.baseline_revision == 0 and restored.start_date is None
