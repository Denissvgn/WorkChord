# test_plan_shares Module

**Path:** `backend/tests/test_plan_shares.py`

## Description

Plan-share ownership and immutable snapshot behavior.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember` |
| `app.models.user_session` | `UserSession` |
| `app.services.plan_share_service` | `PlanShareService` |
| `datetime` | `date` |
| `pytest` | `pytest` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/calendar.py"]
    n1["backend/app/models/iteration.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/models/team_member.py"]
    n4["backend/app/models/user_session.py"]
    n5["backend/app/services/plan_share_service.py"]
    n6["backend/tests/test_plan_shares.py"]
    n0 --> n1
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n1
    n2 --> n3
    n3 --> n1
    n3 --> n2
    n5 --> n4
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/models_calendar.md"
    click n1 "../modules/models_iteration.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/team_member.md"
    click n4 "../modules/user_session.md"
    click n5 "../modules/plan_share_service.md"
    click n6 "../modules/test_plan_shares.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [team_member](../modules/team_member.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [plan_share_service](../modules/plan_share_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_plan_share_replaces_owner_link_with_new_immutable_snapshot` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.asyncio` | — |
| `test_plan_share_missing_iteration_returns_none` | *(async)* `(db_session: AsyncSession) -> None` | `@pytest.mark.asyncio` | — |
