# test_review_record_kind_migration Module

**Path:** `backend/tests/migrations/test_review_record_kind_migration.py`

## Description

Review history gains a kind reversibly and never silently loses an owner override.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.services.upgrade_service` | `alembic_config` |
| `app.utils.time` | `utc_now` |
| `pytest` | `pytest` |
| `sqlalchemy` | `sa`, `create_engine`, `inspect`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/upgrade_service.py"]
    n1["backend/app/utils/time.py"]
    n2["backend/tests/migrations/test_review_record_kind_migration.py"]
    n2 --> n0
    n2 --> n1
    click n0 "../modules/upgrade_service.md"
    click n1 "../modules/time.md"
    click n2 "../modules/test_review_record_kind_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_review_kind_migration_marks_history_as_reviews_and_refuses_losing_an_override` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |
