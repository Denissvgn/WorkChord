"""Review history gains a kind reversibly and never silently loses an owner override."""

import pytest
import sqlalchemy as sa
from alembic import command
from sqlalchemy import create_engine, inspect, select

from app.services.upgrade_service import alembic_config
from app.utils.time import utc_now

PREVIOUS, CURRENT = "20261126_0025", "20261126_0026"


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_review_kind_migration_marks_history_as_reviews_and_refuses_losing_an_override(dialect, request, tmp_path, configure_database):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_review_kind.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    columns = ("original_task_id", "task_version", "brief_revision", "artifact_revision", "verdict", "reason", "evidence", "created_at")
    reviews = sa.table("task_review_records", sa.column("id"), sa.column("kind"), *(sa.column(name) for name in columns))
    row = {"original_task_id": 7, "task_version": 2, "brief_revision": 0, "artifact_revision": 0,
           "verdict": "accept", "reason": "Checked", "evidence": "", "created_at": utc_now()}
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            db.execute(sa.table("task_review_records", *(sa.column(name) for name in columns)).insert().values(**row))
            db.commit()
            command.upgrade(config, CURRENT)
            assert db.execute(select(reviews.c.kind)).scalars().all() == ["review"]
            db.execute(reviews.insert().values(**{**row, "task_version": 3}, kind="owner_override"))
            db.commit()
            with pytest.raises(RuntimeError, match="cannot be downgraded"):
                command.downgrade(config, PREVIOUS)
            db.rollback()
            db.execute(reviews.delete().where(reviews.c.kind == "owner_override"))
            db.commit()
            command.downgrade(config, PREVIOUS)
            assert "kind" not in {column["name"] for column in inspect(db).get_columns("task_review_records")}
            assert db.execute(select(sa.column("task_version")).select_from(sa.table("task_review_records"))).scalars().all() == [2]
    finally:
        engine.dispose()
