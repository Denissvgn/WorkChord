# scheduler_service Module

**Path:** `backend/app/services/scheduler_service.py`

## Description

Gantt Scheduler Service - automatic task scheduling with optimization.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `atomic_command`, `command_transaction`, `commit_or_flush`, `lock_iterations` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task`, `TaskDependency`, `TaskStatus` |
| `app.models.team_member` | `TeamMember`, `Vacation` |
| `app.schemas.gantt` | `SchedulingDecision`, `ScheduleResult`, `WorkloadIssue` |
| `app.services.calendar_service` | `CalendarService` |
| `app.services.scheduling_rules_service` | `SchedulingRulesService` |
| `app.services.task_service` | `TaskService` |
| `app.services.team_service` | `TeamService` |
| `dataclasses` | `dataclass`, `field` |
| `datetime` | `date`, `timedelta` |
| `enum` | `Enum` |
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
| Inbound | `backend` (5) |
| Outbound | `backend` (9) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ChangeType](../entities/ChangeType.md) | Enum | 26 | `Enum` | Types of changes that trigger incremental rescheduling. |
| [TaskChange](../entities/TaskChange.md) | Class | 40 | — | Represents a change to a task for incremental rescheduling. |
| [RescheduleResult](../entities/RescheduleResult.md) | Class | 51 | — | Result of an incremental reschedule operation. |
| [MemberSchedule](../entities/MemberSchedule.md) | Class | 61 | — | Optimized schedule tracking with O(D) slot finding using sliding window. |
| [SchedulerService](../entities/SchedulerService.md) | Class | 341 | — | Service for automatic task scheduling. |
| [IncrementalScheduler](../entities/IncrementalScheduler.md) | Class | 1329 | — | Handles incremental rescheduling when a single task changes. |
