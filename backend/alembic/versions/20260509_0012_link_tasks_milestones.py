"""link tasks to project milestones

Revision ID: 20260509_0012
Revises: 20260509_0011
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0012"
down_revision: Union[str, None] = "20260509_0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("milestone_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_tasks_milestone_id_project_milestones",
            "project_milestones",
            ["milestone_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_index("ix_tasks_milestone_id", ["milestone_id"])


def downgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_index("ix_tasks_milestone_id")
        batch_op.drop_constraint(
            "fk_tasks_milestone_id_project_milestones",
            type_="foreignkey",
        )
        batch_op.drop_column("milestone_id")
