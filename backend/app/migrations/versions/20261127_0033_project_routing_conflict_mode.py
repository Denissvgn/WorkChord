"""Let a project refuse or only warn about task routing that conflicts with its review policy."""

from alembic import op
import sqlalchemy as sa


revision = "20261127_0033"
down_revision = "20261127_0032"
branch_labels = None
depends_on = None

MODE_CHECK = "routing_conflict_mode IN ('refuse', 'warn')"


def upgrade() -> None:
    # Existing projects refuse a conflicting routing; only tasks with structured routing are checked.
    if op.get_bind().dialect.name == "sqlite":
        # Adding the column in place keeps the table definition, including AUTOINCREMENT.
        op.execute(
            "ALTER TABLE projects ADD COLUMN routing_conflict_mode VARCHAR(16) DEFAULT 'refuse' NOT NULL "
            f"CONSTRAINT ck_projects_routing_conflict_mode CHECK ({MODE_CHECK})"
        )
        return
    op.add_column("projects", sa.Column("routing_conflict_mode", sa.String(16), nullable=False, server_default="refuse"))
    op.create_check_constraint("ck_projects_routing_conflict_mode", "projects", MODE_CHECK)


def downgrade() -> None:
    if op.get_bind().dialect.name == "sqlite":
        # SQLite drops a column only without a constraint that names it, so the table is rebuilt.
        with op.batch_alter_table("projects", recreate="always", table_kwargs={"sqlite_autoincrement": True}) as batch:
            batch.drop_constraint("ck_projects_routing_conflict_mode", type_="check")
            batch.drop_column("routing_conflict_mode")
        return
    op.drop_constraint("ck_projects_routing_conflict_mode", "projects", type_="check")
    op.drop_column("projects", "routing_conflict_mode")
