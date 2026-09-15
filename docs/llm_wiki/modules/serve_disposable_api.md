# serve_disposable_api Module

**Path:** `scripts/ci/serve_disposable_api.py`

## Description

Starts the real HTTP application after requiring an explicitly designated temporary SQLite target and isolated execution environment. Schema initialization and deterministic scenario data are created only for that disposable target, then the ordinary application lifespan serves requests.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `async_session_maker`, `close_database` |
| `app.models.identity` | `Principal`, `IdentitySubject`, `ProjectMembership`, `PrincipalProfileLink` |
| `app.services.upgrade_service` | `run_alembic_upgrade` |
| `asyncio` | `asyncio` |
| `os` | `os` |
| `pathlib` | `Path` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tests.support.database` | `assert_safe_test_database_url` |
| `tests.support.delivery` | `seed_delivery_scenario` |
| `uvicorn` | `uvicorn` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/identity.py"]
    n2["backend/app/services/upgrade_service.py"]
    n3["backend/tests/support/database.py"]
    n4["backend/tests/support/delivery.py"]
    n5["scripts/ci/serve_disposable_api.py"]
    n0 --> n2
    n1 --> n0
    n2 --> n0
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models_identity.md"
    click n2 "../modules/upgrade_service.md"
    click n3 "../modules/support_database.md"
    click n4 "../modules/delivery.md"
    click n5 "../modules/serve_disposable_api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [support_database](../modules/support_database.md) |
| Outbound | [delivery](../modules/delivery.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 2 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `main` | `()` | — | — |