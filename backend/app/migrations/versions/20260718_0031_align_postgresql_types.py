"""Align UTC timestamps, legacy nullability, and PostgreSQL sequences.

Revision ID: 20260718_0031
Revises: 20260718_0030
Create Date: 2026-07-18 00:31:00.000000
"""

from collections.abc import Sequence
from typing import Any

import sqlalchemy as sa
from alembic import op


revision: str = "20260718_0031"
down_revision: str | None = "20260718_0030"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


# These columns predate UTCDateTime or were introduced with historical
# timezone-naive DDL. Legacy naive values are UTC by WorkChord convention.
UTC_COLUMNS: tuple[tuple[str, str], ...] = (
    ("agent_actors", "created_at"),
    ("agent_actors", "last_seen_at"),
    ("agent_run_events", "created_at"),
    ("agent_runs", "started_at"),
    ("agent_runs", "ended_at"),
    ("external_links", "created_at"),
    ("external_links", "updated_at"),
    ("github_status_automation_rules", "created_at"),
    ("github_status_automation_rules", "updated_at"),
    ("initiatives", "created_at"),
    ("initiatives", "updated_at"),
    ("label_groups", "created_at"),
    ("label_groups", "updated_at"),
    ("labels", "created_at"),
    ("labels", "updated_at"),
    ("outbound_webhook_deliveries", "last_attempt_at"),
    ("outbound_webhook_deliveries", "next_retry_at"),
    ("outbound_webhook_deliveries", "delivered_at"),
    ("outbound_webhook_deliveries", "created_at"),
    ("outbound_webhook_deliveries", "updated_at"),
    ("outbound_webhook_events", "occurred_at"),
    ("outbound_webhook_targets", "created_at"),
    ("outbound_webhook_targets", "updated_at"),
    ("project_milestones", "completed_at"),
    ("project_milestones", "created_at"),
    ("project_milestones", "updated_at"),
    ("project_updates", "created_at"),
    ("projects", "completed_at"),
    ("projects", "created_at"),
    ("projects", "updated_at"),
    ("release_tasks", "created_at"),
    ("releases", "shipped_at"),
    ("releases", "created_at"),
    ("releases", "updated_at"),
    ("request_source_links", "created_at"),
    ("request_sources", "created_at"),
    ("saved_views", "created_at"),
    ("saved_views", "updated_at"),
    ("system_settings", "created_at"),
    ("system_settings", "updated_at"),
    ("task_events", "created_at"),
    ("task_status_logs", "changed_at"),
    ("tasks", "claim_expires_at"),
    ("tasks", "updated_at"),
    ("team_member_profile_skills", "created_at"),
    ("team_member_profile_skills", "updated_at"),
    ("team_member_profiles", "created_at"),
    ("team_member_profiles", "updated_at"),
    ("triage_classification_suggestions", "created_at"),
    ("triage_items", "snoozed_until"),
    ("triage_items", "created_at"),
    ("triage_items", "updated_at"),
    ("user_sessions", "created_at"),
    ("user_sessions", "last_seen_at"),
    ("work_templates", "created_at"),
    ("work_templates", "updated_at"),
)


# The legacy baseline allowed NULL for fields whose mapped domain contract has
# always supplied these values. Backfill the established application defaults
# before making the live schema match model nullability.
NON_NULL_DEFAULTS: dict[str, tuple[tuple[str, sa.types.TypeEngine[Any], Any], ...]] = {
    "calendars": (
        ("holidays", sa.JSON(), []),
        ("weekend_days", sa.JSON(), [5, 6]),
        ("short_days", sa.JSON(), []),
    ),
    "team_members": (
        ("availability_percent", sa.Float(), 100.0),
        ("professionalism_coefficient", sa.Float(), 1.0),
        ("operational_utilization", sa.Float(), 20.0),
    ),
    "tasks": (
        ("priority", sa.Integer(), 5),
        ("effort_days", sa.Float(), 1.0),
        ("effort_hours", sa.Float(), 8.0),
        ("status", sa.String(length=50), "planned"),
        ("is_optional", sa.Boolean(), False),
        ("is_deferred", sa.Boolean(), False),
        ("sort_order", sa.Integer(), 0),
    ),
}


def _align_nullability(*, nullable: bool) -> None:
    bind = op.get_bind()
    for table_name, columns in NON_NULL_DEFAULTS.items():
        if not nullable:
            table = sa.table(
                table_name,
                *(sa.column(column_name, column_type) for column_name, column_type, _ in columns),
            )
            for column_name, _column_type, default in columns:
                column = table.c[column_name]
                bind.execute(
                    table.update().where(column.is_(None)).values({column_name: default})
                )

        if bind.dialect.name == "sqlite":
            with op.batch_alter_table(table_name) as batch:
                for column_name, column_type, _default in columns:
                    batch.alter_column(
                        column_name,
                        existing_type=column_type,
                        nullable=nullable,
                    )
        else:
            for column_name, column_type, _default in columns:
                op.alter_column(
                    table_name,
                    column_name,
                    existing_type=column_type,
                    nullable=nullable,
                )


def _align_postgresql_timestamps(*, timezone: bool) -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    old_type = sa.DateTime(timezone=not timezone)
    new_type = sa.DateTime(timezone=timezone)
    for table_name, column_name in UTC_COLUMNS:
        op.alter_column(
            table_name,
            column_name,
            existing_type=old_type,
            type_=new_type,
            postgresql_using=f'"{column_name}" AT TIME ZONE \'UTC\'',
        )


def _repair_postgresql_sequences() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    sequence_columns = bind.execute(
        sa.text(
            """
            SELECT
                table_name,
                column_name,
                pg_get_serial_sequence(
                    format('%I.%I', table_schema, table_name),
                    column_name
                ) AS sequence_name
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND column_default LIKE 'nextval(%'
            ORDER BY table_name, ordinal_position
            """
        )
    ).mappings()
    quote = bind.dialect.identifier_preparer.quote
    for row in sequence_columns:
        sequence_name = row["sequence_name"]
        if not sequence_name:
            continue
        table_name = quote(row["table_name"])
        column_name = quote(row["column_name"])
        bind.execute(
            sa.text(
                "SELECT setval(CAST(:sequence_name AS regclass), "
                f"COALESCE(MAX({column_name}), 1), "
                f"MAX({column_name}) IS NOT NULL) FROM {table_name}"
            ),
            {"sequence_name": sequence_name},
        )


def upgrade() -> None:
    _align_nullability(nullable=False)
    _align_postgresql_timestamps(timezone=True)
    _repair_postgresql_sequences()


def downgrade() -> None:
    _align_postgresql_timestamps(timezone=False)
    _align_nullability(nullable=True)
