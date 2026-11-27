"""Gantt Scheduler Service - automatic task scheduling with optimization."""

from app.commands import atomic_command, command_transaction, commit_or_flush, lock_iterations, lock_planning, PlanningConflict
import math
import heapq
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import Any, Callable, Optional, Sequence

logger = logging.getLogger(__name__)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task, TaskDependency, TaskStatus
from app.models.team_member import TeamMember, Vacation
from app.models.iteration import Iteration
from app.services.calendar_service import CalendarService
from app.services.calendar_rules import AnnualCalendars
from app.services.task_service import TaskService
from app.services.team_service import TeamService
from app.services.scheduling_rules_service import SchedulingRulesService
from app.schemas.gantt import KeptDatesTask, SchedulingDecision, ScheduleResult, UnscheduledTask, WaitingOnTask, WorkloadIssue


class MissingCalendarYear(PlanningConflict):
    def __init__(self, year: int):
        self.year = year
        super().__init__("calendar_outside_year", f"No working calendar is selected for {year}.")


class ChangeType(Enum):
    """Types of changes that trigger incremental rescheduling."""
    EFFORT_INCREASED = "effort_increased"
    EFFORT_DECREASED = "effort_decreased"
    ASSIGNEE_CHANGED = "assignee_changed"
    PRIORITY_CHANGED = "priority_changed"
    DEPENDENCY_ADDED = "dependency_added"
    DEPENDENCY_REMOVED = "dependency_removed"
    MIN_START_DATE_CHANGED = "min_start_changed"
    MAX_END_DATE_CHANGED = "max_end_changed"
    STATUS_CHANGED = "status_changed"


@dataclass
class TaskChange:
    """Represents a change to a task for incremental rescheduling."""
    task_id: int
    iteration_id: int
    change_type: ChangeType
    old_value: Any = None
    new_value: Any = None
    assignee_id: Optional[int] = None  # For context in assignee-related changes


@dataclass
class RescheduleResult:
    """Result of an incremental reschedule operation."""
    affected_task_ids: list[int]
    rescheduled_count: int
    decisions: list[SchedulingDecision]




@dataclass
class MemberSchedule:
    """Optimized schedule tracking with O(D) slot finding using sliding window.

    Performance optimizations:
    1. Date-to-index mapping for O(1) lookups
    2. Lazy caching of available dates with invalidation
    3. Sliding window algorithm for find_uninterrupted_slot (O(D) vs O(D²))
    """
    member_id: int
    member_name: str
    capacity_days: float
    working_dates: list[date] = field(default_factory=list)
    vacation_dates: set[date] = field(default_factory=set)
    holiday_dates: set[date] = field(default_factory=set)  # Calendar holidays (full year)
    weekend_days: set[int] = field(default_factory=lambda: {5, 6})  # Calendar weekend weekdays
    allocated_dates: dict[date, int] = field(default_factory=dict)  # date -> task_id
    # Workload accounting in standard effort-days (raw task effort), so it is
    # directly comparable with MemberCapacity.adjusted_days. Calendar dates
    # consumed by a task are inflated by coefficients; counting them here would
    # double-apply operational utilization against the already-deflated capacity.
    allocated_days: float = 0.0
    nominal_day_hours: float = 8.0
    productivity_factor: float = 1.0
    short_dates: set[date] = field(default_factory=set)
    annual_calendars: AnnualCalendars | None = None
    # Dates whose capacity-row percentage a dated adjustment replaces, with their factor.
    dated_factors: dict[date, float] = field(default_factory=dict)

    # Optimization: date-to-index mapping for O(1) lookups
    _date_to_idx: dict[date, int] = field(default_factory=dict, repr=False)
    # Optimization: cached available dates with lazy invalidation
    _available_cache: Optional[list[date]] = field(default=None, repr=False)
    _cache_valid: bool = field(default=False, repr=False)

    def __post_init__(self):
        """Build date-to-index mapping after initialization."""
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Build date-to-index mapping for O(1) lookups."""
        self._date_to_idx = {d: i for i, d in enumerate(self.working_dates)}
        self._invalidate_cache()

    def _invalidate_cache(self) -> None:
        """Invalidate the available dates cache."""
        self._cache_valid = False
        self._available_cache = None

    def get_available_dates(self) -> list[date]:
        """Get dates that are available (working and not allocated).

        Uses lazy caching - O(1) after first call, O(D) on cache miss.
        Cache is invalidated when allocations change.
        """
        if self._cache_valid and self._available_cache is not None:
            return self._available_cache

        # Rebuild cache
        self._available_cache = [
            d for d in self.working_dates
            if d not in self.allocated_dates and d not in self.vacation_dates
        ]
        self._cache_valid = True
        return self._available_cache

    def can_schedule_uninterrupted(self, start_date: date, effort_days: int) -> bool:
        """Check if task can be scheduled without interruption (no vacations in between).

        Weekends and holidays are allowed gaps - tasks naturally span them.
        Only vacations are considered interruptions.
        If a date is both holiday AND vacation, vacation takes priority (it's an interruption).
        """
        available = self.get_available_dates()
        available_from_start = [d for d in available if d >= start_date]

        if len(available_from_start) < effort_days:
            return False

        # Check for continuity in the first effort_days available
        block = available_from_start[:effort_days]
        for i in range(len(block) - 1):
            gap = (block[i + 1] - block[i]).days
            if gap > 1:
                # Check if any vacation days are in this gap
                # Vacation takes priority over holiday
                vacation_in_gap = any(
                    block[i] + timedelta(days=k) in self.vacation_dates
                    for k in range(1, gap)
                )
                # If vacation in gap, NOT contiguous
                # Weekends and holidays (without vacation) are OK
                if vacation_in_gap:
                    return False

        return True

    def find_next_available_date(self, earliest_start: date) -> Optional[date]:
        """Find the first available working date on or after earliest_start.

        Uses cached available dates for efficiency.
        """
        available = self.get_available_dates()
        # Binary search would be O(log D), but linear scan on cached list is fine
        for d in available:
            if d >= earliest_start:
                return d
        return None

    def find_uninterrupted_slot(self, earliest_start: date, effort_days: int) -> Optional[date]:
        """Find the earliest date where effort_days contiguous working days are available.

        OPTIMIZED: O(D) sliding window algorithm instead of O(D²) nested loops.

        A contiguous block means consecutive working days.
        - Weekends and holidays are ALLOWED gaps (task spans them naturally)
        - Vacations are INTERRUPTIONS - task should not be split by vacation
        - If a date is both holiday AND vacation, vacation takes priority (counts as interruption)
        """
        available = self.get_available_dates()

        # Filter to dates >= earliest_start using the index for efficiency
        start_idx = 0
        for i, d in enumerate(available):
            if d >= earliest_start:
                start_idx = i
                break
        else:
            # No dates >= earliest_start
            logger.warning(f"  [FIND_SLOT] No available dates from {earliest_start}")
            return None

        available_from_start = available[start_idx:]
        n = len(available_from_start)

        logger.warning(f"  [FIND_SLOT] Looking for {effort_days} contiguous days from {earliest_start}")
        logger.warning(f"  [FIND_SLOT] Available dates: {[d.isoformat() for d in available_from_start[:20]]}...")
        logger.warning(f"  [FIND_SLOT] Vacation dates for this member: {[d.isoformat() for d in sorted(self.vacation_dates)]}")

        if n < effort_days:
            # Not enough total days - return first available and let allocate handle overflow
            return available_from_start[0] if available_from_start else None

        # SLIDING WINDOW OPTIMIZATION: O(D) instead of O(D²)
        # Track window start and consecutive count
        window_start = 0
        consecutive = 1  # First date is always "consecutive" with itself

        for i in range(1, n):
            prev_date = available_from_start[i - 1]
            curr_date = available_from_start[i]
            gap = (curr_date - prev_date).days

            if gap == 1:
                # Consecutive working days
                consecutive += 1
            elif gap > 1:
                # Gap exists - check if vacation interrupts
                vacation_in_gap = any(
                    prev_date + timedelta(days=k) in self.vacation_dates
                    for k in range(1, gap)
                )

                if vacation_in_gap:
                    # Vacation breaks continuity - reset window
                    window_start = i
                    consecutive = 1
                else:
                    # Weekend/holiday gap without vacation - continuity preserved
                    consecutive += 1

            # Check if we have enough consecutive days
            if consecutive >= effort_days:
                slot_start = available_from_start[window_start]
                logger.warning(f"  [FIND_SLOT] Found contiguous block starting at {slot_start}")
                return slot_start

        # Check if we accumulated enough from the last window
        if consecutive >= effort_days:
            slot_start = available_from_start[window_start]
            logger.warning(f"  [FIND_SLOT] Found contiguous block starting at {slot_start}")
            return slot_start

        # No fully contiguous block found
        # Return first available - the allocate() method will handle spanning
        logger.warning(f"  [FIND_SLOT] No contiguous block found, returning first available: {available_from_start[0] if available_from_start else None}")
        return available_from_start[0] if available_from_start else None

    def _is_projectable_working_day(self, day: date) -> bool:
        """Working-day check for dates that may lie outside the iteration period.

        Uses the calendar's weekend configuration and full-year holidays instead
        of a hardcoded Mon-Fri week, so overflow projections respect custom
        calendars the same way in-iteration scheduling does.
        """
        if self.annual_calendars is not None:
            hours = self.annual_calendars.hours(day)
            if hours is None:
                raise MissingCalendarYear(day.year)
            return hours > 0 and day not in self.vacation_dates
        return (
            day.weekday() not in self.weekend_days
            and day not in self.holiday_dates
            and day not in self.vacation_dates
        )

    def allocate(
        self, start_date: date, effort_days: int, task_id: int,
        accounting_days: Optional[float] = None, required_hours: float | None = None,
    ) -> tuple[date, date]:
        """Reserve whole working dates, including overflow, until the requested effort fits."""
        required = required_hours if required_hours is not None else float(effort_days)
        remaining = required
        allocated = []
        current = start_date
        for _ in range(3660):
            if current in self.allocated_dates:
                # A task's date range must not straddle another task's working
                # hours. Retry after that reservation without consuming the gap.
                allocated = []
                remaining = required
            elif self._is_projectable_working_day(current):
                hours = self.annual_calendars.hours(current) if self.annual_calendars else self.nominal_day_hours - (current in self.short_dates)
                factor = self.dated_factors.get(current, self.productivity_factor)
                if required_hours is not None:
                    capacity = hours * factor
                else:
                    capacity = 0.0 if self.dated_factors.get(current, 1.0) <= 0 else 1.0
                if capacity > 0:
                    allocated.append(current)
                    remaining -= capacity
                    if remaining <= .000001:
                        self.allocated_dates.update({day: task_id for day in allocated})
                        self.allocated_days += accounting_days if accounting_days is not None else effort_days
                        self._invalidate_cache()
                        return allocated[0], current
            current += timedelta(days=1)
        raise PlanningConflict("forecast_horizon_exceeded", "No capacity was found within the forecast horizon. Reconcile availability.")


async def rebind_queued_assignments(db: AsyncSession, task_id: int, previous_version: int, new_version: int,
                                    *, protect_issued: bool = False) -> list[dict]:
    """Keep queued dispatch valid when only a task's dates changed.

    A queued agent assignment is bound to the task version it was created for,
    so that a changed brief sends the PM back to dispatch. Calculated dates are
    not part of that agreement. Model-aware assignments are left alone: their
    routing evidence is bound to the exact task version.
    """
    if new_version == previous_version:
        return []
    from app.models.agent import AgentTaskAssignment
    from app.services.agent_work_service import AgentWorkService

    queued = await db.scalars(
        select(AgentTaskAssignment).where(
            AgentTaskAssignment.task_id == task_id,
            AgentTaskAssignment.state.in_(("queued", "accepted")),
        ).order_by(AgentTaskAssignment.id).with_for_update()
    )
    refreshes = []
    for assignment in queued.all():
        if assignment.state == "accepted":
            if protect_issued:
                raise PlanningConflict("issued_task_schedule_conflict",
                    f"Scheduling would change task {task_id} during accepted assignment {assignment.id}. Preserve its dates or finish that attempt first.")
            continue
        if assignment.task_version != previous_version:
            continue
        if AgentWorkService._is_model_aware_assignment(assignment):
            refreshes.append({"task_id":task_id,"assignment_id":assignment.id,"actor_id":assignment.actor_id,
                              "from_task_version":previous_version,"to_task_version":new_version,
                              "action":"refresh_model_selection"})
        else:
            assignment.task_version = new_version
    return refreshes


class SchedulerService:
    """Service for automatic task scheduling."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.calendar_service = CalendarService(db)
        self.task_service = TaskService(db)
        self.team_service = TeamService(db)
        self.rules_service = SchedulingRulesService.get_instance()

    # What leaves a planned task without dates, and what would change that.
    UNSCHEDULED_MESSAGES = {
        "no_assignee": "Assign this task to a capacity row in this iteration (a person or an agent profile), then schedule again.",
        "assignee_not_in_iteration": "The assignee has no capacity row in this iteration. Add them to the iteration or reassign the task, then schedule again.",
        "no_estimate": "Provide a positive effort estimate to schedule this task.",
        "no_capacity": "The assigned person has no productive capacity. Adjust the allocation before scheduling.",
        "prerequisites_pending": "Accept the delivery prerequisites before scheduling this work.",
        "predecessor_unscheduled": "Estimate and schedule the prerequisite first.",
        "predecessor_postponed": "A prerequisite is postponed and holds no schedule until it is reactivated. "
                                 "Reactivate it or remove the dependency, then schedule again.",
        "deferred": "Deferred work is left out of scheduling. Undefer it to schedule it.",
        "blocked": "Blocked work is left out of scheduling. Clear the block to schedule it.",
        "not_placed": "The scheduler could not place this task. Check its constraint dates and dependencies.",
    }

    # The rule that made saved dates unusable, as the report names it.
    DATE_RULE_MESSAGES = {
        "dates_incomplete": "only one of the start and end dates was set",
        "dates_inverted": "the end date is before the start date",
        "outside_iteration": "they fall outside the iteration",
        "before_min_start_date": "they start before the task's earliest start date",
    }

    @atomic_command
    async def schedule_iteration(
        self,
        iteration_id: int,
        *,
        commit: bool = True,
        expected_revision: int | None = None,
        expected_planning_revision: int | None = None,
        commit_baseline: bool = False,
        protect_issued: bool = False,
        rebaseline_reason: str | None = None,
        follow_date: date | None = None,
        anchor_task_id: int | None = None,
    ) -> ScheduleResult:
        """Schedule an iteration, optionally leaving commit ownership to the caller.

        ``follow_date`` recalculates the plan around what really happened: planned
        work is placed on or after that date, finished work frees its assignee from
        that date, running work holds its assignee at least through it, and a task
        the calculation cannot place keeps its dates. ``anchor_task_id`` names the
        task that started on ``follow_date``; it takes its assignee's row from there.
        """
        from app.services.iteration_service import IterationService

        planning_revision = await lock_planning(self.db, expected=expected_planning_revision)
        iteration_service = IterationService(self.db)
        await lock_iterations(self.db, [iteration_id], expected={iteration_id: expected_revision} if expected_revision is not None else None, require_expected=True, revision_field="expected_revision")
        iteration = await iteration_service.get_by_id(iteration_id)

        if not iteration:
            return ScheduleResult(success=False, decisions=[])

        # Get all data
        all_tasks = await self.task_service.get_all_tasks(iteration_id)
        before_dates = {task.id: (task.start_date, task.end_date) for task in all_tasks}
        before_effort = {task.id: task.calculated_effort_days for task in all_tasks}
        team_members = await self.team_service.get_by_iteration(iteration_id)

        from app.services.capacity_service import CapacityService
        capacity_issues = await CapacityService(self.db).schedule_issues(iteration, team_members)
        input_issues = [issue for issue in capacity_issues if issue["code"] != "committed_capacity_exceeded"]
        if commit_baseline and input_issues:
            raise PlanningConflict(input_issues[0]["code"], input_issues[0]["message"])
        if any(issue["code"] in {"calendar_outside_year", "calendar_reconciliation_required"} for issue in input_issues):
            return ScheduleResult(success=False, planning_revision=planning_revision,
                                  capacity_issues=capacity_issues, workload_balanced=False)

        def uncovered_forecast(exc: MissingCalendarYear) -> ScheduleResult:
            # Forecasting can reach a later year than the configured iteration.
            # Restore draft dates before any task or assignment version is reserved.
            if commit_baseline:
                raise exc
            for row in all_tasks:
                row.start_date, row.end_date = before_dates[row.id]
                row.calculated_effort_days = before_effort[row.id]
            issue = {"code": exc.code, "message": str(exc), "missing_calendar_years": [exc.year]}
            return ScheduleResult(success=False, planning_revision=planning_revision,
                                  capacity_issues=[*capacity_issues, issue], workload_balanced=False)

        # Build member schedules
        member_schedules = await self._build_member_schedules(
            iteration, team_members
        )

        decisions: list[SchedulingDecision] = []
        unscheduled_reasons: dict[int, str] = {}

        # Build task map for dependency lookup during scheduling
        task_map = {t.id: t for t in all_tasks}
        from app.services.work_metrics import effective_work_flags
        self._work_flags = {task.id: effective_work_flags(task, by_id=task_map) for task in all_tasks}

        # Collect all leaf tasks (tasks without children) that need scheduling
        # IMPORTANT: Only schedule tasks with PLANNED status
        # Tasks in ACTIVE, RESOLVED and CLOSED already have actual dates
        # that should not be modified by auto-scheduling
        from app.models.task import TaskStatus

        # Postponed work keeps its last dates as history only: it occupies no capacity, is not placed,
        # and is never reported as kept, unscheduled or missing dates.
        all_leaf_tasks = [t for t in all_tasks if not t.children and not t.is_summary and not self._holds_no_schedule(t) and not t.canceled_at and not t.blocked_reason]

        # Split into schedulable (PLANNED) and locked (non-PLANNED) tasks
        leaf_tasks = [t for t in all_leaf_tasks if t.status == TaskStatus.PLANNED.value]
        locked_tasks = [t for t in all_leaf_tasks if t.status != TaskStatus.PLANNED.value]
        unavailable_estimates = [task for task in leaf_tasks if task.effort_hours is None or task.effort_hours == 0]
        for task in unavailable_estimates:
            unscheduled_reasons[task.id] = "no_estimate"
            task.start_date = task.end_date = task.calculated_effort_days = None
            decisions.append(SchedulingDecision(task_id=task.id, task_title=task.title, decision_type="unavailable",
                reason="Provide a positive effort estimate to schedule this task."))
        unavailable_ids = {task.id for task in unavailable_estimates}
        for task in leaf_tasks:
            dated = getattr(self, "_dated_availability", None)
            no_share = task.assignee is not None and task.assignee.availability_percent <= 0 and not (
                dated is not None and dated.any_positive(task.assignee))
            if task.assignee and (no_share or task.assignee.operational_utilization >= 100):
                unavailable_ids.add(task.id)
                unscheduled_reasons[task.id] = "no_capacity"
                task.start_date = task.end_date = task.calculated_effort_days = None
                decisions.append(SchedulingDecision(task_id=task.id, task_title=task.title, decision_type="unavailable",
                    reason="The assigned person has no productive capacity. Adjust the allocation before scheduling."))
        from app.services.delivery_dependency_service import DeliveryDependencyService
        for task in leaf_tasks:
            if not await DeliveryDependencyService(self.db).ready(task.id):
                unavailable_ids.add(task.id)
                unscheduled_reasons.setdefault(task.id, "prerequisites_pending")
                task.start_date = task.end_date = task.calculated_effort_days = None
                decisions.append(SchedulingDecision(task_id=task.id, task_title=task.title, decision_type="unavailable",
                    reason="Accept the delivery prerequisites before scheduling this work."))
        # Work that depends on postponed work, directly or through a summary, waits for it by name: the
        # postponed task holds no schedule until it is reactivated, so its old dates (or its siblings'
        # dates) are no evidence of when the dependent can start. The wait is the primary reason; the
        # task's own causes are reported beside it.
        predecessor_messages: dict[int, str] = {}
        postponed_waits = self._postponed_waits(all_tasks, task_map)
        # One decision per waiting task: the wait, with any cause of its own named beside it.
        decisions[:] = [decision for decision in decisions if decision.task_id not in postponed_waits]
        for task in leaf_tasks:
            if task.id not in postponed_waits:
                continue
            message = self._postponed_wait_message(postponed_waits[task.id])
            own = unscheduled_reasons.get(task.id)
            if own is not None:
                message = f"{message} It also needs a fix of its own: {self.UNSCHEDULED_MESSAGES[own]}"
            if task.id not in unavailable_ids:
                unavailable_ids.add(task.id)
                task.start_date = task.end_date = task.calculated_effort_days = None
            decisions.append(SchedulingDecision(task_id=task.id, task_title=task.title, decision_type="unavailable",
                reason=message))
        leaf_tasks = [task for task in leaf_tasks if task.id not in unavailable_ids]

        logger.warning(f"[SCHEDULER] Task status filter: {len(leaf_tasks)} PLANNED (to schedule), {len(locked_tasks)} non-PLANNED (dates locked)")

        finished_statuses = {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}
        satisfied_predecessor_ids = {task.id for task in all_tasks
                                     if task.status in finished_statuses or task.canceled_at}
        anchored_ids: set[int] = set()
        if follow_date is not None and anchor_task_id is not None:
            anchor = next((task for task in locked_tasks if task.id == anchor_task_id), None)
            schedule = member_schedules.get(anchor.assignee_id) if anchor is not None else None
            if anchor is not None and schedule is not None and anchor.effort_hours:
                # Work that starts now takes its row first; its end follows the row's working days.
                try:
                    _, anchor_end = schedule.allocate(
                        follow_date, self._calculate_adjusted_effort(anchor), anchor.id,
                        accounting_days=anchor.effort_days, required_hours=anchor.effort_hours,
                    )
                except MissingCalendarYear as exc:
                    return uncovered_forecast(exc)
                except PlanningConflict:
                    # A row without productive capacity cannot place the work; its dates stay as they are.
                    for day in [day for day, owner in schedule.allocated_dates.items() if owner == anchor.id]:
                        del schedule.allocated_dates[day]
                    schedule._invalidate_cache()
                else:
                    anchor.start_date, anchor.end_date = follow_date, max(anchor_end, follow_date)
                    anchor.calculated_effort_days = float(sum(owner == anchor.id for owner in schedule.allocated_dates.values()))
                    anchored_ids.add(anchor.id)

        # Retained execution dates consume slots before new forecasts are placed.
        for task in locked_tasks:
            if task.id in anchored_ids:
                continue
            schedule = member_schedules.get(task.assignee_id)
            if schedule is None or task.start_date is None or task.end_date is None:
                continue
            last_day = task.end_date
            if follow_date is not None:
                if task.status in finished_statuses:
                    last_day = min(last_day, follow_date - timedelta(days=1))
                elif task.status == TaskStatus.ACTIVE.value:
                    last_day = max(last_day, follow_date)
            day = task.start_date
            if schedule.annual_calendars:
                missing = schedule.annual_calendars.missing_years(day, last_day)
                if missing:
                    return uncovered_forecast(MissingCalendarYear(missing[0]))
            while day <= last_day:
                if schedule._is_projectable_working_day(day):
                    schedule.allocated_dates.setdefault(day, task.id)
                day += timedelta(days=1)
            schedule.allocated_days += task.effort_days or 0
            schedule._invalidate_cache()

        # IMPORTANT: Only clear dates for PLANNED tasks
        # Non-PLANNED tasks keep their dates as they are already "locked in"
        for task in leaf_tasks:
            task.start_date = None
            task.end_date = None
        planned_leaf_ids = {task.id for task in all_leaf_tasks if task.status == TaskStatus.PLANNED.value}
        planning_start = self._planning_start(iteration)

        # Calculate earliest_start for each leaf task
        def get_task_earliest_start(task: Task) -> date:
            """Get earliest possible start date for a task."""
            base = planning_start
            if follow_date is not None and follow_date > base:
                base = follow_date

            # Apply min_start_date constraint
            if task.min_start_date and task.min_start_date > base:
                base = task.min_start_date

            # Check dependencies
            for dep in task.dependencies:
                # Completed or canceled work is satisfied regardless of saved forecast dates.
                if dep.depends_on_id in satisfied_predecessor_ids:
                    continue
                dep_task = task_map.get(dep.depends_on_id)
                if dep_task and dep_task.end_date:
                    dep_last = dep_task.end_date
                    if follow_date is not None:
                        if dep_task.status == TaskStatus.ACTIVE.value:
                            dep_last = max(dep_last, follow_date)
                    dep_end = dep_last + timedelta(days=1)
                    if dep_end > base:
                        base = dep_end

            return base

        def get_next_vacation_start(member_id: int) -> Optional[date]:
            """Get the start date of the next vacation for a member."""
            schedule = member_schedules.get(member_id)
            if not schedule or not schedule.vacation_dates:
                return None
            # Get the earliest vacation date that's after the iteration start
            vacation_sorted = sorted(schedule.vacation_dates)
            for vd in vacation_sorted:
                if vd >= iteration.start_date:
                    return vd
            return None

        # Pre-calculate available days before vacation for each assignee
        assignee_days_before_vacation: dict[int, int] = {}
        for member_id, schedule in member_schedules.items():
            vacation_start = get_next_vacation_start(member_id)
            if vacation_start:
                days = sum(
                    1 for d in schedule.get_available_dates()
                    if d < vacation_start
                )
                assignee_days_before_vacation[member_id] = days
            else:
                # No vacation, all days are "before vacation"
                assignee_days_before_vacation[member_id] = len(schedule.get_available_dates())

        # Group leaf tasks by assignee and calculate which can fit before vacation
        # considering other tasks for the same assignee
        from collections import defaultdict
        tasks_by_assignee: dict[int, list[Task]] = defaultdict(list)
        for t in leaf_tasks:
            if t.assignee_id:
                tasks_by_assignee[t.assignee_id].append(t)

        # For each assignee, determine which tasks can fit before vacation
        # Higher priority (lower number) tasks get first chance at pre-vacation slots
        task_can_fit_before_vacation: dict[int, bool] = {}
        task_contexts = {task.id: self._build_task_context(task, task_can_fit_before_vacation)
                         for task in leaf_tasks}

        for assignee_id, assignee_tasks in tasks_by_assignee.items():
            available_days = assignee_days_before_vacation.get(assignee_id, 0)

            # Sort by priority (lower = higher priority), then by effort (smaller first)
            sorted_tasks = sorted(assignee_tasks, key=lambda t: (task_contexts[t.id]["is_optional"],
                                                               t.priority, task_contexts[t.id]["adjusted_effort"]))

            remaining_days = available_days
            for task in sorted_tasks:
                effort = task_contexts[task.id]["adjusted_effort"]
                if remaining_days >= effort:
                    task_can_fit_before_vacation[task.id] = True
                    remaining_days -= effort
                else:
                    task_can_fit_before_vacation[task.id] = False
                task_contexts[task.id]["fits_before_vacation"] = task_can_fit_before_vacation[task.id]

        logger.warning(f"[SCHEDULER] Pre-vacation capacity analysis:")
        for assignee_id, days in assignee_days_before_vacation.items():
            member_name = member_schedules[assignee_id].member_name
            logger.warning(f"  - {member_name}: {days} days before vacation")

        # ══════════════════════════════════════════════════════════════════
        # MULTI-PASS SCHEDULING FROM YAML CONFIGURATION
        # ══════════════════════════════════════════════════════════════════

        def get_fallback_sort_key(task_with_start: tuple[Task, date]) -> tuple:
            """
            Fallback vacation-aware sorting (used when no YAML passes defined):

            1. Tasks that CAN complete before vacation → schedule first (priority 0)
               - Sorted by: is_optional, priority, then smallest first (to fit more before vacation)

            2. Tasks that CANNOT complete before vacation → schedule after (priority 1)
               - Higher priority (lower number) goes first (will span vacation)
               - At same priority: LARGER tasks go first (so they get scheduled and span vacation)
               - Smaller tasks follow after the larger task completes

            Returns tuple for sorting.
            """
            task, earliest_start = task_with_start
            effort = task_contexts[task.id]["adjusted_effort"]

            # Check if this task can fit before vacation (considering other tasks)
            can_fit = task_can_fit_before_vacation.get(task.id, True)

            if can_fit:
                # Can complete before vacation - schedule first
                vacation_priority = 0
                size_order = effort  # Smaller first to fit more
            else:
                # Cannot complete before vacation
                vacation_priority = 1
                # LARGER tasks first (negative effort for descending sort)
                # This ensures large tasks span vacation, small tasks follow after
                size_order = -effort

            # Sort by: vacation_priority, is_optional, priority, size_order
            return (vacation_priority, self._effective_flags(task)["effective_is_optional"], task.priority, size_order)

        # Passes rank tasks that are ready; a prerequisite in a later pass must
        # still be placed before its dependent in an earlier pass.
        scheduling_passes = self.rules_service.get_scheduling_passes()
        pass_sort_keys = [self.rules_service.get_sort_key_function(
            pass_config.id,
            lambda task: task_contexts[task.id],
        ) for pass_config in scheduling_passes]
        ranks = {}
        for index, task in enumerate(leaf_tasks):
            context = task_contexts[task.id]
            for pass_index, pass_config in enumerate(scheduling_passes):
                if self.rules_service.matches_pass_filter(pass_config.id, context):
                    ranks[task.id] = (pass_index, pass_sort_keys[pass_index](task), index)
                    break
            else:
                ranks[task.id] = (len(scheduling_passes),
                    get_fallback_sort_key((task, get_task_earliest_start(task))), index)

        # A summary predecessor waits for current child dates or satisfied work;
        # dates saved by an earlier forecast are not evidence of readiness.
        composite_tasks = [task for task in all_tasks if task.children]
        nodes = leaf_tasks + composite_tasks
        pending = {task.id: task for task in nodes}
        predecessors = {task.id: {dep.depends_on_id for dep in task.dependencies
                                 if dep.depends_on_id not in satisfied_predecessor_ids}
                        for task in leaf_tasks}
        for index, task in enumerate(composite_tasks):
            predecessors[task.id] = {child.id for child in task.children
                                    if not self._holds_no_schedule(child)}
            ranks[task.id] = (-1, (), index)
        dependents: dict[int, list[int]] = defaultdict(list)
        outstanding: dict[int, set[int]] = {}
        ready = []
        for task in nodes:
            waiting = {predecessor_id for predecessor_id in predecessors[task.id]
                       if predecessor_id not in satisfied_predecessor_ids
                       and (predecessor_id in pending or predecessor_id not in task_map
                            or task_map[predecessor_id].start_date is None
                            or task_map[predecessor_id].end_date is None)}
            outstanding[task.id] = waiting
            for predecessor_id in waiting:
                dependents[predecessor_id].append(task.id)
            if not waiting:
                heapq.heappush(ready, (ranks[task.id], task.id))

        assignee_last_end: dict[int, date] = {}
        while ready:
            _, task_id = heapq.heappop(ready)
            task = pending.pop(task_id)
            if task.children:
                children = [task_map[child_id] for child_id in predecessors[task_id]
                            if task_map[child_id].start_date is not None
                            and task_map[child_id].end_date is not None]
                if children:
                    task.start_date = min(child.start_date for child in children)
                    task.end_date = max(child.end_date for child in children)
                elif predecessors[task_id]:
                    # All children are satisfied without dates; release dependents
                    # without inventing dates for completed or canceled work.
                    satisfied_predecessor_ids.add(task_id)
                else:
                    continue
            else:
                earliest_start = get_task_earliest_start(task)
                if task.assignee_id in assignee_last_end:
                    # Keep the cursor even beyond the iteration. Looking for a date
                    # only inside the iteration can otherwise backfill an earlier gap.
                    earliest_start = max(earliest_start, assignee_last_end[task.assignee_id] + timedelta(days=1))
                try:
                    await self._schedule_leaf_task(
                        task, iteration, member_schedules, decisions, task_map, earliest_start
                    )
                except MissingCalendarYear as exc:
                    return uncovered_forecast(exc)
                if task.start_date is not None and task.end_date is not None:
                    assignee_last_end[task.assignee_id] = task.end_date
            if task_id not in satisfied_predecessor_ids and (task.start_date is None or task.end_date is None):
                continue
            for dependent_id in dependents[task_id]:
                outstanding[dependent_id].remove(task_id)
                if not outstanding[dependent_id]:
                    heapq.heappush(ready, (ranks[dependent_id], dependent_id))

        for task in pending.values():
            if task.children:
                continue
            missing = min(outstanding[task.id])
            predecessor = task_map.get(missing)
            name = f"'{predecessor.title}' (ID {missing})" if predecessor else f"ID {missing}"
            message = f"Predecessor {name} has no complete schedule. Schedule it before this task."
            unscheduled_reasons[task.id] = "predecessor_unscheduled"
            predecessor_messages[task.id] = message
            task.calculated_effort_days = None
            decisions.append(SchedulingDecision(task_id=task.id, task_title=task.title,
                decision_type="unavailable", reason=message))

        # A task the run could not place keeps the dates it already had, so the run never leaves it
        # blocked by missing dates. The report names a rule the kept dates break. Only a half-dated task
        # (one date set) loses its dates outside follow mode: it has no period to keep.
        kept_dates: dict[int, str | None] = {}
        incomplete_ids: set[int] = set()
        for task in all_tasks:
            if task.id not in planned_leaf_ids or task.start_date is not None or task.end_date is not None:
                continue
            saved = before_dates[task.id]
            if saved == (None, None):
                continue
            rule = None if follow_date is not None else self._date_rule_violation(task, saved, iteration)
            if rule == "dates_incomplete":
                incomplete_ids.add(task.id)
                continue
            task.start_date, task.end_date = saved
            task.calculated_effort_days = before_effort[task.id]
            if saved[0] is not None and saved[1] is not None:
                kept_dates[task.id] = rule

        # Update composite (parent) task dates based on their children
        for parent in composite_tasks:
            self._update_composite_task_dates(parent, iteration, decisions)

        assignment_refreshes = []
        for task in sorted(all_tasks, key=lambda task: task.id):
            if before_dates[task.id] != (task.start_date, task.end_date):
                previous_version = task.version
                await self.task_service.reserve_task_version(task, task.version)
                assignment_refreshes.extend(await rebind_queued_assignments(self.db, task.id, previous_version, task.version,
                    protect_issued=commit_baseline or protect_issued))

        if commit_baseline:
            from app.models.recovery import TaskScheduleBaseline
            from app.models.project import Project
            # Only dates the run calculated are checked; dates it kept as saved are reported with their rule.
            if any(task.start_date is not None and task.end_date is not None and task.id not in kept_dates and
                   (task.start_date < iteration.start_date or task.end_date > iteration.end_date)
                   for task in leaf_tasks):
                raise PlanningConflict("schedule_outside_allocation",
                    "The forecast exceeds its allocation dates. Extend the iteration or move the work before committing.")
            authority = self.db.info.get("authority")
            timezone = await self.db.scalar(select(Project.timezone).where(Project.id == iteration.project_id)) if iteration.project_id else iteration.calendar.timezone
            for task in all_leaf_tasks:
                # Dates kept for work the run could not place were not committed by it.
                if task.start_date is None or task.end_date is None or task.id in kept_dates:
                    continue
                if task.baseline_revision and not rebaseline_reason:
                    continue
                if rebaseline_reason is not None and len(rebaseline_reason.strip()) < 8:
                    raise ValueError("A deliberate rebaseline requires a clear reason")
                task.baseline_revision += 1
                task.baseline_start_date, task.baseline_end_date = task.start_date, task.end_date
                task.baseline_provenance = "committed" if getattr(authority, "principal_id", None) else "committed_unattributed"
                self.db.add(TaskScheduleBaseline(task_id=task.id, revision=task.baseline_revision,
                    start_date=task.start_date, end_date=task.end_date, timezone=timezone or "UTC",
                    reason=rebaseline_reason or "Initial schedule commitment", principal_id=getattr(authority, "principal_id", None)))

        if commit_baseline:
            await self.db.flush()
            committed_issues = await CapacityService(self.db).schedule_issues(iteration, team_members)
            if committed_issues:
                raise PlanningConflict(committed_issues[0]["code"], committed_issues[0]["message"])

        # Agent command adapters need the schedule and their exact receipt to
        # share one transaction. Existing callers retain commit-by-default.
        if commit:
            await commit_or_flush(self.db)
        else:
            await self.db.flush()

        # Check workload balance
        workload_issues = self._check_workload_balance(member_schedules)
        unscheduled, kept_items = self._unscheduled_tasks(
            all_tasks, member_schedules, unscheduled_reasons, predecessor_messages, before_dates,
            kept_dates=kept_dates, incomplete_ids=incomplete_ids, postponed_waits=postponed_waits,
            iteration_dates=(iteration.start_date, iteration.end_date),
            planning_start=planning_start, satisfied_ids=satisfied_predecessor_ids)
        # Causes found only now (no assignee, assignee outside the iteration) also explain themselves as decisions.
        for item in [*unscheduled, *kept_items]:
            if item.reason in {"no_assignee", "assignee_not_in_iteration", "not_placed"}:
                decisions.append(SchedulingDecision(task_id=item.task_id, task_title=item.task_title,
                    decision_type="unavailable", reason=item.message))

        return ScheduleResult(
            success=True,
            planning_revision=planning_revision,
            capacity_issues=capacity_issues,
            assignment_refreshes=assignment_refreshes,
            decisions=decisions,
            workload_balanced=len(workload_issues) == 0,
            workload_issues=workload_issues,
            unscheduled=unscheduled,
            kept_dates=kept_items,
        )

    async def follow_actual_dates(self, task: Task, today: date, *, started: bool = False) -> list[int]:
        """Move planned work to what really happened after ``task`` started or finished.

        The caller owns the command transaction. A plan the calculation cannot
        place keeps its dates: following actual dates never blocks the work itself.
        Returns the IDs of the other tasks whose dates moved.
        """
        if task.iteration_id is None:
            return []
        from app.authority import internal_authority
        from app.commands import current_command

        moved: list[int] = []
        # The caller's own change is authorized as the caller; the recalculation is the server's.
        await self.db.flush()
        with internal_authority(self.db):
            await lock_iterations(self.db, [task.iteration_id])
            tasks = await self.task_service.get_all_tasks(task.iteration_id)
            before = {item.id: (item.start_date, item.end_date, item.calculated_effort_days) for item in tasks}
            command = current_command(self.db)
            try:
                await self.schedule_iteration(
                    task.iteration_id,
                    commit=False,
                    expected_revision=command.iterations[task.iteration_id] if command is not None else None,
                    follow_date=today,
                    anchor_task_id=task.id if started else None,
                )
            except PlanningConflict as exc:
                for item in tasks:
                    item.start_date, item.end_date, item.calculated_effort_days = before[item.id]
                logger.warning("[SCHEDULER] Dates did not follow task %s: %s", task.id, exc)
                return []
            reason = f"Dates follow the actual {'start' if started else 'finish'} of '{task.title}'"
            for item in tasks:
                old_start, old_end, _ = before[item.id]
                if item.id == task.id or (item.start_date, item.end_date) == (old_start, old_end):
                    continue
                moved.append(item.id)
                await self.task_service.record_task_event(
                    item.id,
                    "task_schedule_applied",
                    {
                        "changes": {
                            "start_date": {"old": old_start.isoformat() if old_start else None,
                                           "new": item.start_date.isoformat() if item.start_date else None},
                            "end_date": {"old": old_end.isoformat() if old_end else None,
                                         "new": item.end_date.isoformat() if item.end_date else None},
                        },
                        "reason": reason,
                        "source_task_id": task.id,
                        "version": item.version,
                        "iteration_id": task.iteration_id,
                    },
                    actor_type="auto",
                )
            await self.db.flush()
        return moved

    @staticmethod
    def _date_rule_violation(task: Task, saved: tuple[date | None, date | None], iteration: Iteration) -> str | None:
        """The first rule the saved dates break for this iteration, or None when they are valid."""
        start, end = saved
        if start is None or end is None:
            return "dates_incomplete"
        if end < start:
            return "dates_inverted"
        if start < iteration.start_date or end > iteration.end_date:
            return "outside_iteration"
        if task.min_start_date is not None and start < task.min_start_date:
            return "before_min_start_date"
        return None

    def _date_rule_message(self, rule: str, task: Task, iteration_dates: tuple[date, date] | None = None) -> str:
        if rule == "outside_iteration" and iteration_dates is not None:
            return f"{self.DATE_RULE_MESSAGES[rule]} ({iteration_dates[0]} to {iteration_dates[1]})"
        if rule == "before_min_start_date" and task.min_start_date is not None:
            return f"{self.DATE_RULE_MESSAGES[rule]} ({task.min_start_date})"
        return self.DATE_RULE_MESSAGES[rule]

    def _unscheduled_tasks(
        self,
        all_tasks: Sequence[Task],
        member_schedules: dict[int, "MemberSchedule"],
        known_reasons: dict[int, str],
        messages: dict[int, str] | None = None,
        before_dates: dict[int, tuple[date | None, date | None]] | None = None,
        *,
        kept_dates: dict[int, str | None] | None = None,
        incomplete_ids: set[int] | None = None,
        postponed_waits: dict[int, list[Task]] | None = None,
        iteration_dates: tuple[date, date] | None = None,
        planning_start: date | None = None,
        satisfied_ids: set[int] | None = None,
    ) -> tuple[list[UnscheduledTask], list[KeptDatesTask]]:
        """Planned leaf tasks the run could not place, each with the first cause that applies.

        A task without dates goes to the first list; a task that keeps the dates it had goes to the second,
        with the rule those dates break when they break one.
        """
        from app.models.task import TaskStatus

        unscheduled: list[UnscheduledTask] = []
        kept_items: list[KeptDatesTask] = []
        kept_dates = kept_dates or {}
        incomplete_ids = incomplete_ids or set()
        postponed_waits = postponed_waits or {}
        by_id = {task.id: task for task in all_tasks}
        for task in all_tasks:
            if task.children or task.is_summary or task.canceled_at or task.status != TaskStatus.PLANNED.value:
                continue
            kept = task.id in kept_dates
            if not kept and task.start_date is not None and task.end_date is not None:
                continue
            if self._effective_flags(task)["effective_is_deferred"]:
                continue
            own_cause = None
            if not task.assignee_id:
                own_cause = "no_assignee"
            elif task.assignee_id not in member_schedules:
                own_cause = "assignee_not_in_iteration"
            waits = postponed_waits.get(task.id, [])
            if waits:
                # Waiting on postponed work comes first; every cause of its own is reported beside it.
                reason = "predecessor_postponed"
                message = self._postponed_wait_message(waits)
                also = [cause for cause in ("blocked" if task.blocked_reason else None, known_reasons.get(task.id), own_cause)
                        if cause is not None and cause != reason]
            else:
                if task.blocked_reason:
                    reason = "blocked"
                elif task.id in known_reasons:
                    reason = known_reasons[task.id]
                elif own_cause:
                    reason = own_cause
                else:
                    reason = "not_placed"
                message = (messages or {}).get(task.id, self.UNSCHEDULED_MESSAGES[reason])
                # A task waiting on a predecessor still has its own cause to fix afterwards.
                also = [own_cause] if own_cause and reason == "predecessor_unscheduled" else []
            if also:
                fixes = " ".join(self.UNSCHEDULED_MESSAGES[cause] for cause in also)
                message = f"{message} It also needs a fix of its own: {fixes}"
            waiting_on = [WaitingOnTask(task_id=item.id, task_title=item.title) for item in waits]
            if kept:
                rule = kept_dates[task.id]
                message = f"{message} Its saved dates {task.start_date} to {task.end_date} were kept."
                if rule is not None:
                    message = f"{message} They break rule {rule}: {self._date_rule_message(rule, task, iteration_dates)}."
                notes = self._kept_dates_notes(task, by_id, kept_dates, planning_start, satisfied_ids or set())
                if notes:
                    message = f"{message} {' '.join(notes)}"
                kept_items.append(KeptDatesTask(task_id=task.id, task_title=task.title, reason=reason, message=message,
                    start_date=task.start_date, end_date=task.end_date, date_rule=rule, also=also,
                    waiting_on=waiting_on))
                continue
            rule = "dates_incomplete" if task.id in incomplete_ids else None
            if rule is not None:
                saved = (before_dates or {}).get(task.id, (None, None))
                message = (f"{message} Its saved dates ({saved[0] or 'no start'} to {saved[1] or 'no end'}) were removed (rule {rule}): "
                           f"{self._date_rule_message(rule, task, iteration_dates)}.")
            had_dates = any(value is not None for value in (before_dates or {}).get(task.id, (None, None)))
            unscheduled.append(UnscheduledTask(task_id=task.id, task_title=task.title, reason=reason,
                message=message, dates_cleared=had_dates, date_rule=rule, also=also, waiting_on=waiting_on))
        return unscheduled, kept_items

    @staticmethod
    def _kept_dates_notes(
        task: Task,
        by_id: dict[int, Task],
        kept_dates: dict[int, str | None],
        planning_start: date | None,
        satisfied_ids: set[int],
    ) -> list[str]:
        """Limits of dates kept as saved: they were not checked against the plan the run placed."""
        notes = []
        if planning_start is not None and task.start_date is not None and task.start_date < planning_start:
            notes.append(f"They start before the planning start ({planning_start}).")
        for dependency in task.dependencies:
            predecessor = by_id.get(dependency.depends_on_id)
            # A postponed prerequisite's dates are history; the report already names it as the wait.
            if (predecessor is None or predecessor.id in satisfied_ids or predecessor.id in kept_dates
                    or predecessor.status == "postponed" or predecessor.end_date is None or task.start_date is None):
                continue
            if task.start_date <= predecessor.end_date:
                notes.append(f"They start on or before the end of its prerequisite '{predecessor.title}' "
                             f"({predecessor.end_date}).")
        return notes

    async def _build_member_schedules(
        self,
        iteration: Iteration,
        team_members: Sequence[TeamMember]
    ) -> dict[int, MemberSchedule]:
        """Build schedule tracking for each team member."""
        schedules = {}

        self._member_day_hours = {}
        from app.services.capacity_service import CapacityService
        from app.services.capacity_adjustments import load_dated_availability
        shared_capacity = CapacityService(self.db)
        self._dated_availability = dated = await load_dated_availability(self.db, [member.id for member in team_members])
        for member in team_members:
            coverage = await shared_capacity.coverage_for(member)
            calendar = coverage.primary
            self._member_day_hours[member.id] = calendar.nominal_day_hours
            working_dates = self.calendar_service.get_working_dates(coverage, iteration.start_date, iteration.end_date)
            vacation_dates = set()
            for start, end in await shared_capacity.absence_ranges(member):
                current = max(start, iteration.start_date)
                last = end
                while current <= last:
                    vacation_dates.add(current)
                    current += timedelta(days=1)

            # Calculate capacity
            capacity = await self.team_service.calculate_capacity(member.id)

            schedule = MemberSchedule(
                member_id=member.id,
                member_name=member.name,
                nominal_day_hours=calendar.nominal_day_hours,
                productivity_factor=member.availability_percent / 100 * (1 - member.operational_utilization / 100) * member.professionalism_coefficient,
                annual_calendars=coverage,
                capacity_days=capacity.adjusted_days if capacity else 0,
                working_dates=working_dates.copy(),
                vacation_dates=vacation_dates,
                dated_factors={
                    day: percent / 100 * (1 - member.operational_utilization / 100) * member.professionalism_coefficient
                    for day, percent in dated.adjusted_days(member)
                },
            )

            # Log available dates after excluding vacations
            available = schedule.get_available_dates()
            logger.warning(f"  - Available dates (after vacation exclusion): {len(available)}")

            schedules[member.id] = schedule

        return schedules

    def _topological_sort(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks respecting dependencies."""
        task_map = {t.id: t for t in tasks}
        visited = set()
        result = []

        def visit(task: Task):
            if task.id in visited:
                return
            visited.add(task.id)

            for dep in task.dependencies:
                if dep.depends_on_id in task_map:
                    visit(task_map[dep.depends_on_id])

            result.append(task)

        for task in tasks:
            visit(task)

        return result

    def _topological_sort_children(self, children: list[Task], child_ids: set[int]) -> list[Task]:
        """Sort child tasks respecting internal dependencies, then by (is_optional, priority).

        Only considers dependencies within the child set.
        """
        task_map = {t.id: t for t in children}
        visited = set()
        result = []

        # Sort by (is_optional, priority) first, then apply topological order
        priority_sorted = sorted(children, key=lambda c: (self._effective_flags(c)["effective_is_optional"], c.priority))

        def visit(task: Task):
            if task.id in visited:
                return
            visited.add(task.id)

            # Visit dependencies first (only those within this child set)
            for dep in task.dependencies:
                if dep.depends_on_id in child_ids and dep.depends_on_id in task_map:
                    visit(task_map[dep.depends_on_id])

            result.append(task)

        for task in priority_sorted:
            visit(task)

        return result

    def _get_dependency_depth(self, task: Task, all_tasks: Sequence[Task]) -> int:
        """Get the depth of a task in dependency chain."""
        task_map = {t.id: t for t in all_tasks}

        def get_depth(t: Task, visited: set) -> int:
            if t.id in visited:
                return 0
            visited.add(t.id)

            max_dep_depth = 0
            for dep in t.dependencies:
                if dep.depends_on_id in task_map:
                    dep_depth = get_depth(task_map[dep.depends_on_id], visited)
                    max_dep_depth = max(max_dep_depth, dep_depth + 1)

            return max_dep_depth

        return get_depth(task, set())

    def _calculate_adjusted_effort(self, task: Task) -> int:
        """Calculate adjusted effort days after applying assignee coefficients.

        Uses SchedulingRulesService if YAML config is available, otherwise
        falls back to hardcoded logic.

        Returns rounded number of working days after applying:
        - professionalism coefficient (higher = faster)
        - operational utilization (higher = longer)
        """
        coefficient = task.assignee.professionalism_coefficient if task.assignee else 1.0
        operational_util = task.assignee.operational_utilization if task.assignee else 0.0

        # Dated capacity adjustments are deliberately not applied here. This estimate has
        # no dates: it ranks work for the pass rules ("adjusted_effort") and sizes the
        # contiguous slot that find_uninterrupted_slot looks for. MemberSchedule.allocate
        # then places the task's effort hours with each date's own factor (dated_factors),
        # so forecast start and end dates honour every adjustment. A dated factor here would
        # need the start date being searched for and would reorder passes for adjusted rows.
        return self.rules_service.calculate_adjusted_effort(
            base_effort=(task.effort_hours / getattr(self, "_member_day_hours", {}).get(task.assignee_id, task.nominal_day_hours or 8))
                / (task.assignee.availability_percent / 100 if task.assignee and task.assignee.availability_percent else 1),
            professionalism_coefficient=coefficient,
            operational_utilization=operational_util,
        )

    def _build_task_context(
        self,
        task: Task,
        task_can_fit_before_vacation: dict[int, bool],
    ) -> dict:
        """Build task context dictionary for YAML pass filters and sorting.

        This context is used by scheduling_rules_service to evaluate
        filter conditions and sort criteria from YAML configuration.
        """
        return {
            "priority": task.priority,
            "is_optional": self._effective_flags(task)["effective_is_optional"],
            "is_deferred": self._effective_flags(task)["effective_is_deferred"],
            "adjusted_effort": self._calculate_adjusted_effort(task),
            "fits_before_vacation": task_can_fit_before_vacation.get(task.id, True),
            "max_finish_date": task.max_end_date,
            "min_start_date": task.min_start_date,
        }

    def _effective_flags(self, task):
        from app.services.work_metrics import effective_work_flags
        return getattr(self, "_work_flags", {}).get(task.id) or effective_work_flags(task)

    def _postponed_waits(self, all_tasks: Sequence[Task], task_map: dict[int, Task]) -> dict[int, list[Task]]:
        """Planned leaves that wait on postponed work, each with the postponed tasks it waits on."""
        from app.models.task import TaskStatus
        from app.services.work_metrics import postponed_work_under

        waits: dict[int, list[Task]] = {}
        for task in all_tasks:
            if (task.children or task.is_summary or task.canceled_at or task.status != TaskStatus.PLANNED.value
                    or self._effective_flags(task)["effective_is_deferred"]):
                continue
            found = {item.id: item for dep in task.dependencies if dep.depends_on_id in task_map
                     for item in postponed_work_under(task_map[dep.depends_on_id])}
            if found:
                waits[task.id] = [found[key] for key in sorted(found)]
        return waits

    @staticmethod
    def _postponed_wait_message(postponed: Sequence[Task]) -> str:
        names = ", ".join(f"'{item.title}' (ID {item.id})" for item in postponed)
        return (f"Waiting on postponed task {names}. Postponed work holds no schedule until it is reactivated; "
                "reactivate it or remove the dependency, then schedule again.")

    def _holds_no_schedule(self, task) -> bool:
        """Deferred work is backlog and postponed work is stopped: neither is placed nor occupies capacity."""
        from app.models.task import TaskStatus
        return task.status == TaskStatus.POSTPONED.value or self._effective_flags(task)["effective_is_deferred"]

    @staticmethod
    def _planning_start(iteration: Iteration) -> date:
        """Keep new forecasts on or after the workspace's current working date."""
        from app.services.work_metrics import working_today

        zone = iteration.project.timezone if iteration.project else iteration.calendar.timezone
        return max(iteration.start_date, working_today(zone))

    async def _schedule_leaf_task(
        self,
        task: Task,
        iteration: Iteration,
        member_schedules: dict[int, MemberSchedule],
        decisions: list[SchedulingDecision],
        task_map: dict[int, Task],
        earliest_start: Optional[date] = None
    ):
        """Schedule a leaf task (no children).

        Args:
            earliest_start: If provided, use this as the earliest start date.
                           If None, calculate from iteration start and dependencies.
        """
        # Skip deferred tasks - they are excluded from scheduling
        if self._effective_flags(task)["effective_is_deferred"]:
            return

        if not task.assignee_id or task.assignee_id not in member_schedules:
            # Unassigned task - skip
            return

        schedule = member_schedules[task.assignee_id]

        # Use provided earliest_start or calculate it
        if earliest_start is None:
            base_start = iteration.start_date
            earliest_start = self._get_earliest_start(task, base_start, task_map)

            # Apply task's min_start_date constraint if set
            task_min_start = task.min_start_date or iteration.start_date
            if task_min_start > earliest_start:
                earliest_start = task_min_start

        earliest_start = max(earliest_start, self._planning_start(iteration))

        # Calculate real duration - round UP to full days
        # Apply professionalism coefficient: higher coefficient = faster work = shorter duration
        # Apply operational utilization: higher util = more overhead = longer duration
        coefficient = task.assignee.professionalism_coefficient if task.assignee else 1.0
        operational_util = task.assignee.operational_utilization if task.assignee else 0.0

        effort_days = self._calculate_adjusted_effort(task)
        adjusted_effort = float(effort_days)

        # DEBUG LOGGING
        available_dates = schedule.get_available_dates()
        available_from_start = [d for d in available_dates if d >= earliest_start]
        logger.warning(f"[SCHEDULE] Task '{task.title}' (id={task.id})")
        logger.warning(f"  - effort_days (raw): {task.effort_days}, coefficient: {coefficient}, op_util: {operational_util}%")
        logger.warning(f"  - adjusted_effort: {adjusted_effort:.2f} -> effort_days (rounded): {effort_days}")
        logger.warning(f"  - earliest_start: {earliest_start}")
        logger.warning(f"  - already allocated dates: {len(schedule.allocated_dates)}")
        if schedule.allocated_dates:
            allocated_list = sorted(schedule.allocated_dates.keys())[:10]
            logger.warning(f"  - first 10 allocated: {[d.isoformat() for d in allocated_list]}")
        logger.warning(f"  - available_dates total: {len(available_dates)}, from start: {len(available_from_start)}")

        # Find uninterrupted slot
        slot_start = schedule.find_uninterrupted_slot(earliest_start, effort_days)

        decision_type = "scheduled"
        reason = f"Scheduled from {earliest_start}"
        affected_tasks = []

        if slot_start and slot_start > earliest_start:
            decision_type = "delayed"
            reason = f"Delayed to {slot_start} to ensure uninterrupted execution (original: {earliest_start})"

        if slot_start:
            start_date, end_date = schedule.allocate(
                slot_start, effort_days, task.id, accounting_days=task.effort_days, required_hours=task.effort_hours
            )
            task.start_date = start_date
            task.end_date = end_date
            task.calculated_effort_days = float(sum(owner == task.id for owner in schedule.allocated_dates.values()))
            logger.warning(f"  - ALLOCATED: {start_date} to {end_date} ({(end_date - start_date).days + 1} calendar days)")

            # Check if overdue
            if end_date > iteration.end_date:
                decision_type = "overdue"
                reason = f"Task extends beyond iteration by {(end_date - iteration.end_date).days} days"
        else:
            task.start_date, task.end_date = schedule.allocate(earliest_start, effort_days, task.id,
                accounting_days=task.effort_days, required_hours=task.effort_hours)
            task.calculated_effort_days = float(sum(owner == task.id for owner in schedule.allocated_dates.values()))
            decision_type = "overdue"
            reason = "The forecast extends beyond the available iteration slots"

        decisions.append(SchedulingDecision(
            task_id=task.id,
            task_title=task.title,
            decision_type=decision_type,
            reason=reason,
            affected_tasks=affected_tasks,
        ))

    async def _schedule_composite_task(
        self,
        task: Task,
        iteration: Iteration,
        member_schedules: dict[int, MemberSchedule],
        decisions: list[SchedulingDecision],
        task_map: dict[int, Task],
        parent_earliest_start: Optional[date] = None
    ):
        """Schedule a composite task (with children)."""
        # Calculate earliest start for this composite task based on its own dependencies
        # AND any constraint from parent composite tasks
        base_start = parent_earliest_start if parent_earliest_start else iteration.start_date
        earliest_start = self._get_earliest_start(task, base_start, task_map)

        # Schedule all children, respecting parent's earliest_start constraint
        # First topological sort to respect dependencies, then prioritize by (is_optional, priority)
        child_ids = {c.id for c in task.children}
        sorted_children = self._topological_sort_children(task.children, child_ids)

        for child in sorted_children:
            if self._holds_no_schedule(child):
                continue  # Skip deferred and postponed tasks
            if child.children:
                await self._schedule_composite_task(
                    child, iteration, member_schedules, decisions, task_map, earliest_start
                )
            else:
                await self._schedule_leaf_task(
                    child, iteration, member_schedules, decisions, task_map, earliest_start
                )

        # Compute parent dates from children (excluding deferred and postponed tasks)
        children_with_dates = [c for c in task.children if c.start_date and c.end_date and not self._holds_no_schedule(c)]

        if children_with_dates:
            child_start_dates = [
                c.start_date for c in children_with_dates if c.start_date is not None
            ]
            child_end_dates = [
                c.end_date for c in children_with_dates if c.end_date is not None
            ]
            parent_start_date = min(child_start_dates)
            parent_end_date = max(child_end_dates)
            task.start_date = parent_start_date
            task.end_date = parent_end_date

            is_overdue = parent_end_date > iteration.end_date

            decisions.append(SchedulingDecision(
                task_id=task.id,
                task_title=task.title,
                decision_type="overdue" if is_overdue else "scheduled",
                reason=f"Composite task: {parent_start_date} - {parent_end_date} (from {len(children_with_dates)} subtasks)",
                affected_tasks=[c.id for c in children_with_dates],
            ))

    def _get_earliest_start(self, task: Task, iteration_start: date, task_map: dict[int, Task]) -> date:
        """Get earliest possible start date based on dependencies."""
        earliest = iteration_start

        for dep in task.dependencies:
            # Use task_map to get the actual scheduled task object (with updated end_date)
            dep_task = task_map.get(dep.depends_on_id)
            if dep_task and dep_task.end_date:
                dep_end = dep_task.end_date + timedelta(days=1)
                if dep_end > earliest:
                    earliest = dep_end

        return earliest

    def _update_composite_task_dates(
        self,
        task: Task,
        iteration: Iteration,
        decisions: list[SchedulingDecision]
    ):
        """Update a composite task's dates based on its children."""
        # Recursively update nested composites first
        for child in task.children:
            if child.children:
                self._update_composite_task_dates(child, iteration, decisions)

        # Compute dates from children (excluding deferred and postponed tasks)
        children_with_dates = [c for c in task.children if c.start_date and c.end_date and not self._holds_no_schedule(c)]

        if children_with_dates:
            child_start_dates = [
                c.start_date for c in children_with_dates if c.start_date is not None
            ]
            child_end_dates = [
                c.end_date for c in children_with_dates if c.end_date is not None
            ]
            parent_start_date = min(child_start_dates)
            parent_end_date = max(child_end_dates)
            task.start_date = parent_start_date
            task.end_date = parent_end_date

            is_overdue = parent_end_date > iteration.end_date

            decisions.append(SchedulingDecision(
                task_id=task.id,
                task_title=task.title,
                decision_type="overdue" if is_overdue else "scheduled",
                reason=f"Composite task: {parent_start_date} - {parent_end_date} (from {len(children_with_dates)} subtasks)",
                affected_tasks=[c.id for c in children_with_dates],
            ))

    def _check_workload_balance(
        self,
        member_schedules: dict[int, MemberSchedule]
    ) -> list[WorkloadIssue]:
        """Check for workload imbalances.

        Both sides of the comparison are in standard effort-days:
        ``allocated_days`` accumulates raw task effort and ``capacity_days``
        is MemberCapacity.adjusted_days (coefficient-adjusted delivery capacity).
        """
        issues = []

        for schedule in member_schedules.values():
            if schedule.capacity_days > 0:
                overload = schedule.allocated_days - schedule.capacity_days
                overload_percent = (overload / schedule.capacity_days) * 100

                if overload_percent >= 5:
                    issues.append(WorkloadIssue(
                        member_id=schedule.member_id,
                        member_name=schedule.member_name,
                        issue=f"Overloaded by {overload:.1f} days ({overload_percent:.0f}%)"
                    ))

        return issues


class IncrementalScheduler:
    """Handles incremental rescheduling when a single task changes.

    Instead of rescheduling the entire iteration (O(N)), this scheduler:
    1. Detects what changed on a task
    2. Identifies only the affected tasks (dependents, same-assignee tasks)
    3. Reschedules only the affected subset (O(A) where A << N)

    Performance: O(A) instead of O(N), typically 10x faster for single-task changes.
    """

    def __init__(self, scheduler_service: SchedulerService):
        self.scheduler = scheduler_service
        self.db = scheduler_service.db
        self.task_service = scheduler_service.task_service

    async def reschedule_affected(
        self,
        change: TaskChange,
    ) -> RescheduleResult:
        """Reschedule only tasks affected by the change.

        Args:
            change: Describes what changed on a task

        Returns:
            RescheduleResult with affected task IDs and rescheduling decisions
        """
        # Find affected tasks
        affected_task_ids = await self._find_affected_tasks(change)

        if not affected_task_ids:
            return RescheduleResult(
                affected_task_ids=[],
                rescheduled_count=0,
                decisions=[],
            )

        logger.warning(f"[INCREMENTAL] Found {len(affected_task_ids)} affected tasks for change: {change.change_type.value}")

        # Reschedule affected subset
        result = await self._reschedule_subset(change.iteration_id, affected_task_ids)

        return result

    async def _find_affected_tasks(self, change: TaskChange) -> set[int]:
        """Find all tasks affected by the change.

        Different change types affect different sets of tasks:
        - Effort increased: task + all dependents (recursive)
        - Effort decreased: all same-assignee tasks (can shift left)
        - Assignee changed: both old and new assignee's tasks
        - Priority changed: all same-assignee tasks (reordering)
        - Dependency added/removed: task + all dependents
        """
        affected = {change.task_id}

        match change.change_type:
            case ChangeType.EFFORT_INCREASED:
                # Task took longer → dependents shift right
                dependents = await self._find_all_dependents(change.task_id)
                affected |= dependents

            case ChangeType.EFFORT_DECREASED:
                # Task shortened → same assignee tasks may shift left
                if change.assignee_id:
                    assignee_tasks = await self._find_assignee_tasks(
                        change.iteration_id, change.assignee_id
                    )
                    affected |= assignee_tasks

            case ChangeType.ASSIGNEE_CHANGED:
                # Both old and new assignee's tasks need rebalancing
                if change.old_value:
                    old_tasks = await self._find_assignee_tasks(
                        change.iteration_id, change.old_value
                    )
                    affected |= old_tasks
                if change.new_value:
                    new_tasks = await self._find_assignee_tasks(
                        change.iteration_id, change.new_value
                    )
                    affected |= new_tasks

            case ChangeType.PRIORITY_CHANGED:
                # Priority changed → reorder same assignee's queue
                if change.assignee_id:
                    assignee_tasks = await self._find_assignee_tasks(
                        change.iteration_id, change.assignee_id
                    )
                    affected |= assignee_tasks

            case ChangeType.DEPENDENCY_ADDED | ChangeType.DEPENDENCY_REMOVED:
                # Dependency changed → task may shift + all dependents
                dependents = await self._find_all_dependents(change.task_id)
                affected |= dependents

            case ChangeType.MIN_START_DATE_CHANGED | ChangeType.MAX_END_DATE_CHANGED:
                # Constraint changed → task + dependents
                dependents = await self._find_all_dependents(change.task_id)
                affected |= dependents

            case ChangeType.STATUS_CHANGED:
                # Status changed (e.g., to ACTIVE) → dependents may shift
                dependents = await self._find_all_dependents(change.task_id)
                affected |= dependents

        return affected

    async def _find_all_dependents(self, task_id: int) -> set[int]:
        """Find all tasks that depend on this task (recursive BFS).

        Uses BFS to avoid deep recursion and handles cycles.
        """
        result: set[int] = set()
        queue = [task_id]
        visited: set[int] = set()

        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue
            visited.add(current_id)

            # Find direct dependents (tasks that depend on current)
            stmt = select(TaskDependency.task_id).where(
                TaskDependency.depends_on_id == current_id
            )
            execution_result = await self.db.execute(stmt)
            dependent_ids = [row[0] for row in execution_result.fetchall()]

            for dep_id in dependent_ids:
                if dep_id not in result:
                    result.add(dep_id)
                    queue.append(dep_id)

        return result

    async def _find_assignee_tasks(
        self, iteration_id: int, assignee_id: int
    ) -> set[int]:
        """Find all tasks assigned to a specific person in the iteration."""
        stmt = select(Task.id).where(
            Task.iteration_id == iteration_id,
            Task.assignee_id == assignee_id,
            Task.status == TaskStatus.PLANNED.value,
        )
        result = await self.db.execute(stmt)
        return {row[0] for row in result.fetchall()}

    async def _reschedule_subset(
        self,
        iteration_id: int,
        affected_task_ids: set[int],
    ) -> RescheduleResult:
        """Reschedule only the affected tasks.

        Loads the affected tasks, clears their dates, and uses the
        existing parallel scheduler to reschedule them.
        """
        from app.services.iteration_service import IterationService

        # Load iteration
        iteration_service = IterationService(self.db)
        iteration = await iteration_service.get_by_id(iteration_id)
        if not iteration:
            return RescheduleResult(
                affected_task_ids=list(affected_task_ids),
                rescheduled_count=0,
                decisions=[],
            )

        all_tasks = await self.task_service.get_all_tasks(iteration_id)
        task_map = {task.id: task for task in all_tasks}
        from app.services.work_metrics import effective_work_flags
        self.scheduler._work_flags = {task.id: effective_work_flags(task, by_id=task_map) for task in all_tasks}

        # Load affected tasks
        tasks: list[Task] = []
        for task_id in affected_task_ids:
            task = await self.task_service.get_by_id(task_id)
            if task and task.status == TaskStatus.PLANNED.value and not self.scheduler._effective_flags(task)["effective_is_deferred"]:
                task.start_date = None
                task.end_date = None
                tasks.append(task)

        if not tasks:
            return RescheduleResult(
                affected_task_ids=list(affected_task_ids),
                rescheduled_count=0,
                decisions=[],
            )

        # Get team members for the iteration
        team_members = await self.scheduler.team_service.get_by_iteration(iteration_id)

        # Build member schedules
        member_schedules = await self.scheduler._build_member_schedules(
            iteration, team_members
        )

        # Track existing allocations for non-affected tasks
        for existing_task in all_tasks:
            if existing_task.id not in affected_task_ids and existing_task.start_date and not self.scheduler._holds_no_schedule(existing_task):
                if existing_task.assignee_id and existing_task.assignee_id in member_schedules:
                    schedule = member_schedules[existing_task.assignee_id]
                    if existing_task.end_date:
                        for d in schedule.working_dates:
                            if existing_task.start_date <= d <= existing_task.end_date:
                                if d not in schedule.vacation_dates:
                                    schedule.allocated_dates[d] = existing_task.id
                        schedule._invalidate_cache()

        decisions: list[SchedulingDecision] = []

        # Schedule each affected task
        for task in tasks:
            earliest_start = iteration.start_date
            if task.min_start_date and task.min_start_date > earliest_start:
                earliest_start = task.min_start_date

            for dep in task.dependencies:
                dep_task = task_map.get(dep.depends_on_id)
                if dep_task and dep_task.end_date:
                    dep_end = dep_task.end_date + timedelta(days=1)
                    if dep_end > earliest_start:
                        earliest_start = dep_end

            await self.scheduler._schedule_leaf_task(
                task, iteration, member_schedules, decisions, task_map, earliest_start
            )

        await commit_or_flush(self.db)

        logger.warning(f"[INCREMENTAL] Rescheduled {len(tasks)} tasks")

        return RescheduleResult(
            affected_task_ids=list(affected_task_ids),
            rescheduled_count=len(tasks),
            decisions=decisions,
        )

    @staticmethod
    def detect_changes(
        old_task: Task,
        new_effort: Optional[int] = None,
        new_assignee_id: Optional[int] = None,
        new_priority: Optional[int] = None,
        new_min_start_date: Optional[date] = None,
        new_max_end_date: Optional[date] = None,
    ) -> list[TaskChange]:
        """Detect what changed between old task state and new values."""
        changes: list[TaskChange] = []

        if new_effort is not None and new_effort != old_task.effort_days:
            change_type = (
                ChangeType.EFFORT_INCREASED if old_task.effort_days is None or new_effort > old_task.effort_days
                else ChangeType.EFFORT_DECREASED
            )
            changes.append(TaskChange(
                task_id=old_task.id,
                iteration_id=old_task.iteration_id,
                change_type=change_type,
                old_value=old_task.effort_days,
                new_value=new_effort,
                assignee_id=old_task.assignee_id,
            ))

        if new_assignee_id is not None and new_assignee_id != old_task.assignee_id:
            changes.append(TaskChange(
                task_id=old_task.id,
                iteration_id=old_task.iteration_id,
                change_type=ChangeType.ASSIGNEE_CHANGED,
                old_value=old_task.assignee_id,
                new_value=new_assignee_id,
            ))

        if new_priority is not None and new_priority != old_task.priority:
            changes.append(TaskChange(
                task_id=old_task.id,
                iteration_id=old_task.iteration_id,
                change_type=ChangeType.PRIORITY_CHANGED,
                old_value=old_task.priority,
                new_value=new_priority,
                assignee_id=old_task.assignee_id,
            ))

        if new_min_start_date is not None and new_min_start_date != old_task.min_start_date:
            changes.append(TaskChange(
                task_id=old_task.id,
                iteration_id=old_task.iteration_id,
                change_type=ChangeType.MIN_START_DATE_CHANGED,
                old_value=old_task.min_start_date,
                new_value=new_min_start_date,
                assignee_id=old_task.assignee_id,
            ))

        if new_max_end_date is not None and new_max_end_date != old_task.max_end_date:
            changes.append(TaskChange(
                task_id=old_task.id,
                iteration_id=old_task.iteration_id,
                change_type=ChangeType.MAX_END_DATE_CHANGED,
                old_value=old_task.max_end_date,
                new_value=new_max_end_date,
                assignee_id=old_task.assignee_id,
            ))

        return changes
