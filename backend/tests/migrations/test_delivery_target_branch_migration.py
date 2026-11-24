"""A delivery prerequisite's target branch migrates reversibly and is never dropped silently."""

import pytest
from alembic import command
from sqlalchemy import create_engine, inspect, select

from app.models.delivery_dependency import DeliveryDependency
from app.models.project import Project
from app.models.task import Task
from app.services.upgrade_service import alembic_config

PREVIOUS, CURRENT = "20261124_0023", "20261124_0024"


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_target_branch_migration_keeps_edges_and_refuses_losing_a_branch(dialect, request, tmp_path, configure_database):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_delivery_target_branch.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    edges, tasks = DeliveryDependency.__table__, Task.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            project = db.execute(Project.__table__.insert().values(name="Kernel")).inserted_primary_key[0]
            first, second = (
                db.execute(tasks.insert().values(title=title, project_id=project, version=1)).inserted_primary_key[0]
                for title in ("First", "Second")
            )
            db.execute(edges.insert().values(task_id=second, prerequisite_task_id=first))
            db.commit()
            command.upgrade(config, CURRENT)
            assert db.execute(select(edges.c.target_branch)).scalars().all() == [None]
            db.execute(edges.update().values(target_branch="main"))
            db.commit()
            with pytest.raises(RuntimeError, match="remove them before downgrading"):
                command.downgrade(config, PREVIOUS)
            db.rollback()
            db.execute(edges.update().values(target_branch=None))
            db.commit()
            command.downgrade(config, PREVIOUS)
            assert "target_branch" not in {column["name"] for column in inspect(db).get_columns("delivery_dependencies")}
            assert db.execute(select(edges.c.task_id)).scalars().all() == [second]
    finally:
        engine.dispose()
