"""Task model."""
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text, and_
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship

from app.database import Base
from app.models.external_link import ExternalLink
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment, TaskEvent
    from app.models.external_link import ExternalLink
    from app.models.iteration import Iteration
    from app.models.project import Project, ProjectMilestone
    from app.models.request_source import RequestSourceLink
    from app.models.team_member import TeamMember
    from app.models.task_status_log import TaskStatusLog


class TaskStatus(str, Enum):
    """Task status enumeration for work tracking.

    Workflow: PLANNED -> ACTIVE -> RESOLVED -> CLOSED
    - PLANNED: Auto-assigned on task creation
    - ACTIVE: Work has started
    - RESOLVED: Work completed, pending validation
    - CLOSED: Fully completed and validated
    """
    PLANNED = "planned"
    ACTIVE = "active"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Task(Base):
    """Task model with tree structure and dependencies."""
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=5)  # 1=highest

    # Effort estimation
    effort_days: Mapped[float] = mapped_column(Float, default=1.0)
    effort_hours: Mapped[float] = mapped_column(Float, default=8.0)

    # Status
    status: Mapped[str] = mapped_column(String(50), default=TaskStatus.PLANNED.value)

    # Scheduled dates (computed by scheduler)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Actual dates (set when status changes)
    actual_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)  # Set when status -> ACTIVE
    actual_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)    # Set when status -> CLOSED

    # Calculated effort (computed by scheduler, includes coefficients)
    calculated_effort_days: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # User-defined constraint dates (task scheduling limits)
    min_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    max_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Task flags
    is_optional: Mapped[bool] = mapped_column(default=False)  # Lower priority in scheduling
    is_deferred: Mapped[bool] = mapped_column(default=False)  # Excluded from scheduling

    # Tags (JSON array of strings)
    tags: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, default="[]")

    # Manual ordering within parent (for drag-drop)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    # External task source and agent control-plane metadata
    external_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    claim_expires_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    claim_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    claim_generation: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    # Foreign keys
    iteration_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("iterations.id"), nullable=False
    )
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True, index=True
    )
    milestone_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("project_milestones.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=True
    )
    assignee_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("team_members.id"), nullable=True
    )
    claimed_by: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("agent_actors.id"), nullable=True
    )

    # Relationships
    iteration: Mapped["Iteration"] = relationship("Iteration", back_populates="tasks")
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="tasks")
    milestone: Mapped[Optional["ProjectMilestone"]] = relationship(
        "ProjectMilestone",
        back_populates="tasks",
    )
    assignee: Mapped[Optional["TeamMember"]] = relationship("TeamMember", back_populates="tasks")
    claimed_agent: Mapped[Optional["AgentActor"]] = relationship(
        "AgentActor", back_populates="claimed_tasks"
    )

    # Self-referential relationship for tree structure
    parent: Mapped[Optional["Task"]] = relationship(
        "Task", back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Task"]] = relationship(
        "Task", back_populates="parent", cascade="all, delete-orphan",
        order_by="Task.sort_order"
    )

    # Dependencies (many-to-many through TaskDependency)
    dependencies: Mapped[list["TaskDependency"]] = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    dependents: Mapped[list["TaskDependency"]] = relationship(
        "TaskDependency",
        foreign_keys="TaskDependency.depends_on_id",
        back_populates="depends_on",
        cascade="all, delete-orphan"
    )

    # Status change audit log
    status_logs: Mapped[list["TaskStatusLog"]] = relationship(
        "TaskStatusLog",
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="TaskStatusLog.changed_at.desc()"
    )
    events: Mapped[list["TaskEvent"]] = relationship(
        "TaskEvent",
        back_populates="task",
        passive_deletes=True,
        order_by="TaskEvent.created_at.desc()"
    )
    agent_runs: Mapped[list["AgentRun"]] = relationship(
        "AgentRun",
        back_populates="task",
        passive_deletes=True,
        order_by="AgentRun.started_at.desc()"
    )
    agent_assignments: Mapped[list["AgentTaskAssignment"]] = relationship(
        "AgentTaskAssignment",
        back_populates="task",
        cascade="all, delete-orphan",
        order_by="AgentTaskAssignment.created_at.desc()",
    )
    external_links: Mapped[list["ExternalLink"]] = relationship(
        "ExternalLink",
        primaryjoin=lambda: and_(
            Task.id == foreign(ExternalLink.entity_id),
            ExternalLink.entity_type == "task",
        ),
        order_by="ExternalLink.created_at, ExternalLink.id",
        viewonly=True,
    )
    request_source_links: Mapped[list["RequestSourceLink"]] = relationship(
        "RequestSourceLink",
        back_populates="task",
        passive_deletes=True,
        order_by="RequestSourceLink.created_at, RequestSourceLink.id",
    )


class TaskDependency(Base):
    """Task dependency relationship (including cross-parent subtask dependencies)."""
    __tablename__ = "task_dependencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    task_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=False
    )
    depends_on_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tasks.id"), nullable=False
    )

    # Relationships
    task: Mapped["Task"] = relationship(
        "Task", foreign_keys=[task_id], back_populates="dependencies"
    )
    depends_on: Mapped["Task"] = relationship(
        "Task", foreign_keys=[depends_on_id], back_populates="dependents"
    )
