"""Durable authentication subjects, scoped authority and attributable ownership."""

from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.utils.time import UTCDateTime, utc_now


class Principal(Base):
    __tablename__ = "principals"
    __table_args__ = (CheckConstraint("kind IN ('human', 'agent', 'system')", name="ck_principals_kind"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    agent_actor_id: Mapped[int | None] = mapped_column(ForeignKey("agent_actors.id", ondelete="RESTRICT"), unique=True)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class IdentitySubject(Base):
    __tablename__ = "identity_subjects"
    __table_args__ = (UniqueConstraint("issuer", "subject", name="uq_identity_subject"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="CASCADE"), index=True)
    issuer: Mapped[str] = mapped_column(String(512), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class WorkspaceMembership(Base):
    __tablename__ = "workspace_memberships"
    __table_args__ = (CheckConstraint("role IN ('owner', 'operator', 'member')", name="ck_workspace_memberships_role"),)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class WorkspaceAuthorityState(Base):
    __tablename__ = "workspace_authority_state"
    __table_args__ = (CheckConstraint("id = 1", name="ck_workspace_authority_singleton"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    bootstrap_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    operator_principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))


class ProjectMembership(Base):
    __tablename__ = "project_memberships"
    __table_args__ = (CheckConstraint("role IN ('viewer', 'editor', 'executor', 'reviewer', 'manager')", name="ck_project_memberships_role"),)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="CASCADE"), primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class PrincipalProfileLink(Base):
    __tablename__ = "principal_profile_links"
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="CASCADE"), primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("team_member_profiles.id", ondelete="RESTRICT"), unique=True)
    linked_by_principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"))
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class OIDCLoginAttempt(Base):
    __tablename__ = "oidc_login_attempts"
    state_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    browser_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    nonce: Mapped[str] = mapped_column(String(128), nullable=False)
    verifier: Mapped[str] = mapped_column(String(128), nullable=False)
    return_path: Mapped[str] = mapped_column(String(512), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, index=True)
    consumed_at: Mapped[datetime | None] = mapped_column(UTCDateTime())


class OwnershipTransfer(Base):
    __tablename__ = "ownership_transfers"
    guest_session_id: Mapped[int] = mapped_column(ForeignKey("user_sessions.id", ondelete="RESTRICT"), primary_key=True)
    principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"), nullable=False)
    authorized_by_principal_id: Mapped[int] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    transferred_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now)


class CommandAudit(Base):
    __tablename__ = "command_audit"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    principal_id: Mapped[int | None] = mapped_column(ForeignKey("principals.id", ondelete="RESTRICT"), index=True)
    project_id: Mapped[int | None] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    details: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), default=utc_now, index=True)
