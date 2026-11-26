# test_runtime_boundaries Module

**Path:** `backend/tests/test_runtime_boundaries.py`

## Description

DBM-PERF-002 and DBM-MAINT-001 runtime-boundary tests.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app` | `authority`, `mcp_server` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.maintenance` | `MaintenanceModeError`, `RuntimeBoundaryMiddleware`, `enforce_mcp_access`, `scope_requirement_is_mutating` |
| `app.models.agent` | `AgentActor` |
| `app.models.user_session` | `UserSession` |
| `app.services.agent_service` | `AgentService`, `hash_api_key` |
| `app.services.email_settings_service` | `EmailSettings` |
| `app.services.notification_service` | `NotificationService` |
| `app.services.session_service` | `_token_digest`, `get_or_create_session` |
| `ast` | `ast` |
| `datetime` | `UTC`, `datetime`, `timedelta` |
| `fastapi` | `FastAPI` |
| `fastapi.routing` | `APIRoute` |
| `json` | `json` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/config.py"]
    n2["backend/app/main.py"]
    n3["backend/app/maintenance.py"]
    n4["backend/app/mcp_server.py"]
    n5["backend/app/models/agent.py"]
    n6["backend/app/models/user_session.py"]
    n7["backend/app/services/agent_service.py"]
    n8["backend/app/services/email_settings_service.py"]
    n9["backend/app/services/notification_service.py"]
    n10["backend/app/services/session_service.py"]
    n11["backend/tests/test_runtime_boundaries.py"]
    n0 --> n1
    n0 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n3 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n5
    n8 --> n1
    n9 --> n8
    n10 --> n0
    n10 --> n1
    n10 --> n3
    n10 --> n6
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n9
    n11 --> n10
    click n0 "../modules/authority.md"
    click n1 "../modules/config.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/app_maintenance.md"
    click n4 "../modules/mcp_server.md"
    click n5 "../modules/models_agent.md"
    click n6 "../modules/user_session.md"
    click n7 "../modules/agent_service.md"
    click n8 "../modules/email_settings_service.md"
    click n9 "../modules/notification_service.md"
    click n10 "../modules/session_service.md"
    click n11 "../modules/test_runtime_boundaries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [authority](../modules/authority.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [app_main](../modules/app_main.md) |
| Outbound | [app_maintenance](../modules/app_maintenance.md) |
| Outbound | [mcp_server](../modules/mcp_server.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [agent_service](../modules/agent_service.md) |
| Outbound | [email_settings_service](../modules/email_settings_service.md) |
| Outbound | [notification_service](../modules/notification_service.md) |
| Outbound | [session_service](../modules/session_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ScalarResult](../entities/ScalarResult.md) | 36 | — | — |
| [SessionDouble](../entities/SessionDouble.md) | 44 | — | — |
| [ProviderSessionDouble](../entities/ProviderSessionDouble.md) | 388 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `clear_runtime_settings_cache` | `() -> Any` | `@pytest.fixture(autouse=True)` | — |
| `_configure_mode` | `(monkeypatch: pytest.MonkeyPatch, mode: str) -> None` | — | — |
| `_asgi_request` | *(async)* `(app: Any, method: str, path: str) -> tuple[int, dict[str, str], bytes]` | — | — |
| `_boundary_app` | `() -> FastAPI` | — | — |
| `test_validation_only_is_exact_allowlist_and_fail_closed` | *(async)* `(monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |
| `test_read_only_maintenance_allows_reads_but_rejects_every_new_write` | *(async)* `(monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |
| `test_mcp_scope_contract_fences_mutations_and_preserves_read_tools` | `(monkeypatch: pytest.MonkeyPatch) -> None` | — | — |
| `test_application_has_one_fail_closed_boundary_for_all_rest_mutations` | `() -> None` | — | — |
| `test_every_mcp_tool_uses_scope_classification_and_mutators_are_write_only` | `() -> None` | — | — |
| `test_active_browser_reads_skip_session_commits` | *(async)* `(monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |
| `test_validation_session_resolution_has_no_hidden_touch` | *(async)* `(monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |
| `test_validation_agent_authentication_has_no_hidden_last_seen_write` | *(async)* `(monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |
| `test_smtp_provider_wait_starts_after_database_release` | *(async)* `(monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.asyncio` | — |
