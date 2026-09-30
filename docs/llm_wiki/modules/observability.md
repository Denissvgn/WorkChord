# observability Module

**Path:** `backend/app/observability.py`

## Description

Database-backed readiness, drain state, and low-cardinality instrumentation.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.database` | `async_session_maker`, `database_runtime_summary` |
| `app.database_runtime` | `classify_database_failure` |
| `app.maintenance` | `maintenance_state` |
| `app.models.outbound_webhook` | `OutboundWebhookDelivery`, `OutboundWebhookDeliveryStatus` |
| `app.runtime_telemetry` | `activity`, `correlation_id_context`, `metrics` |
| `app.services.upgrade_service` | `head_revision` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `asyncio` | `asyncio` |
| `datetime` | `datetime` |
| `logging` | `logging` |
| `pathlib` | `Path` |
| `sqlalchemy` | `event`, `func`, `or_`, `select`, `text` |
| `sqlalchemy.engine` | `Engine` |
| `sqlalchemy.exc` | `SQLAlchemyError` |
| `sqlalchemy.ext.asyncio` | `AsyncEngine`, `AsyncSession` |
| `time` | `monotonic` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/database.py"]
    n2["backend/app/database_runtime.py"]
    n3["backend/app/main.py"]
    n4["backend/app/maintenance.py"]
    n5["backend/app/models/outbound_webhook.py"]
    n6["backend/app/observability.py"]
    n7["backend/app/runtime_telemetry.py"]
    n8["backend/app/services/upgrade_service.py"]
    n9["backend/app/utils/time.py"]
    n10["backend/tests/database/test_observability.py"]
    n1 --> n0
    n1 --> n6
    n1 --> n8
    n2 --> n7
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n6
    n3 --> n7
    n4 --> n0
    n4 --> n7
    n5 --> n1
    n5 --> n9
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n4
    n10 --> n0
    n10 --> n6
    n10 --> n7
    click n0 "../modules/config.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/database_runtime.md"
    click n3 "../modules/app_main.md"
    click n4 "../modules/maintenance.md"
    click n5 "../modules/models_outbound_webhook.md"
    click n6 "../modules/observability.md"
    click n7 "../modules/runtime_telemetry.md"
    click n8 "../modules/upgrade_service.md"
    click n9 "../modules/time.md"
    click n10 "../modules/test_observability.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [app_database](../modules/app_database.md) |
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [test_observability](../modules/test_observability.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [database_runtime](../modules/database_runtime.md) |
| Outbound | [maintenance](../modules/maintenance.md) |
| Outbound | [models_outbound_webhook](../modules/models_outbound_webhook.md) |
| Outbound | [runtime_telemetry](../modules/runtime_telemetry.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_query_operation` | `(statement: str) -> str` | — | — |
| `install_database_instrumentation` | `(async_engine: AsyncEngine) -> None` | — | Attach one credential/parameter-free instrumentation set to an engine. |
| `_resident_set_size_bytes` | `() -> int \| None` | — | Read current Linux RSS without introducing a monitoring dependency. |
| `_queue_snapshot` | *(async)* `(db: AsyncSession) -> dict[str, Any]` | — | — |
| `_postgresql_snapshot` | *(async)* `(db: AsyncSession) -> dict[str, Any]` | — | — |
| `readiness_snapshot` | *(async)* `() -> tuple[bool, dict[str, Any]]` | — | Check connectivity, a short query, schema head, and drain evidence. |
| `collect_metrics` | *(async)* `() -> None` | — | Refresh database/queue gauges for a scrape without failing the scrape. |
