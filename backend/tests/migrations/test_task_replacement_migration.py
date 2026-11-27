"""Clean-replacement dispositions migrate reversibly and an existing disposition is never dropped silently."""

from datetime import datetime, timezone

import pytest
from alembic import command
from sqlalchemy import MetaData, Table, create_engine, inspect, select
from sqlalchemy.exc import IntegrityError

from app.models.project import Project
from app.models.task import Task
from app.services.upgrade_service import alembic_config

PREVIOUS, CURRENT = "20261124_0022", "20261124_0023"


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_replacement_migration_keeps_tasks_and_refuses_losing_dispositions(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_task_replacement_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    tasks = Task.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            project = db.execute(Project.__table__.insert().values(name="Kernel")).inserted_primary_key[0]
            original, replacement = (
                db.execute(tasks.insert().values(title=title, project_id=project, version=3)).inserted_primary_key[0]
                for title in ("Original", "Replacement")
            )
            db.commit()
            for attempt in range(2):
                command.upgrade(config, CURRENT)
                # Later revisions add columns to the model, so read the table as this revision made it.
                replacements = Table("task_replacements", MetaData(), autoload_with=db)
                assert db.execute(select(replacements)).all() == []
                assert db.execute(select(tasks.c.version).order_by(tasks.c.id)).scalars().all() == [3, 3]
                checks = {check["name"] for check in inspect(db).get_check_constraints("task_replacements")}
                assert "ck_task_replacements_distinct" in checks
                row = dict(project_id=project, original_task_id=original, replacement_task_id=replacement,
                           reason="Unknown publisher", owner_decision="Owner approved", base_commit_url="https://github.com/o/r/commit/" + "0" * 40,
                           carried_run_ids=[], moved_dependencies=[], moved_release_ids=[], original_snapshot={},
                           review_policy={}, decided_at=datetime(2026, 11, 24, tzinfo=timezone.utc))
                db.execute(replacements.insert().values(**row))
                db.commit()
                # One disposition per original and per replacement.
                with pytest.raises(IntegrityError):
                    db.execute(replacements.insert().values(**row))
                db.rollback()
                with pytest.raises(RuntimeError, match="export them before downgrading"):
                    command.downgrade(config, PREVIOUS)
                db.rollback()
                assert len(db.execute(select(replacements)).all()) == 1
                db.execute(replacements.delete())
                db.commit()
                if attempt == 0:
                    command.downgrade(config, PREVIOUS)
                    assert not inspect(db).has_table("task_replacements")
                    db.commit()
    finally:
        engine.dispose()
