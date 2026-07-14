"""Project model."""
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.release import Release
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.agent import AgentActor
    from app.models.iteration import Iteration
    from app.models.request_source import RequestSourceLink
    from app.models.task import Task
    from app.models.team_member import TeamMember, TeamMemberProfile
    from app.models.user_session import UserSession


class ProjectStatus(str, Enum):
    """Project lifecycle status."""
    PROPOSED = "proposed"
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELED = "canceled"


class ProjectHealth(str, Enum):
    """Project delivery health."""
    UNKNOWN = "unknown"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"


class ProjectMilestoneStatus(str, Enum):
    """Explicit lifecycle status for a project milestone."""
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Initiative(Base):
    """Strategic goal that groups related projects on the roadmap."""
    __tablename__ = "initiatives"
    __table_args__ = (
        CheckConstraint(
            "health IN ('unknown', 'on_track', 'at_risk', 'off_track')",
            name="ck_initiatives_health",
        ),
        Index("ix_initiatives_target_name", "target_date", "name", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("team_members.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    owner_profile_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("team_member_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    health: Mapped[str] = mapped_column(
        String(50),
        default=ProjectHealth.UNKNOWN.value,
        nullable=False,
        index=True,
    )
    target_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    owner: Mapped[Optional["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="owned_initiatives",
    )
    owner_profile: Mapped[Optional["TeamMemberProfile"]] = relationship(
        "TeamMemberProfile",
        back_populates="owned_initiatives",
    )
    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="initiative",
        passive_deletes=True,
    )


class Project(Base):
    """Outcome-oriented planning container above tasks and iterations."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default=ProjectStatus.PLANNED.value, nullable=False, index=True
    )
    health: Mapped[str] = mapped_column(
        String(50), default=ProjectHealth.UNKNOWN.value, nullable=False, index=True
    )
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    target_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    owner_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("team_members.id", ondelete="SET NULL"), nullable=True, index=True
    )
    owner_profile_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("team_member_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    initiative_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("initiatives.id", ondelete="SET NULL"), nullable=True, index=True
    )

    owner: Mapped[Optional["TeamMember"]] = relationship(
        "TeamMember", back_populates="owned_projects"
    )
    owner_profile: Mapped[Optional["TeamMemberProfile"]] = relationship(
        "TeamMemberProfile", back_populates="owned_projects"
    )
    initiative: Mapped[Optional["Initiative"]] = relationship(
        "Initiative", back_populates="projects"
    )
    iterations: Mapped[list["Iteration"]] = relationship(
        "Iteration", back_populates="project", passive_deletes=True
    )
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="project")
    updates: Mapped[list["ProjectUpdateEntry"]] = relationship(
        "ProjectUpdateEntry",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    milestones: Mapped[list["ProjectMilestone"]] = relationship(
        "ProjectMilestone",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by=(
            "ProjectMilestone.sort_order, "
            "ProjectMilestone.target_date, "
            "ProjectMilestone.id"
        ),
    )
    releases: Mapped[list["Release"]] = relationship(
        "Release",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by=lambda: [
            Release.target_date.is_(None),
            Release.target_date,
            Release.id,
        ],
    )
    request_source_links: Mapped[list["RequestSourceLink"]] = relationship(
        "RequestSourceLink",
        back_populates="project",
        passive_deletes=True,
        order_by="RequestSourceLink.created_at, RequestSourceLink.id",
    )


class ProjectUpdateEntry(Base):
    """Append-only structured status update for a project."""
    __tablename__ = "project_updates"
    __table_args__ = (
        CheckConstraint(
            "health IN ('unknown', 'on_track', 'at_risk', 'off_track')",
            name="ck_project_updates_health",
        ),
        Index("ix_project_updates_project_created", "project_id", "created_at", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    health: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    progress_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risks_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    decisions_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    next_steps_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_session_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("user_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by_actor_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("agent_actors.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    evidence_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    correlation_id: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, index=True
    )
    idempotency_key: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False, index=True
    )

    project: Mapped["Project"] = relationship("Project", back_populates="updates")
    created_by_session: Mapped[Optional["UserSession"]] = relationship(
        "UserSession",
        back_populates="project_updates",
    )
    created_by_actor: Mapped[Optional["AgentActor"]] = relationship(
        "AgentActor", back_populates="project_updates_authored"
    )


class ProjectMilestone(Base):
    """Manually ordered milestone for a single project roadmap."""
    __tablename__ = "project_milestones"
    __table_args__ = (
        CheckConstraint(
            "status IN ('planned', 'active', 'completed', 'canceled')",
            name="ck_project_milestones_status",
        ),
        Index(
            "ix_project_milestones_project_order",
            "project_id",
            "sort_order",
            "target_date",
            "id",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    target_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(UTCDateTime(), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default=ProjectMilestoneStatus.PLANNED.value,
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    project: Mapped["Project"] = relationship("Project", back_populates="milestones")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="milestone")
