# installed_wheel_postgresql_qualification Module

**Path:** `scripts/ci/installed_wheel_postgresql_qualification.py`

## Description

Qualify the installed backend wheel across the SQLite/PostgreSQL boundary.

The coordinator intentionally imports no ``app`` modules.  Each phase runs in a
fresh interpreter with its database configuration frozen before the installed
package is imported.  CI invokes this file from the repository checkout while
the phase interpreters run with a temporary working directory, so an editable
source tree cannot accidentally satisfy the wheel boundary.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `alembic.config` | `Config` |
| `alembic.script` | `ScriptDirectory` |
| `app` | `app` |
| `app.cli.closeout` | `build_parser` |
| `app.cli.cutover` | `build_parser` |
| `app.database_migration.manifest` | `write_document` |
| `app.database_migration.source` | `preflight_source` |
| `app.database_migration.transfer` | `load_snapshot`, `reconcile_snapshot`, `record_post_copy_repairs`, `target_identifier` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.user_session` | `UserSession` |
| `app.services.upgrade_service` | `bootstrap_database_schema`, `bootstrap_database_schema`, `database_configuration`, `head_revision` |
| `argparse` | `argparse` |
| `datetime` | `UTC`, `date`, `datetime`, `timedelta` |
| `fastapi.testclient` | `TestClient` |
| `hashlib` | `hashlib` |
| `importlib.resources` | `as_file`, `files` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `psycopg` | `psycopg`, `sql` |
| `sqlalchemy` | `create_engine`, `create_engine`, `text` |
| `sqlalchemy.orm` | `Session` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `urllib.parse` | `urlsplit`, `urlunsplit` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["scripts/ci/installed_wheel_postgresql_qualification.py"]
    n1 --> n0
    click n1 "../modules/installed_wheel_postgresql_qualification.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 5 | 5 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_psycopg_url` | `(sqlalchemy_url: str) -> str` | — | — |
| `_database_url` | `(admin_url: str, database_name: str) -> str` | — | — |
| `_target_identifier` | `(database_url: str) -> str` | — | — |
| `_phase_environment` | `(*, database_url: str, role: str) -> dict[str, str]` | — | — |
| `_run_phase` | `(phase: str, *, workspace: Path, database_url: str, role: str, target: str \| None = None, maintenance_mode: str = 'off') -> None` | — | — |
| `_create_database` | `(admin_url: str, database_name: str, runtime_role: str) -> None` | — | — |
| `_drop_database` | `(admin_url: str, database_name: str, runtime_role: str) -> None` | — | — |
| `_assert_installed_package` | `() -> None` | — | — |
| `_source_phase` | `(workspace: Path) -> None` | — | — |
| `_target_phase` | `(workspace: Path, authorized_target: str) -> None` | — | — |
| `_maintenance_phase` | `(expected_mode: str) -> None` | — | — |
| `_coordinate` | `(admin_url: str) -> None` | — | — |
| `_parser` | `() -> argparse.ArgumentParser` | — | — |
| `main` | `() -> int` | — | — |
