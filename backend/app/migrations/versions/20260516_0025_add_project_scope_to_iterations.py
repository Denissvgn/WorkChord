"""Add optional project scope to iterations.

Revision ID: 20260516_0025
Revises: 20260515_0024
Create Date: 2026-05-16
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260516_0025"
down_revision: str | None = "20260515_0024"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("iterations") as batch_op:
        batch_op.add_column(sa.Column("project_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_iterations_project_id", ["project_id"])
        batch_op.create_foreign_key(
            "fk_iterations_project_id_projects",
            "projects",
            ["project_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("iterations") as batch_op:
        batch_op.drop_constraint(
            "fk_iterations_project_id_projects",
            type_="foreignkey",
        )
        batch_op.drop_index("ix_iterations_project_id")
        batch_op.drop_column("project_id")
