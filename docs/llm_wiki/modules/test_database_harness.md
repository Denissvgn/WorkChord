# test_database_harness Module

**Path:** `backend/tests/test_database_harness.py`

## Description

Fast unit coverage for the Wave 0 database test infrastructure.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database` | `Base` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `asyncio` | `asyncio` |
| `datetime` | `timedelta` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `inspect`, `select` |
| `sqlite3` | `sqlite3` |
| `tests.support` | `AsyncBarrier`, `UnsafeDatabaseTarget` |
| `tests.support.database` | `assert_safe_test_database_url` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/calendar.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/tests/support/__init__.py"]
    n4["backend/tests/support/database.py"]
    n5["backend/tests/test_database_harness.py"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    n2 --> n1
    n3 --> n4
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models_calendar.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/support___init__.md"
    click n4 "../modules/support_database.md"
    click n5 "../modules/test_database_harness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [support___init__](../modules/support___init__.md) |
| Outbound | [support_database](../modules/support_database.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_safety_fence_rejects_production_like_targets` | `(database_url: str) -> None` | `@pytest.mark.parametrize('database_url', ['postgresql+psycopg://postgres:secret@localhost/workchord', 'postgresql+psycopg://postgres:secret@db.production/workchord_test_0123456789abcdef0123456789abcdef', 'sqlite+aiosqlite:////mnt/data/projects/WorkChord/workchord_test_bad.db'])` | — |
| `test_safety_fence_requires_test_environment` | `() -> None` | — | — |
| `test_safety_fence_accepts_only_unique_local_test_target` | `() -> None` | — | — |
| `test_isolated_sqlite_session_round_trips_representative_graph` | *(async)* `(db_session, mapped_model_factory) -> None` | `@pytest.mark.sqlite`, `@pytest.mark.asyncio` | — |
| `test_generic_factory_covers_every_mapped_table` | `(mapped_model_factory) -> None` | — | — |
| `test_legacy_factory_builds_valid_and_orphan_sources` | `(tmp_path: Path, legacy_sqlite_factory) -> None` | `@pytest.mark.sqlite` | — |
| `test_clock_and_failure_injector_are_deterministic` | `(frozen_clock, failure_injector) -> None` | — | — |
| `test_async_barrier_controls_interleaving` | *(async)* `() -> None` | `@pytest.mark.asyncio` | — |
