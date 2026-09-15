# test_identity_lifecycle Module

**Path:** `backend/tests/test_identity_lifecycle.py`

## Description

OIDC, native bearer, revocation, ownership and real MCP transport contracts.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_server` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.identity` | `Principal`, `WorkspaceMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.saved_view` | `SavedView` |
| `app.models.task` | `Task` |
| `app.models.user_session` | `UserSession` |
| `app.services` | `identity_service` |
| `app.services.identity_service` | `digest`, `safe_return_path` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.utils.time` | `utc_now` |
| `base64` | `base64` |
| `cryptography.hazmat.primitives.asymmetric` | `rsa` |
| `datetime` | `timedelta` |
| `hashlib` | `hashlib` |
| `httpx` | `httpx` |
| `json` | `json` |
| `jwt` | `jwt` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store`, `client` |
| `types` | `SimpleNamespace` |
| `urllib.parse` | `parse_qs`, `urlencode`, `urlsplit` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_identity_lifecycle.py"]
    n1 --> n0
    click n1 "../modules/test_identity_lifecycle.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 5 | 1 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_oidc_code_flow_rotates_and_revokes_real_sessions` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `test_shared_iteration_snapshots_cannot_reveal_another_project` | *(async)* `(managed_store)` | — | — |
| `test_retention_preserves_references_and_revoked_sessions_stay_revoked` | *(async)* `(managed_store)` | — | — |
| `test_mcp_http_uses_the_same_principal_and_project_boundary` | *(async)* `(managed_store)` | — | — |
| `test_return_paths_stay_within_the_application` | `(value)` | `@pytest.mark.parametrize('value', ['//foreign.example', '/%2f%2fforeign.example', '/%255cforeign.example', '/%0aLocation:foreign', 'https://foreign.example'])` | — |
