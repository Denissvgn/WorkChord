# IncrementalScheduler

**Location:** `backend/app/services/scheduler_service.py:1329`
**Kind:** Class
**Bases:** —
**Module:** [scheduler_service](../modules/scheduler_service.md)

## Description

Handles incremental rescheduling when a single task changes.

Instead of rescheduling the entire iteration (O(N)), this scheduler:
1. Detects what changed on a task
2. Identifies only the affected tasks (dependents, same-assignee tasks)
3. Reschedules only the affected subset (O(A) where A << N)

Performance: O(A) instead of O(N), typically 10x faster for single-task changes.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(scheduler_service: SchedulerService)` | — | — |
| `reschedule_affected` | *(async)* `(change: TaskChange) -> RescheduleResult` | — | Reschedule only tasks affected by the change. |
| `_find_affected_tasks` | *(async)* `(change: TaskChange) -> set[int]` | — | Find all tasks affected by the change. |
| `_find_all_dependents` | *(async)* `(task_id: int) -> set[int]` | — | Find all tasks that depend on this task (recursive BFS). |
| `_find_assignee_tasks` | *(async)* `(iteration_id: int, assignee_id: int) -> set[int]` | — | Find all tasks assigned to a specific person in the iteration. |
| `_reschedule_subset` | *(async)* `(iteration_id: int, affected_task_ids: set[int]) -> RescheduleResult` | — | Reschedule only the affected tasks. |
| `detect_changes` | `(old_task: Task, new_effort: Optional[int] = None, new_assignee_id: Optional[int] = None, new_priority: Optional[int] = None, new_min_start_date: Optional[date] = None, new_max_end_date: Optional[date] = None) -> list[TaskChange]` | `@staticmethod` | Detect what changed between old task state and new values. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [scheduler_service](../modules/scheduler_service.md) | 7 | — |
