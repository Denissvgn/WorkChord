"""Add operator-owned agent-team setup and onboarding state.

Revision ID: 20260728_0035
Revises: 20260727_0034
Create Date: 2026-07-28 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from app.utils.time import UTCDateTime


revision: str = "20260728_0035"
down_revision: str | None = "20260727_0034"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("agent_actors") as batch:
        batch.add_column(
            sa.Column(
                "lifecycle_state",
                sa.String(length=30),
                nullable=True,
                server_default="active",
            )
        )

    op.execute(
        sa.text(
            "UPDATE agent_actors SET lifecycle_state = "
            "CASE WHEN enabled THEN 'active' ELSE 'disabled' END"
        )
    )

    with op.batch_alter_table("agent_actors") as batch:
        batch.alter_column(
            "lifecycle_state",
            existing_type=sa.String(length=30),
            nullable=False,
        )
        batch.create_check_constraint(
            "ck_agent_actors_lifecycle_state",
            "lifecycle_state IN ('active', 'onboarding', 'disabled')",
        )

    op.create_table(
        "agent_team_topologies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topology_key", sa.String(length=100), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("manifest_digest", sa.String(length=64), nullable=False),
        sa.Column("manifest_payload", sa.Text(), nullable=False),
        sa.Column("primary_actor_id", sa.Integer(), nullable=True),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("blocker_codes", sa.Text(), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "revision >= 1",
            name="ck_agent_team_topologies_revision",
        ),
        sa.CheckConstraint(
            "state IN ('configured', 'onboarding', 'runtime_ready', "
            "'blocked', 'disabled')",
            name="ck_agent_team_topologies_state",
        ),
        sa.ForeignKeyConstraint(
            ["primary_actor_id"],
            ["agent_actors.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("primary_actor_id"),
        sa.UniqueConstraint("topology_key"),
    )
    op.create_index(
        "ix_agent_team_topologies_state",
        "agent_team_topologies",
        ["state"],
        unique=False,
    )

    op.create_table(
        "agent_team_topology_members",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topology_id", sa.Integer(), nullable=False),
        sa.Column("actor_key", sa.String(length=100), nullable=False),
        sa.Column("actor_id", sa.Integer(), nullable=True),
        sa.Column("actor_name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("object_revision", sa.Integer(), nullable=False),
        sa.Column("lifecycle_state", sa.String(length=40), nullable=False),
        sa.Column("desired_member_digest", sa.String(length=64), nullable=False),
        sa.Column("desired_member_payload", sa.Text(), nullable=False),
        sa.Column("scope_preset", sa.String(length=40), nullable=False),
        sa.Column("profile_key", sa.String(length=120), nullable=False),
        sa.Column("skill_package_name", sa.String(length=120), nullable=False),
        sa.Column("skill_package_version", sa.String(length=40), nullable=False),
        sa.Column("skill_package_checksum", sa.String(length=64), nullable=False),
        sa.Column("model_binding_keys", sa.Text(), nullable=False),
        sa.Column("default_model_binding_key", sa.String(length=120), nullable=False),
        sa.Column("assignment_modes", sa.Text(), nullable=False),
        sa.Column("runtime_ref", sa.String(length=1024), nullable=False),
        sa.Column("credential_ref", sa.String(length=1024), nullable=False),
        sa.Column("credential_delivery_state", sa.String(length=30), nullable=False),
        sa.Column(
            "credential_delivery_receipt_digest",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column("handoff_digest", sa.String(length=64), nullable=True),
        sa.Column(
            "runtime_acknowledgement_digest",
            sa.String(length=64),
            nullable=True,
        ),
        sa.Column("runtime_acknowledgement_payload", sa.Text(), nullable=True),
        sa.Column("runtime_acknowledged_at", UTCDateTime(), nullable=True),
        sa.Column("ack_attempt_count", sa.Integer(), nullable=False),
        sa.Column("ack_window_started_at", UTCDateTime(), nullable=True),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "object_revision >= 1",
            name="ck_agent_team_members_object_revision",
        ),
        sa.CheckConstraint(
            "role IN ('pm', 'worker', 'verifier')",
            name="ck_agent_team_members_role",
        ),
        sa.CheckConstraint(
            "lifecycle_state IN ('desired', 'configured', "
            "'credential_delivered', 'onboarding', 'connected', "
            "'runtime_ready', 'disabled')",
            name="ck_agent_team_members_lifecycle",
        ),
        sa.CheckConstraint(
            "credential_delivery_state IN "
            "('pending', 'delivered', 'uncertain', 'not_required')",
            name="ck_agent_team_members_credential_state",
        ),
        sa.CheckConstraint(
            "ack_attempt_count >= 0",
            name="ck_agent_team_members_ack_attempts",
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["agent_actors.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["topology_id"],
            ["agent_team_topologies.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "topology_id",
            "actor_key",
            name="uq_agent_team_members_actor_key",
        ),
        sa.UniqueConstraint(
            "actor_id",
            name="uq_agent_team_members_actor",
        ),
        sa.UniqueConstraint(
            "runtime_ref",
            name="uq_agent_team_members_runtime_ref",
        ),
        sa.UniqueConstraint(
            "credential_ref",
            name="uq_agent_team_members_credential_ref",
        ),
    )
    op.create_index(
        "ix_agent_team_members_topology_lifecycle",
        "agent_team_topology_members",
        ["topology_id", "lifecycle_state"],
        unique=False,
    )

    op.create_table(
        "agent_team_managed_objects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topology_id", sa.Integer(), nullable=False),
        sa.Column("object_type", sa.String(length=30), nullable=False),
        sa.Column("logical_key", sa.String(length=160), nullable=False),
        sa.Column("object_id", sa.Integer(), nullable=False),
        sa.Column("object_revision", sa.Integer(), nullable=False),
        sa.Column("desired_digest", sa.String(length=64), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "object_revision >= 1",
            name="ck_agent_team_managed_objects_revision",
        ),
        sa.CheckConstraint(
            "object_type IN ('profile', 'model_catalog', 'model_binding')",
            name="ck_agent_team_managed_objects_type",
        ),
        sa.ForeignKeyConstraint(
            ["topology_id"],
            ["agent_team_topologies.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "topology_id",
            "object_type",
            "logical_key",
            name="uq_agent_team_managed_objects_logical",
        ),
        sa.UniqueConstraint(
            "topology_id",
            "object_type",
            "object_id",
            name="uq_agent_team_managed_objects_reference",
        ),
    )

    op.create_table(
        "agent_team_apply_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("apply_id", sa.String(length=32), nullable=False),
        sa.Column("topology_id", sa.Integer(), nullable=True),
        sa.Column("topology_key", sa.String(length=100), nullable=False),
        sa.Column("principal_key", sa.String(length=160), nullable=False),
        sa.Column("principal_actor_id", sa.Integer(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("request_digest", sa.String(length=64), nullable=False),
        sa.Column("manifest_digest", sa.String(length=64), nullable=False),
        sa.Column("plan_digest", sa.String(length=64), nullable=False),
        sa.Column("expected_topology_revision", sa.Integer(), nullable=False),
        sa.Column("resulting_topology_revision", sa.Integer(), nullable=False),
        sa.Column("approved_action_ids", sa.Text(), nullable=False),
        sa.Column("confirmed_action_ids", sa.Text(), nullable=False),
        sa.Column("plan_payload", sa.Text(), nullable=False),
        sa.Column("rationale", sa.String(length=2000), nullable=False),
        sa.Column("correlation_id", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("blocker_codes", sa.Text(), nullable=False),
        sa.Column("response_payload", sa.Text(), nullable=True),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "expected_topology_revision >= 0",
            name="ck_agent_team_apply_runs_expected_revision",
        ),
        sa.CheckConstraint(
            "resulting_topology_revision >= 0",
            name="ck_agent_team_apply_runs_resulting_revision",
        ),
        sa.CheckConstraint(
            "status IN ('running', 'completed', 'partial', 'blocked')",
            name="ck_agent_team_apply_runs_status",
        ),
        sa.ForeignKeyConstraint(
            ["principal_actor_id"],
            ["agent_actors.id"],
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["topology_id"],
            ["agent_team_topologies.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("apply_id"),
        sa.UniqueConstraint(
            "principal_key",
            "idempotency_key",
            name="uq_agent_team_apply_runs_idempotency",
        ),
    )
    op.create_index(
        "ix_agent_team_apply_runs_topology_created",
        "agent_team_apply_runs",
        ["topology_key", "created_at"],
        unique=False,
    )

    op.create_table(
        "agent_team_action_receipts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("apply_run_id", sa.Integer(), nullable=False),
        sa.Column("action_id", sa.String(length=128), nullable=False),
        sa.Column("action_digest", sa.String(length=64), nullable=False),
        sa.Column("reconciliation_class", sa.String(length=40), nullable=False),
        sa.Column("operation", sa.String(length=80), nullable=False),
        sa.Column("actor_key", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("target_actor_id", sa.Integer(), nullable=True),
        sa.Column("before_revision", sa.Integer(), nullable=True),
        sa.Column("after_revision", sa.Integer(), nullable=True),
        sa.Column("blocker_code", sa.String(length=128), nullable=True),
        sa.Column("next_action", sa.String(length=255), nullable=True),
        sa.Column("result_payload", sa.Text(), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "status IN ('pending', 'applied', 'no_change', 'blocked')",
            name="ck_agent_team_action_receipts_status",
        ),
        sa.CheckConstraint(
            "(before_revision IS NULL OR before_revision >= 1) AND "
            "(after_revision IS NULL OR after_revision >= 1)",
            name="ck_agent_team_action_receipts_revisions",
        ),
        sa.ForeignKeyConstraint(
            ["apply_run_id"],
            ["agent_team_apply_runs.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "apply_run_id",
            "action_id",
            name="uq_agent_team_action_receipts_action",
        ),
    )


def downgrade() -> None:
    op.drop_table("agent_team_action_receipts")
    op.drop_index(
        "ix_agent_team_apply_runs_topology_created",
        table_name="agent_team_apply_runs",
    )
    op.drop_table("agent_team_apply_runs")
    op.drop_table("agent_team_managed_objects")
    op.drop_index(
        "ix_agent_team_members_topology_lifecycle",
        table_name="agent_team_topology_members",
    )
    op.drop_table("agent_team_topology_members")
    op.drop_index(
        "ix_agent_team_topologies_state",
        table_name="agent_team_topologies",
    )
    op.drop_table("agent_team_topologies")

    with op.batch_alter_table("agent_actors") as batch:
        batch.drop_constraint(
            "ck_agent_actors_lifecycle_state",
            type_="check",
        )
        batch.drop_column("lifecycle_state")
