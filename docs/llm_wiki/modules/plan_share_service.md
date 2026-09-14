# plan_share_service Module

**Path:** `backend/app/services/plan_share_service.py`

## Description

Creation, ownership, and revocation of immutable plan shares.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.plan_share` | `PlanShare` |
| `app.models.user_session` | `UserSession` |
| `app.schemas.plan_share` | `PlanShareResponse` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.utils.time` | `utc_now` |
| `secrets` | `secrets` |
| `sqlalchemy` | `select`, `update` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/plan_share.py"]
    n1["backend/app/models/user_session.py"]
    n2["backend/app/routers/plan_shares.py"]
    n3["backend/app/schemas/plan_share.py"]
    n4["backend/app/services/plan_share_service.py"]
    n5["backend/app/services/snapshot_service.py"]
    n6["backend/app/utils/time.py"]
    n7["backend/tests/test_plan_shares.py"]
    n0 --> n1
    n0 --> n6
    n1 --> n0
    n1 --> n6
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n5 --> n6
    n7 --> n1
    n7 --> n4
    click n0 "../modules/models_plan_share.md"
    click n1 "../modules/user_session.md"
    click n2 "../modules/plan_shares.md"
    click n3 "../modules/schemas_plan_share.md"
    click n4 "../modules/plan_share_service.md"
    click n5 "../modules/snapshot_service.md"
    click n6 "../modules/time.md"
    click n7 "../modules/test_plan_shares.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [plan_shares](../modules/plan_shares.md) |
| Inbound | [test_plan_shares](../modules/test_plan_shares.md) |
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
| [PlanShareService](../entities/PlanShareService.md) | 16 | — | Persist plan snapshots without exposing mutable planning records. |
