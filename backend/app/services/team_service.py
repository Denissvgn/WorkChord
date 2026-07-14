"""Team member service with business logic."""
import csv
from datetime import date
from io import StringIO
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.team_member import TeamMember, TeamMemberProfile, TeamMemberProfileSkill, Vacation
from app.models.task import Task
from app.models.iteration import Iteration
from app.schemas.team import (
    TeamMemberCreate,
    TeamMemberProfileCreate,
    TeamMemberProfileSkillCreate,
    TeamMemberProfileSkillUpdate,
    TeamMemberProfileUpdate,
    TeamMemberOptionResponse,
    TeamMemberUpdate,
    VacationCreate,
    VacationUpdate,
    VacationImportError,
    VacationImportResponse,
    MemberCapacity,
    MemberWorkload,
)
from app.services.calendar_service import CalendarService


class TeamService:
    """Service for team member operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _profile_options(self):
        """Return eager loading options for reusable profile responses."""
        return selectinload(TeamMemberProfile.skills)

    def _member_options(self):
        """Return eager loading options for team member responses."""
        return (
            selectinload(TeamMember.vacations),
            selectinload(TeamMember.profile).selectinload(TeamMemberProfile.skills),
        )

    def _normalize_text_key(self, value: str | None) -> str:
        """Return a lowercase matching key for display names and emails."""
        return " ".join((value or "").strip().lower().split())

    async def _get_profile_by_id(self, profile_id: int) -> TeamMemberProfile | None:
        """Load a reusable profile by id."""
        result = await self.db.execute(
            select(TeamMemberProfile)
            .options(self._profile_options())
            .where(TeamMemberProfile.id == profile_id)
        )
        return result.scalar_one_or_none()

    async def _require_profile_not_assigned_to_iteration(
        self,
        profile_id: int,
        iteration_id: int | None,
        *,
        exclude_member_id: int | None = None,
    ) -> None:
        """Ensure a profile has at most one capacity row in an iteration."""
        if iteration_id is None:
            return

        query = select(TeamMember.id).where(
            TeamMember.profile_id == profile_id,
            TeamMember.iteration_id == iteration_id,
        )
        if exclude_member_id is not None:
            query = query.where(TeamMember.id != exclude_member_id)

        result = await self.db.execute(query)
        if result.scalar_one_or_none() is not None:
            raise ValueError(
                f"Team member profile with id {profile_id} is already assigned to iteration {iteration_id}"
            )

    async def _resolve_profile_for_member(
        self,
        *,
        name: str,
        email: str | None,
        profile_id: int | None,
        create_if_missing: bool = True,
    ) -> TeamMemberProfile | None:
        """Resolve explicit or inferred reusable profile for a team member."""
        if profile_id is not None:
            profile = await self._get_profile_by_id(profile_id)
            if not profile:
                raise ValueError(f"Team member profile with id {profile_id} not found")
            return profile

        normalized_email = self._normalize_text_key(email)
        if normalized_email:
            result = await self.db.execute(
                select(TeamMemberProfile)
                .options(self._profile_options())
                .where(TeamMemberProfile.email.ilike(normalized_email))
                .order_by(TeamMemberProfile.id)
            )
            profile = result.scalars().first()
            if profile:
                return profile

        normalized_name = self._normalize_text_key(name)
        if normalized_name:
            result = await self.db.execute(
                select(TeamMemberProfile)
                .options(self._profile_options())
                .order_by(TeamMemberProfile.id)
            )
            for profile in result.scalars().all():
                if self._normalize_text_key(profile.display_name) == normalized_name:
                    return profile

        if not create_if_missing:
            return None

        profile = TeamMemberProfile(
            display_name=name.strip(),
            email=email.strip() if email else None,
            headline=None,
            summary=None,
            notes=None,
            automation_enabled=True,
        )
        self.db.add(profile)
        await self.db.flush()
        return profile

    async def list_profiles(self) -> Sequence[TeamMemberProfile]:
        """List reusable capability profiles."""
        result = await self.db.execute(
            select(TeamMemberProfile)
            .options(self._profile_options())
            .order_by(TeamMemberProfile.display_name, TeamMemberProfile.id)
        )
        return result.scalars().unique().all()

    async def get_profile(self, profile_id: int) -> TeamMemberProfile | None:
        """Get a reusable capability profile by id."""
        return await self._get_profile_by_id(profile_id)

    async def create_profile(
        self,
        data: TeamMemberProfileCreate,
        *,
        commit: bool = True,
    ) -> TeamMemberProfile:
        """Create a profile, optionally leaving commit ownership to the caller."""
        profile = TeamMemberProfile(**data.model_dump())
        self.db.add(profile)
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(profile)
        return await self._get_profile_by_id(profile.id) or profile

    async def update_profile(
        self,
        profile_id: int,
        data: TeamMemberProfileUpdate,
        *,
        commit: bool = True,
    ) -> TeamMemberProfile | None:
        """Update profile metadata, optionally deferring the commit."""
        profile = await self._get_profile_by_id(profile_id)
        if not profile:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(profile)
        return await self._get_profile_by_id(profile.id)

    async def delete_profile(self, profile_id: int) -> bool:
        """Delete a reusable profile and detach linked team members."""
        profile = await self._get_profile_by_id(profile_id)
        if not profile:
            return False

        await self.db.delete(profile)
        await self.db.commit()
        return True

    async def add_profile_skill(
        self,
        profile_id: int,
        data: TeamMemberProfileSkillCreate,
    ) -> TeamMemberProfileSkill | None:
        """Add a skill or weakness to a profile."""
        profile = await self._get_profile_by_id(profile_id)
        if not profile:
            return None

        skill = TeamMemberProfileSkill(profile_id=profile_id, **data.model_dump())
        self.db.add(skill)
        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def update_profile_skill(
        self,
        profile_id: int,
        skill_id: int,
        data: TeamMemberProfileSkillUpdate,
    ) -> TeamMemberProfileSkill | None:
        """Update a profile skill or weakness."""
        result = await self.db.execute(
            select(TeamMemberProfileSkill).where(
                TeamMemberProfileSkill.id == skill_id,
                TeamMemberProfileSkill.profile_id == profile_id,
            )
        )
        skill = result.scalar_one_or_none()
        if not skill:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(skill, field, value)

        await self.db.commit()
        await self.db.refresh(skill)
        return skill

    async def delete_profile_skill(self, profile_id: int, skill_id: int) -> bool:
        """Delete one profile skill or weakness."""
        result = await self.db.execute(
            select(TeamMemberProfileSkill).where(
                TeamMemberProfileSkill.id == skill_id,
                TeamMemberProfileSkill.profile_id == profile_id,
            )
        )
        skill = result.scalar_one_or_none()
        if not skill:
            return False

        await self.db.delete(skill)
        await self.db.commit()
        return True

    async def get_by_iteration(self, iteration_id: int) -> Sequence[TeamMember]:
        """Get all team members for an iteration."""
        result = await self.db.execute(
            select(TeamMember)
            .options(*self._member_options())
            .where(TeamMember.iteration_id == iteration_id)
            .order_by(TeamMember.name)
        )
        return result.scalars().all()

    async def get_all_unique_members(self) -> list[dict]:
        """Get unique members by name across all iterations (for reuse)."""
        result = await self.db.execute(
            select(TeamMember.name, TeamMember.position)
            .distinct(TeamMember.name)
            .order_by(TeamMember.name)
        )
        rows = result.all()
        return [{"name": row[0], "position": row[1]} for row in rows]

    async def list_member_options(self) -> list[TeamMemberOptionResponse]:
        """List all team members with enough context for owner selectors."""
        result = await self.db.execute(
            select(TeamMember)
            .options(selectinload(TeamMember.iteration))
            .order_by(
                TeamMember.name,
                TeamMember.position,
                TeamMember.iteration_id,
                TeamMember.id,
            )
        )
        return [
            TeamMemberOptionResponse.model_validate(member)
            for member in result.scalars().unique().all()
        ]

    async def get_by_id(self, member_id: int) -> TeamMember | None:
        """Get team member by ID."""
        result = await self.db.execute(
            select(TeamMember)
            .options(
                *self._member_options(),
                selectinload(TeamMember.tasks),
                selectinload(TeamMember.iteration).selectinload(Iteration.calendar)
            )
            .where(TeamMember.id == member_id)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        iteration_id: int,
        data: TeamMemberCreate,
        *,
        commit: bool = True,
    ) -> TeamMember:
        """Create a team member, optionally leaving commit ownership to the caller."""
        profile = await self._resolve_profile_for_member(
            name=data.name,
            email=data.email,
            profile_id=data.profile_id,
            create_if_missing=True,
        )
        if profile is not None:
            await self._require_profile_not_assigned_to_iteration(profile.id, iteration_id)

        member = TeamMember(
            iteration_id=iteration_id,
            name=profile.display_name if profile and data.profile_id is not None else data.name,
            position=data.position,
            email=profile.email if profile and data.profile_id is not None else data.email,
            profile_id=profile.id if profile else None,
            availability_percent=data.availability_percent,
            professionalism_coefficient=data.professionalism_coefficient,
            operational_utilization=data.operational_utilization,
        )
        self.db.add(member)
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(member)
        return member

    async def update(
        self,
        member_id: int,
        data: TeamMemberUpdate,
        *,
        commit: bool = True,
    ) -> TeamMember | None:
        """Update a team member, optionally leaving commit ownership to the caller."""
        member = await self.get_by_id(member_id)
        if not member:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "profile_id" in update_data and update_data["profile_id"] is not None:
            profile = await self._get_profile_by_id(update_data["profile_id"])
            if not profile:
                raise ValueError(f"Team member profile with id {update_data['profile_id']} not found")
            await self._require_profile_not_assigned_to_iteration(
                profile.id,
                member.iteration_id,
                exclude_member_id=member.id,
            )
            update_data["name"] = profile.display_name
            update_data["email"] = profile.email

        for field, value in update_data.items():
            setattr(member, field, value)

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(member)
        return member

    async def delete(self, member_id: int) -> bool:
        """Delete a team member."""
        member = await self.get_by_id(member_id)
        if not member:
            return False

        await self.db.delete(member)
        await self.db.commit()
        return True

    async def add_vacation(
        self,
        member_id: int,
        data: VacationCreate,
        *,
        commit: bool = True,
    ) -> Vacation | None:
        """Add a vacation, optionally leaving commit ownership to the caller."""
        member = await self.get_by_id(member_id)
        if not member:
            return None

        vacation = Vacation(
            team_member_id=member_id,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        self.db.add(vacation)
        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(vacation)
        return vacation

    async def update_vacation(
        self,
        vacation_id: int,
        data: VacationUpdate,
        *,
        commit: bool = True,
    ) -> Vacation | None:
        """Update a vacation period, optionally leaving commit ownership to the caller."""
        result = await self.db.execute(
            select(Vacation).where(Vacation.id == vacation_id)
        )
        vacation = result.scalar_one_or_none()
        if vacation is None:
            return None

        updates = data.model_dump(exclude_unset=True)
        next_start = updates.get("start_date", vacation.start_date)
        next_end = updates.get("end_date", vacation.end_date)
        if next_start > next_end:
            raise ValueError("start_date must be before or equal to end_date")
        for field, value in updates.items():
            setattr(vacation, field, value)

        if commit:
            await self.db.commit()
        else:
            await self.db.flush()
        await self.db.refresh(vacation)
        return vacation

    async def delete_vacation(self, vacation_id: int) -> bool:
        """Delete a vacation."""
        result = await self.db.execute(
            select(Vacation).where(Vacation.id == vacation_id)
        )
        vacation = result.scalar_one_or_none()
        if not vacation:
            return False

        await self.db.delete(vacation)
        await self.db.commit()
        return True

    async def import_vacations(self, iteration_id: int, csv_text: str) -> VacationImportResponse:
        """Import vacation ranges for iteration team members from CSV text."""
        if not csv_text.strip():
            raise ValueError("csv_text is required")

        reader = csv.DictReader(StringIO(csv_text))
        required_fields = {"start_date", "end_date"}
        fieldnames = {field.strip() for field in (reader.fieldnames or [])}
        if not required_fields.issubset(fieldnames) or not ({"member_id", "email"} & fieldnames):
            raise ValueError("CSV must include member_id or email plus start_date and end_date columns")

        result = await self.db.execute(
            select(TeamMember)
            .options(selectinload(TeamMember.vacations))
            .where(TeamMember.iteration_id == iteration_id)
            .order_by(TeamMember.id)
        )
        members = result.scalars().unique().all()
        members_by_id = {member.id: member for member in members}
        members_by_email: dict[str, list[TeamMember]] = {}
        for member in members:
            key = self._normalize_text_key(member.email)
            if key:
                members_by_email.setdefault(key, []).append(member)

        imported: list[Vacation] = []
        errors: list[VacationImportError] = []
        skipped_count = 0

        for row_number, row in enumerate(reader, start=2):
            member: TeamMember | None = None
            raw_member_id = (row.get("member_id") or "").strip()
            raw_email = (row.get("email") or "").strip()

            if raw_member_id:
                try:
                    member = members_by_id.get(int(raw_member_id))
                except ValueError:
                    errors.append(VacationImportError(row=row_number, message=f"Invalid member_id '{raw_member_id}'"))
                    continue
                if not member:
                    errors.append(VacationImportError(row=row_number, message=f"Unknown member_id '{raw_member_id}'"))
                    continue
            elif raw_email:
                matches = members_by_email.get(self._normalize_text_key(raw_email), [])
                if len(matches) == 1:
                    member = matches[0]
                elif len(matches) > 1:
                    errors.append(VacationImportError(row=row_number, message=f"Email '{raw_email}' matches multiple members"))
                    continue
                else:
                    errors.append(VacationImportError(row=row_number, message=f"Unknown email '{raw_email}'"))
                    continue
            else:
                errors.append(VacationImportError(row=row_number, message="Missing member_id or email"))
                continue

            raw_start = (row.get("start_date") or "").strip()
            raw_end = (row.get("end_date") or "").strip()
            try:
                start_date = date.fromisoformat(raw_start)
                end_date = date.fromisoformat(raw_end)
            except ValueError:
                errors.append(VacationImportError(row=row_number, message="Invalid start_date or end_date"))
                continue
            if start_date > end_date:
                errors.append(VacationImportError(row=row_number, message="start_date must be before or equal to end_date"))
                continue

            exists = any(
                vacation.start_date == start_date and vacation.end_date == end_date
                for vacation in member.vacations
            )
            if exists:
                skipped_count += 1
                continue

            vacation = Vacation(
                team_member_id=member.id,
                start_date=start_date,
                end_date=end_date,
            )
            self.db.add(vacation)
            member.vacations.append(vacation)
            imported.append(vacation)

        await self.db.commit()
        for vacation in imported:
            await self.db.refresh(vacation)

        return VacationImportResponse(
            imported_count=len(imported),
            skipped_count=skipped_count + len(errors),
            errors=errors,
            vacations=imported,
        )

    async def calculate_capacity(self, member_id: int) -> MemberCapacity | None:
        """Calculate capacity for a team member."""
        member = await self.get_by_id(member_id)
        if not member or not member.iteration:
            return None

        iteration = member.iteration
        calendar_service = CalendarService(self.db)

        # Get working days info
        working_days_info = calendar_service.calculate_working_days(
            iteration.calendar, iteration.start_date, iteration.end_date
        )
        working_days = working_days_info.working_days

        # Calculate vacation days
        vacation_days = 0
        for vacation in member.vacations:
            vac_working = calendar_service.calculate_working_days(
                iteration.calendar,
                max(vacation.start_date, iteration.start_date),
                min(vacation.end_date, iteration.end_date)
            ).working_days
            vacation_days += vac_working

        # Apply factors
        available_days = (working_days - vacation_days) * (member.availability_percent / 100)
        effective_days = available_days * (1 - member.operational_utilization / 100)
        adjusted_days = effective_days * member.professionalism_coefficient

        return MemberCapacity(
            team_member_id=member_id,
            working_days=working_days,
            vacation_days=vacation_days,
            available_days=round(available_days, 2),
            effective_days=round(effective_days, 2),
            adjusted_days=round(adjusted_days, 2),
            hours=round(adjusted_days * 8, 2),
        )

    async def get_workload(self, member_id: int) -> MemberWorkload | None:
        """Get workload information for a team member."""
        member = await self.get_by_id(member_id)
        if not member:
            return None

        capacity = await self.calculate_capacity(member_id)
        if not capacity:
            return None

        # Calculate allocated days from assigned tasks (deferred tasks are excluded)
        allocated_days = sum(t.effort_days for t in member.tasks if not t.is_deferred)
        # Use effective_days for capacity display - professionalism_coefficient only affects Gantt scheduling
        free_days = capacity.effective_days - allocated_days

        # Determine workload status
        if free_days >= 0:
            status = "green"
        elif abs(free_days) / capacity.effective_days < 0.05:
            status = "yellow"
        else:
            status = "red"

        workload_percent = (allocated_days / capacity.effective_days * 100) if capacity.effective_days > 0 else 0

        return MemberWorkload(
            team_member_id=member_id,
            name=member.name,
            capacity_days=capacity.effective_days,
            allocated_days=round(allocated_days, 2),
            free_days=round(free_days, 2),
            workload_status=status,
            workload_percent=round(workload_percent, 1),
        )

    async def import_members(
        self,
        iteration_id: int,
        text: str
    ) -> list[TeamMember]:
        """
        Import multiple team members from text format.

        Format:
        -- "John Doe" Developer 100 1.0 20
        -- "Jane Smith" Designer 80 1.2 15

        Returns list of created team members.
        """
        from app.utils.import_parser import parse_team_members_text

        parsed_members = parse_team_members_text(text)
        created_members: list[TeamMember] = []

        for parsed in parsed_members:
            profile = await self._resolve_profile_for_member(
                name=parsed.name,
                email=None,
                profile_id=None,
                create_if_missing=True,
            )
            if profile is not None:
                await self._require_profile_not_assigned_to_iteration(profile.id, iteration_id)
            member = TeamMember(
                iteration_id=iteration_id,
                name=parsed.name,
                position=parsed.position,
                profile_id=profile.id if profile else None,
                availability_percent=parsed.availability_percent,
                professionalism_coefficient=parsed.professionalism_coefficient,
                operational_utilization=parsed.operational_utilization,
            )
            self.db.add(member)
            created_members.append(member)

        await self.db.commit()

        # Refresh all members to get IDs
        for member in created_members:
            await self.db.refresh(member)

        return created_members
