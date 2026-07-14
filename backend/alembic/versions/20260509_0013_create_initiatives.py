"""create initiatives

Revision ID: 20260509_0013
Revises: 20260509_0012
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0013"
down_revision: Union[str, None] = "20260509_0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "initiatives",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "owner_id",
            sa.Integer(),
            sa.ForeignKey("team_members.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "health",
            sa.String(length=50),
            nullable=False,
            server_default="unknown",
        ),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "health IN ('unknown', 'on_track', 'at_risk', 'off_track')",
            name="ck_initiatives_health",
        ),
    )
    op.create_index("ix_initiatives_owner_id", "initiatives", ["owner_id"])
    op.create_index("ix_initiatives_health", "initiatives", ["health"])
    op.create_index("ix_initiatives_target_date", "initiatives", ["target_date"])
    op.create_index(
        "ix_initiatives_target_name",
        "initiatives",
        ["target_date", "name", "id"],
    )

    with op.batch_alter_table("projects") as batch_op:
        batch_op.add_column(sa.Column("initiative_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_projects_initiative_id_initiatives",
            "initiatives",
            ["initiative_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_index("ix_projects_initiative_id", ["initiative_id"])


def downgrade() -> None:
    with op.batch_alter_table("projects") as batch_op:
        batch_op.drop_index("ix_projects_initiative_id")
        batch_op.drop_constraint(
            "fk_projects_initiative_id_initiatives",
            type_="foreignkey",
        )
        batch_op.drop_column("initiative_id")

    op.drop_index("ix_initiatives_target_name", table_name="initiatives")
    op.drop_index("ix_initiatives_target_date", table_name="initiatives")
    op.drop_index("ix_initiatives_health", table_name="initiatives")
    op.drop_index("ix_initiatives_owner_id", table_name="initiatives")
    op.drop_table("initiatives")
