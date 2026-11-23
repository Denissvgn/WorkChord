# task_timeline_service Module

**Path:** `backend/app/services/task_timeline_service.py`

## Description

Merged history is read in bounded per-source queries and sorted by timestamp, source and stable record ID. Opaque task-bound cursors are validated and every request rechecks task visibility. Run-event actor provenance comes from the owning run. The compatible timeline preserves chronological output and explicitly rejects overflow.
Agent-authored items carry the actor's display name, looked up once per page, so task Activity names the agent that reported progress or a blocker.

Bounded, permission-scoped keyset reads of the merged task timeline.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority` |
| `app.models.agent` | `AgentActor`, `AgentRun`, `AgentRunEvent`, `TaskEvent` |
| `app.models.identity` | `Principal` |
| `app.models.task` | `Task` |
| `app.models.task_status_log` | `TaskStatusLog` |
| `app.models.team_member` | `TeamMemberProfile` |
| `app.services.agent_service` | `AgentService` |
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
    n0["backend/app/authority.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/identity.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/models/task_status_log.py"]
    n5["backend/app/models/team_member.py"]
    n6["backend/app/routers/tasks.py"]
    n7["backend/app/services/agent_service.py"]
    n8["backend/app/services/task_timeline_service.py"]
    n9["backend/app/utils/time.py"]
    n10["backend/tests/test_task_discussion.py"]
    n11["backend/tests/test_task_pagination.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    n1 --> n5
    n1 --> n9
    n2 --> n9
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n9
    n4 --> n3
    n4 --> n9
    n5 --> n1
    n5 --> n3
    n5 --> n9
    n6 --> n3
    n6 --> n7
    n6 --> n8
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n8
    n7 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n7
    n8 --> n9
    n10 --> n0
    n10 --> n2
    n10 --> n3
    n10 --> n5
    n10 --> n8
    n10 --> n9
    n11 --> n0
    n11 --> n1
    n11 --> n3
    n11 --> n4
    n11 --> n7
    n11 --> n8
    click n0 "../modules/authority.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_identity.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/task_status_log.md"
    click n5 "../modules/team_member.md"
    click n6 "../modules/tasks.md"
    click n7 "../modules/agent_service.md"
    click n8 "../modules/task_timeline_service.md"
    click n9 "../modules/time.md"
    click n10 "../modules/test_task_discussion.md"
    click n11 "../modules/test_task_pagination.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [agent_service](../modules/agent_service.md) |
| Inbound | [test_task_discussion](../modules/test_task_discussion.md) |
| Inbound | [test_task_pagination](../modules/test_task_pagination.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [task_status_log](../modules/task_status_log.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [agent_service](../modules/agent_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskTimelineService](../entities/TaskTimelineService.md) | 16 | — | — |