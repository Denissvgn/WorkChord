# task_timeline_service Module

**Path:** `backend/app/services/task_timeline_service.py`

## Description

Merged history is read in bounded per-source queries and sorted by timestamp, source and stable record ID. Opaque task-bound cursors are validated and every request rechecks task visibility. Run-event actor provenance comes from the owning run. The compatible timeline preserves chronological output and explicitly rejects overflow.

Bounded, permission-scoped keyset reads of the merged task timeline.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `AgentRun`, `AgentRunEvent`, `TaskEvent` |
| `app.models.task` | `Task` |
| `app.models.task_status_log` | `TaskStatusLog` |
| `app.utils.time` | `as_utc` |
| `base64` | `base64` |
| `datetime` | `datetime` |
| `json` | `json` |
| `sqlalchemy` | `and_`, `or_`, `select` |
| `sqlalchemy.orm` | `selectinload` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/task_status_log.py"]
    n3["backend/app/routers/tasks.py"]
    n4["backend/app/services/task_timeline_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/test_task_pagination.py"]
    n0 --> n1
    n0 --> n5
    n1 --> n0
    n1 --> n2
    n1 --> n5
    n2 --> n1
    n2 --> n5
    n3 --> n1
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n4
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/task_status_log.md"
    click n3 "../modules/tasks.md"
    click n4 "../modules/task_timeline_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_task_pagination.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [test_task_pagination](../modules/test_task_pagination.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [task_status_log](../modules/task_status_log.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskTimelineService](../entities/TaskTimelineService.md) | 16 | — | — |
