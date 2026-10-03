# delivery Module

**Path:** `backend/tests/support/delivery.py`

## Description

Deterministic shared delivery graph for database and HTTP scenarios.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `AgentActor` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.models.user_session` | `UserSession` |
| `app.services.agent_service` | `hash_api_key` |
| `dataclasses` | `dataclass` |
| `datetime` | `date` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/calendar.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/models/project.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/models/team_member.py"]
    n6["backend/app/models/user_session.py"]
    n7["backend/app/services/agent_service.py"]
    n8["backend/tests/support/delivery.py"]
    n9["backend/tests/test_delivery_scenarios.py"]
    n10["scripts/ci/serve_disposable_api.py"]
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n2
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n6 --> n3
    n7 --> n0
    n7 --> n4
    n7 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n8 --> n7
    n9 --> n4
    n9 --> n5
    n9 --> n7
    n9 --> n8
    n10 --> n4
    n10 --> n8
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_calendar.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/models_project.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/team_member.md"
    click n6 "../modules/user_session.md"
    click n7 "../modules/agent_service.md"
    click n8 "../modules/delivery.md"
    click n9 "../modules/test_delivery_scenarios.md"
    click n10 "../modules/serve_disposable_api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Inbound | [serve_disposable_api](../modules/serve_disposable_api.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [agent_service](../modules/agent_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryScenario](../entities/DeliveryScenario.md) | 19 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `seed_delivery_scenario` | *(async)* `(db: AsyncSession) -> DeliveryScenario` | — | — |
