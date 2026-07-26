"""add autonomous topology and verification projections

Revision ID: 20260719_0033
Revises: 20260718_0032
Create Date: 2026-07-19
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

from app.utils.time import UTCDateTime


revision = "20260719_0033"
down_revision = "20260718_0032"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agent_autonomy_topologies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topology_key", sa.String(length=100), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("manifest_digest", sa.String(length=64), nullable=False),
        sa.Column("charter_digest", sa.String(length=64), nullable=False),
        sa.Column("primary_actor_id", sa.Integer(), nullable=True),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("external_journal_revision", sa.Integer(), nullable=False),
        sa.Column("external_journal_head_digest", sa.String(length=64), nullable=False),
        sa.Column("applied_receipt_digest", sa.String(length=64), nullable=True),
        sa.Column("blocker_codes", sa.Text(), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint("revision >= 1", name="ck_agent_autonomy_topologies_revision"),
        sa.CheckConstraint(
            "external_journal_revision >= 0",
            name="ck_agent_autonomy_topologies_journal_revision",
        ),
        sa.CheckConstraint(
            "state IN ('planned', 'applying', 'active', 'blocked', 'disabled')",
            name="ck_agent_autonomy_topologies_state",
        ),
        sa.ForeignKeyConstraint(
            ["primary_actor_id"], ["agent_actors.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("primary_actor_id"),
        sa.UniqueConstraint("topology_key"),
    )
    op.create_table(
        "agent_autonomy_topology_members",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topology_id", sa.Integer(), nullable=False),
        sa.Column("logical_key", sa.String(length=100), nullable=False),
        sa.Column("actor_id", sa.Integer(), nullable=True),
        sa.Column("object_revision", sa.Integer(), nullable=False),
        sa.Column("lifecycle_state", sa.String(length=40), nullable=False),
        sa.Column("desired_member_digest", sa.String(length=64), nullable=False),
        sa.Column("independence_group", sa.String(length=100), nullable=False),
        sa.Column("role_package_checksum", sa.String(length=64), nullable=False),
        sa.Column("external_identity_binding_digest", sa.String(length=64), nullable=False),
        sa.Column("runtime_attestation_digest", sa.String(length=64), nullable=True),
        sa.Column("credential_delivery_receipt_digest", sa.String(length=64), nullable=True),
        sa.Column("runtime_acknowledgement_digest", sa.String(length=64), nullable=True),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint("object_revision >= 1", name="ck_agent_autonomy_members_revision"),
        sa.CheckConstraint(
            "lifecycle_state IN ('desired', 'configured', 'credential_delivered', "
            "'onboarding', 'connected', 'runtime_ready', 'disabled')",
            name="ck_agent_autonomy_members_lifecycle",
        ),
        sa.ForeignKeyConstraint(["actor_id"], ["agent_actors.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["topology_id"], ["agent_autonomy_topologies.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("actor_id", name="uq_agent_autonomy_members_actor"),
        sa.UniqueConstraint(
            "topology_id", "logical_key", name="uq_agent_autonomy_members_logical_key"
        ),
    )
    op.create_index(
        "ix_agent_autonomy_members_topology_state",
        "agent_autonomy_topology_members",
        ["topology_id", "lifecycle_state"],
        unique=False,
    )
    op.create_table(
        "agent_work_packages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("package_key", sa.String(length=255), nullable=False),
        sa.Column("package_version", sa.Integer(), nullable=False),
        sa.Column("execution_task_id", sa.Integer(), nullable=True),
        sa.Column("predecessor_package_id", sa.Integer(), nullable=True),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("artifact_set_digest", sa.String(length=64), nullable=False),
        sa.Column("contract_manifest_digest", sa.String(length=64), nullable=False),
        sa.Column("source_contract_digest", sa.String(length=64), nullable=False),
        sa.Column("creation_request_digest", sa.String(length=64), nullable=False),
        sa.Column("external_journal_revision", sa.Integer(), nullable=False),
        sa.Column("external_journal_head_digest", sa.String(length=64), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint("package_version >= 1", name="ck_agent_work_packages_version"),
        sa.CheckConstraint(
            "external_journal_revision >= 1",
            name="ck_agent_work_packages_journal_revision",
        ),
        sa.CheckConstraint(
            "state IN ('planned', 'evaluating', 'passed', 'rework_required')",
            name="ck_agent_work_packages_state",
        ),
        sa.ForeignKeyConstraint(
            ["execution_task_id"], ["tasks.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["predecessor_package_id"], ["agent_work_packages.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "package_key", "package_version", name="uq_agent_work_packages_key_version"
        ),
    )
    op.create_index(
        "ix_agent_work_packages_execution_task_id",
        "agent_work_packages",
        ["execution_task_id"],
        unique=False,
    )
    op.create_index(
        "ix_agent_work_packages_state", "agent_work_packages", ["state"], unique=False
    )
    op.create_table(
        "agent_verification_requirements",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=False),
        sa.Column("slot_key", sa.String(length=255), nullable=False),
        sa.Column("verifier_logical_key", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("assigned_verifier_actor_id", sa.Integer(), nullable=True),
        sa.Column("assignment_id", sa.Integer(), nullable=True),
        sa.Column("criterion_schema", sa.String(length=255), nullable=False),
        sa.Column("artifact_set_digest", sa.String(length=64), nullable=False),
        sa.Column("evaluator_version", sa.String(length=255), nullable=False),
        sa.Column("executor_independence_group", sa.String(length=100), nullable=False),
        sa.Column("verifier_independence_group", sa.String(length=100), nullable=False),
        sa.Column("lease_generation", sa.Integer(), nullable=False),
        sa.Column("lease_digest", sa.String(length=64), nullable=True),
        sa.Column("attempt_start_digest", sa.String(length=64), nullable=True),
        sa.Column("lease_expires_at", UTCDateTime(), nullable=True),
        sa.Column("heartbeat_at", UTCDateTime(), nullable=True),
        sa.Column("evidence_digest", sa.String(length=64), nullable=True),
        sa.Column("verdict_digest", sa.String(length=64), nullable=True),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint(
            "state IN ('planned', 'ready', 'claimed', 'running', 'passed', "
            "'rejected', 'expired')",
            name="ck_agent_verification_requirements_state",
        ),
        sa.CheckConstraint(
            "lease_generation >= 0",
            name="ck_agent_verification_requirements_lease_generation",
        ),
        sa.CheckConstraint(
            "executor_independence_group <> verifier_independence_group",
            name="ck_agent_verification_requirements_independence",
        ),
        sa.CheckConstraint(
            "state NOT IN ('claimed', 'running', 'passed', 'rejected') OR "
            "(assigned_verifier_actor_id IS NOT NULL AND lease_generation >= 1 "
            "AND lease_digest IS NOT NULL AND attempt_start_digest IS NOT NULL "
            "AND lease_expires_at IS NOT NULL)",
            name="ck_agent_verification_requirements_live_fence",
        ),
        sa.ForeignKeyConstraint(
            ["assigned_verifier_actor_id"], ["agent_actors.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["assignment_id"], ["agent_task_assignments.id"], ondelete="RESTRICT"
        ),
        sa.ForeignKeyConstraint(
            ["package_id"], ["agent_work_packages.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "assignment_id", name="uq_agent_verification_requirements_assignment"
        ),
        sa.UniqueConstraint(
            "package_id", "slot_key", name="uq_agent_verification_requirements_slot"
        ),
    )
    op.create_index(
        "ix_agent_verification_requirements_actor_state",
        "agent_verification_requirements",
        ["assigned_verifier_actor_id", "state"],
        unique=False,
    )
    op.create_index(
        "ix_agent_verification_requirements_assigned_verifier_actor_id",
        "agent_verification_requirements",
        ["assigned_verifier_actor_id"],
        unique=False,
    )
    op.create_table(
        "agent_verification_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("requirement_id", sa.Integer(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("actor_id", sa.Integer(), nullable=True),
        sa.Column("lease_generation", sa.Integer(), nullable=False),
        sa.Column("payload_digest", sa.String(length=64), nullable=False),
        sa.Column("previous_hash", sa.String(length=64), nullable=False),
        sa.Column("event_digest", sa.String(length=64), nullable=False),
        sa.Column("idempotency_key", sa.String(length=255), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint("sequence >= 1", name="ck_agent_verification_events_sequence"),
        sa.ForeignKeyConstraint(["actor_id"], ["agent_actors.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(
            ["requirement_id"], ["agent_verification_requirements.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "requirement_id", "idempotency_key", name="uq_agent_verification_events_idempotency"
        ),
        sa.UniqueConstraint(
            "requirement_id", "sequence", name="uq_agent_verification_events_sequence"
        ),
    )
    op.create_table(
        "agent_observation_jobs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("job_key", sa.String(length=255), nullable=False),
        sa.Column("job_version", sa.Integer(), nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=True),
        sa.Column("observation_kind", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=30), nullable=False),
        sa.Column("policy_digest", sa.String(length=64), nullable=False),
        sa.Column("trusted_clock_ref_digest", sa.String(length=64), nullable=False),
        sa.Column("minimum_elapsed_seconds", sa.Integer(), nullable=False),
        sa.Column("starts_at", UTCDateTime(), nullable=False),
        sa.Column("due_at", UTCDateTime(), nullable=False),
        sa.Column("valid_until", UTCDateTime(), nullable=False),
        sa.Column("checkpoint_digest", sa.String(length=64), nullable=True),
        sa.Column("credential_lineage_digest", sa.String(length=64), nullable=False),
        sa.Column("result_evidence_digest", sa.String(length=64), nullable=True),
        sa.Column("external_journal_revision", sa.Integer(), nullable=False),
        sa.Column("external_journal_head_digest", sa.String(length=64), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("updated_at", UTCDateTime(), nullable=False),
        sa.CheckConstraint("job_version >= 1", name="ck_agent_observation_jobs_version"),
        sa.CheckConstraint(
            "state IN ('planned', 'scheduled', 'running', 'met', 'missed', "
            "'failed', 'blocked_external')",
            name="ck_agent_observation_jobs_state",
        ),
        sa.CheckConstraint(
            "minimum_elapsed_seconds >= 1",
            name="ck_agent_observation_jobs_minimum_elapsed",
        ),
        sa.CheckConstraint(
            "starts_at < due_at AND due_at < valid_until",
            name="ck_agent_observation_jobs_time_order",
        ),
        sa.CheckConstraint(
            "external_journal_revision >= 0",
            name="ck_agent_observation_jobs_journal_revision",
        ),
        sa.ForeignKeyConstraint(
            ["package_id"], ["agent_work_packages.id"], ondelete="RESTRICT"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "job_key", "job_version", name="uq_agent_observation_jobs_key_version"
        ),
    )
    op.create_index(
        "ix_agent_observation_jobs_due_state",
        "agent_observation_jobs",
        ["due_at", "state"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_agent_observation_jobs_due_state", table_name="agent_observation_jobs")
    op.drop_table("agent_observation_jobs")
    op.drop_table("agent_verification_events")
    op.drop_index(
        "ix_agent_verification_requirements_assigned_verifier_actor_id",
        table_name="agent_verification_requirements",
    )
    op.drop_index(
        "ix_agent_verification_requirements_actor_state",
        table_name="agent_verification_requirements",
    )
    op.drop_table("agent_verification_requirements")
    op.drop_index("ix_agent_work_packages_state", table_name="agent_work_packages")
    op.drop_index(
        "ix_agent_work_packages_execution_task_id", table_name="agent_work_packages"
    )
    op.drop_table("agent_work_packages")
    op.drop_index(
        "ix_agent_autonomy_members_topology_state",
        table_name="agent_autonomy_topology_members",
    )
    op.drop_table("agent_autonomy_topology_members")
    op.drop_table("agent_autonomy_topologies")
