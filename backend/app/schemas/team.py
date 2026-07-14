"""Team member schemas."""
from datetime import date, datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


def _clean_optional_text(value: Optional[str]) -> Optional[str]:
    """Trim optional text values and normalize blanks to null."""
    if value is None:
        return None
    text = value.strip()
    return text or None


def _dedupe_keywords(values: list[Any]) -> list[str]:
    """Trim keyword strings and preserve first occurrence order."""
    result: list[str] = []
    for value in values or []:
        text = str(value).strip()
        if text and text not in result:
            result.append(text)
    return result


class VacationCreate(BaseModel):
    """Schema for creating a vacation."""
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_date_range(self) -> "VacationCreate":
        """Reject an inverted vacation period."""
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before or equal to end_date")
        return self


class VacationUpdate(BaseModel):
    """Schema for partially updating a vacation period."""

    start_date: Optional[date] = None
    end_date: Optional[date] = None


class VacationResponse(BaseModel):
    """Schema for vacation response."""
    id: int
    team_member_id: int
    start_date: date
    end_date: date

    class Config:
        from_attributes = True


class VacationImportError(BaseModel):
    """One vacation import row that could not be applied."""
    row: int
    message: str


class VacationImportRequest(BaseModel):
    """CSV text for bulk importing team vacations."""
    csv_text: str = Field(..., min_length=1)


class VacationImportResponse(BaseModel):
    """Summary of bulk vacation import results."""
    imported_count: int
    skipped_count: int
    errors: list[VacationImportError] = Field(default_factory=list)
    vacations: list[VacationResponse] = Field(default_factory=list)


class TeamMemberCreate(BaseModel):
    """Schema for creating a team member."""
    name: str = Field(..., min_length=1, max_length=255)
    position: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    profile_id: Optional[int] = None
    availability_percent: float = Field(default=100.0, ge=0, le=100)
    professionalism_coefficient: float = Field(default=1.0, ge=0.5, le=5.0)
    operational_utilization: float = Field(default=20.0, ge=0, le=100)


class TeamMemberUpdate(BaseModel):
    """Schema for updating a team member."""
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    position: Optional[str] = Field(default=None, min_length=1, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    profile_id: Optional[int] = None
    availability_percent: Optional[float] = Field(default=None, ge=0, le=100)
    professionalism_coefficient: Optional[float] = Field(default=None, ge=0.5, le=5.0)
    operational_utilization: Optional[float] = Field(default=None, ge=0, le=100)


class TeamMemberProfileSkillCreate(BaseModel):
    """Schema for creating a profile skill or weakness."""
    skill_key: str = Field(..., min_length=1, max_length=120)
    skill_name: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(default=None, max_length=120)
    level: int = Field(default=3, ge=1, le=5)
    interest: int = Field(default=3, ge=1, le=5)
    is_weakness: bool = False
    keywords_json: list[str] = Field(default_factory=list)
    notes: Optional[str] = None

    @field_validator("skill_key", "skill_name", mode="after")
    @classmethod
    def trim_required_text(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("Text fields cannot be blank")
        return text

    @field_validator("category", "notes", mode="after")
    @classmethod
    def trim_optional_text(cls, value: Optional[str]) -> Optional[str]:
        return _clean_optional_text(value)

    @field_validator("keywords_json", mode="before")
    @classmethod
    def validate_keywords(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise ValueError("keywords_json must be a list")
        return _dedupe_keywords(value)


class TeamMemberProfileSkillUpdate(BaseModel):
    """Schema for updating a profile skill or weakness."""
    skill_key: Optional[str] = Field(default=None, min_length=1, max_length=120)
    skill_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    category: Optional[str] = Field(default=None, max_length=120)
    level: Optional[int] = Field(default=None, ge=1, le=5)
    interest: Optional[int] = Field(default=None, ge=1, le=5)
    is_weakness: Optional[bool] = None
    keywords_json: Optional[list[str]] = None
    notes: Optional[str] = None

    @field_validator("skill_key", "skill_name", mode="after")
    @classmethod
    def trim_required_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        text = value.strip()
        if not text:
            raise ValueError("Text fields cannot be blank")
        return text

    @field_validator("category", "notes", mode="after")
    @classmethod
    def trim_optional_text(cls, value: Optional[str]) -> Optional[str]:
        return _clean_optional_text(value)

    @field_validator("keywords_json", mode="before")
    @classmethod
    def validate_keywords(cls, value: Any) -> Optional[list[str]]:
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError("keywords_json must be a list")
        return _dedupe_keywords(value)


class TeamMemberProfileSkillResponse(BaseModel):
    """Schema for profile skill responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile_id: int
    skill_key: str
    skill_name: str
    category: Optional[str] = None
    level: int
    interest: int
    is_weakness: bool
    keywords_json: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TeamMemberProfileCreate(BaseModel):
    """Schema for creating a reusable team-member profile."""
    seed_key: Optional[str] = Field(default=None, max_length=120)
    display_name: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    headline: Optional[str] = Field(default=None, max_length=255)
    summary: Optional[str] = None
    notes: Optional[str] = None
    automation_enabled: bool = True
    profile_kind: Literal["human", "agent", "hybrid"] = "human"
    assignment_modes: list[Literal["ownership", "execution", "verification", "design_handoff"]] = Field(
        default_factory=list
    )

    @field_validator("display_name", mode="after")
    @classmethod
    def trim_display_name(cls, value: str) -> str:
        text = value.strip()
        if not text:
            raise ValueError("display_name cannot be blank")
        return text

    @field_validator("seed_key", "email", "headline", "summary", "notes", mode="after")
    @classmethod
    def trim_optional_text(cls, value: Optional[str]) -> Optional[str]:
        return _clean_optional_text(value)


class TeamMemberProfileUpdate(BaseModel):
    """Schema for updating a reusable team-member profile."""
    display_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    email: Optional[str] = Field(default=None, max_length=255)
    headline: Optional[str] = Field(default=None, max_length=255)
    summary: Optional[str] = None
    notes: Optional[str] = None
    automation_enabled: Optional[bool] = None
    profile_kind: Optional[Literal["human", "agent", "hybrid"]] = None
    assignment_modes: Optional[
        list[Literal["ownership", "execution", "verification", "design_handoff"]]
    ] = None

    @field_validator("display_name", mode="after")
    @classmethod
    def trim_display_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        text = value.strip()
        if not text:
            raise ValueError("display_name cannot be blank")
        return text

    @field_validator("email", "headline", "summary", "notes", mode="after")
    @classmethod
    def trim_optional_text(cls, value: Optional[str]) -> Optional[str]:
        return _clean_optional_text(value)


class TeamMemberProfileResponse(BaseModel):
    """Schema for reusable team-member profile responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    seed_key: Optional[str] = None
    display_name: str
    email: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    notes: Optional[str] = None
    automation_enabled: bool
    profile_kind: str = "human"
    assignment_modes: list[str] = Field(default_factory=list)
    skills: list[TeamMemberProfileSkillResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class TeamMemberProfileCompact(BaseModel):
    """Compact profile data embedded in team-member responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    email: Optional[str] = None
    headline: Optional[str] = None
    automation_enabled: bool
    profile_kind: str = "human"
    assignment_modes: list[str] = Field(default_factory=list)
    skills: list[TeamMemberProfileSkillResponse] = Field(default_factory=list)


class TeamMemberResponse(BaseModel):
    """Schema for team member response."""
    id: int
    iteration_id: Optional[int] = None
    profile_id: Optional[int] = None
    name: str
    position: str
    email: Optional[str] = None
    availability_percent: float
    professionalism_coefficient: float
    operational_utilization: float
    profile: Optional[TeamMemberProfileCompact] = None
    vacations: list[VacationResponse] = []

    class Config:
        from_attributes = True


class TeamMemberOptionResponse(BaseModel):
    """Compact team-member identity for owner and assignee selectors."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    iteration_id: Optional[int] = None
    iteration_name: Optional[str] = None
    name: str
    position: str
    email: Optional[str] = None


class MemberCapacity(BaseModel):
    """Capacity calculation for a team member."""
    team_member_id: int
    working_days: int
    vacation_days: int
    available_days: float
    effective_days: float
    adjusted_days: float
    hours: float


class MemberWorkload(BaseModel):
    """Workload information for a team member."""
    team_member_id: int
    name: str
    capacity_days: float
    allocated_days: float
    free_days: float  # Can be negative
    workload_status: Literal["green", "yellow", "red"]
    workload_percent: float


class TeamImportRequest(BaseModel):
    """Request for importing team members from text."""
    text: str


class TeamImportResponse(BaseModel):
    """Response for team import."""
    imported_count: int
    members: list[TeamMemberResponse]


class AssigneeRecommendationResponse(BaseModel):
    """Explainable candidate score for assigning a task or triage item."""
    team_member_id: int
    name: str
    position: str
    profile_id: Optional[int] = None
    score: float
    confidence: float
    matched_skills: list[str] = Field(default_factory=list)
    weakness_matches: list[str] = Field(default_factory=list)
    workload_warnings: list[str] = Field(default_factory=list)
    rationale: str
