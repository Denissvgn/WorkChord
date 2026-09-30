"""Validated working zones and optional aggregate revisions for shared inputs."""

from typing import Annotated
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
    expected_revisions: dict[int, PositiveInt] = Field(default_factory=dict)
