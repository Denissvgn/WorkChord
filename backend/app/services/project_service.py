"""Project service with CRUD and summary logic."""
from datetime import date, datetime
from typing import Optional, Sequence

from sqlalchemy import Select, case, exists, func, select, update
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.iteration import Iteration
from app.models.project import (
    Initiative,
    Project,
    ProjectMilestone,
    ProjectMilestoneStatus,
    ProjectStatus,
    ProjectUpdateEntry,
)
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.team_member import TeamMember, TeamMemberProfile
from app.query_limits import (
    CollectionLimitExceededError,
    MAX_BOUNDED_LIST_ITEMS,
    MAX_PROJECT_LIST_ITEMS,
    MAX_PROJECT_TREE_TASKS,
)
from app.schemas.project import (
    InitiativeCreate,
    InitiativeUpdate,
    ProjectCreate,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneSummary,
    ProjectMilestoneTaskGroup,
    ProjectMilestoneUpdate,
    ProjectSummary,
    STALE_PROJECT_UPDATE_DAYS,
    ProjectTargetDateRisk,
    ProjectUpdate,
    ProjectUpdateEntryCreate,
    ProjectUpdateEntryResponse,
    ProjectUpdateFreshness,
)
from app.schemas.team import TeamMemberOptionResponse, TeamMemberProfileCompact
from app.services.outbound_webhook_service import emit_outbound_webhook_event
from app.services.request_source_service import RequestSourceService
from app.sql_semantics import portable_case_insensitive_equal
from app.utils.time import as_utc, utc_now


class ProjectService:
    """Service for project CRUD, linked task retrieval, and summary metrics."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _project_options(self) -> tuple:
        """Return relationship loading options shared by project reads."""
        return (
            selectinload(Project.owner).selectinload(TeamMember.iteration),
            selectinload(Project.owner_profile).selectinload(TeamMemberProfile.skills),
            selectinload(Project.initiative)
            .selectinload(Initiative.owner)
            .selectinload(TeamMember.iteration),
            selectinload(Project.initiative)
            .selectinload(Initiative.owner_profile)
            .selectinload(TeamMemberProfile.skills),
        )

    def _project_query(self) -> Select:
        """Build a base project query with common relationship options."""
        return select(Project).options(*self._project_options())

    def _enum_value(self, value):
        """Normalize Pydantic enum values before assigning to string columns."""
        return value.value if hasattr(value, "value") else value

    def _normalize_text_key(self, value: str | None) -> str:
        """Return a lowercase matching key for profile backfill and legacy owner writes."""
        return " ".join((value or "").strip().lower().split())

    async def _get_owner_member(self, owner_id: int) -> TeamMember | None:
        """Load a legacy team-member owner by id."""
        result = await self.db.execute(
            select(TeamMember).where(TeamMember.id == owner_id)
        )
        return result.scalar_one_or_none()

    async def _get_owner_profile(self, profile_id: int) -> TeamMemberProfile | None:
        """Load a reusable owner profile by id."""
        result = await self.db.execute(
            select(TeamMemberProfile).where(TeamMemberProfile.id == profile_id)
        )
        return result.scalar_one_or_none()

    async def _require_owner_profile_exists(
        self,
        owner_profile_id: Optional[int],
    ) -> TeamMemberProfile | None:
        """Validate an optional global owner profile reference."""
        if owner_profile_id is None:
            return None

        profile = await self._get_owner_profile(owner_profile_id)
        if profile is None:
            raise ValueError(f"Team member profile with id {owner_profile_id} not found")
        return profile

    async def _find_matching_profile_for_member(
        self,
        member: TeamMember,
    ) -> TeamMemberProfile | None:
        """Find an existing profile by email or display name for a legacy owner."""
        normalized_email = self._normalize_text_key(member.email)
        if normalized_email:
            result = await self.db.execute(
                select(TeamMemberProfile)
                .where(
                    portable_case_insensitive_equal(
                        TeamMemberProfile.email,
                        normalized_email,
                    )
                )
                .order_by(TeamMemberProfile.id)
            )
            profile = result.scalars().first()
            if profile is not None:
                return profile

        normalized_name = self._normalize_text_key(member.name)
        if normalized_name:
            result = await self.db.execute(
                select(TeamMemberProfile).order_by(TeamMemberProfile.id)
            )
            for profile in result.scalars().all():
                if self._normalize_text_key(profile.display_name) == normalized_name:
                    return profile

        return None

    async def _resolve_profile_for_legacy_owner(
        self,
        member: TeamMember,
    ) -> TeamMemberProfile:
        """Return or create the global profile for a legacy team-member owner."""
        if member.profile_id is not None:
            profile = await self._get_owner_profile(member.profile_id)
            if profile is not None:
                return profile

        profile = await self._find_matching_profile_for_member(member)
        if profile is None:
            profile = TeamMemberProfile(
                display_name=member.name.strip(),
                email=member.email.strip() if member.email else None,
                headline=member.position,
                summary=None,
                notes=None,
                automation_enabled=True,
            )
            self.db.add(profile)
            await self.db.flush()

        member.profile_id = profile.id
        await self.db.flush()
        return profile

    async def _resolve_owner_refs(
        self,
        owner_id: Optional[int],
        owner_profile_id: Optional[int],
    ) -> tuple[Optional[int], Optional[int]]:
        """Normalize legacy and profile owner references for a write payload."""
        profile = await self._require_owner_profile_exists(owner_profile_id)
        if owner_id is None:
            return None, profile.id if profile else None

        member = await self._get_owner_member(owner_id)
        if member is None:
            raise ValueError(f"Team member with id {owner_id} not found")

        if profile is not None:
            if member.profile_id is not None and member.profile_id != profile.id:
                raise ValueError(
                    f"Team member with id {owner_id} is linked to profile "
                    f"{member.profile_id}, not {profile.id}"
                )
            if member.profile_id is None:
                member.profile_id = profile.id
                await self.db.flush()
            return owner_id, profile.id

        profile = await self._resolve_profile_for_legacy_owner(member)
        return owner_id, profile.id

    async def _normalize_owner_update_data(self, update_data: dict) -> None:
        """Mutate update data so any owner write carries both transitional refs."""
        if "owner_id" not in update_data and "owner_profile_id" not in update_data:
            return

        owner_id, owner_profile_id = await self._resolve_owner_refs(
            update_data.get("owner_id"),
            update_data.get("owner_profile_id"),
        )
        update_data["owner_id"] = owner_id
        update_data["owner_profile_id"] = owner_profile_id

    async def _initiative_exists(self, initiative_id: int) -> bool:
        """Return whether an initiative exists without loading relationships."""
        result = await self.db.execute(
            select(Initiative.id).where(Initiative.id == initiative_id)
        )
        return result.scalar_one_or_none() is not None

    async def _require_initiative_exists(self, initiative_id: Optional[int]) -> None:
        """Validate an optional initiative reference."""
        if initiative_id is not None and not await self._initiative_exists(initiative_id):
            raise ValueError(f"Initiative with id {initiative_id} not found")

    async def list_initiatives(self) -> Sequence[Initiative]:
        """List initiatives ordered for portfolio planning."""
        result = await self.db.execute(
            select(Initiative)
            .options(
                selectinload(Initiative.owner).selectinload(TeamMember.iteration),
                selectinload(Initiative.owner_profile).selectinload(TeamMemberProfile.skills),
            )
            .order_by(
                Initiative.target_date.asc().nulls_last(),
                Initiative.name.asc(),
                Initiative.id.asc(),
            )
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        initiatives = list(result.scalars().all())
        if len(initiatives) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "initiative list",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return initiatives

    async def get_initiative_by_id(self, initiative_id: int) -> Optional[Initiative]:
        """Get initiative by ID."""
        result = await self.db.execute(
            select(Initiative)
            .options(
                selectinload(Initiative.owner).selectinload(TeamMember.iteration),
                selectinload(Initiative.owner_profile).selectinload(TeamMemberProfile.skills),
            )
            .where(Initiative.id == initiative_id)
        )
        return result.scalar_one_or_none()

    async def count_initiative_projects(self, initiative_id: int) -> int:
        """Count projects assigned to an initiative."""
        result = await self.db.execute(
            select(func.count(Project.id)).where(Project.initiative_id == initiative_id)
        )
        return int(result.scalar_one())

    async def create_initiative(self, data: InitiativeCreate) -> Initiative:
        """Create an initiative."""
        owner_id, owner_profile_id = await self._resolve_owner_refs(
            data.owner_id,
            data.owner_profile_id,
        )

        initiative = Initiative(
            name=data.name,
            description=data.description,
            owner_id=owner_id,
            owner_profile_id=owner_profile_id,
            health=self._enum_value(data.health),
            target_date=data.target_date,
        )
        self.db.add(initiative)
        try:
            await self.db.flush()
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="project.initiative_created",
                entity_type="initiative",
                entity_id=initiative.id,
                data={
                    "initiative_id": initiative.id,
                    "name": initiative.name,
                    "owner_id": initiative.owner_id,
                    "owner_profile_id": initiative.owner_profile_id,
                    "health": initiative.health,
                    "target_date": initiative.target_date.isoformat() if initiative.target_date else None,
                },
            )
            await self.db.commit()
            await self.db.refresh(initiative)
        except Exception:
            await self.db.rollback()
            raise
        created = await self.get_initiative_by_id(initiative.id)
        if created is None:
            raise RuntimeError("Created initiative could not be reloaded")
        return created

    async def update_initiative(
        self,
        initiative_id: int,
        data: InitiativeUpdate,
    ) -> Optional[Initiative]:
        """Apply a partial initiative update."""
        initiative = await self.get_initiative_by_id(initiative_id)
        if not initiative:
            return None

        update_data = data.model_dump(exclude_unset=True)
        await self._normalize_owner_update_data(update_data)

        for field, value in update_data.items():
            setattr(initiative, field, self._enum_value(value))

        try:
            if update_data:
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="project.initiative_updated",
                    entity_type="initiative",
                    entity_id=initiative.id,
                    data={
                        "initiative_id": initiative.id,
                        "name": initiative.name,
                        "changes": {
                            field: self._enum_value(value)
                            for field, value in update_data.items()
                        },
                    },
                )
            await self.db.commit()
            await self.db.refresh(initiative)
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_initiative_by_id(initiative.id)

    async def delete_initiative(self, initiative_id: int) -> bool:
        """Delete an initiative, leaving assigned projects intact."""
        initiative = await self.get_initiative_by_id(initiative_id)
        if not initiative:
            return False

        initiative_name = initiative.name
        try:
            await self.db.execute(
                update(Project)
                .where(Project.initiative_id == initiative_id)
                .values(initiative_id=None)
            )
            await self.db.delete(initiative)
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="project.initiative_deleted",
                entity_type="initiative",
                entity_id=initiative_id,
                data={"initiative_id": initiative_id, "name": initiative_name},
            )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return True

    async def list_projects(self) -> Sequence[Project]:
        """List projects ordered for planning views."""
        result = await self.db.execute(
            self._project_query()
            .order_by(
                Project.sort_order.asc(),
                Project.target_date.asc().nulls_last(),
                Project.id.asc(),
            )
            .limit(MAX_PROJECT_LIST_ITEMS + 1)
        )
        projects = list(result.scalars().all())
        if len(projects) > MAX_PROJECT_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "project list",
                MAX_PROJECT_LIST_ITEMS,
            )
        return projects

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID."""
        result = await self.db.execute(
            self._project_query().where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def _project_exists(self, project_id: int) -> bool:
        """Return whether a project exists without loading relationships."""
        result = await self.db.execute(
            select(Project.id).where(Project.id == project_id)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, data: ProjectCreate, *, commit: bool = True) -> Project:
        """Create a project, optionally leaving commit ownership to the caller."""
        owner_id, owner_profile_id = await self._resolve_owner_refs(
            data.owner_id,
            data.owner_profile_id,
        )
        await self._require_initiative_exists(data.initiative_id)

        project = Project(
            name=data.name,
            description=data.description,
            status=self._enum_value(data.status),
            health=self._enum_value(data.health),
            owner_id=owner_id,
            owner_profile_id=owner_profile_id,
            initiative_id=data.initiative_id,
            start_date=data.start_date,
            target_date=data.target_date,
            sort_order=data.sort_order,
        )
        self.db.add(project)
        try:
            await self.db.flush()
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="project.created",
                entity_type="project",
                entity_id=project.id,
                data={
                    "project_id": project.id,
                    "name": project.name,
                    "status": project.status,
                    "health": project.health,
                    "owner_id": project.owner_id,
                    "owner_profile_id": project.owner_profile_id,
                    "initiative_id": project.initiative_id,
                },
            )
            if commit:
                await self.db.commit()
            else:
                await self.db.flush()
            await self.db.refresh(project)
        except Exception:
            await self.db.rollback()
            raise
        created = await self.get_by_id(project.id)
        if created is None:
            raise RuntimeError("Created project could not be reloaded")
        return created

    async def update(
        self,
        project_id: int,
        data: ProjectUpdate,
        *,
        commit: bool = True,
    ) -> Optional[Project]:
        """Apply a partial project update, optionally deferring the commit."""
        project = await self.get_by_id(project_id)
        if not project:
            return None

        update_data = data.model_dump(exclude_unset=True)
        await self._normalize_owner_update_data(update_data)
        if "initiative_id" in update_data:
            await self._require_initiative_exists(update_data["initiative_id"])
        if update_data.get("completed_at") is not None:
            update_data["completed_at"] = as_utc(update_data["completed_at"])

        for field, value in update_data.items():
            setattr(project, field, self._enum_value(value))

        updated_project_id = project.id
        try:
            if update_data:
                await emit_outbound_webhook_event(
                    self.db,
                    commit=False,
                    event_type="project.updated",
                    entity_type="project",
                    entity_id=updated_project_id,
                    data={
                        "project_id": updated_project_id,
                        "name": project.name,
                        "changes": {
                            field: self._enum_value(value)
                            for field, value in update_data.items()
                        },
                    },
                )
            if commit:
                await self.db.commit()
            else:
                await self.db.flush()
            await self.db.refresh(project)
        except Exception:
            await self.db.rollback()
            raise
        return await self.get_by_id(updated_project_id)

    async def create_project_update(
        self,
        project_id: int,
        data: ProjectUpdateEntryCreate,
        created_by_session_id: Optional[int],
        *,
        created_by_actor_id: Optional[int] = None,
        evidence_json: Optional[dict] = None,
        correlation_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[ProjectUpdateEntry]:
        """Create an append-only project update and apply its health to the project."""
        project = await self.get_by_id(project_id)
        if not project:
            return None

        update_entry = ProjectUpdateEntry(
            project_id=project_id,
            health=self._enum_value(data.health),
            summary=data.summary,
            progress_text=data.progress_text,
            risks_text=data.risks_text,
            decisions_text=data.decisions_text,
            next_steps_text=data.next_steps_text,
            created_by_session_id=created_by_session_id,
            created_by_actor_id=created_by_actor_id,
            evidence_json=evidence_json or {},
            correlation_id=correlation_id,
            idempotency_key=idempotency_key,
        )
        project.health = update_entry.health

        self.db.add(update_entry)
        try:
            await self.db.flush()
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="project.health_updated",
                entity_type="project",
                entity_id=project_id,
                data={
                    "project_id": project_id,
                    "project_update_id": update_entry.id,
                    "health": update_entry.health,
                    "summary": update_entry.summary,
                    "created_by_session_id": created_by_session_id,
                    "created_by_actor_id": created_by_actor_id,
                    "evidence": evidence_json or {},
                    "correlation_id": correlation_id,
                },
            )
            if commit:
                await self.db.commit()
                await self.db.refresh(update_entry)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return update_entry

    async def list_project_updates(
        self,
        project_id: int,
    ) -> Optional[Sequence[ProjectUpdateEntry]]:
        """List append-only project updates in newest-first order."""
        if not await self._project_exists(project_id):
            return None

        result = await self.db.execute(
            select(ProjectUpdateEntry)
            .where(ProjectUpdateEntry.project_id == project_id)
            .order_by(ProjectUpdateEntry.created_at.desc(), ProjectUpdateEntry.id.desc())
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        updates = list(result.scalars().all())
        if len(updates) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "project update list",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return updates

    async def list_milestones(
        self,
        project_id: int,
    ) -> Optional[Sequence[ProjectMilestone]]:
        """List project milestones in roadmap order."""
        if not await self._project_exists(project_id):
            return None

        result = await self.db.execute(
            select(ProjectMilestone)
            .where(ProjectMilestone.project_id == project_id)
            .order_by(
                ProjectMilestone.sort_order.asc(),
                ProjectMilestone.target_date.asc().nulls_last(),
                ProjectMilestone.id.asc(),
            )
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        milestones = list(result.scalars().all())
        if len(milestones) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "project milestone list",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return milestones

    async def get_milestone_for_project(
        self,
        project_id: int,
        milestone_id: int,
    ) -> Optional[ProjectMilestone]:
        """Return a milestone only when it belongs to the requested project."""
        result = await self.db.execute(
            select(ProjectMilestone).where(
                ProjectMilestone.id == milestone_id,
                ProjectMilestone.project_id == project_id,
            )
        )
        return result.scalar_one_or_none()

    def _completed_at_for_milestone_write(
        self,
        status_value: str,
        completed_at: Optional[datetime],
        existing_completed_at: Optional[datetime] = None,
    ) -> Optional[datetime]:
        """Apply milestone completion timestamp defaults for status writes."""
        if status_value == ProjectMilestoneStatus.COMPLETED.value:
            value = completed_at or existing_completed_at or utc_now()
            return as_utc(value)
        return as_utc(completed_at) if completed_at is not None else None

    async def create_milestone(
        self,
        project_id: int,
        data: ProjectMilestoneCreateRequest,
        *,
        commit: bool = True,
    ) -> Optional[ProjectMilestone]:
        """Create a milestone under a project path."""
        if not await self._project_exists(project_id):
            return None

        status_value = self._enum_value(data.status)
        milestone = ProjectMilestone(
            project_id=project_id,
            name=data.name,
            description=data.description,
            target_date=data.target_date,
            completed_at=self._completed_at_for_milestone_write(
                status_value,
                data.completed_at,
            ),
            sort_order=data.sort_order,
            status=status_value,
        )
        self.db.add(milestone)
        try:
            await self.db.flush()
            if commit:
                await self.db.commit()
                await self.db.refresh(milestone)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return milestone

    async def update_milestone(
        self,
        project_id: int,
        milestone_id: int,
        data: ProjectMilestoneUpdate,
        *,
        commit: bool = True,
    ) -> Optional[ProjectMilestone]:
        """Apply a partial update to a project-scoped milestone."""
        milestone = await self.get_milestone_for_project(project_id, milestone_id)
        if milestone is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "status" in update_data:
            status_value = self._enum_value(update_data["status"])
            update_data["status"] = status_value
            if "completed_at" not in update_data:
                update_data["completed_at"] = self._completed_at_for_milestone_write(
                    status_value,
                    None,
                    milestone.completed_at,
                )

        for field, value in update_data.items():
            setattr(milestone, field, self._enum_value(value))

        try:
            await self.db.flush()
            if commit:
                await self.db.commit()
                await self.db.refresh(milestone)
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return milestone

    async def delete_milestone(
        self,
        project_id: int,
        milestone_id: int,
        *,
        commit: bool = True,
    ) -> Optional[int]:
        """Delete a project milestone after detaching linked tasks."""
        milestone = await self.get_milestone_for_project(project_id, milestone_id)
        if milestone is None:
            return None

        result = await self.db.execute(
            select(func.count(Task.id)).where(Task.milestone_id == milestone_id)
        )
        detached_task_count = int(result.scalar_one())
        if detached_task_count:
            await self.db.execute(
                update(Task)
                .where(Task.milestone_id == milestone_id)
                .values(milestone_id=None)
            )

        await self.db.delete(milestone)
        try:
            await self.db.flush()
            if commit:
                await self.db.commit()
        except Exception:
            if commit:
                await self.db.rollback()
            raise
        return detached_task_count

    async def list_iterations(
        self,
        project_id: int,
    ) -> Optional[Sequence[Iteration]]:
        """List iterations scoped to a project in newest-first order."""
        if not await self._project_exists(project_id):
            return None

        result = await self.db.execute(
            select(Iteration)
            .where(Iteration.project_id == project_id)
            .options(
                selectinload(Iteration.calendar),
                selectinload(Iteration.project),
            )
            .order_by(Iteration.start_date.desc(), Iteration.id.desc())
            .limit(MAX_BOUNDED_LIST_ITEMS + 1)
        )
        iterations = list(result.scalars().all())
        if len(iterations) > MAX_BOUNDED_LIST_ITEMS:
            raise CollectionLimitExceededError(
                "project iteration list",
                MAX_BOUNDED_LIST_ITEMS,
            )
        return iterations

    async def get_latest_project_update(
        self,
        project_id: int,
    ) -> Optional[ProjectUpdateEntry]:
        """Get the newest project update for summary display."""
        result = await self.db.execute(
            select(ProjectUpdateEntry)
            .where(ProjectUpdateEntry.project_id == project_id)
            .order_by(ProjectUpdateEntry.created_at.desc(), ProjectUpdateEntry.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def count_linked_tasks(self, project_id: int) -> int:
        """Count all tasks linked to a project."""
        result = await self.db.execute(
            select(func.count(Task.id)).where(Task.project_id == project_id)
        )
        return int(result.scalar_one())

    async def delete(self, project_id: int, detach_tasks: bool = False) -> str:
        """Delete a project, optionally detaching linked tasks first."""
        project = await self.get_by_id(project_id)
        if not project:
            return "not_found"

        linked_task_count = await self.count_linked_tasks(project_id)
        if linked_task_count and not detach_tasks:
            return "has_tasks"

        project_name = project.name
        try:
            if linked_task_count:
                await self.db.execute(
                    update(Task)
                    .where(Task.project_id == project_id)
                    .values(project_id=None, milestone_id=None)
                )
            await self.db.delete(project)
            await emit_outbound_webhook_event(
                self.db,
                commit=False,
                event_type="project.deleted",
                entity_type="project",
                entity_id=project_id,
                data={
                    "project_id": project_id,
                    "name": project_name,
                    "detached_task_count": linked_task_count if detach_tasks else 0,
                },
            )
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return "deleted"

    async def get_tasks(self, project_id: int) -> Optional[Sequence[Task]]:
        """Get linked root tasks for a project with response relationships loaded."""
        if not await self.get_by_id(project_id):
            return None

        bounded_ids = list(
            (
                await self.db.execute(
                    select(Task.id)
                    .where(Task.project_id == project_id)
                    .order_by(Task.id.asc())
                    .limit(MAX_PROJECT_TREE_TASKS + 1)
                )
            ).scalars()
        )
        if len(bounded_ids) > MAX_PROJECT_TREE_TASKS:
            raise CollectionLimitExceededError(
                "project task tree",
                MAX_PROJECT_TREE_TASKS,
            )

        query = (
            select(Task)
            .where(
                Task.project_id == project_id,
                Task.parent_id.is_(None),
            )
            .options(
                selectinload(Task.project),
                selectinload(Task.milestone),
                selectinload(Task.assignee),
                selectinload(Task.claimed_agent),
                selectinload(Task.external_links),
                selectinload(Task.request_source_links),
                selectinload(Task.dependencies).selectinload(TaskDependency.depends_on),
                selectinload(Task.children).selectinload(Task.project),
                selectinload(Task.children).selectinload(Task.milestone),
                selectinload(Task.children).selectinload(Task.assignee),
                selectinload(Task.children).selectinload(Task.claimed_agent),
                selectinload(Task.children).selectinload(Task.external_links),
                selectinload(Task.children).selectinload(Task.request_source_links),
                selectinload(Task.children)
                .selectinload(Task.dependencies)
                .selectinload(TaskDependency.depends_on),
                selectinload(Task.children).selectinload(Task.children),
            )
            .order_by(Task.sort_order, Task.id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def _get_all_linked_tasks(self, project_id: int) -> Sequence[Task]:
        """Get every task linked to a project for aggregate calculations."""
        result = await self.db.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .options(
                selectinload(Task.milestone),
                selectinload(Task.dependencies).selectinload(TaskDependency.depends_on)
            )
        )
        return result.scalars().all()

    def _calculate_task_date_range(
        self, tasks: Sequence[Task]
    ) -> tuple[Optional[date], Optional[date]]:
        """Calculate min scheduled start and max scheduled end date."""
        start_dates = [task.start_date for task in tasks if task.start_date is not None]
        end_dates = [task.end_date for task in tasks if task.end_date is not None]
        return (
            min(start_dates) if start_dates else None,
            max(end_dates) if end_dates else None,
        )

    def _calculate_completion_percent(
        self, total_tasks: int, completed_tasks: int
    ) -> float:
        """Calculate completion percentage for linked tasks."""
        if total_tasks == 0:
            return 0.0
        return round((completed_tasks / total_tasks) * 100, 1)

    def _calculate_schedule_progress(
        self,
        project: Project,
        task_start_date: Optional[date],
    ) -> Optional[float]:
        """Calculate elapsed schedule percentage against the project target."""
        if project.target_date is None:
            return None

        schedule_start = project.start_date or task_start_date
        if schedule_start is None:
            return None

        total_days = (project.target_date - schedule_start).days
        if total_days <= 0:
            return None

        elapsed_days = (date.today() - schedule_start).days
        progress = (elapsed_days / total_days) * 100
        return max(0.0, min(100.0, progress))

    def _calculate_target_date_risk(
        self,
        project: Project,
        total_tasks: int,
        completed_tasks: int,
        completion_percent: float,
        blocked_tasks: int,
        overdue_tasks: int,
        remaining_effort_days: float,
        task_start_date: Optional[date],
        task_end_date: Optional[date],
    ) -> tuple[ProjectTargetDateRisk, Optional[str], int, Optional[int]]:
        """Calculate target-date risk and supporting date deltas."""
        today = date.today()
        days_until_target = (
            (project.target_date - today).days
            if project.target_date is not None
            else None
        )
        target_date_slip_days = (
            max(0, (task_end_date - project.target_date).days)
            if project.target_date is not None and task_end_date is not None
            else 0
        )

        if project.status == ProjectStatus.CANCELED.value:
            return (
                ProjectTargetDateRisk.UNKNOWN,
                "Project is canceled.",
                target_date_slip_days,
                days_until_target,
            )

        if project.target_date is None:
            return (
                ProjectTargetDateRisk.UNKNOWN,
                "No project target date is set.",
                target_date_slip_days,
                days_until_target,
            )

        if total_tasks == 0:
            return (
                ProjectTargetDateRisk.UNKNOWN,
                "No linked tasks to evaluate.",
                target_date_slip_days,
                days_until_target,
            )

        if task_end_date is None:
            return (
                ProjectTargetDateRisk.UNKNOWN,
                "Linked tasks have no scheduled end dates.",
                target_date_slip_days,
                days_until_target,
            )

        if target_date_slip_days > 0:
            return (
                ProjectTargetDateRisk.OFF_TRACK,
                f"Scheduled work exceeds target by {target_date_slip_days} day(s).",
                target_date_slip_days,
                days_until_target,
            )

        if days_until_target is not None and days_until_target < 0 and completed_tasks < total_tasks:
            return (
                ProjectTargetDateRisk.OFF_TRACK,
                "Target date has passed with incomplete tasks.",
                target_date_slip_days,
                days_until_target,
            )

        if overdue_tasks > 0:
            return (
                ProjectTargetDateRisk.OFF_TRACK,
                f"{overdue_tasks} linked task(s) exceed the target date.",
                target_date_slip_days,
                days_until_target,
            )

        if blocked_tasks > 0:
            return (
                ProjectTargetDateRisk.AT_RISK,
                f"{blocked_tasks} linked task(s) are blocked.",
                target_date_slip_days,
                days_until_target,
            )

        if (
            days_until_target is not None
            and 0 <= days_until_target <= 7
            and remaining_effort_days > 0
        ):
            return (
                ProjectTargetDateRisk.AT_RISK,
                "Target date is within 7 days with remaining effort.",
                target_date_slip_days,
                days_until_target,
            )

        schedule_progress = self._calculate_schedule_progress(project, task_start_date)
        if schedule_progress is not None:
            progress_gap = schedule_progress - completion_percent
            if progress_gap > 15:
                return (
                    ProjectTargetDateRisk.AT_RISK,
                    f"Schedule progress exceeds completion by {progress_gap:.1f} percentage points.",
                    target_date_slip_days,
                    days_until_target,
                )

        return (
            ProjectTargetDateRisk.ON_TRACK,
            "Project is tracking within current target-date thresholds.",
            target_date_slip_days,
            days_until_target,
        )

    def _calculate_update_freshness(
        self,
        project: Project,
        days_since_latest_update: Optional[int],
    ) -> ProjectUpdateFreshness:
        """Classify whether a project needs a fresher stakeholder update."""
        if project.status in {ProjectStatus.COMPLETED.value, ProjectStatus.CANCELED.value}:
            return ProjectUpdateFreshness.NOT_REQUIRED
        if days_since_latest_update is None:
            return ProjectUpdateFreshness.MISSING
        if days_since_latest_update >= STALE_PROJECT_UPDATE_DAYS:
            return ProjectUpdateFreshness.STALE
        return ProjectUpdateFreshness.FRESH

    def _empty_task_status_counts(self) -> dict[str, int]:
        """Return a fresh task status counter."""
        return {
            TaskStatus.PLANNED.value: 0,
            TaskStatus.ACTIVE.value: 0,
            TaskStatus.RESOLVED.value: 0,
            TaskStatus.CLOSED.value: 0,
        }

    def _build_milestone_task_group(
        self,
        milestone: Optional[ProjectMilestone],
        tasks: Sequence[Task],
        done_statuses: set[str],
        remaining_statuses: set[str],
    ) -> ProjectMilestoneTaskGroup:
        """Build task aggregate metrics for one milestone bucket."""
        status_counts = self._empty_task_status_counts()
        total_effort_days = 0.0
        remaining_effort_days = 0.0

        for task in tasks:
            if task.status in status_counts:
                status_counts[task.status] += 1

            task_effort = float(task.effort_days or 0)
            total_effort_days += task_effort
            if task.status in remaining_statuses:
                remaining_effort_days += task_effort

        task_count = len(tasks)
        completed_tasks = sum(status_counts[status] for status in done_statuses)
        milestone_summary = (
            ProjectMilestoneSummary(
                id=milestone.id,
                project_id=milestone.project_id,
                name=milestone.name,
                status=milestone.status,
                target_date=milestone.target_date,
                sort_order=milestone.sort_order,
            )
            if milestone is not None
            else None
        )

        return ProjectMilestoneTaskGroup(
            milestone_id=milestone.id if milestone is not None else None,
            milestone=milestone_summary,
            name=milestone.name if milestone is not None else "Unassigned",
            task_count=task_count,
            completed_tasks=completed_tasks,
            completion_percent=self._calculate_completion_percent(
                task_count,
                completed_tasks,
            ),
            status_counts=status_counts,
            total_effort_days=total_effort_days,
            remaining_effort_days=remaining_effort_days,
        )

    async def _calculate_milestone_groups(
        self,
        project_id: int,
        tasks: Sequence[Task],
        done_statuses: set[str],
        remaining_statuses: set[str],
    ) -> list[ProjectMilestoneTaskGroup]:
        """Group linked project tasks by milestone, with unassigned work last."""
        milestones = await self.list_milestones(project_id) or []
        tasks_by_milestone: dict[Optional[int], list[Task]] = {}
        for task in tasks:
            tasks_by_milestone.setdefault(task.milestone_id, []).append(task)

        groups = [
            self._build_milestone_task_group(
                milestone,
                tasks_by_milestone.get(milestone.id, []),
                done_statuses,
                remaining_statuses,
            )
            for milestone in milestones
        ]

        unassigned_tasks = tasks_by_milestone.get(None, [])
        if unassigned_tasks:
            groups.append(
                self._build_milestone_task_group(
                    None,
                    unassigned_tasks,
                    done_statuses,
                    remaining_statuses,
                )
            )

        return groups

    async def _project_task_aggregates(
        self,
        project: Project,
    ) -> dict[str, object]:
        """Compute workspace-sized project summary inputs inside the database."""

        dependency_task = aliased(Task)
        done_statuses = (TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value)
        remaining_statuses = (TaskStatus.PLANNED.value, TaskStatus.ACTIVE.value)
        blocked = exists(
            select(TaskDependency.task_id)
            .join(
                dependency_task,
                dependency_task.id == TaskDependency.depends_on_id,
            )
            .where(
                TaskDependency.task_id == Task.id,
                dependency_task.status.not_in(done_statuses),
            )
        )
        overdue_expression = (
            case(
                (
                    Task.end_date.is_not(None)
                    & (Task.end_date > project.target_date),
                    1,
                ),
                else_=0,
            )
            if project.target_date is not None
            else 0
        )
        row = (
            await self.db.execute(
                select(
                    func.count(Task.id).label("total_tasks"),
                    *(
                        func.coalesce(
                            func.sum(case((Task.status == status, 1), else_=0)),
                            0,
                        ).label(f"status_{status}")
                        for status in self._empty_task_status_counts()
                    ),
                    func.coalesce(func.sum(Task.effort_days), 0.0).label(
                        "total_effort_days"
                    ),
                    func.coalesce(
                        func.sum(
                            case(
                                (Task.status.in_(remaining_statuses), Task.effort_days),
                                else_=0.0,
                            )
                        ),
                        0.0,
                    ).label("remaining_effort_days"),
                    func.coalesce(
                        func.sum(case((blocked, 1), else_=0)),
                        0,
                    ).label("blocked_tasks"),
                    func.coalesce(func.sum(overdue_expression), 0).label(
                        "overdue_tasks"
                    ),
                    func.min(Task.start_date).label("task_start_date"),
                    func.max(Task.end_date).label("task_end_date"),
                ).where(Task.project_id == project.id)
            )
        ).one()
        status_counts = {
            status: int(getattr(row, f"status_{status}"))
            for status in self._empty_task_status_counts()
        }
        return {
            "total_tasks": int(row.total_tasks),
            "status_counts": status_counts,
            "total_effort_days": float(row.total_effort_days),
            "remaining_effort_days": float(row.remaining_effort_days),
            "blocked_tasks": int(row.blocked_tasks),
            "overdue_tasks": int(row.overdue_tasks),
            "task_start_date": row.task_start_date,
            "task_end_date": row.task_end_date,
        }

    async def _aggregated_milestone_groups(
        self,
        project_id: int,
    ) -> list[ProjectMilestoneTaskGroup]:
        """Build milestone summaries from grouped rows rather than task objects."""

        milestones = list(await self.list_milestones(project_id) or [])
        rows = (
            await self.db.execute(
                select(
                    Task.milestone_id,
                    Task.status,
                    func.count(Task.id),
                    func.coalesce(func.sum(Task.effort_days), 0.0),
                )
                .where(Task.project_id == project_id)
                .group_by(Task.milestone_id, Task.status)
                .order_by(Task.milestone_id.asc().nulls_last(), Task.status.asc())
            )
        ).all()
        buckets: dict[int | None, dict[str, object]] = {}
        for milestone_id, task_status, task_count, effort in rows:
            bucket = buckets.setdefault(
                milestone_id,
                {
                    "status_counts": self._empty_task_status_counts(),
                    "total_effort_days": 0.0,
                    "effort_by_status": {},
                },
            )
            status_counts = bucket["status_counts"]
            assert isinstance(status_counts, dict)
            if task_status in status_counts:
                status_counts[task_status] = int(task_count)
            bucket["total_effort_days"] = float(bucket["total_effort_days"]) + float(
                effort
            )
            effort_by_status = bucket["effort_by_status"]
            assert isinstance(effort_by_status, dict)
            effort_by_status[task_status] = float(effort)

        groups: list[ProjectMilestoneTaskGroup] = []
        done_statuses = {TaskStatus.RESOLVED.value, TaskStatus.CLOSED.value}
        remaining_statuses = {TaskStatus.PLANNED.value, TaskStatus.ACTIVE.value}
        for milestone in [*milestones, None]:
            milestone_id = milestone.id if milestone is not None else None
            bucket = buckets.get(milestone_id)
            if milestone is None and bucket is None:
                continue
            status_counts = (
                dict(bucket["status_counts"])
                if bucket is not None
                else self._empty_task_status_counts()
            )
            task_count = sum(status_counts.values())
            completed_tasks = sum(status_counts[status] for status in done_statuses)
            total_effort = (
                float(bucket["total_effort_days"])
                if bucket is not None
                else 0.0
            )
            effort_by_status = (
                bucket["effort_by_status"] if bucket is not None else {}
            )
            assert isinstance(effort_by_status, dict)
            remaining_effort = sum(
                float(effort_by_status.get(status, 0.0))
                for status in remaining_statuses
            )
            milestone_summary = (
                ProjectMilestoneSummary(
                    id=milestone.id,
                    project_id=milestone.project_id,
                    name=milestone.name,
                    status=milestone.status,
                    target_date=milestone.target_date,
                    sort_order=milestone.sort_order,
                )
                if milestone is not None
                else None
            )
            groups.append(
                ProjectMilestoneTaskGroup(
                    milestone_id=milestone_id,
                    milestone=milestone_summary,
                    name=milestone.name if milestone is not None else "Unassigned",
                    task_count=task_count,
                    completed_tasks=completed_tasks,
                    completion_percent=self._calculate_completion_percent(
                        task_count,
                        completed_tasks,
                    ),
                    status_counts=status_counts,
                    total_effort_days=total_effort,
                    remaining_effort_days=remaining_effort,
                )
            )
        return groups

    async def get_summary(self, project_id: int) -> Optional[ProjectSummary]:
        """Calculate project task summary metrics."""
        project = await self.get_by_id(project_id)
        if not project:
            return None

        aggregates = await self._project_task_aggregates(project)
        latest_update = await self.get_latest_project_update(project_id)
        days_since_latest_update = (
            (date.today() - latest_update.created_at.date()).days
            if latest_update is not None
            else None
        )
        update_freshness = self._calculate_update_freshness(
            project,
            days_since_latest_update,
        )
        status_counts = aggregates["status_counts"]
        assert isinstance(status_counts, dict)
        blocked_tasks = int(aggregates["blocked_tasks"])
        overdue_tasks = int(aggregates["overdue_tasks"])
        total_effort_days = float(aggregates["total_effort_days"])
        remaining_effort_days = float(aggregates["remaining_effort_days"])
        task_start_date = aggregates["task_start_date"]
        task_end_date = aggregates["task_end_date"]
        milestone_groups = await self._aggregated_milestone_groups(project_id)
        request_count = await RequestSourceService(self.db).count_for_project(project_id)

        total_tasks = int(aggregates["total_tasks"])
        completed_tasks = (
            status_counts[TaskStatus.RESOLVED.value]
            + status_counts[TaskStatus.CLOSED.value]
        )
        completion_percent = self._calculate_completion_percent(
            total_tasks, completed_tasks
        )
        (
            target_date_risk,
            target_date_risk_reason,
            target_date_slip_days,
            days_until_target,
        ) = self._calculate_target_date_risk(
            project=project,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            completion_percent=completion_percent,
            blocked_tasks=blocked_tasks,
            overdue_tasks=overdue_tasks,
            remaining_effort_days=remaining_effort_days,
            task_start_date=task_start_date,
            task_end_date=task_end_date,
        )

        return ProjectSummary(
            id=project.id,
            name=project.name,
            status=project.status,
            health=project.health,
            owner_id=project.owner_id,
            owner=(
                TeamMemberOptionResponse.model_validate(project.owner)
                if project.owner
                else None
            ),
            owner_profile_id=project.owner_profile_id,
            owner_profile=(
                TeamMemberProfileCompact.model_validate(project.owner_profile)
                if project.owner_profile
                else None
            ),
            initiative_id=project.initiative_id,
            start_date=project.start_date,
            target_date=project.target_date,
            completed_at=project.completed_at,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            completion_percent=completion_percent,
            active_tasks=status_counts[TaskStatus.ACTIVE.value],
            blocked_tasks=blocked_tasks,
            overdue_tasks=overdue_tasks,
            target_date_risk=target_date_risk,
            target_date_risk_reason=target_date_risk_reason,
            target_date_slip_days=target_date_slip_days,
            days_until_target=days_until_target,
            status_counts=status_counts,
            total_effort_days=total_effort_days,
            remaining_effort_days=remaining_effort_days,
            milestone_groups=milestone_groups,
            request_count=request_count,
            task_start_date=task_start_date,
            task_end_date=task_end_date,
            latest_update=(
                ProjectUpdateEntryResponse.model_validate(latest_update)
                if latest_update
                else None
            ),
            latest_update_at=latest_update.created_at if latest_update else None,
            days_since_latest_update=days_since_latest_update,
            update_freshness=update_freshness,
            is_update_stale=update_freshness
            in {ProjectUpdateFreshness.STALE, ProjectUpdateFreshness.MISSING},
            stale_update_threshold_days=STALE_PROJECT_UPDATE_DAYS,
        )
