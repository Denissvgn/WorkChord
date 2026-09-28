# test_task_domain_migrations Module

**Path:** `backend/tests/test_task_domain_migrations.py`

## Description

Nonempty upgrade preservation and resumable task-domain backfill evidence.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.utils.time` | `utc_now` |
| `datetime` | `date` |
| `importlib` | `importlib` |
| `pytest` | `pytest` |
| `sqlalchemy` | `Boolean`, `Date`, `DateTime`, `Float`, `Integer`, `JSON`, `MetaData`, `select`, `text`, `inspect` |
| `sqlalchemy.exc` | `IntegrityError` |
| `tests.test_authority_migrations` | `legacy_authority_database` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/utils/time.py"]
    n1["backend/tests/test_authority_migrations.py"]
    n2["backend/tests/test_task_domain_migrations.py"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    click n0 "../modules/time.md"
    click n1 "../modules/test_authority_migrations.md"
    click n2 "../modules/test_task_domain_migrations.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [time](../modules/time.md) |
| Outbound | [test_authority_migrations](../modules/test_authority_migrations.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `insert_fixture` | `(connection, table, **values)` | — | Fill required scalar data while every relationship remains explicitly supplied. |
| `test_nonempty_domain_upgrade_preserves_ids_history_and_backfill_provenance` | `(legacy_authority_database)` | — | — |
| `test_backfill_cursor_resumes_without_rewriting_completed_rows` | `(legacy_authority_database)` | — | — |
| `test_deletion_fence_upgrade_preserves_unknown_history_and_survives_without_tasks` | `(legacy_authority_database)` | — | — |
