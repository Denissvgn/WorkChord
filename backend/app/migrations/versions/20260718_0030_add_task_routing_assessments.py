"""Add task assessments and assignment/run model linkage.

Revision ID: 20260718_0030
Revises: 20260718_0029
Create Date: 2026-07-18 00:10:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260718_0030"
down_revision: str | None = "20260718_0029"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_MODEL_BINDING_PAIR_CHECK = (
    "(model_binding_id IS NULL AND model_binding_revision IS NULL) OR "
    "(model_binding_id IS NOT NULL AND model_binding_revision IS NOT NULL "
    "AND model_binding_revision >= 1)"
)


def upgrade() -> None:
    op.create_table(
        "task_routing_assessments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("task_version", sa.Integer(), nullable=False),
        sa.Column(
            "policy_version",
            sa.String(length=80),
            server_default="model-aware-routing-v1",
            nullable=False,
        ),
        sa.Column("band", sa.String(length=20), nullable=False),
        sa.Column("reasoning_axis", sa.Integer(), nullable=False),
        sa.Column("ambiguity_axis", sa.Integer(), nullable=False),
        sa.Column("context_breadth_axis", sa.Integer(), nullable=False),
        sa.Column("risk_axis", sa.Integer(), nullable=False),
        sa.Column("verification_burden_axis", sa.Integer(), nullable=False),
        sa.Column(
            "required_skill_levels",
            sa.JSON(),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column(
            "required_model",
            sa.JSON(),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column("review_mode", sa.String(length=40), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False),
        sa.Column(
            "reason_codes",
            sa.JSON(),
            server_default=sa.text("'[]'"),
            nullable=False,
        ),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("assessor", sa.String(length=255), nullable=False),
        sa.Column("assessor_actor_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "task_version >= 1",
            name="ck_task_routing_assessments_task_version",
        ),
        sa.CheckConstraint(
            "policy_version = 'model-aware-routing-v1'",
            name="ck_task_routing_assessments_policy_version",
        ),
        sa.CheckConstraint(
            "band IN ('routine', 'standard', 'advanced')",
            name="ck_task_routing_assessments_band",
        ),
        sa.CheckConstraint(
            "reasoning_axis BETWEEN 1 AND 3 "
            "AND ambiguity_axis BETWEEN 1 AND 3 "
            "AND context_breadth_axis BETWEEN 1 AND 3 "
            "AND risk_axis BETWEEN 1 AND 3 "
            "AND verification_burden_axis BETWEEN 1 AND 3",
            name="ck_task_routing_assessments_axes",
        ),
        sa.CheckConstraint(
            "band <> 'routine' OR (reasoning_axis = 1 "
            "AND ambiguity_axis = 1 AND context_breadth_axis = 1 "
            "AND risk_axis = 1 AND verification_burden_axis = 1)",
            name="ck_task_routing_assessments_routine_band",
        ),
        sa.CheckConstraint(
            "band <> 'standard' OR (reasoning_axis < 3 "
            "AND ambiguity_axis < 3 AND context_breadth_axis < 3 "
            "AND risk_axis < 3 AND verification_burden_axis < 3)",
            name="ck_task_routing_assessments_standard_band",
        ),
        sa.CheckConstraint(
            "review_mode IN ('none', 'standard', 'independent', "
            "'specialist-independent')",
            name="ck_task_routing_assessments_review_mode",
        ),
        sa.CheckConstraint(
            "risk_axis < 3 OR review_mode IN "
            "('independent', 'specialist-independent')",
            name="ck_task_routing_assessments_risk_review",
        ),
        sa.CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="ck_task_routing_assessments_confidence",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            ondelete="CASCADE",
            name="fk_task_routing_assessments_task_id",
        ),
        sa.ForeignKeyConstraint(
            ["assessor_actor_id"],
            ["agent_actors.id"],
            ondelete="SET NULL",
            name="fk_task_routing_assessments_assessor_actor_id",
        ),
        sa.UniqueConstraint(
            "task_id",
            "task_version",
            "policy_version",
            name="uq_task_routing_assessments_task_version_policy",
        ),
    )
    op.create_index(
        "ix_task_routing_assessments_task_version",
        "task_routing_assessments",
        ["task_id", "task_version"],
    )
    op.create_index(
        "ix_task_routing_assessments_policy_band",
        "task_routing_assessments",
        ["policy_version", "band"],
    )

    with op.batch_alter_table("agent_task_assignments") as batch:
        batch.add_column(sa.Column("model_binding_id", sa.Integer(), nullable=True))
        batch.add_column(
            sa.Column("model_binding_revision", sa.Integer(), nullable=True)
        )
        batch.create_foreign_key(
            "fk_agent_task_assignments_model_binding_id",
            "agent_model_bindings",
            ["model_binding_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch.create_check_constraint(
            "ck_agent_task_assignments_model_binding_pair",
            _MODEL_BINDING_PAIR_CHECK,
        )
        batch.create_index(
            "ix_agent_task_assignments_model_binding_id",
            ["model_binding_id"],
            unique=False,
        )

    with op.batch_alter_table("agent_runs") as batch:
        batch.add_column(sa.Column("model_binding_id", sa.Integer(), nullable=True))
        batch.add_column(
            sa.Column("model_binding_revision", sa.Integer(), nullable=True)
        )
        batch.add_column(
            sa.Column("configured_model_alias", sa.String(length=255), nullable=True)
        )
        batch.add_column(
            sa.Column("resolved_model_id", sa.String(length=255), nullable=True)
        )
        batch.create_foreign_key(
            "fk_agent_runs_model_binding_id",
            "agent_model_bindings",
            ["model_binding_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch.create_check_constraint(
            "ck_agent_runs_model_binding_pair",
            _MODEL_BINDING_PAIR_CHECK,
        )
        batch.create_index(
            "ix_agent_runs_model_binding_id",
            ["model_binding_id"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("agent_runs") as batch:
        batch.drop_index("ix_agent_runs_model_binding_id")
        batch.drop_constraint("ck_agent_runs_model_binding_pair", type_="check")
        batch.drop_constraint("fk_agent_runs_model_binding_id", type_="foreignkey")
        batch.drop_column("resolved_model_id")
        batch.drop_column("configured_model_alias")
        batch.drop_column("model_binding_revision")
        batch.drop_column("model_binding_id")

    with op.batch_alter_table("agent_task_assignments") as batch:
        batch.drop_index("ix_agent_task_assignments_model_binding_id")
        batch.drop_constraint(
            "ck_agent_task_assignments_model_binding_pair", type_="check"
        )
        batch.drop_constraint(
            "fk_agent_task_assignments_model_binding_id", type_="foreignkey"
        )
        batch.drop_column("model_binding_revision")
        batch.drop_column("model_binding_id")

    op.drop_index(
        "ix_task_routing_assessments_policy_band",
        table_name="task_routing_assessments",
    )
    op.drop_index(
        "ix_task_routing_assessments_task_version",
        table_name="task_routing_assessments",
    )
    op.drop_table("task_routing_assessments")
