"""Gantt Scheduler Service - automatic task scheduling with optimization."""
import math
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
from app.services.task_service import TaskService
from app.services.team_service import TeamService
from app.services.scheduling_rules_service import SchedulingRulesService
from app.schemas.gantt import SchedulingDecision, ScheduleResult, WorkloadIssue


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
        return (
            day.weekday() not in self.weekend_days
            and day not in self.holiday_dates
            and day not in self.vacation_dates
        )

    def allocate(
        self,
        start_date: date,
        effort_days: int,
        task_id: int,
        accounting_days: Optional[float] = None,
    ) -> tuple[date, date]:
        """Allocate dates for a task, returns (start, end).

        The end_date is calculated as the actual calendar date when the task
        completes, accounting for weekends/holidays that the task spans.
        If not enough working days are available, the task extends beyond
        the available period with the correct calendar duration.

        ``accounting_days`` is the task's raw effort in standard effort-days,
        recorded for workload reporting. It defaults to ``effort_days`` (the
        coefficient-inflated calendar demand) when not provided.

        IMPORTANT: Invalidates the available dates cache after allocation.
        """
        if accounting_days is None:
            accounting_days = float(effort_days)

        available = [d for d in self.get_available_dates() if d >= start_date]

        if len(available) < effort_days:
            # Not enough available working days within the iteration period
            # Allocate what we can within the iteration
            allocated_count = len(available)
            for d in available:
                self.allocated_dates[d] = task_id
            # The member owns the whole task even when it overflows the
            # iteration, so account its full effort for workload reporting.
            self.allocated_days += accounting_days
            self._invalidate_cache()  # Cache invalidation

            if available:
                remaining_working_days = effort_days - allocated_count
                last_available = available[-1]

                if remaining_working_days > 0:
                    # Calculate end_date by finding actual working days after last available
                    # Skip calendar-configured weekends/holidays and vacations
                    current = last_available
                    working_days_found = 0
                    while working_days_found < remaining_working_days:
                        current = current + timedelta(days=1)
                        if self._is_projectable_working_day(current):
                            working_days_found += 1
                    end_date = current
                else:
                    # All days fit within available - use last available as end
                    end_date = last_available

                logger.warning(f"  - Overflow allocation: {allocated_count} available + {remaining_working_days} remaining = end {end_date}")
                return (available[0], end_date)

            # No available days at all - find working days from start_date
            current = start_date
            working_days_found = 0
            while working_days_found < effort_days:
                if self._is_projectable_working_day(current):
                    working_days_found += 1
                    if working_days_found == effort_days:
                        break
                current = current + timedelta(days=1)
            return (start_date, current)

        # Allocate exactly effort_days working days
        allocated = []
        for d in available:
            if len(allocated) >= effort_days:
                break
            self.allocated_dates[d] = task_id
            allocated.append(d)

        self.allocated_days += accounting_days
        self._invalidate_cache()  # Cache invalidation

        if allocated:
            # end_date is the last working day allocated
            logger.warning(f"  - Allocated {len(allocated)} working days: {allocated[0]} to {allocated[-1]}")
            return (allocated[0], allocated[-1])
        return (start_date, start_date)


class SchedulerService:
    """Service for automatic task scheduling."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.calendar_service = CalendarService(db)
        self.task_service = TaskService(db)
        self.team_service = TeamService(db)
        self.rules_service = SchedulingRulesService.get_instance()

    async def schedule_iteration(
        self,
        iteration_id: int,
        *,
        commit: bool = True,
    ) -> ScheduleResult:
        """Schedule an iteration, optionally leaving commit ownership to the caller."""
        from app.services.iteration_service import IterationService

        iteration_service = IterationService(self.db)
        iteration = await iteration_service.get_by_id(iteration_id)

        if not iteration:
            return ScheduleResult(success=False, decisions=[])

        # Get all data
        all_tasks = await self.task_service.get_all_tasks(iteration_id)
        team_members = await self.team_service.get_by_iteration(iteration_id)

        # Build member schedules
        member_schedules = await self._build_member_schedules(
            iteration, team_members
        )

        decisions: list[SchedulingDecision] = []

        # Build task map for dependency lookup during scheduling
        task_map = {t.id: t for t in all_tasks}

        # Collect all leaf tasks (tasks without children) that need scheduling
        # IMPORTANT: Only schedule tasks with PLANNED status
        # Tasks in other statuses (ACTIVE, RESOLVED, CLOSED) already have actual dates
        # that should not be modified by auto-scheduling
        from app.models.task import TaskStatus

        all_leaf_tasks = [t for t in all_tasks if not t.children and not t.is_deferred]

        # Split into schedulable (PLANNED) and locked (non-PLANNED) tasks
        leaf_tasks = [t for t in all_leaf_tasks if t.status == TaskStatus.PLANNED.value]
        locked_tasks = [t for t in all_leaf_tasks if t.status != TaskStatus.PLANNED.value]

        logger.warning(f"[SCHEDULER] Task status filter: {len(leaf_tasks)} PLANNED (to schedule), {len(locked_tasks)} non-PLANNED (dates locked)")

        # IMPORTANT: Only clear dates for PLANNED tasks
        # Non-PLANNED tasks keep their dates as they are already "locked in"
        for task in leaf_tasks:
            task.start_date = None
            task.end_date = None

        # Calculate earliest_start for each leaf task
        def get_task_earliest_start(task: Task) -> date:
            """Get earliest possible start date for a task."""
            # Start with iteration start
            base = iteration.start_date

            # Apply min_start_date constraint
            if task.min_start_date and task.min_start_date > base:
                base = task.min_start_date

            # Check dependencies
            for dep in task.dependencies:
                dep_task = task_map.get(dep.depends_on_id)
                if dep_task and dep_task.end_date:
                    dep_end = dep_task.end_date + timedelta(days=1)
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

        for assignee_id, assignee_tasks in tasks_by_assignee.items():
            available_days = assignee_days_before_vacation.get(assignee_id, 0)

            # Sort by priority (lower = higher priority), then by effort (smaller first)
            sorted_tasks = sorted(assignee_tasks, key=lambda t: (t.is_optional, t.priority, self._calculate_adjusted_effort(t)))

            remaining_days = available_days
            for task in sorted_tasks:
                effort = self._calculate_adjusted_effort(task)
                if remaining_days >= effort:
                    task_can_fit_before_vacation[task.id] = True
                    remaining_days -= effort
                else:
                    task_can_fit_before_vacation[task.id] = False

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
            effort = self._calculate_adjusted_effort(task)

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
            return (vacation_priority, task.is_optional, task.priority, size_order)

        def topological_sort_with_dependencies(
            tasks_with_start: list[tuple[Task, date]],
            sort_key_fn
        ) -> list[tuple[Task, date]]:
            """Reorder tasks to ensure dependencies are scheduled before dependents."""
            if not tasks_with_start:
                return []

            task_ids = {t.id for t, _ in tasks_with_start}
            task_map_local = {t.id: (t, es) for t, es in tasks_with_start}

            # Build dependency graph (only for dependencies within this task set)
            in_degree: dict[int, int] = {t.id: 0 for t, _ in tasks_with_start}
            dependents: dict[int, list[int]] = {t.id: [] for t, _ in tasks_with_start}

            for task, _ in tasks_with_start:
                for dep in task.dependencies:
                    if dep.depends_on_id in task_ids:
                        in_degree[task.id] += 1
                        dependents[dep.depends_on_id].append(task.id)

            # Kahn's algorithm for topological sort
            # Start with tasks that have no dependencies (in_degree == 0)
            result = []
            no_deps = [tid for tid in in_degree if in_degree[tid] == 0]

            # Sort no_deps by provided sort key function
            no_deps.sort(key=lambda tid: sort_key_fn(task_map_local[tid]))

            while no_deps:
                # Take the first task (respecting original sort order)
                tid = no_deps.pop(0)
                result.append(task_map_local[tid])

                # Process dependents
                for dep_tid in dependents[tid]:
                    in_degree[dep_tid] -= 1
                    if in_degree[dep_tid] == 0:
                        no_deps.append(dep_tid)
                        # Re-sort to maintain order
                        no_deps.sort(key=lambda x: sort_key_fn(task_map_local[x]))

            # If we didn't process all tasks, there's a cycle - fall back to original order
            if len(result) != len(tasks_with_start):
                logger.warning("[SCHEDULER] Warning: Dependency cycle detected, using original order")
                return tasks_with_start

            return result

        # Track latest end_date per assignee for sequential scheduling
        assignee_last_end: dict[int, date] = {}
        scheduled_task_ids: set[int] = set()

        # Thread-safe lock for scheduled_task_ids (used in parallel mode)
        import asyncio
        scheduling_lock = asyncio.Lock()

        async def schedule_single_task(task: Task) -> None:
            """Schedule a single task with proper locking for parallel execution."""
            nonlocal assignee_last_end

            async with scheduling_lock:
                if task.id in scheduled_task_ids:
                    return

                # Re-calculate earliest_start (dependencies may have been scheduled)
                earliest_start = get_task_earliest_start(task)

                # Ensure sequential scheduling: new task starts after previous task for same assignee
                if task.assignee_id and task.assignee_id in assignee_last_end:
                    prev_end = assignee_last_end[task.assignee_id]
                    schedule = member_schedules.get(task.assignee_id)
                    if schedule:
                        next_available = schedule.find_next_available_date(prev_end + timedelta(days=1))
                        if next_available and next_available > earliest_start:
                            earliest_start = next_available
                            logger.warning(f"  [SEQUENTIAL] Task '{task.title}' starts {earliest_start} (after previous task end: {prev_end})")

            # Schedule outside lock (I/O operations)
            await self._schedule_leaf_task(
                task, iteration, member_schedules, decisions, task_map, earliest_start
            )

            async with scheduling_lock:
                scheduled_task_ids.add(task.id)

                # Update assignee's last end date
                if task.assignee_id and task.end_date and task.start_date:
                    if task.start_date <= iteration.end_date:
                        current_last = assignee_last_end.get(task.assignee_id)
                        if current_last is None or task.end_date > current_last:
                            assignee_last_end[task.assignee_id] = task.end_date

        async def schedule_task_list(tasks_with_start: list[tuple[Task, date]]) -> None:
            """Schedule a list of tasks in order (sequential per-assignee)."""
            for task, _ in tasks_with_start:
                await schedule_single_task(task)

        async def schedule_assignee_tasks(
            assignee_id: int,
            tasks: list[Task],
            sort_key_fn,
        ) -> None:
            """Schedule all tasks for a single assignee in priority order."""
            tasks_with_start = [(t, get_task_earliest_start(t)) for t in tasks]
            tasks_with_start.sort(key=sort_key_fn)

            # Apply topological sort for intra-assignee dependencies
            tasks_with_start = topological_sort_with_dependencies(tasks_with_start, sort_key_fn)

            for task, _ in tasks_with_start:
                await schedule_single_task(task)

        async def schedule_parallel_by_assignee(
            tasks: list[Task],
            sort_key_fn,
        ) -> None:
            """Schedule tasks using parallel processing where safe.

            Strategy:
            1. Build cross-assignee dependency graph
            2. Schedule independent assignees in parallel
            3. Schedule dependent assignees level-by-level (parallel within level)
            """
            # Build assignee dependency graph
            assignee_deps, independent_assignees = self._build_assignee_dependency_graph(tasks)

            # Group tasks by assignee
            from collections import defaultdict
            tasks_by_assignee_local: dict[int, list[Task]] = defaultdict(list)
            unassigned_tasks: list[Task] = []

            for task in tasks:
                if task.assignee_id:
                    tasks_by_assignee_local[task.assignee_id].append(task)
                else:
                    unassigned_tasks.append(task)

            # Step 1: Schedule independent assignees in parallel
            if independent_assignees:
                logger.warning(f"[PARALLEL] Scheduling {len(independent_assignees)} independent assignees in parallel")
                await asyncio.gather(*[
                    schedule_assignee_tasks(aid, tasks_by_assignee_local[aid], sort_key_fn)
                    for aid in independent_assignees
                    if aid in tasks_by_assignee_local
                ])

            # Step 2: Schedule dependent assignees level by level
            levels = self._topological_sort_assignees(assignee_deps)
            for level_idx, level in enumerate(levels):
                logger.warning(f"[PARALLEL] Scheduling level {level_idx}: {len(level)} assignees in parallel")
                await asyncio.gather(*[
                    schedule_assignee_tasks(aid, tasks_by_assignee_local[aid], sort_key_fn)
                    for aid in level
                    if aid in tasks_by_assignee_local
                ])

            # Step 3: Schedule unassigned tasks sequentially
            if unassigned_tasks:
                logger.warning(f"[PARALLEL] Scheduling {len(unassigned_tasks)} unassigned tasks sequentially")
                await schedule_task_list([(t, get_task_earliest_start(t)) for t in unassigned_tasks])

        # Get scheduling passes from YAML configuration
        scheduling_passes = self.rules_service.get_scheduling_passes()

        if scheduling_passes:
            # ═══ USE YAML-BASED MULTI-PASS SCHEDULING (with parallel optimization) ═══
            logger.warning(f"[SCHEDULER] Using {len(scheduling_passes)} passes from YAML configuration:")
            for sp in scheduling_passes:
                logger.warning(f"  - {sp.id}: {sp.description}")

            for pass_config in scheduling_passes:
                # Filter tasks that match this pass and haven't been scheduled yet
                matching_tasks = []
                for task in leaf_tasks:
                    if task.id in scheduled_task_ids:
                        continue
                    ctx = self._build_task_context(task, task_can_fit_before_vacation)
                    if self.rules_service.matches_pass_filter(pass_config.id, ctx):
                        matching_tasks.append(task)

                if not matching_tasks:
                    logger.warning(f"[SCHEDULER] Pass '{pass_config.id}': no matching tasks")
                    continue

                # Sort by criteria from YAML
                def make_sort_key(pass_id: str):
                    def sort_key(task_with_start: tuple[Task, date]) -> tuple:
                        task, _ = task_with_start
                        key_fn = self.rules_service.get_sort_key_function(
                            pass_id,
                            lambda t: self._build_task_context(t, task_can_fit_before_vacation)
                        )
                        return key_fn(task)
                    return sort_key

                sort_key_fn = make_sort_key(pass_config.id)

                logger.warning(f"[SCHEDULER] Pass '{pass_config.id}': scheduling {len(matching_tasks)} tasks (parallel mode)")

                # Use parallel scheduling for this pass
                await schedule_parallel_by_assignee(matching_tasks, sort_key_fn)

            # Schedule any remaining unscheduled tasks with fallback logic (parallel mode)
            remaining_tasks = [t for t in leaf_tasks if t.id not in scheduled_task_ids]
            if remaining_tasks:
                logger.warning(f"[SCHEDULER] Fallback pass: scheduling {len(remaining_tasks)} remaining tasks (parallel mode)")
                await schedule_parallel_by_assignee(remaining_tasks, get_fallback_sort_key)
        else:
            # ═══ FALLBACK: USE PARALLEL VACATION-AWARE SCHEDULING ═══
            logger.warning("[SCHEDULER] No YAML passes found, using parallel vacation-aware scheduling")

            logger.warning(f"[SCHEDULER] Scheduling {len(leaf_tasks)} leaf tasks (parallel mode):")
            for t in leaf_tasks[:10]:  # Log first 10 only
                effort = self._calculate_adjusted_effort(t)
                can_fit = task_can_fit_before_vacation.get(t.id, True)
                logger.warning(f"  - {t.title} (id={t.id}): effort={effort}, priority={t.priority}, can_fit={can_fit}")
            if len(leaf_tasks) > 10:
                logger.warning(f"  ... and {len(leaf_tasks) - 10} more tasks")

            await schedule_parallel_by_assignee(leaf_tasks, get_fallback_sort_key)

        # Update composite (parent) task dates based on their children
        composite_tasks = [t for t in all_tasks if t.children]
        for parent in composite_tasks:
            self._update_composite_task_dates(parent, iteration, decisions)

        # Agent command adapters need the schedule and their exact receipt to
        # share one transaction. Existing callers retain commit-by-default.
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()

        # Check workload balance
        workload_issues = self._check_workload_balance(member_schedules)

        return ScheduleResult(
            success=True,
            decisions=decisions,
            workload_balanced=len(workload_issues) == 0,
            workload_issues=workload_issues,
        )

    async def _build_member_schedules(
        self,
        iteration: Iteration,
        team_members: Sequence[TeamMember]
    ) -> dict[int, MemberSchedule]:
        """Build schedule tracking for each team member."""
        schedules = {}

        working_dates = self.calendar_service.get_working_dates(
            iteration.calendar, iteration.start_date, iteration.end_date
        )

        # Extract all holiday dates from the calendar (not just the iteration
        # window) so overflow projections beyond the iteration end can skip
        # them the same way in-iteration scheduling does.
        holiday_dates = set()
        if iteration.calendar and iteration.calendar.holidays:
            for holiday_str in iteration.calendar.holidays:
                try:
                    holiday_dates.add(date.fromisoformat(holiday_str))
                except ValueError:
                    logger.warning(
                        "Ignoring invalid calendar holiday value",
                        exc_info=True,
                        extra={"holiday_value": holiday_str, "iteration_id": iteration.id},
                    )

        weekend_days = (
            set(iteration.calendar.weekend_days)
            if iteration.calendar and iteration.calendar.weekend_days is not None
            else {5, 6}
        )

        logger.warning(f"[BUILD_SCHEDULES] Total working dates in iteration: {len(working_dates)}")
        logger.warning(f"[BUILD_SCHEDULES] Calendar holiday dates: {[d.isoformat() for d in sorted(holiday_dates)]}")

        for member in team_members:
            # Get vacation dates
            vacation_dates = set()
            logger.warning(f"[BUILD_SCHEDULES] Member '{member.name}' has {len(member.vacations)} vacations")
            for vacation in member.vacations:
                logger.warning(f"  - Vacation: {vacation.start_date} to {vacation.end_date}")
                current = vacation.start_date
                while current <= vacation.end_date:
                    vacation_dates.add(current)
                    current += timedelta(days=1)

            logger.warning(f"  - Total vacation dates: {len(vacation_dates)}")

            # Calculate capacity
            capacity = await self.team_service.calculate_capacity(member.id)

            schedule = MemberSchedule(
                member_id=member.id,
                member_name=member.name,
                capacity_days=capacity.adjusted_days if capacity else 0,
                working_dates=working_dates.copy(),
                vacation_dates=vacation_dates,
                holiday_dates=holiday_dates,  # Used by overflow projection beyond the iteration
                weekend_days=weekend_days,
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
        priority_sorted = sorted(children, key=lambda c: (c.is_optional, c.priority))

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

        return self.rules_service.calculate_adjusted_effort(
            base_effort=task.effort_days,
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
            "is_optional": task.is_optional,
            "is_deferred": task.is_deferred,
            "adjusted_effort": self._calculate_adjusted_effort(task),
            "fits_before_vacation": task_can_fit_before_vacation.get(task.id, True),
            "max_finish_date": task.max_end_date,
            "min_start_date": task.min_start_date,
        }

    def _build_assignee_dependency_graph(
        self,
        tasks: list[Task],
    ) -> tuple[dict[int, set[int]], set[int]]:
        """Build cross-assignee dependency graph.

        Analyzes dependencies between tasks to identify which assignees
        have cross-dependencies (task of assignee A depends on task of assignee B).

        Args:
            tasks: List of tasks to analyze

        Returns:
            Tuple of:
            - assignee_deps: dict mapping assignee_id -> set of assignee_ids it depends on
            - independent_assignees: set of assignee_ids with no cross-dependencies
        """
        from collections import defaultdict

        assignee_deps: dict[int, set[int]] = defaultdict(set)
        task_to_assignee = {t.id: t.assignee_id for t in tasks if t.assignee_id}

        for task in tasks:
            if not task.assignee_id:
                continue
            for dep in task.dependencies:
                dep_assignee = task_to_assignee.get(dep.depends_on_id)
                if dep_assignee and dep_assignee != task.assignee_id:
                    # Cross-assignee dependency found
                    assignee_deps[task.assignee_id].add(dep_assignee)

        all_assignees = set(task_to_assignee.values())
        dependent_assignees = set(assignee_deps.keys()) | {
            a for deps in assignee_deps.values() for a in deps
        }
        independent_assignees = all_assignees - dependent_assignees

        logger.warning(f"[PARALLEL] Assignee dependency analysis: {len(independent_assignees)} independent, {len(dependent_assignees)} in dependency chain")
        if assignee_deps:
            for aid, deps in assignee_deps.items():
                logger.warning(f"  - Assignee {aid} depends on: {deps}")

        return dict(assignee_deps), independent_assignees

    def _topological_sort_assignees(
        self,
        assignee_deps: dict[int, set[int]],
    ) -> list[set[int]]:
        """Group dependent assignees into levels for sequential processing.

        Uses Kahn's algorithm to sort assignees topologically.
        Each level contains assignees that can be processed in parallel
        (no mutual dependencies), but levels must be processed sequentially.

        Args:
            assignee_deps: dict mapping assignee_id -> set of assignee_ids it depends on

        Returns:
            List of sets where each set can be processed in parallel,
            but sets must be processed sequentially.
        """
        if not assignee_deps:
            return []

        # Collect all assignees involved in dependencies
        all_assignees = set(assignee_deps.keys()) | {
            a for deps in assignee_deps.values() for a in deps
        }

        # Calculate in-degree for each assignee
        in_degree = {a: 0 for a in all_assignees}
        for assignee, deps in assignee_deps.items():
            in_degree[assignee] = len(deps)

        # Build reverse graph (who depends on whom)
        dependents: dict[int, set[int]] = {a: set() for a in all_assignees}
        for assignee, deps in assignee_deps.items():
            for dep in deps:
                dependents[dep].add(assignee)

        levels: list[set[int]] = []
        remaining = set(all_assignees)

        while remaining:
            # Find all assignees with no remaining dependencies (in_degree == 0)
            level = {a for a in remaining if in_degree.get(a, 0) == 0}

            if not level:
                # Cycle detected - put all remaining in one level (fallback)
                logger.warning(f"[PARALLEL] Cycle detected in assignee dependencies, falling back to sequential")
                levels.append(remaining)
                break

            levels.append(level)
            remaining -= level

            # Update in-degrees for dependents
            for assignee in level:
                for dependent in dependents.get(assignee, set()):
                    if dependent in remaining:
                        in_degree[dependent] -= 1

        logger.warning(f"[PARALLEL] Assignee levels: {len(levels)} levels")
        for i, level in enumerate(levels):
            logger.warning(f"  - Level {i}: {level}")

        return levels

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
        if task.is_deferred:
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

        # Calculate real duration - round UP to full days
        # Apply professionalism coefficient: higher coefficient = faster work = shorter duration
        # Apply operational utilization: higher util = more overhead = longer duration
        coefficient = task.assignee.professionalism_coefficient if task.assignee else 1.0
        operational_util = task.assignee.operational_utilization if task.assignee else 0.0

        adjusted_effort = task.effort_days / coefficient if coefficient > 0 else task.effort_days
        adjusted_effort = adjusted_effort / (1 - operational_util / 100) if operational_util < 100 else adjusted_effort
        effort_days = max(1, math.ceil(adjusted_effort))

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
                slot_start, effort_days, task.id, accounting_days=task.effort_days
            )
            task.start_date = start_date
            task.end_date = end_date
            task.calculated_effort_days = float(effort_days)  # Save to DB for Gantt display
            logger.warning(f"  - ALLOCATED: {start_date} to {end_date} ({(end_date - start_date).days + 1} calendar days)")

            # Check if overdue
            if end_date > iteration.end_date:
                decision_type = "overdue"
                reason = f"Task extends beyond iteration by {(end_date - iteration.end_date).days} days"
        else:
            # No slot available - use calendar days calculation (5 working = 7 calendar)
            task.start_date = earliest_start
            calendar_days = int(effort_days * 7 / 5)
            task.end_date = earliest_start + timedelta(days=calendar_days)
            task.calculated_effort_days = float(effort_days)  # Save to DB for Gantt display
            # The member still owns this effort; keep workload reporting truthful.
            schedule.allocated_days += task.effort_days
            decision_type = "overdue"
            reason = "No available slot found within iteration"

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
            if child.is_deferred:
                continue  # Skip deferred tasks
            if child.children:
                await self._schedule_composite_task(
                    child, iteration, member_schedules, decisions, task_map, earliest_start
                )
            else:
                await self._schedule_leaf_task(
                    child, iteration, member_schedules, decisions, task_map, earliest_start
                )

        # Compute parent dates from children (excluding deferred tasks)
        children_with_dates = [c for c in task.children if c.start_date and c.end_date and not c.is_deferred]

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

        # Compute dates from children (excluding deferred tasks)
        children_with_dates = [c for c in task.children if c.start_date and c.end_date and not c.is_deferred]

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

        # Load affected tasks
        tasks: list[Task] = []
        for task_id in affected_task_ids:
            task = await self.task_service.get_by_id(task_id)
            if task and task.status == TaskStatus.PLANNED.value:
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
        all_tasks = await self.task_service.get_all_tasks(iteration_id)
        for existing_task in all_tasks:
            if existing_task.id not in affected_task_ids and existing_task.start_date:
                if existing_task.assignee_id and existing_task.assignee_id in member_schedules:
                    schedule = member_schedules[existing_task.assignee_id]
                    if existing_task.end_date:
                        for d in schedule.working_dates:
                            if existing_task.start_date <= d <= existing_task.end_date:
                                if d not in schedule.vacation_dates:
                                    schedule.allocated_dates[d] = existing_task.id
                        schedule._invalidate_cache()

        decisions: list[SchedulingDecision] = []
        task_map = {t.id: t for t in all_tasks}

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

        await self.db.commit()

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
                ChangeType.EFFORT_INCREASED if new_effort > old_task.effort_days
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
