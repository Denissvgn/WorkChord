"""Keep a run's declared harness session in columns a reader can search."""

import json

from alembic import op
import sqlalchemy as sa


revision = "20261116_0017"
down_revision = "20261116_0016"
branch_labels = None
depends_on = None


def _declared(metadata):
    try:
        harness = json.loads(metadata or "{}").get("harness")
    except (ValueError, AttributeError):
        return None
    if not isinstance(harness, dict) or set(harness) != {"kind", "session_id"}:
        return None
    from app.schemas.agent import check_harness_identity
    try:
        check_harness_identity(harness["kind"], harness["session_id"], label="harness")
    except ValueError:
        return None
    return harness["kind"], harness["session_id"]


def upgrade():
    op.add_column("agent_runs", sa.Column("harness_kind", sa.String(40), nullable=True))
    op.add_column("agent_runs", sa.Column("harness_session_id", sa.String(255), nullable=True))
    op.create_index("ix_agent_runs_harness_session_id", "agent_runs", ["harness_session_id"])
    connection = op.get_bind()
    runs = sa.table("agent_runs", sa.column("id", sa.Integer), sa.column("run_metadata", sa.Text),
                    sa.column("harness_kind", sa.String), sa.column("harness_session_id", sa.String))
    rows = connection.execute(sa.select(runs.c.id, runs.c.run_metadata)
                              .where(runs.c.run_metadata.like('%"harness"%'))).all()
    for run_id, metadata in rows:
        declared = _declared(metadata)
        if declared is not None:
            connection.execute(sa.update(runs).where(runs.c.id == run_id)
                               .values(harness_kind=declared[0], harness_session_id=declared[1]))


def downgrade():
    with op.batch_alter_table("agent_runs") as batch:
        batch.drop_index("ix_agent_runs_harness_session_id")
        batch.drop_column("harness_session_id")
        batch.drop_column("harness_kind")
