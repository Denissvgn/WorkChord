"""Preserve profile lifetimes across recovery and deletion."""

from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from app.database_migration.allocation_identity import allocation_floor


revision = "20261009_0011"
down_revision = "20261009_0010"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    floor = allocation_floor(connection, "team_member_profiles")
    op.add_column("team_member_profiles", sa.Column("profile_token", sa.String(36), nullable=True))
    members = sa.table("team_member_profiles", sa.column("id", sa.Integer), sa.column("profile_token", sa.String(36)))
    for identifier in connection.scalars(sa.select(members.c.id)):
        connection.execute(members.update().where(members.c.id == identifier).values(profile_token=str(uuid4())))
    if connection.dialect.name == "sqlite" and connection.scalar(sa.text("PRAGMA foreign_keys")):
        raise RuntimeError("Profile table rebuild requires the serialized SQLite migration environment")
    with op.batch_alter_table("team_member_profiles", recreate="always" if connection.dialect.name == "sqlite" else "auto", table_kwargs={"sqlite_autoincrement": True}) as batch:
        batch.alter_column("profile_token", existing_type=sa.String(36), nullable=False)
        batch.create_unique_constraint("uq_team_member_profiles_profile_token", ["profile_token"])
    if connection.dialect.name == "sqlite":
        connection.execute(sa.text("DELETE FROM sqlite_sequence WHERE name='team_member_profiles'"))
        connection.execute(sa.text("INSERT INTO sqlite_sequence(name,seq) VALUES ('team_member_profiles',:floor)"), {"floor": floor})
    elif connection.dialect.name == "postgresql":
        sequence = connection.scalar(sa.text("SELECT pg_get_serial_sequence('team_member_profiles','id')"))
        if sequence:
            quoted = ".".join(connection.dialect.identifier_preparer.quote(part.strip('"')) for part in sequence.split("."))
            current, called = connection.execute(sa.text(f"SELECT last_value,is_called FROM {quoted}")).one()
            if floor > current or floor == current and floor > 0 and not called:
                connection.execute(sa.text("SELECT setval(CAST(:sequence AS regclass),:floor,true)"), {"sequence": sequence, "floor": floor})


def downgrade():
    raise RuntimeError("Profile lifetime provenance cannot be downgraded; restore the matching verified backup")
