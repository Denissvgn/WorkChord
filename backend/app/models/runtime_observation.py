"""Advisory observations of agent runtime sessions, reported by independent observers."""

from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, UniqueConstraint, event
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

OBSERVATION_KINDS = ("session_active", "session_idle", "session_ended", "model_observed")


class AgentRuntimeObservation(Base):
    """What an independent observer saw of an agent runtime session.

    Advisory only: no dispatch, routing, readiness, assignment or work decision
    reads this table, and recording a row writes nothing else. Rows are never
    edited; operator cleanup removes rows past the retention period.
    """

    __tablename__ = "agent_runtime_observations"
    __table_args__ = (
        CheckConstraint(
            "kind IN ('session_active', 'session_idle', 'session_ended', 'model_observed')",
            name="ck_agent_runtime_observations_kind",
        ),
        UniqueConstraint("observer_session_id", "idempotency_key", name="uq_agent_runtime_observation_key"),
        Index("ix_agent_runtime_observations_observer_time", "observer_session_id", "received_at"),
        Index("ix_agent_runtime_observations_harness", "harness_kind", "harness_session_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # task_id makes reads follow the task read scope; rows without a task are
    # visible only to operators and trusted-local readers.
    task_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id", ondelete="SET NULL"), index=True)
    run_id: Mapped[int | None] = mapped_column(ForeignKey("agent_runs.id", ondelete="SET NULL"), index=True)
    subject_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="SET NULL"))
    observer_session_id: Mapped[int | None] = mapped_column(ForeignKey("user_sessions.id", ondelete="SET NULL"))
    observer_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="SET NULL"))
    observer_label: Mapped[str | None] = mapped_column(String(80))
    kind: Mapped[str] = mapped_column(String(30), nullable=False)
    harness_kind: Mapped[str] = mapped_column(String(40), nullable=False)
    harness_session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    observed_model: Mapped[str | None] = mapped_column(String(255))
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    received_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)


def immutable_observation(*_args):
    raise ValueError("Runtime observations are not edited; record a new observation instead")


event.listen(AgentRuntimeObservation, "before_update", immutable_observation)
