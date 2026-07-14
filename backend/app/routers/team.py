"""Team API router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.team import (
    TeamMemberCreate, TeamMemberUpdate, TeamMemberResponse,
    TeamMemberOptionResponse,
    VacationCreate, VacationResponse, MemberCapacity, MemberWorkload,
    VacationImportRequest, VacationImportResponse,
    TeamImportRequest, TeamImportResponse,
    TeamMemberProfileCreate, TeamMemberProfileResponse,
    TeamMemberProfileSkillCreate, TeamMemberProfileSkillResponse,
    TeamMemberProfileSkillUpdate, TeamMemberProfileUpdate,
)
from app.schemas.common import MessageResponse
from app.services.team_service import TeamService

router = APIRouter()


async def get_team_service(db: Annotated[AsyncSession, Depends(get_db)]) -> TeamService:
    """Dependency for team service."""
    return TeamService(db)


@router.get(
    "/iterations/{iteration_id}/team",
    response_model=list[TeamMemberResponse]
)
async def get_team_members(
    iteration_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Get all team members for an iteration."""
    return await service.get_by_iteration(iteration_id)


@router.get("/employees/unique", response_model=list[dict])
async def get_unique_employees(
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Get unique employees from all iterations for reuse."""
    return await service.get_all_unique_members()


@router.get("/team-members", response_model=list[TeamMemberOptionResponse])
async def list_team_member_options(
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """List all team members for owner and assignee selectors."""
    return await service.list_member_options()


@router.get("/team-member-profiles", response_model=list[TeamMemberProfileResponse])
async def list_team_member_profiles(
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """List reusable capability profiles."""
    return await service.list_profiles()


@router.post(
    "/team-member-profiles",
    response_model=TeamMemberProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_team_member_profile(
    data: TeamMemberProfileCreate,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Create a reusable capability profile."""
    return await service.create_profile(data)


@router.get("/team-member-profiles/{profile_id}", response_model=TeamMemberProfileResponse)
async def get_team_member_profile(
    profile_id: int,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Get a reusable capability profile."""
    profile = await service.get_profile(profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member profile with id {profile_id} not found",
        )
    return profile


@router.put("/team-member-profiles/{profile_id}", response_model=TeamMemberProfileResponse)
async def update_team_member_profile(
    profile_id: int,
    data: TeamMemberProfileUpdate,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Update a reusable capability profile."""
    profile = await service.update_profile(profile_id, data)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member profile with id {profile_id} not found",
        )
    return profile


@router.delete("/team-member-profiles/{profile_id}", response_model=MessageResponse)
async def delete_team_member_profile(
    profile_id: int,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Delete a reusable capability profile and detach linked team members."""
    deleted = await service.delete_profile(profile_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member profile with id {profile_id} not found",
        )
    return MessageResponse(message=f"Team member profile {profile_id} deleted", success=True)


@router.post(
    "/team-member-profiles/{profile_id}/skills",
    response_model=TeamMemberProfileSkillResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_team_member_profile_skill(
    profile_id: int,
    data: TeamMemberProfileSkillCreate,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Add a skill or weakness to a reusable capability profile."""
    skill = await service.add_profile_skill(profile_id, data)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member profile with id {profile_id} not found",
        )
    return skill


@router.put(
    "/team-member-profiles/{profile_id}/skills/{skill_id}",
    response_model=TeamMemberProfileSkillResponse,
)
async def update_team_member_profile_skill(
    profile_id: int,
    skill_id: int,
    data: TeamMemberProfileSkillUpdate,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Update a skill or weakness on a reusable capability profile."""
    skill = await service.update_profile_skill(profile_id, skill_id, data)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member profile skill with id {skill_id} not found",
        )
    return skill


@router.delete(
    "/team-member-profiles/{profile_id}/skills/{skill_id}",
    response_model=MessageResponse,
)
async def delete_team_member_profile_skill(
    profile_id: int,
    skill_id: int,
    service: Annotated[TeamService, Depends(get_team_service)],
):
    """Delete a skill or weakness from a reusable capability profile."""
    deleted = await service.delete_profile_skill(profile_id, skill_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member profile skill with id {skill_id} not found",
        )
    return MessageResponse(message=f"Team member profile skill {skill_id} deleted", success=True)


@router.post(
    "/iterations/{iteration_id}/team",
    response_model=TeamMemberResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_team_member(
    iteration_id: int,
    data: TeamMemberCreate,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Add a team member to an iteration."""
    try:
        member = await service.create(iteration_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    return await service.get_by_id(member.id)


@router.get("/team-members/{member_id}", response_model=TeamMemberResponse)
async def get_team_member(
    member_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Get team member by ID."""
    member = await service.get_by_id(member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return member


@router.put("/team-members/{member_id}", response_model=TeamMemberResponse)
async def update_team_member(
    member_id: int,
    data: TeamMemberUpdate,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Update a team member."""
    try:
        member = await service.update(member_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return member


@router.delete("/team-members/{member_id}", response_model=MessageResponse)
async def delete_team_member(
    member_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Delete a team member."""
    deleted = await service.delete(member_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return MessageResponse(message=f"Team member {member_id} deleted", success=True)


@router.get("/team-members/{member_id}/capacity", response_model=MemberCapacity)
async def get_member_capacity(
    member_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Calculate capacity for a team member."""
    capacity = await service.calculate_capacity(member_id)
    if not capacity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return capacity


@router.get("/team-members/{member_id}/workload", response_model=MemberWorkload)
async def get_member_workload(
    member_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Get workload information for a team member."""
    workload = await service.get_workload(member_id)
    if not workload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return workload


@router.get(
    "/team-members/{member_id}/vacations",
    response_model=list[VacationResponse]
)
async def get_vacations(
    member_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Get vacations for a team member."""
    member = await service.get_by_id(member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return member.vacations


@router.post(
    "/team-members/{member_id}/vacations",
    response_model=VacationResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_vacation(
    member_id: int,
    data: VacationCreate,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Add vacation for a team member."""
    vacation = await service.add_vacation(member_id, data)
    if not vacation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team member with id {member_id} not found"
        )
    return vacation


@router.delete("/vacations/{vacation_id}", response_model=MessageResponse)
async def delete_vacation(
    vacation_id: int,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Delete a vacation."""
    deleted = await service.delete_vacation(vacation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vacation with id {vacation_id} not found"
        )
    return MessageResponse(message=f"Vacation {vacation_id} deleted", success=True)


@router.post(
    "/iterations/{iteration_id}/team/vacations/import",
    response_model=VacationImportResponse,
)
async def import_team_vacations(
    iteration_id: int,
    data: VacationImportRequest,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Import vacation periods for iteration team members from CSV text."""
    try:
        return await service.import_vacations(iteration_id, data.csv_text)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/iterations/{iteration_id}/team/import",
    response_model=TeamImportResponse,
    status_code=status.HTTP_201_CREATED
)
async def import_team_members(
    iteration_id: int,
    data: TeamImportRequest,
    service: Annotated[TeamService, Depends(get_team_service)]
):
    """Import team members from text format."""
    try:
        members = await service.import_members(iteration_id, data.text)
        # Re-fetch members with vacations loaded
        full_members = []
        for member in members:
            full_member = await service.get_by_id(member.id)
            full_members.append(full_member)

        return TeamImportResponse(
            imported_count=len(full_members),
            members=full_members
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
