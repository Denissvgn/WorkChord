# runtime_observation_service Module

**Path:** `backend/app/services/runtime_observation_service.py`

## Description

Record and read advisory runtime observations.

Observations come from independent observers, such as a dashboard watching
agent sessions on a host. They are advisory: recording one writes only its own
row, never an actor, assignment, run, task event, topology member or webhook,
and no dispatch, routing or readiness code reads them.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority`, `require_operator` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.runtime_observation` | `AgentRuntimeObservation` |
| `app.models.task` | `Task` |
| `app.models.user_session` | `UserSession` |
| `app.schemas.runtime_observation` | `AgentRuntimeObservationCreate` |
| `app.utils.time` | `utc_now`, `as_utc` |
| `datetime` | `timedelta` |
| `sqlalchemy` | `delete`, `func`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/config.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/models/runtime_observation.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/models/user_session.py"]
    n6["backend/app/routers/agent.py"]
    n7["backend/app/schemas/runtime_observation.py"]
    n8["backend/app/services/runtime_observation_service.py"]
    n9["backend/app/utils/time.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n4
    n2 --> n4
    n2 --> n9
    n3 --> n9
    n4 --> n2
    n4 --> n9
    n5 --> n9
    n6 --> n1
    n6 --> n2
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n7 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n7
    n8 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/config.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/models_runtime_observation.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/user_session.md"
    click n6 "../modules/routers_agent.md"
    click n7 "../modules/schemas_runtime_observation.md"
    click n8 "../modules/runtime_observation_service.md"
    click n9 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_agent](../modules/routers_agent.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_runtime_observation](../modules/models_runtime_observation.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [schemas_runtime_observation](../modules/schemas_runtime_observation.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [RuntimeObservationService](../entities/RuntimeObservationService.md) | 26 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_same` | `(stored, requested)` | — | — |
