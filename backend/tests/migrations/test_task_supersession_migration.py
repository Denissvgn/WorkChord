"""Supersession dispositions migrate reversibly; existing replacements keep their basis and none is dropped silently."""

import importlib
from datetime import datetime, timezone

import pytest
from alembic import command
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.exc import IntegrityError

from app.models.project import Project
from app.models.task import Task
from app.models.task_replacement import TaskReplacement
from app.services.upgrade_service import alembic_config

MIGRATION = importlib.import_module("app.migrations.versions.20261127_0030_task_supersession")
PREVIOUS, CURRENT = MIGRATION.down_revision, MIGRATION.revision


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_supersession_migration_keeps_replacements_and_refuses_losing_supersessions(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_task_supersession_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    replacements, tasks = TaskReplacement.__table__, Task.__table__
    decided = datetime(2026, 11, 27, tzinfo=timezone.utc)
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            project = db.execute(Project.__table__.insert().values(name="Importer")).inserted_primary_key[0]
            original, replacement, superseded, successor = (
                db.execute(tasks.insert().values(title=title, project_id=project, version=2)).inserted_primary_key[0]
                for title in ("Original", "Replacement", "Superseded", "Successor")
            )
            common = dict(project_id=project, reason="Unknown publisher", carried_run_ids=[], moved_dependencies=[],
                          moved_release_ids=[], original_snapshot={}, review_policy={}, decided_at=decided)
            existing = dict(common, original_task_id=original, replacement_task_id=replacement,
                            owner_decision="Owner approved", base_commit_url="https://github.com/o/r/commit/" + "0" * 40)
            db.execute(_legacy_insert(db, existing))
            db.commit()
            for attempt in range(2):
                command.upgrade(config, CURRENT)
                rows = db.execute(select(replacements.c.disposition, replacements.c.owner_decision)).all()
                assert rows == [("replacement", "Owner approved")]
                checks = {check["name"] for check in inspect(db).get_check_constraints("task_replacements")}
                assert {"ck_task_replacements_distinct", "ck_task_replacements_disposition",
                        "ck_task_replacements_replacement_basis"} <= checks
                supersession = dict(common, original_task_id=superseded, replacement_task_id=successor,
                                    disposition="supersession", owner_decision=None, base_commit_url=None)
                db.execute(replacements.insert().values(**supersession))
                db.commit()
                # A replacement still needs its base commit and owner decision.
                with pytest.raises(IntegrityError):
                    db.execute(replacements.insert().values(**dict(supersession, original_task_id=successor,
                                                                   replacement_task_id=superseded,
                                                                   disposition="replacement")))
                db.rollback()
                with pytest.raises(IntegrityError):
                    db.execute(replacements.insert().values(**dict(supersession, original_task_id=successor,
                                                                   replacement_task_id=superseded,
                                                                   disposition="unknown")))
                db.rollback()
                with pytest.raises(RuntimeError, match="export them before downgrading"):
                    command.downgrade(config, PREVIOUS)
                db.rollback()
                assert len(db.execute(select(replacements)).all()) == 2
                db.execute(replacements.delete().where(replacements.c.disposition == "supersession"))
                db.commit()
                if attempt == 0:
                    command.downgrade(config, PREVIOUS)
                    columns = {column["name"]: column for column in inspect(db).get_columns("task_replacements")}
                    assert "disposition" not in columns
                    assert not columns["base_commit_url"]["nullable"] and not columns["owner_decision"]["nullable"]
                    checks = {check["name"] for check in inspect(db).get_check_constraints("task_replacements")}
                    assert "ck_task_replacements_distinct" in checks
                    assert len(db.execute(select(replacements.c.id)).all()) == 1
                    db.commit()
    finally:
        engine.dispose()


def _legacy_insert(db, values):
    """Insert through the pre-upgrade table shape, which has no disposition column."""
    from sqlalchemy import MetaData, Table
    table = Table("task_replacements", MetaData(), autoload_with=db)
    return table.insert().values(**values)
