# test_server_features Module

**Path:** `backend/tests/test_server_features.py`

## Description

The public feature list names only features this server has.

## Imports

| Source | Symbols |
|--------|---------|
| `app.main` | `app` |
| `app.routers.identity` | `NativeConnectionStart` |
| `app.schemas.external_link` | `ExternalLinkProvider` |
| `app.server_features` | `SERVER_FEATURES` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client`, `managed_store` |
| `tests.test_observer_sessions` | `local_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/main.py"]
    n1["backend/app/routers/identity.py"]
    n2["backend/app/schemas/external_link.py"]
    n3["backend/app/server_features.py"]
    n4["backend/tests/test_delivery_scenarios.py"]
    n5["backend/tests/test_managed_authority.py"]
    n6["backend/tests/test_observer_sessions.py"]
    n7["backend/tests/test_server_features.py"]
    n0 --> n1
    n1 --> n3
    n4 --> n0
    n5 --> n0
    n5 --> n4
    n6 --> n4
    n6 --> n5
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    click n0 "../modules/app_main.md"
    click n1 "../modules/routers_identity.md"
    click n2 "../modules/schemas_external_link.md"
    click n3 "../modules/server_features.md"
    click n4 "../modules/test_delivery_scenarios.md"
    click n5 "../modules/test_managed_authority.md"
    click n6 "../modules/test_observer_sessions.md"
    click n7 "../modules/test_server_features.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [app_main](../modules/app_main.md) |
| Outbound | [routers_identity](../modules/routers_identity.md) |
| Outbound | [schemas_external_link](../modules/schemas_external_link.md) |
| Outbound | [server_features](../modules/server_features.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |
| Outbound | [test_observer_sessions](../modules/test_observer_sessions.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `routes` | `()` | — | — |
| `test_every_listed_feature_is_present_and_named_once` | `()` | — | — |
| `anonymous_features` | *(async)* `()` | — | — |
| `test_a_managed_server_lists_features_without_a_credential` | *(async)* `(managed_store)` | — | — |
| `test_a_trusted_local_server_lists_features_without_a_credential` | *(async)* `(local_store)` | — | — |
