"""The packaged initial schema and fail-closed development reset boundary."""

from pathlib import Path

from alembic import command
from alembic.script import ScriptDirectory
import pytest
from sqlalchemy import CheckConstraint, create_engine, text

from app.services.upgrade_service import (
    UpgradeError, alembic_config, bootstrap_database_schema,
    head_revision, inspect_database, run_alembic_upgrade,
)


def test_initial_schema_is_one_frozen_revision():
    scripts = ScriptDirectory.from_config(alembic_config())
    revisions = list(scripts.walk_revisions())
    roots = [revision for revision in revisions if revision.down_revision is None]
    assert len(roots) == 1
    assert roots[0].revision == "20260928_0001"
    assert len(scripts.get_heads()) == 1
    source = Path(roots[0].path).read_text()
    assert "app.models" not in source
    assert "Base.metadata" not in source
    assert "create_all" not in source


@pytest.mark.sqlite
@pytest.mark.parametrize("revision", ["20260506_0000", "20260916_0039", None])
def test_unreleased_databases_are_refused_without_mutation(tmp_path, configure_database, revision):
    path = tmp_path / 'unreleased.db'
    configure_database(f'sqlite+aiosqlite:///{path}')
    # A complete-looking unversioned database must not be stamped from table names.
    bootstrap_database_schema()
    engine = create_engine(f'sqlite:///{path}')
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO task_deletion_fences VALUES (917, 42)"))
        if revision is None:
            connection.execute(text("DROP TABLE alembic_version"))
        else:
            connection.execute(text("UPDATE alembic_version SET version_num=:revision"), {'revision': revision})
    before = path.read_bytes()
    with pytest.raises(UpgradeError, match="empty database"):
        run_alembic_upgrade(backup=False, run_repairs=False)
    assert path.read_bytes() == before
    engine.dispose()


@pytest.mark.sqlite
def test_current_upgrade_is_idempotent_and_downgrade_is_refused(tmp_path, configure_database):
    path = tmp_path / 'current.db'
    configure_database(f'sqlite+aiosqlite:///{path}')
    bootstrap_database_schema()
    engine = create_engine(f'sqlite:///{path}')
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO task_deletion_fences VALUES (918, 43)"))
    run_alembic_upgrade(backup=False, run_repairs=False)
    with pytest.raises(RuntimeError, match="cannot be downgraded|immutable history"):
        command.downgrade(alembic_config(), 'base')
    assert inspect_database().current_revision == head_revision()
    with engine.connect() as connection:
        assert connection.execute(text('SELECT last_version FROM task_deletion_fences')).scalar_one() == 43
    engine.dispose()


@pytest.mark.sqlite
def test_current_bootstrap_keeps_model_foreign_keys_and_checks(tmp_path, configure_database):
    from sqlalchemy import inspect
    from app.database import Base

    path = tmp_path / 'constraints.db'
    configure_database(f'sqlite+aiosqlite:///{path}')
    bootstrap_database_schema()
    engine = create_engine(f'sqlite:///{path}')
    inspector = inspect(engine)
    try:
        for name, table in Base.metadata.tables.items():
            live_keys = {
                (tuple(key['constrained_columns']), key['referred_table'],
                 tuple(key['referred_columns']), key['options'].get('ondelete'))
                for key in inspector.get_foreign_keys(name)
            }
            for key in table.foreign_key_constraints:
                assert (tuple(column.name for column in key.columns), key.referred_table.name,
                        tuple(element.column.name for element in key.elements), key.ondelete) in live_keys, name
            live_checks = {check['name'] for check in inspector.get_check_constraints(name)}
            expected_checks = {constraint.name for constraint in table.constraints
                               if isinstance(constraint, CheckConstraint)}
            assert expected_checks <= live_checks, name
        with engine.connect() as connection:
            assert connection.exec_driver_sql('PRAGMA foreign_key_check').all() == []
            task_sql = connection.execute(text("SELECT sql FROM sqlite_master WHERE name='tasks'")).scalar_one()
            assert 'AUTOINCREMENT' in task_sql
    finally:
        engine.dispose()
