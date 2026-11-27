# test_server_features Module

**Path:** `backend/tests/test_server_features.py`

## Description

The public feature list names only features this server has.

## Imports

| Source | Symbols |
|--------|---------|
| `app.main` | `app` |
| `app.mcp_server` | `mcp` |
| `app.routers.identity` | `NativeConnectionStart` |
| `app.schemas.external_link` | `ExternalLinkProvider` |
| `app.server_features` | `SERVER_FEATURES` |
| `asyncio` | `asyncio` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client`, `managed_store` |
| `tests.test_observer_sessions` | `local_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/main.py"]
    n1["backend/app/mcp_server.py"]
    n2["backend/app/routers/identity.py"]
    n3["backend/app/schemas/external_link.py"]
    n4["backend/app/server_features.py"]
    n5["backend/tests/test_delivery_scenarios.py"]
    n6["backend/tests/test_managed_authority.py"]
    n7["backend/tests/test_observer_sessions.py"]
    n8["backend/tests/test_server_features.py"]
    n0 --> n1
    n0 --> n2
    n2 --> n4
    n5 --> n0
    n6 --> n0
    n6 --> n5
    n7 --> n5
    n7 --> n6
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    n8 --> n7
    click n0 "../modules/app_main.md"
    click n1 "../modules/mcp_server.md"
    click n2 "../modules/routers_identity.md"
    click n3 "../modules/schemas_external_link.md"
    click n4 "../modules/server_features.md"
    click n5 "../modules/test_delivery_scenarios.md"
    click n6 "../modules/test_managed_authority.md"
    click n7 "../modules/test_observer_sessions.md"
    click n8 "../modules/test_server_features.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [app_main](../modules/app_main.md) |
| Outbound | [mcp_server](../modules/mcp_server.md) |
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
