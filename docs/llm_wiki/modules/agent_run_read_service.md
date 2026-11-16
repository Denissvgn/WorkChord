# agent_run_read_service Module

**Path:** `backend/app/services/agent_run_read_service.py`

## Description

List runs for readers within the task read scope.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority` |
| `app.models.agent` | `AgentActor`, `AgentRun` |
| `app.models.execution_usage` | `ExecutionUsageRecord` |
| `app.schemas.agent` | `AgentAssignmentActorSummary` |
| `app.schemas.agent_run_read` | `AgentRunHarness`, `AgentRunReadItem` |
| `app.services.execution_usage_service` | `ExecutionUsageService`, `run_identity` |
| `sqlalchemy` | `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/execution_usage.py"]
    n3["backend/app/routers/agent.py"]
    n4["backend/app/schemas/agent.py"]
    n5["backend/app/schemas/agent_run_read.py"]
    n6["backend/app/services/agent_run_read_service.py"]
    n7["backend/app/services/execution_usage_service.py"]
    n0 --> n1
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n5 --> n4
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    click n0 "../modules/authority.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_execution_usage.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/schemas_agent.md"
    click n5 "../modules/agent_run_read.md"
    click n6 "../modules/agent_run_read_service.md"
    click n7 "../modules/execution_usage_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_agent](../modules/routers_agent.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_execution_usage](../modules/models_execution_usage.md) |
| Outbound | [schemas_agent](../modules/schemas_agent.md) |
| Outbound | [agent_run_read](../modules/agent_run_read.md) |
| Outbound | [execution_usage_service](../modules/execution_usage_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentRunReadService](../entities/AgentRunReadService.md) | 13 | — | — |
