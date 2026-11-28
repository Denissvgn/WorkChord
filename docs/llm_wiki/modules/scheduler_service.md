# scheduler_service Module

**Path:** `backend/app/services/scheduler_service.py`

## Description

Builds forecasts from canonical person calendars and shared absences, retaining actual execution dates. Productive-hour reservations include shortened days, existing execution slots and overflow dates. Preview and apply use the same shared planning revision. A forecast may overflow, but a new commitment must fit allocation dates and shared capacity; accepted baselines are changed only through deliberate rebaselining.

YAML and fallback scheduling, incremental rescheduling and reservations use complete inherited deferred and optional policy. Deferred descendants cannot consume schedule capacity or acquire forecast dates through these paths.

A calculation may also follow actual dates. Given the day a task started or was submitted, it places planned work on or after that day, lets finished work free its assignee from that day, keeps running work on its assignee at least through it, and leaves the dates of work it cannot place. The task that just started takes its assignee's row first. When only a task's dates change, its queued agent assignments move to the new task version; model-aware assignments do not, because their routing evidence is bound to the exact version.

An estimate consumes the dated hours of each selected annual record. If a forecast reaches an uncovered year, the scheduler retains the existing dates and reports the missing year. A successful date-only apply reports a model-bound queue entry that needs a fresh selection and identifies an accepted assignment whose dates would need to move.

Applying dates that change accepted work is guarded regardless of how the iteration or person selected their calendars. An unchanged accepted task retains its version while eligible planned work can move.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority` |
| `app.commands` | `atomic_command`, `command_transaction`, `commit_or_flush`, `lock_iterations`, `lock_planning`, `PlanningConflict`, `current_command` |
| `app.models.agent` | `AgentTaskAssignment` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.recovery` | `TaskScheduleBaseline` |
| `app.models.task` | `Task`, `TaskDependency`, `TaskStatus`, `TaskStatus`, `TaskStatus`, `TaskStatus`, `TaskStatus` |
| `app.models.team_member` | `TeamMember`, `Vacation` |
| `app.schemas.gantt` | `AssigneeIdleDays`, `IdleGap`, `KeptDatesTask`, `SchedulingDecision`, `ScheduleResult`, `UnscheduledTask`, `WaitingOnTask`, `WorkloadIssue` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `app.services.calendar_rules` | `AnnualCalendars` |
| `app.services.calendar_service` | `CalendarService` |
| `app.services.capacity_adjustments` | `load_dated_availability` |
| `app.services.capacity_service` | `CapacityService`, `CapacityService` |
| `app.services.delivery_dependency_service` | `DeliveryDependencyService` |
| `app.services.iteration_service` | `IterationService`, `IterationService` |
| `app.services.scheduling_rules_service` | `SchedulingRulesService` |
| `app.services.task_service` | `TaskService` |
| `app.services.team_service` | `TeamService` |
| `app.services.work_metrics` | `effective_work_flags`, `effective_work_flags`, `postponed_work_under`, `working_today`, `effective_work_flags` |
| `collections` | `defaultdict` |
| `dataclasses` | `dataclass`, `field` |
| `datetime` | `date`, `timedelta` |
| `enum` | `Enum` |
| `heapq` | `heapq` |
| `logging` | `logging` |
| `math` | `math` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Callable`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/scheduler_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/scheduler_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (17) |
| Outbound | `backend` (20) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 36 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [MissingCalendarYear](../entities/MissingCalendarYear.md) | Class | 28 | `PlanningConflict` | — |
| [ChangeType](../entities/ChangeType.md) | Enum | 34 | `Enum` | Types of changes that trigger incremental rescheduling. |
| [TaskChange](../entities/TaskChange.md) | Class | 48 | — | Represents a change to a task for incremental rescheduling. |
| [RescheduleResult](../entities/RescheduleResult.md) | Class | 59 | — | Result of an incremental reschedule operation. |
| [MemberSchedule](../entities/MemberSchedule.md) | Class | 69 | — | Optimized schedule tracking with O(D) slot finding using sliding window. |
| [SchedulerService](../entities/SchedulerService.md) | Class | 389 | — | Service for automatic task scheduling. |
| [IncrementalScheduler](../entities/IncrementalScheduler.md) | Class | 1744 | — | Handles incremental rescheduling when a single task changes. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `rebind_queued_assignments` | *(async)* `(db: AsyncSession, task_id: int, previous_version: int, new_version: int, *, protect_issued: bool = False) -> list[dict]` | — | Keep queued dispatch valid when only a task's dates changed. |
