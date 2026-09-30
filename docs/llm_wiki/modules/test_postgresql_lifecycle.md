# test_postgresql_lifecycle Module

**Path:** `backend/tests/test_postgresql_lifecycle.py`

## Description

Real-server smoke for create, migrate, exercise, and drop lifecycle.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `alembic` | `command` |
| `alembic.config` | `Config` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `text` |
| `sqlalchemy.pool` | `NullPool` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_postgresql_database_lifecycle_from_empty_database` | `(postgres_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.destructive`, `@pytest.mark.allow_network` | — |
