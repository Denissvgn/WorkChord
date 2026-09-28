# TaskScheduleBaseline

**Location:** `backend/app/models/recovery.py:40`
**Kind:** Class
**Bases:** `Base`
**Module:** [recovery](../modules/recovery.md)

## Description

_Auto-generated from `TaskScheduleBaseline` in `backend/app/models/recovery.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `task_id` | `Mapped[int]` | `mapped_column(ForeignKey('tasks.id', ondelete='CASCADE'), index=True)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `start_date` | `Mapped[date \| None]` | `mapped_column(Date)` | — |
| `end_date` | `Mapped[date \| None]` | `mapped_column(Date)` | — |
| `timezone` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `reason` | `Mapped[str]` | `mapped_column(Text, nullable=False)` | — |
| `principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'))` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskScheduleBaseline (backend/app/models/recovery.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["SchedulerService.schedule_iteration (backend/app/services/scheduler_service.py)"]
    n4["SnapshotService.restore (backend/app/services/snapshot_service.py)"]
    n5["backend/tests/test_work_correctness.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/recovery.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/scheduler_service.md"
    click n4 "../modules/snapshot_service.md"
    click n5 "../modules/test_work_correctness.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [recovery](../modules/recovery.md) | 0 | `created_at`, `end_date`, `id`, `principal_id`, `reason`, `revision`, `start_date`, `task_id`, `timezone` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `SchedulerService.schedule_iteration` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SnapshotService.restore` | call | [snapshot_service](../modules/snapshot_service.md) | 1 |
| `test_work_correctness` | import | [test_work_correctness](../modules/test_work_correctness.md) | — |
