"""Add explicit configured-versus-observed model trust evidence.

Revision ID: 20260727_0034
Revises: 20260719_0033
Create Date: 2026-07-27 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260727_0034"
down_revision: str | None = "20260719_0033"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_MODEL_TRUST_STATE_CHECK = (
    "model_trust_state IN "
    "('matched', 'mismatch', 'unreported', 'unverifiable')"
)
_MODEL_MATCH_BASIS_CHECK = (
    "(model_trust_state = 'matched' AND "
    "model_match_basis IS NOT NULL AND "
    "model_match_basis IN ('configured_alias', 'catalog_key')) OR "
    "(model_trust_state <> 'matched' AND model_match_basis IS NULL)"
)


def upgrade() -> None:
    with op.batch_alter_table("agent_runs") as batch:
        batch.add_column(
            sa.Column(
                "model_trust_state",
                sa.String(length=30),
                nullable=True,
                server_default="unreported",
            )
        )
        batch.add_column(
            sa.Column("model_match_basis", sa.String(length=40), nullable=True)
        )

    op.execute(
        sa.text(
            "UPDATE agent_runs "
            "SET model_trust_state = CASE "
            "WHEN COALESCE("
            "NULLIF(TRIM(resolved_model_id), ''), "
            "NULLIF(TRIM(model), '')"
            ") IS NULL "
            "THEN 'unreported' ELSE 'unverifiable' END"
        )
    )

    with op.batch_alter_table("agent_runs") as batch:
        batch.alter_column(
            "model_trust_state",
            existing_type=sa.String(length=30),
            nullable=False,
        )
        batch.create_check_constraint(
            "ck_agent_runs_model_trust_state",
            _MODEL_TRUST_STATE_CHECK,
        )
        batch.create_check_constraint(
            "ck_agent_runs_model_match_basis",
            _MODEL_MATCH_BASIS_CHECK,
        )


def downgrade() -> None:
    with op.batch_alter_table("agent_runs") as batch:
        batch.drop_constraint(
            "ck_agent_runs_model_match_basis",
            type_="check",
        )
        batch.drop_constraint(
            "ck_agent_runs_model_trust_state",
            type_="check",
        )
        batch.drop_column("model_match_basis")
        batch.drop_column("model_trust_state")
