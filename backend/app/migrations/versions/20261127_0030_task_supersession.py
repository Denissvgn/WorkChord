"""Record a supersession: an original whose deliverable was already closed or accepted as another task."""

from alembic import op
import sqlalchemy as sa


revision = "20261127_0030"
down_revision = "20261126_0029"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Existing dispositions are clean replacements and keep their base commit and owner decision.
    with op.batch_alter_table("task_replacements") as batch:
        batch.add_column(sa.Column("disposition", sa.String(16), nullable=False, server_default="replacement"))
        batch.alter_column("owner_decision", existing_type=sa.Text(), nullable=True)
        batch.alter_column("base_commit_url", existing_type=sa.String(1000), nullable=True)
        batch.create_check_constraint("ck_task_replacements_disposition",
                                      "disposition IN ('replacement', 'supersession')")
        batch.create_check_constraint(
            "ck_task_replacements_replacement_basis",
            "disposition = 'supersession' OR (base_commit_url IS NOT NULL AND owner_decision IS NOT NULL)")


def downgrade() -> None:
    # An older server would read a supersession as a clean replacement with no base commit.
    connection = op.get_bind()
    table = sa.table("task_replacements", sa.column("disposition"))
    if connection.scalar(sa.select(sa.literal(1)).select_from(table).where(table.c.disposition != "replacement").limit(1)):
        raise RuntimeError("Task supersessions exist; export them before downgrading.")
    with op.batch_alter_table("task_replacements") as batch:
        batch.drop_constraint("ck_task_replacements_replacement_basis", type_="check")
        batch.drop_constraint("ck_task_replacements_disposition", type_="check")
        batch.alter_column("base_commit_url", existing_type=sa.String(1000), nullable=False)
        batch.alter_column("owner_decision", existing_type=sa.Text(), nullable=False)
        batch.drop_column("disposition")
