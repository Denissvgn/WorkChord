# team Module

**Path:** `backend/app/schemas/team.py`

## Description

Team member schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.planning_inputs` | `PlanningInputRevisions`, `WorkingZone` |
| `datetime` | `date`, `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `field_validator`, `model_validator` |
| `typing` | `Any`, `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/schemas/team.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/schemas_team.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (20) |
| Outbound | `backend` (1) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [VacationCreate](../entities/schemas_team_VacationCreate.md) | 28 | `PlanningInputRevisions` | Schema for creating a vacation. |
| [VacationUpdate](../entities/VacationUpdate.md) | 41 | `PlanningInputRevisions` | Schema for partially updating a vacation period. |
| [VacationResponse](../entities/VacationResponse.md) | 55 | `BaseModel` | Schema for vacation response. |
| [VacationImportError](../entities/schemas_team_VacationImportError.md) | 66 | `BaseModel` | One vacation import row that could not be applied. |
| [VacationImportRequest](../entities/VacationImportRequest.md) | 72 | `BaseModel` | CSV text for bulk importing team vacations. |
| [VacationImportResponse](../entities/schemas_team_VacationImportResponse.md) | 77 | `BaseModel` | Summary of bulk vacation import results. |
| [TeamMemberCreate](../entities/schemas_team_TeamMemberCreate.md) | 85 | `PlanningInputRevisions` | Schema for creating a team member. |
| [TeamMemberUpdate](../entities/TeamMemberUpdate.md) | 96 | `PlanningInputRevisions` | Schema for updating a team member. |
| [TeamMemberProfileSkillCreate](../entities/schemas_team_TeamMemberProfileSkillCreate.md) | 107 | `PlanningInputRevisions` | Schema for creating a profile skill or weakness. |
| [TeamMemberProfileSkillUpdate](../entities/schemas_team_TeamMemberProfileSkillUpdate.md) | 141 | `PlanningInputRevisions` | Schema for updating a profile skill or weakness. |
| [TeamMemberProfileSkillResponse](../entities/TeamMemberProfileSkillResponse.md) | 177 | `BaseModel` | Schema for profile skill responses. |
| [TeamMemberProfileCreate](../entities/schemas_team_TeamMemberProfileCreate.md) | 195 | `BaseModel` | Schema for creating a reusable team-member profile. |
| [TeamMemberProfileUpdate](../entities/schemas_team_TeamMemberProfileUpdate.md) | 223 | `PlanningInputRevisions` | Schema for updating a reusable team-member profile. |
| [TeamMemberProfileResponse](../entities/TeamMemberProfileResponse.md) | 252 | `BaseModel` | Schema for reusable team-member profile responses. |
| [TeamMemberProfileCompact](../entities/schemas_team_TeamMemberProfileCompact.md) | 271 | `BaseModel` | Compact profile data embedded in team-member responses. |
| [TeamMemberResponse](../entities/TeamMemberResponse.md) | 285 | `BaseModel` | Schema for team member response. |
| [TeamMemberOptionResponse](../entities/TeamMemberOptionResponse.md) | 303 | `BaseModel` | Compact team-member identity for owner and assignee selectors. |
| [MemberCapacity](../entities/schemas_team_MemberCapacity.md) | 315 | `BaseModel` | Capacity calculation for a team member. |
| [MemberWorkload](../entities/schemas_team_MemberWorkload.md) | 330 | `BaseModel` | Workload information for a team member. |
| [TeamImportRequest](../entities/TeamImportRequest.md) | 341 | `PlanningInputRevisions` | Request for importing team members from text. |
| [TeamImportResponse](../entities/TeamImportResponse.md) | 346 | `BaseModel` | Response for team import. |
| [AssigneeRecommendationResponse](../entities/AssigneeRecommendationResponse.md) | 352 | `BaseModel` | Explainable candidate score for assigning a task or triage item. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_clean_optional_text` | `(value: Optional[str]) -> Optional[str]` | — | Trim optional text values and normalize blanks to null. |
| `_dedupe_keywords` | `(values: list[Any]) -> list[str]` | — | Trim keyword strings and preserve first occurrence order. |
