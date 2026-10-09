"""Preserve project allocation identity across retained history."""

from alembic import op
from sqlalchemy import text

from app.database_migration.project_identity import project_allocation_floor


revision = "20261008_0009"
down_revision = "20261007_0008"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    floor = project_allocation_floor(connection)
    if connection.dialect.name == "sqlite":
        if connection.scalar(text("PRAGMA foreign_keys")):
            raise RuntimeError("Project table rebuild requires the serialized SQLite migration environment")
        with op.batch_alter_table("projects", recreate="always", table_kwargs={"sqlite_autoincrement": True}):
            pass
        connection.execute(text("DELETE FROM sqlite_sequence WHERE name='projects'"))
        connection.execute(text("INSERT INTO sqlite_sequence(name,seq) VALUES ('projects',:floor)"), {"floor": floor})
    elif connection.dialect.name == "postgresql":
        sequence = connection.scalar(text("SELECT pg_get_serial_sequence('projects','id')"))
        if sequence:
            quoted = ".".join(connection.dialect.identifier_preparer.quote(part.strip('"')) for part in sequence.split("."))
            current, called = connection.execute(text(f"SELECT last_value,is_called FROM {quoted}")).one()
            if floor > current or floor == current and floor > 0 and not called:
                connection.execute(text("SELECT setval(CAST(:sequence AS regclass),:floor,true)"), {"sequence": sequence, "floor": floor})


def downgrade():
    raise RuntimeError("Retained project identity cannot be downgraded; restore the matching verified backup")
