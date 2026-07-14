"""create releases

Revision ID: 20260509_0016
Revises: 20260509_0015
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0016"
down_revision: Union[str, None] = "20260509_0015"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "releases",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="planned",
        ),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("shipped_at", sa.DateTime(), nullable=True),
        sa.Column("version", sa.String(length=100), nullable=True),
        sa.Column("environment", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "status IN ('planned', 'building', 'shipped', 'canceled')",
            name="ck_releases_status",
        ),
    )
    op.create_index("ix_releases_project_id", "releases", ["project_id"])
    op.create_index("ix_releases_status", "releases", ["status"])
    op.create_index("ix_releases_target_date", "releases", ["target_date"])
    op.create_index(
        "ix_releases_project_status_date",
        "releases",
        ["project_id", "status", "target_date", "id"],
    )

    op.create_table(
        "release_tasks",
        sa.Column(
            "release_id",
            sa.Integer(),
            sa.ForeignKey("releases.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "task_id",
            sa.Integer(),
            sa.ForeignKey("tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("release_id", "task_id", name="pk_release_tasks"),
    )
    op.create_index("ix_release_tasks_task_id", "release_tasks", ["task_id"])


def downgrade() -> None:
    op.drop_index("ix_release_tasks_task_id", table_name="release_tasks")
    op.drop_table("release_tasks")

    op.drop_index("ix_releases_project_status_date", table_name="releases")
    op.drop_index("ix_releases_target_date", table_name="releases")
    op.drop_index("ix_releases_status", table_name="releases")
    op.drop_index("ix_releases_project_id", table_name="releases")
    op.drop_table("releases")
