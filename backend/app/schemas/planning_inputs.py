"""Validated working zones and optional aggregate revisions for shared inputs."""

from typing import Annotated, Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from pydantic import AfterValidator, BaseModel, Field, PositiveInt


def validate_working_zone(value: str) -> str:
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError("Use a valid IANA time zone") from exc
    return value


WorkingZone = Annotated[str, AfterValidator(validate_working_zone)]


class PlanningInputRevisions(BaseModel):
    expected_revisions: dict[PositiveInt, PositiveInt] = Field(default_factory=dict, max_length=500)


class PlanningInputContext(BaseModel):
    kind: Literal["calendar", "project", "iteration", "profile", "member", "vacation"]
    resource_id: PositiveInt
    resource: dict[str, Any]
    expected_revisions: dict[PositiveInt, PositiveInt] = Field(max_length=500)
    complete: Literal[True] = True


class MemberPlanningIntent(BaseModel):
    profile_id: PositiveInt | None = None
    name: str = Field(default='', max_length=255)
    email: str | None = Field(default=None, max_length=255)
    text: str | None = Field(default=None, max_length=2 * 1024 * 1024)
    csv_text: str | None = Field(default=None, max_length=2 * 1024 * 1024)
