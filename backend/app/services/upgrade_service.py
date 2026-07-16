"""Database upgrade and schema-version helpers."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import shutil
from typing import Literal, Optional

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import make_url

from app.config import get_settings


LEGACY_BASELINE_REVISION = "20260506_0000"

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


def alembic_config() -> Config:
    """Build an Alembic config independent of the caller's cwd."""
    migrations = migrations_dir()
    config = Config(str(migrations / "alembic.ini"))
    config.set_main_option("script_location", str(migrations))
    return config


def sync_database_url() -> str:
    """Return a sync SQLAlchemy URL for Alembic/schema inspection."""
    return get_settings().database_url.replace("+aiosqlite", "")


def head_revision() -> str:
    """Return the single Alembic head revision."""
    script = ScriptDirectory.from_config(alembic_config())
    heads = script.get_heads()
    if len(heads) != 1:
        raise UpgradeError(f"Expected one Alembic head, found: {', '.join(heads)}")
    return heads[0]


def _current_revision(engine) -> Optional[str]:
    inspector = inspect(engine)
    if "alembic_version" not in inspector.get_table_names():
        return None
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version_num FROM alembic_version"))
        values = [row[0] for row in result.fetchall()]
    if not values:
        return None
    if len(values) > 1:
        return ",".join(sorted(values))
    return values[0]


def inspect_database() -> DatabaseStatus:
    """Classify the configured database without mutating it."""
    engine = create_engine(sync_database_url())
    try:
        inspector = inspect(engine)
        tables = sorted(inspector.get_table_names())
        current = _current_revision(engine)
    finally:
        engine.dispose()

    table_set = set(tables)
    head = head_revision()

    if not table_set or table_set == {"alembic_version"}:
        state: DatabaseState = "empty"
    elif current is not None:
        state = "alembic_managed"
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


def sqlite_database_path() -> Optional[Path]:
    """Return the configured SQLite database path, if applicable."""
    url = make_url(sync_database_url())
    if not url.drivername.startswith("sqlite"):
        return None
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
    from app.database import async_session_maker
    from app.services.calendar_service import CalendarService
    from app.services.github_status_automation_service import GitHubStatusAutomationService
    from app.services.label_service import LabelService
    from app.services.saved_view_service import SavedViewService
    from app.services.system_settings_service import RuntimeSettingsService
    from app.services.template_service import TemplateService

    async with async_session_maker() as db:
        await CalendarService(db).get_or_create_default()
        await TemplateService(db).seed_default_templates()
        await LabelService(db).seed_default_labels()
        await SavedViewService(db).seed_default_views()
        await GitHubStatusAutomationService(db).seed_default_rules()
        await RuntimeSettingsService(db).migrate_legacy_email_settings()


def run_alembic_upgrade(
    *,
    backup: bool = True,
    backup_dir: Optional[Path] = None,
    stamp_unversioned_current: bool = True,
    run_repairs: bool = True,
) -> tuple[DatabaseStatus, Optional[Path], DatabaseStatus]:
    """Upgrade the configured database to the current Alembic head."""
    before = inspect_database()
    backup_path: Optional[Path] = None

    if before.state == "unknown":
        raise UpgradeError(
            "Database schema is not recognized. Refusing to run migrations automatically."
        )

    if before.is_current and before.state == "alembic_managed":
        if run_repairs:
            asyncio.run(run_post_migration_repairs())
        return before, None, inspect_database()

    if backup and before.state != "empty":
        backup_path = backup_sqlite_database(backup_dir)
        if backup_path is None and sqlite_database_path() is None and before.state != "empty":
            raise UpgradeError(
                "Automatic backups are only supported for SQLite. "
                "Create an external database backup or rerun with --skip-backup."
            )

    config = alembic_config()
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

    if run_repairs:
        asyncio.run(run_post_migration_repairs())

    return before, backup_path, inspect_database()


def assert_database_current() -> None:
    """Raise a clear error when the app database is not Alembic-current."""
    status = inspect_database()
    if status.state == "alembic_managed" and status.is_current:
        return
    raise UpgradeError(
        "Database schema is not ready. Run "
        "`cd backend && ../.venv/bin/python -m app.cli.upgrade` before starting the API. "
        f"Detected state={status.state}, revision={status.current_revision or 'none'}, "
        f"head={status.head_revision}."
    )
