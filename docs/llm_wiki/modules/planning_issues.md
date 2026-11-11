# planning_issues Module

**Path:** `backend/app/services/planning_issues.py`

## Description

One rule for the planning gaps people and the PM see: "needs an assignee" and "missing effort".

The scheduler places only planned leaf work, so a task is a scheduling gap only
while it is planned, a leaf, and not deferred. A task an agent is already
working on is "Agent working · no capacity row", not unassigned.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `math` | `isfinite` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/iteration_service.py"]
    n1["backend/app/services/planning_issues.py"]
    n2["backend/app/services/saved_view_service.py"]
    n3["backend/app/services/task_service.py"]
    n4["backend/tests/test_planning_issues.py"]
    n0 --> n1
    n0 --> n3
    n2 --> n1
    n2 --> n3
    n3 --> n1
    n4 --> n1
    click n0 "../modules/iteration_service.md"
    click n1 "../modules/planning_issues.md"
    click n2 "../modules/saved_view_service.md"
    click n3 "../modules/task_service.md"
    click n4 "../modules/test_planning_issues.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [iteration_service](../modules/iteration_service.md) |
| Inbound | [saved_view_service](../modules/saved_view_service.md) |
| Inbound | [task_service](../modules/task_service.md) |
| Inbound | [test_planning_issues](../modules/test_planning_issues.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `is_planning_gap_candidate` | `(task: Any) -> bool` | — | A planned, non-deferred leaf: the only work the scheduler places. |
| `_agent_working` | `(task: Any) -> bool` | — | Whether an agent holds live execution work: a response's ``agent_working`` field, |
| `needs_assignee` | `(task: Any) -> bool` | — | — |
| `agent_working_without_capacity` | `(task: Any) -> bool` | — | — |
| `missing_effort` | `(task: Any) -> bool` | — | — |
