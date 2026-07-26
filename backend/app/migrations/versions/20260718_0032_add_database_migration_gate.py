"""add target-owned database migration gate

Revision ID: 20260718_0032
Revises: 20260718_0031
Create Date: 2026-07-18
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

from app.utils.time import UTCDateTime


revision = "20260718_0032"
down_revision = "20260718_0031"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "database_migration_gates",
        sa.Column("run_id", sa.String(length=64), nullable=False),
        sa.Column("source_manifest_sha256", sa.String(length=64), nullable=False),
        sa.Column("source_snapshot_sha256", sa.String(length=64), nullable=False),
        sa.Column("target_identity_sha256", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("completed_tables", sa.JSON(), nullable=False),
        sa.Column("failure_code", sa.String(length=120), nullable=True),
        sa.Column("raw_report_sha256", sa.String(length=64), nullable=True),
        sa.Column("reconciliation_report_sha256", sa.String(length=64), nullable=True),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('loading', 'loaded', 'reconciling', "
            "'raw_reconciled', 'reconciled', 'failed')",
            name="ck_database_migration_gates_status",
        ),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index(
        "ix_database_migration_gates_status",
        "database_migration_gates",
        ["status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_database_migration_gates_status",
        table_name="database_migration_gates",
    )
    op.drop_table("database_migration_gates")
