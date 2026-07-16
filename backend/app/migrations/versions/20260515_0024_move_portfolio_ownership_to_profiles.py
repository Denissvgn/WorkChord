"""Move portfolio ownership to team member profiles.

Revision ID: 20260515_0024
Revises: 20260510_0023
Create Date: 2026-05-15
"""
from collections.abc import Iterable, Sequence
from datetime import datetime

import sqlalchemy as sa
from alembic import op


revision: str = "20260515_0024"
down_revision: str | None = "20260510_0023"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _normalize_text_key(value: str | None) -> str:
    return " ".join((value or "").strip().lower().split())


def _find_profile_id(
    connection,
    *,
    email: str | None,
    name: str | None,
) -> int | None:
    normalized_email = _normalize_text_key(email)
    if normalized_email:
        profile_id = connection.execute(
            sa.text(
                """
                SELECT id
                FROM team_member_profiles
                WHERE lower(email) = :email
                ORDER BY id
                LIMIT 1
                """
            ),
            {"email": normalized_email},
        ).scalar_one_or_none()
        if profile_id is not None:
            return int(profile_id)

    normalized_name = _normalize_text_key(name)
    if normalized_name:
        rows = connection.execute(
            sa.text("SELECT id, display_name FROM team_member_profiles ORDER BY id")
        ).mappings()
        for row in rows:
            if _normalize_text_key(row["display_name"]) == normalized_name:
                return int(row["id"])

    return None


def _create_profile_for_member(connection, member: dict) -> int:
    now = datetime.utcnow()
    connection.execute(
        sa.text(
            """
            INSERT INTO team_member_profiles (
                display_name,
                email,
                headline,
                summary,
                notes,
                automation_enabled,
                created_at,
                updated_at
            )
            VALUES (
                :display_name,
                :email,
                :headline,
                NULL,
                NULL,
                :automation_enabled,
                :created_at,
                :updated_at
            )
            """
        ),
        {
            "display_name": (member["name"] or "").strip(),
            "email": (member["email"] or "").strip() or None,
            "headline": (member["position"] or "").strip() or None,
            "automation_enabled": True,
            "created_at": now,
            "updated_at": now,
        },
    )
    return int(
        connection.execute(
            sa.text("SELECT max(id) FROM team_member_profiles")
        ).scalar_one()
    )


def _resolve_profile_id(connection, member: dict) -> int:
    if member["profile_id"] is not None:
        return int(member["profile_id"])

    profile_id = _find_profile_id(
        connection,
        email=member["email"],
        name=member["name"],
    )
    if profile_id is None:
        profile_id = _create_profile_for_member(connection, member)

    connection.execute(
        sa.text("UPDATE team_members SET profile_id = :profile_id WHERE id = :member_id"),
        {"profile_id": profile_id, "member_id": member["owner_id"]},
    )
    return profile_id


def _backfill_owner_profiles(
    connection,
    *,
    table_name: str,
    rows: Iterable[dict],
) -> None:
    for row in rows:
        profile_id = _resolve_profile_id(connection, row)
        connection.execute(
            sa.text(
                f"UPDATE {table_name} "
                "SET owner_profile_id = :profile_id "
                "WHERE id = :object_id"
            ),
            {"profile_id": profile_id, "object_id": row["object_id"]},
        )


def upgrade() -> None:
    with op.batch_alter_table("projects") as batch_op:
        batch_op.add_column(sa.Column("owner_profile_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_projects_owner_profile_id", ["owner_profile_id"])
        batch_op.create_foreign_key(
            "fk_projects_owner_profile_id_team_member_profiles",
            "team_member_profiles",
            ["owner_profile_id"],
            ["id"],
            ondelete="SET NULL",
        )

    with op.batch_alter_table("initiatives") as batch_op:
        batch_op.add_column(sa.Column("owner_profile_id", sa.Integer(), nullable=True))
        batch_op.create_index("ix_initiatives_owner_profile_id", ["owner_profile_id"])
        batch_op.create_foreign_key(
            "fk_initiatives_owner_profile_id_team_member_profiles",
            "team_member_profiles",
            ["owner_profile_id"],
            ["id"],
            ondelete="SET NULL",
        )

    connection = op.get_bind()
    project_rows = connection.execute(
        sa.text(
            """
            SELECT
                projects.id AS object_id,
                team_members.id AS owner_id,
                team_members.name AS name,
                team_members.position AS position,
                team_members.email AS email,
                team_members.profile_id AS profile_id
            FROM projects
            JOIN team_members ON team_members.id = projects.owner_id
            WHERE projects.owner_id IS NOT NULL
              AND projects.owner_profile_id IS NULL
            ORDER BY projects.id
            """
        )
    ).mappings().all()
    _backfill_owner_profiles(connection, table_name="projects", rows=project_rows)

    initiative_rows = connection.execute(
        sa.text(
            """
            SELECT
                initiatives.id AS object_id,
                team_members.id AS owner_id,
                team_members.name AS name,
                team_members.position AS position,
                team_members.email AS email,
                team_members.profile_id AS profile_id
            FROM initiatives
            JOIN team_members ON team_members.id = initiatives.owner_id
            WHERE initiatives.owner_id IS NOT NULL
              AND initiatives.owner_profile_id IS NULL
            ORDER BY initiatives.id
            """
        )
    ).mappings().all()
    _backfill_owner_profiles(connection, table_name="initiatives", rows=initiative_rows)


def downgrade() -> None:
    with op.batch_alter_table("initiatives") as batch_op:
        batch_op.drop_index("ix_initiatives_owner_profile_id")
        batch_op.drop_constraint(
            "fk_initiatives_owner_profile_id_team_member_profiles",
            type_="foreignkey",
        )
        batch_op.drop_column("owner_profile_id")

    with op.batch_alter_table("projects") as batch_op:
        batch_op.drop_index("ix_projects_owner_profile_id")
        batch_op.drop_constraint(
            "fk_projects_owner_profile_id_team_member_profiles",
            type_="foreignkey",
        )
        batch_op.drop_column("owner_profile_id")
