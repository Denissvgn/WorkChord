# plan_share_service Module

**Path:** `backend/app/services/plan_share_service.py`

## Description

Creation, ownership, and revocation of immutable plan shares.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.models.plan_share` | `PlanShare` |
| `app.models.user_session` | `UserSession` |
| `app.schemas.plan_share` | `PlanShareResponse` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `timedelta` |
| `secrets` | `secrets` |
| `sqlalchemy` | `select`, `update`, `or_` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/models/plan_share.py"]
    n2["backend/app/models/user_session.py"]
    n3["backend/app/routers/plan_shares.py"]
    n4["backend/app/schemas/plan_share.py"]
    n5["backend/app/services/plan_share_service.py"]
    n6["backend/app/services/snapshot_service.py"]
    n7["backend/app/utils/time.py"]
    n8["backend/tests/test_plan_shares.py"]
    n0 --> n6
    n1 --> n2
    n1 --> n7
    n2 --> n1
    n2 --> n7
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n6 --> n0
    n6 --> n7
    n8 --> n2
    n8 --> n5
    click n0 "../modules/commands.md"
    click n1 "../modules/models_plan_share.md"
    click n2 "../modules/user_session.md"
    click n3 "../modules/plan_shares.md"
    click n4 "../modules/schemas_plan_share.md"
    click n5 "../modules/plan_share_service.md"
    click n6 "../modules/snapshot_service.md"
    click n7 "../modules/time.md"
    click n8 "../modules/test_plan_shares.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [plan_shares](../modules/plan_shares.md) |
| Inbound | [test_plan_shares](../modules/test_plan_shares.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_plan_share](../modules/models_plan_share.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [schemas_plan_share](../modules/schemas_plan_share.md) |
| Outbound | [snapshot_service](../modules/snapshot_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [PlanShareService](../entities/PlanShareService.md) | 19 | — | Persist plan snapshots without exposing mutable planning records. |
