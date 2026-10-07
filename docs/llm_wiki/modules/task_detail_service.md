# task_detail_service Module

**Path:** `backend/app/services/task_detail_service.py`

## Description

Reference lookup supports bounded ascending-ID reads, status/search/scope filters and root or direct-child expansion. Parent visibility and scope are checked before child paging. Existing live-read behavior requires refresh for changes behind a cursor; no projection replaces the complete execution graph.

Provides bounded task references, title/ID lookup and human ownership queues without loading the full execution graph. Human work can be filtered by authorized project, iteration or backlog before pagination. Queue categorization remains server-owned, including blocked prerequisites and acceptance reconciliation. Reference projections do not establish complete execution context.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `require_project` |
| `app.models.task` | `Task`, `TaskDependency` |
| `app.schemas.task` | `TaskAgentReadiness` |
| `app.schemas.task_detail` | `TaskDetailResponse`, `TaskReference`, `TaskReferencePage` |
| `sqlalchemy` | `and_`, `or_`, `select` |
| `sqlalchemy.orm` | `selectinload`, `raiseload` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/routers/task_domain.py"]
    n4["backend/app/schemas/task.py"]
    n5["backend/app/schemas/task_detail.py"]
    n6["backend/app/services/task_detail_service.py"]
    n7["backend/tests/test_human_work_queries.py"]
    n8["backend/tests/test_task_domain.py"]
    n9["backend/tests/test_task_pagination.py"]
    n10["scripts/load/service_worksets.py"]
    n0 --> n2
    n1 --> n4
    n1 --> n6
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n5 --> n4
    n6 --> n0
    n6 --> n2
    n6 --> n4
    n6 --> n5
    n7 --> n0
    n7 --> n2
    n7 --> n4
    n7 --> n6
    n7 --> n8
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n4
    n8 --> n6
    n9 --> n0
    n9 --> n2
    n9 --> n6
    n10 --> n0
    n10 --> n2
    n10 --> n6
    click n0 "../modules/authority.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/schemas_task.md"
    click n5 "../modules/task_detail.md"
    click n6 "../modules/task_detail_service.md"
    click n7 "../modules/test_human_work_queries.md"
    click n8 "../modules/test_task_domain.md"
    click n9 "../modules/test_task_pagination.md"
    click n10 "../modules/service_worksets.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [test_human_work_queries](../modules/test_human_work_queries.md) |
| Inbound | [test_task_domain](../modules/test_task_domain.md) |
| Inbound | [test_task_pagination](../modules/test_task_pagination.md) |
| Inbound | [service_worksets](../modules/service_worksets.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [task_detail](../modules/task_detail.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskDetailService](../entities/TaskDetailService.md) | 12 | — | — |