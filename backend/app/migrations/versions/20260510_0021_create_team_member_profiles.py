"""Create team member capability profiles.

Revision ID: 20260510_0021
Revises: 20260509_0020
Create Date: 2026-05-10 00:21:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260510_0021"
down_revision: str | None = "20260509_0020"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "team_member_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("headline", sa.String(length=255), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("automation_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_team_member_profiles_display_name", "team_member_profiles", ["display_name"])
    op.create_index("ix_team_member_profiles_email", "team_member_profiles", ["email"])
    op.create_index("ix_team_member_profiles_automation_enabled", "team_member_profiles", ["automation_enabled"])

    op.create_table(
        "team_member_profile_skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("skill_key", sa.String(length=120), nullable=False),
        sa.Column("skill_name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=True),
        sa.Column("level", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("interest", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("is_weakness", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("keywords_json", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("level >= 1 AND level <= 5", name="ck_team_member_profile_skills_level"),
        sa.CheckConstraint("interest >= 1 AND interest <= 5", name="ck_team_member_profile_skills_interest"),
        sa.ForeignKeyConstraint(["profile_id"], ["team_member_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_team_member_profile_skills_profile_id", "team_member_profile_skills", ["profile_id"])
    op.create_index("ix_team_member_profile_skills_skill_key", "team_member_profile_skills", ["skill_key"])
    op.create_index("ix_team_member_profile_skills_category", "team_member_profile_skills", ["category"])
    op.create_index("ix_team_member_profile_skills_is_weakness", "team_member_profile_skills", ["is_weakness"])

    with op.batch_alter_table("team_members") as batch_op:
        batch_op.add_column(sa.Column("profile_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_team_members_profile_id", ["profile_id"])
        batch_op.create_foreign_key(
            "fk_team_members_profile_id_team_member_profiles",
            "team_member_profiles",
            ["profile_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("team_members") as batch_op:
        batch_op.drop_index("ix_team_members_profile_id")
        batch_op.drop_constraint(
            "fk_team_members_profile_id_team_member_profiles",
            type_="foreignkey",
        )
        batch_op.drop_column("profile_id")

    op.drop_index("ix_team_member_profile_skills_is_weakness", table_name="team_member_profile_skills")
    op.drop_index("ix_team_member_profile_skills_category", table_name="team_member_profile_skills")
    op.drop_index("ix_team_member_profile_skills_skill_key", table_name="team_member_profile_skills")
    op.drop_index("ix_team_member_profile_skills_profile_id", table_name="team_member_profile_skills")
    op.drop_table("team_member_profile_skills")

    op.drop_index("ix_team_member_profiles_automation_enabled", table_name="team_member_profiles")
    op.drop_index("ix_team_member_profiles_email", table_name="team_member_profiles")
    op.drop_index("ix_team_member_profiles_display_name", table_name="team_member_profiles")
    op.drop_table("team_member_profiles")
