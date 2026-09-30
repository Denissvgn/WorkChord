"""Initial task-domain constraints, evidence retention and identity fences."""

from datetime import date

from alembic import command
from sqlalchemy import Boolean, Date, DateTime, Float, Integer, JSON, MetaData, select
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
import pytest

from app.utils.time import utc_now
from tests.test_authority_migrations import initial_database


def insert_fixture(connection, table, **values):
    """Fill required scalar data while every relationship remains explicitly supplied."""
    for column in table.columns:
        if column.name in values or column.nullable or column.server_default is not None:
            continue
        if isinstance(column.type, Boolean):
            values[column.name] = False
        elif isinstance(column.type, Integer):
            values[column.name] = 1
        elif isinstance(column.type, Float):
            values[column.name] = 1.0
        elif isinstance(column.type, DateTime):
            values[column.name] = utc_now()
        elif isinstance(column.type, Date):
            values[column.name] = date(2026, 1, 1)
        elif isinstance(column.type, JSON):
            values[column.name] = {}
        else:
            values[column.name] = "fixture"
    connection.execute(table.insert().values(**values))


def test_deletion_fence_survives_without_tasks(initial_database):
    config, engine = initial_database
    command.upgrade(config, "head")
    schema = MetaData()
    schema.reflect(engine)
    fence = schema.tables["task_deletion_fences"]
    assert inspect(engine).get_foreign_keys(fence.name) == []
    with engine.begin() as db:
        assert db.execute(select(fence)).all() == []
        db.execute(fence.insert().values(original_task_id=9001, last_version=17))
    with engine.begin() as db:
        assert db.execute(select(fence.c.last_version).where(fence.c.original_task_id == 9001)).scalar_one() == 17
    with pytest.raises(IntegrityError), engine.begin() as db:
        db.execute(fence.insert().values(original_task_id=9002, last_version=0))


def test_initial_schema_enforces_scope_and_retains_deleted_task_evidence(initial_database):
    _config, engine = initial_database
    schema = MetaData()
    schema.reflect(engine)
    tables = schema.tables
    with engine.begin() as db:
        insert_fixture(db, tables['projects'], id=61, name='Project', status='planned', health='unknown')
        insert_fixture(db, tables['tasks'], id=101, project_id=61, title='Backlog work',
                       status='planned', effort_days=None, effort_hours=None, tags='[]')
        insert_fixture(db, tables['tasks'], id=102, project_id=61, parent_id=101,
                       title='Child', status='planned', effort_days=None, effort_hours=None, tags='[]')
        insert_fixture(db, tables['task_brief_revisions'], id=201, task_id=102, original_task_id=102,
                       task_version=7, revision=1, payload={'objective': 'Preserve'}, provenance='explicit')
        assert db.execute(select(tables['tasks'].c.effort_hours).where(tables['tasks'].c.id == 101)).scalar_one() is None
    for values in ({'project_id': None}, {'effort_hours': -1}, {'nominal_day_hours': 0}):
        with pytest.raises(IntegrityError), engine.begin() as db:
            db.execute(tables['tasks'].update().where(tables['tasks'].c.id == 101).values(**values))
    with pytest.raises(IntegrityError), engine.begin() as db:
        db.execute(tables['tasks'].delete().where(tables['tasks'].c.id == 101))
    with engine.begin() as db:
        # Subtrees are removed child-first by the application; the FK prevents orphans.
        db.execute(tables['tasks'].delete().where(tables['tasks'].c.id == 102))
        db.execute(tables['tasks'].delete().where(tables['tasks'].c.id == 101))
        history = db.execute(select(tables['task_brief_revisions'])).mappings().one()
        assert history['task_id'] is None
        assert history['original_task_id'] == 102 and history['task_version'] == 7
        assert history['payload'] == {'objective': 'Preserve'}
        assert db.execute(select(tables['tasks'])).all() == []
        if engine.dialect.name == 'sqlite':
            assert db.exec_driver_sql('PRAGMA foreign_key_check').all() == []
