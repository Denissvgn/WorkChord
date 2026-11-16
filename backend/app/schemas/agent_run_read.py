"""A run as a reader sees it: status, model, harness session and declared usage, without logs."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.agent import AgentAssignmentActorSummary
from app.schemas.execution_usage import ExecutionUsageResponse


class AgentRunHarness(BaseModel):
    """The harness session the actor declared at begin; never verified."""

    kind: str
    session_id: str


class AgentRunReadItem(BaseModel):
    """One run, for people, observers, operators and planning agents.

    Run events, logs, artifacts, summaries and errors stay with run detail,
    which needs the admin key or an agent key.
    """

    id: int
    task_id: Optional[int] = None
    assignment_id: Optional[int] = None
    actor_id: int
    actor: Optional[AgentAssignmentActorSummary] = None
    status: str
    trace_id: Optional[str] = None
    harness: Optional[AgentRunHarness] = None
    model: Optional[str] = None
    configured_model_alias: Optional[str] = None
    resolved_model_id: Optional[str] = None
    model_trust_state: str
    started_at: datetime
    heartbeat_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    # The latest declared usage report for this run; actor declarations, not reconciled.
    usage: Optional[ExecutionUsageResponse] = None
