"""Database upgrade and schema-version helpers."""
from __future__ import annotations

import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import shutil
from typing import Iterator, Literal, Optional

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.database_config import (
    DatabaseConfiguration,
    alembic_safe_url,
    parse_database_configuration,
)


LEGACY_BASELINE_REVISION = "20260506_0000"
MIGRATION_ADVISORY_LOCK_KEY = 0x574F524B43484F52

# Upgrade classification is closed because every unknown state must fail safely
# before a migration mutates persistent data.
DatabaseState = Literal[
    "empty",
    "legacy_pre_backlog",
    "alembic_managed",
    "unversioned_current",
    "unknown",
]

LEGACY_CORE_TABLES = {
    "calendars",
    "iterations",
    "team_members",
    "vacations",
    "tasks",
    "task_dependencies",
    "task_status_logs",
}

CURRENT_SENTINEL_TABLES = {
    "agent_actors",
    "projects",
    "triage_items",
    "work_templates",
    "label_groups",
    "saved_views",
    "project_updates",
    "project_milestones",
    "initiatives",
    "external_links",
    "github_status_automation_rules",
    "releases",
    "request_sources",
    "outbound_webhook_targets",
    "team_member_profiles",
    "system_settings",
}


class UpgradeError(RuntimeError):
    """Raised when a database cannot be upgraded safely."""


@dataclass(frozen=True)
class DatabaseStatus:
    """Inspected database schema state."""

    state: DatabaseState
    current_revision: Optional[str]
    head_revision: str
    table_count: int
    tables: list[str]

    @property
    def is_current(self) -> bool:
        return self.current_revision == self.head_revision

    @property
    def needs_upgrade(self) -> bool:
        upgradable_states = {
            "empty",
            "legacy_pre_backlog",
            "alembic_managed",
            "unversioned_current",
        }
        return self.state in upgradable_states and not self.is_current


def migrations_dir() -> Path:
    """Return the packaged Alembic migration directory."""
    return Path(__file__).resolve().parents[1] / "migrations"


def database_configuration() -> DatabaseConfiguration:
    """Return the shared validated database configuration."""

    return parse_database_configuration(get_settings())


def alembic_config(*, connection: Connection | None = None) -> Config:
    """Build an Alembic config independent of the caller's cwd."""
    migrations = migrations_dir()
    config = Config(str(migrations / "alembic.ini"))
    config.set_main_option("script_location", str(migrations))
    config.set_main_option(
        "sqlalchemy.url",
        alembic_safe_url(database_configuration().sync_url),
    )
    if connection is not None:
        config.attributes["connection"] = connection
    return config


def sync_database_url() -> str:
    """Return a sync SQLAlchemy URL for Alembic/schema inspection."""

    return database_configuration().sync_url.render_as_string(hide_password=False)


def head_revision() -> str:
    """Return the single Alembic head revision."""
    script = ScriptDirectory.from_config(alembic_config())
    heads = script.get_heads()
    if len(heads) != 1:
        raise UpgradeError(f"Expected one Alembic head, found: {', '.join(heads)}")
    return heads[0]


def _sync_engine(configuration: DatabaseConfiguration | None = None) -> Engine:
    configuration = configuration or database_configuration()
    return create_engine(
        configuration.sync_url,
        poolclass=NullPool,
        connect_args=dict(configuration.connect_args),
    )


def _current_revision(connection: Connection) -> Optional[str]:
    inspector = inspect(connection)
    if "alembic_version" not in inspector.get_table_names():
        return None
    result = connection.execute(text("SELECT version_num FROM alembic_version"))
    values = [row[0] for row in result.fetchall()]
    if not values:
        return None
    if len(values) > 1:
        return ",".join(sorted(values))
    return values[0]


def _inspect_database_connection(connection: Connection) -> DatabaseStatus:
    inspector = inspect(connection)
    tables = sorted(inspector.get_table_names())
    current = _current_revision(connection)
    table_set = set(tables)
    head = head_revision()

    if current is not None:
        state = "alembic_managed"
    elif not table_set or table_set == {"alembic_version"}:
        state = "empty"
    elif LEGACY_CORE_TABLES.issubset(table_set) and not (CURRENT_SENTINEL_TABLES & table_set):
        state = "legacy_pre_backlog"
    elif LEGACY_CORE_TABLES.issubset(table_set) and CURRENT_SENTINEL_TABLES.issubset(table_set):
        state = "unversioned_current"
    else:
        state = "unknown"

    return DatabaseStatus(
        state=state,
        current_revision=current,
        head_revision=head,
        table_count=len(tables),
        tables=tables,
    )


def inspect_database(*, connection: Connection | None = None) -> DatabaseStatus:
    """Classify the configured database without mutating it."""

    if connection is not None:
        return _inspect_database_connection(connection)
    engine = _sync_engine()
    try:
        with engine.connect() as owned_connection:
            return _inspect_database_connection(owned_connection)
    finally:
        engine.dispose()


def sqlite_database_path() -> Optional[Path]:
    """Return the configured SQLite database path, if applicable."""
    configuration = database_configuration()
    if configuration.backend != "sqlite":
        return None
    url = configuration.sync_url
    database = url.database
    if not database or database == ":memory:":
        return None
    path = Path(database)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def backup_sqlite_database(backup_dir: Optional[Path] = None) -> Optional[Path]:
    """Create a timestamped SQLite backup and return its path."""
    db_path = sqlite_database_path()
    if db_path is None or not db_path.exists():
        return None
    target_dir = backup_dir or db_path.parent / "backups"
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    backup_path = target_dir / f"{db_path.name}.{timestamp}.bak"
    shutil.copy2(db_path, backup_path)
    return backup_path


async def run_post_migration_repairs() -> None:
    """Run idempotent seeders and compatibility repairs after migrations."""
    from app.maintenance import require_background_writes_enabled
    from app.database import async_session_maker
    from app.services.calendar_service import CalendarService
    from app.services.github_status_automation_service import GitHubStatusAutomationService
    from app.services.label_service import LabelService
    from app.services.saved_view_service import SavedViewService
    from app.services.system_settings_service import RuntimeSettingsService
    from app.services.template_service import TemplateService

    require_background_writes_enabled("database repair and default seeding")
    async with async_session_maker() as db:
        await CalendarService(db).get_or_create_default()
        await TemplateService(db).seed_default_templates()
        await LabelService(db).seed_default_labels()
        await SavedViewService(db).seed_default_views()
        await GitHubStatusAutomationService(db).seed_default_rules()
        await RuntimeSettingsService(db).migrate_legacy_email_settings()


@contextmanager
def migration_connection() -> Iterator[Connection]:
    """Yield one NullPool connection holding the cross-runner migration lock."""

    configuration = database_configuration()
    engine = _sync_engine(configuration)
    try:
        with engine.connect() as connection:
            if configuration.backend == "postgresql":
                connection.execute(
                    text("SELECT pg_advisory_lock(:lock_key)"),
                    {"lock_key": MIGRATION_ADVISORY_LOCK_KEY},
                )
                # Session advisory locks survive transaction boundaries. Commit
                # the lock query so Alembic can own its DDL transaction.
                connection.commit()
            try:
                yield connection
            finally:
                if connection.in_transaction():
                    connection.rollback()
                if configuration.backend == "postgresql":
                    connection.execute(
                        text("SELECT pg_advisory_unlock(:lock_key)"),
                        {"lock_key": MIGRATION_ADVISORY_LOCK_KEY},
                    )
                    connection.commit()
    finally:
        engine.dispose()


def _validate_managed_revision(status: DatabaseStatus) -> None:
    if status.state != "alembic_managed" or status.current_revision is None:
        return
    known_revisions = {
        revision.revision
        for revision in ScriptDirectory.from_config(alembic_config()).walk_revisions()
    }
    current_revisions = set(status.current_revision.split(","))
    unknown = sorted(current_revisions - known_revisions)
    if unknown:
        raise UpgradeError(
            "Database reports unknown Alembic revision(s): " + ", ".join(unknown)
        )


def _application_tables_with_rows(connection: Connection) -> list[str]:
    inspector = inspect(connection)
    quote = connection.dialect.identifier_preparer.quote
    populated: list[str] = []
    for table_name in sorted(
        set(inspector.get_table_names()) - {"alembic_version"}
    ):
        statement = text(f"SELECT 1 FROM {quote(table_name)} LIMIT 1")
        if connection.execute(statement).first() is not None:
            populated.append(table_name)
    return populated


def _backup_precondition(
    *,
    before: DatabaseStatus,
    backup: bool,
    backup_dir: Optional[Path],
    external_backup_reference: str | None,
) -> Optional[Path]:
    if before.state == "empty":
        return None
    configuration = database_configuration()
    if configuration.backend == "postgresql":
        if not external_backup_reference or not external_backup_reference.strip():
            raise UpgradeError(
                "Non-empty PostgreSQL upgrades require --external-backup-reference "
                "confirming an operator-verified backup/PITR recovery point."
            )
        return None
    if not backup:
        return None
    backup_path = backup_sqlite_database(backup_dir)
    if backup_path is None:
        raise UpgradeError("Configured SQLite database could not be backed up")
    return backup_path


def _run_schema_upgrade(
    connection: Connection,
    before: DatabaseStatus,
    *,
    stamp_unversioned_current: bool,
) -> None:
    config = alembic_config(connection=connection)
    if connection.in_transaction():
        connection.commit()
    if before.state == "legacy_pre_backlog":
        command.stamp(config, LEGACY_BASELINE_REVISION)
        command.upgrade(config, "head")
    elif before.state == "unversioned_current":
        if not stamp_unversioned_current:
            raise UpgradeError(
                "Database looks current but lacks alembic_version. "
                "Rerun without --no-stamp-unversioned-current to mark it as managed."
            )
        command.stamp(config, "head")
    else:
        command.upgrade(config, "head")


def run_alembic_upgrade(
    *,
    backup: bool = True,
    backup_dir: Optional[Path] = None,
    stamp_unversioned_current: bool = True,
    run_repairs: bool = True,
    external_backup_reference: str | None = None,
    require_empty: bool = False,
) -> tuple[DatabaseStatus, Optional[Path], DatabaseStatus]:
    """Upgrade the configured database to the current Alembic head."""
    with migration_connection() as connection:
        before = inspect_database(connection=connection)
        if before.state == "unknown":
            raise UpgradeError(
                "Database schema is not recognized. Refusing to run migrations automatically."
            )
        _validate_managed_revision(before)
        if require_empty and before.state != "empty":
            raise UpgradeError(
                f"Schema-only bootstrap requires an empty database; found {before.state}"
            )

        if before.is_current and before.state == "alembic_managed":
            if run_repairs:
                asyncio.run(run_post_migration_repairs())
            return before, None, inspect_database(connection=connection)

        backup_path = _backup_precondition(
            before=before,
            backup=backup,
            backup_dir=backup_dir,
            external_backup_reference=external_backup_reference,
        )
        _run_schema_upgrade(
            connection,
            before,
            stamp_unversioned_current=stamp_unversioned_current,
        )

        if require_empty:
            populated = _application_tables_with_rows(connection)
            if populated:
                raise UpgradeError(
                    "Schema-only bootstrap created application rows in: "
                    + ", ".join(populated)
                )
        if run_repairs:
            asyncio.run(run_post_migration_repairs())

        after = inspect_database(connection=connection)
        return before, backup_path, after


def bootstrap_database_schema() -> tuple[DatabaseStatus, None, DatabaseStatus]:
    """Migrate an empty target without creating application-owned rows."""

    before, _backup, after = run_alembic_upgrade(
        backup=False,
        run_repairs=False,
        require_empty=True,
    )
    return before, None, after


def run_database_repairs() -> tuple[DatabaseStatus, DatabaseStatus]:
    """Run serialized post-copy seed/compatibility repairs on a current schema."""

    with migration_connection() as connection:
        before = inspect_database(connection=connection)
        _validate_managed_revision(before)
        if before.state != "alembic_managed" or not before.is_current:
            raise UpgradeError(
                "Post-copy repairs require an Alembic-current managed schema"
            )
        asyncio.run(run_post_migration_repairs())
        return before, inspect_database(connection=connection)


def assert_database_current() -> None:
    """Raise a clear error when the app database is not Alembic-current."""
    status = inspect_database()
    if status.state == "alembic_managed" and status.is_current:
        return
    raise UpgradeError(
        "Database schema is not ready. Run "
        "`cd backend && DATABASE_PROCESS_ROLE=migration DATABASE_POOL_SIZE=1 "
        "DATABASE_MAX_OVERFLOW=0 ../.venv/bin/python -m app.cli.upgrade --no-repairs` "
        "before starting the API. "
        f"Detected state={status.state}, revision={status.current_revision or 'none'}, "
        f"head={status.head_revision}."
    )
