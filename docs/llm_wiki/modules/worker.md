# worker Module

**Path:** `backend/app/cli/worker.py`

## Description

Dedicated durable outbound-delivery worker process.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.config` | `get_settings` |
| `app.database` | `close_database`, `init_db` |
| `app.services.outbound_webhook_service` | `outbound_delivery_worker_loop`, `run_due_outbound_delivery_jobs` |
| `argparse` | `argparse` |
| `asyncio` | `asyncio` |
| `signal` | `signal` |
| `sys` | `sys` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/cli/worker.py"]
    n1["backend/app/config.py"]
    n2["backend/app/database.py"]
    n3["backend/app/services/outbound_webhook_service.py"]
    n4["backend/tests/test_process_roles.py"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n3 --> n2
    n4 --> n0
    n4 --> n1
    click n0 "../modules/worker.md"
    click n1 "../modules/config.md"
    click n2 "../modules/app_database.md"
    click n3 "../modules/outbound_webhook_service.md"
    click n4 "../modules/test_process_roles.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_process_roles](../modules/test_process_roles.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `build_parser` | `() -> argparse.ArgumentParser` | — | — |
| `_run` | *(async)* `(*, once: bool) -> int` | — | — |
| `main` | `(argv: Optional[list[str]] = None) -> int` | — | — |
