"""Team member model."""
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, CheckConstraint, Date, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.utils.time import UTCDateTime, utc_now

if TYPE_CHECKING:
    from app.models.agent import AgentActor
    from app.models.iteration import Iteration
    from app.models.project import Initiative, Project
    from app.models.task import Task


class TeamMember(Base):
    """Team member model with availability and capacity settings."""
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)

    # Email for notifications (optional)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Availability settings
    availability_percent: Mapped[float] = mapped_column(Float, default=100.0)
    professionalism_coefficient: Mapped[float] = mapped_column(Float, default=1.0)
    operational_utilization: Mapped[float] = mapped_column(Float, default=20.0)

    # Foreign keys - nullable to allow team member reuse across iterations
    iteration_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("iterations.id", ondelete="SET NULL"), nullable=True
    )
    profile_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("team_member_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    iteration: Mapped["Iteration | None"] = relationship("Iteration", back_populates="team_members")
    profile: Mapped["TeamMemberProfile | None"] = relationship(
        "TeamMemberProfile",
        back_populates="team_members",
    )
    vacations: Mapped[list["Vacation"]] = relationship(
        "Vacation", back_populates="team_member", cascade="all, delete-orphan"
    )
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="assignee")
    owned_projects: Mapped[list["Project"]] = relationship(
        "Project", back_populates="owner"
    )
    owned_initiatives: Mapped[list["Initiative"]] = relationship(
        "Initiative", back_populates="owner"
    )

    @property
    def iteration_name(self) -> str | None:
        """Return the iteration display name for compact owner selectors."""
        return self.iteration.name if self.iteration else None


class TeamMemberProfile(Base):
    """Reusable person profile for durable capability and preference metadata."""
    __tablename__ = "team_member_profiles"
    __table_args__ = (
        Index("ix_team_member_profiles_display_name", "display_name"),
        Index("ix_team_member_profiles_email", "email"),
        Index("ix_team_member_profiles_automation_enabled", "automation_enabled"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seed_key: Mapped[Optional[str]] = mapped_column(
        String(120), nullable=True, unique=True, index=True
    )
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    automation_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    profile_kind: Mapped[str] = mapped_column(String(30), default="human", nullable=False)
    assignment_modes: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    skills: Mapped[list["TeamMemberProfileSkill"]] = relationship(
        "TeamMemberProfileSkill",
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by="TeamMemberProfileSkill.category, TeamMemberProfileSkill.skill_name, TeamMemberProfileSkill.id",
    )
    team_members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="profile",
        passive_deletes=True,
    )
    agent_actors: Mapped[list["AgentActor"]] = relationship(
        "AgentActor",
        back_populates="profile",
        passive_deletes=True,
    )
    owned_projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="owner_profile",
        passive_deletes=True,
    )
    owned_initiatives: Mapped[list["Initiative"]] = relationship(
        "Initiative",
        back_populates="owner_profile",
        passive_deletes=True,
    )


class TeamMemberProfileSkill(Base):
    """Structured skill or weakness attached to a reusable team-member profile."""
    __tablename__ = "team_member_profile_skills"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 5", name="ck_team_member_profile_skills_level"),
        CheckConstraint("interest >= 1 AND interest <= 5", name="ck_team_member_profile_skills_interest"),
        Index("ix_team_member_profile_skills_profile_id", "profile_id"),
        Index("ix_team_member_profile_skills_skill_key", "skill_key"),
        Index("ix_team_member_profile_skills_category", "category"),
        Index("ix_team_member_profile_skills_is_weakness", "is_weakness"),
        UniqueConstraint(
            "profile_id",
            "skill_key",
            name="uq_team_member_profile_skills_profile_skill_key",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("team_member_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    skill_key: Mapped[str] = mapped_column(String(120), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    level: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    interest: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    is_weakness: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    keywords_json: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False
    )

    profile: Mapped["TeamMemberProfile"] = relationship(
        "TeamMemberProfile",
        back_populates="skills",
    )


class Vacation(Base):
    """Vacation period for a team member."""
    __tablename__ = "vacations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Foreign keys
    team_member_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("team_members.id"), nullable=False
    )

    # Relationships
    team_member: Mapped["TeamMember"] = relationship("TeamMember", back_populates="vacations")
