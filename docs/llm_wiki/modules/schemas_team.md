# team Module

**Path:** `backend/app/schemas/team.py`

## Description

Team member schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.agent_team_setup` | `STABLE_KEY_PATTERN` |
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
| Inbound | `backend` (22) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 24 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [VacationCreate](../entities/schemas_team_VacationCreate.md) | 29 | `PlanningInputRevisions` | Schema for creating a vacation. |
| [VacationUpdate](../entities/VacationUpdate.md) | 42 | `PlanningInputRevisions` | Schema for partially updating a vacation period. |
| [VacationResponse](../entities/VacationResponse.md) | 56 | `BaseModel` | Schema for vacation response. |
| [VacationImportError](../entities/schemas_team_VacationImportError.md) | 67 | `BaseModel` | One vacation import row that could not be applied. |
| [VacationImportRequest](../entities/VacationImportRequest.md) | 73 | `BaseModel` | CSV text for bulk importing team vacations. |
| [VacationImportResponse](../entities/schemas_team_VacationImportResponse.md) | 78 | `BaseModel` | Summary of bulk vacation import results. |
| [TeamMemberCreate](../entities/schemas_team_TeamMemberCreate.md) | 86 | `PlanningInputRevisions` | Schema for creating a team member. |
| [TeamMemberUpdate](../entities/TeamMemberUpdate.md) | 97 | `PlanningInputRevisions` | Schema for updating a team member. |
| [TeamMemberProfileSkillCreate](../entities/schemas_team_TeamMemberProfileSkillCreate.md) | 108 | `PlanningInputRevisions` | Schema for creating a profile skill or weakness. |
| [TeamMemberProfileSkillUpdate](../entities/schemas_team_TeamMemberProfileSkillUpdate.md) | 142 | `PlanningInputRevisions` | Schema for updating a profile skill or weakness. |
| [TeamMemberProfileSkillResponse](../entities/TeamMemberProfileSkillResponse.md) | 178 | `BaseModel` | Schema for profile skill responses. |
| [TeamMemberProfileCreate](../entities/schemas_team_TeamMemberProfileCreate.md) | 196 | `BaseModel` | Schema for creating a reusable team-member profile. |
| [TeamMemberProfileUpdate](../entities/schemas_team_TeamMemberProfileUpdate.md) | 224 | `PlanningInputRevisions` | Schema for updating a reusable team-member profile. |
| [TeamMemberProfileSeedKeyBind](../entities/TeamMemberProfileSeedKeyBind.md) | 253 | `BaseModel` | Operator request that binds a stable seed key to a profile that has none. |
| [TeamMemberProfileResponse](../entities/TeamMemberProfileResponse.md) | 264 | `BaseModel` | Schema for reusable team-member profile responses. |
| [TeamMemberProfileCompact](../entities/schemas_team_TeamMemberProfileCompact.md) | 283 | `BaseModel` | Compact profile data embedded in team-member responses. |
| [TeamMemberResponse](../entities/TeamMemberResponse.md) | 306 | `BaseModel` | Schema for team member response. |
| [TeamMemberOptionResponse](../entities/TeamMemberOptionResponse.md) | 333 | `BaseModel` | Compact team-member identity for owner and assignee selectors. |
| [MemberCapacity](../entities/schemas_team_MemberCapacity.md) | 345 | `BaseModel` | Capacity calculation for a team member. |
| [MemberWorkload](../entities/schemas_team_MemberWorkload.md) | 361 | `BaseModel` | Workload information for a team member. |
| [TeamImportRequest](../entities/TeamImportRequest.md) | 379 | `PlanningInputRevisions` | Request for importing team members from text. |
| [TeamImportResponse](../entities/TeamImportResponse.md) | 384 | `BaseModel` | Response for team import. |
| [AssigneeRecommendationResponse](../entities/AssigneeRecommendationResponse.md) | 390 | `BaseModel` | Explainable candidate score for assigning a task or triage item. |
| [CapacityAdjustmentItem](../entities/CapacityAdjustmentItem.md) | 404 | `BaseModel` | One dated replacement of a capacity row's availability percentage. |
| [CapacityAdjustmentCommand](../entities/CapacityAdjustmentCommand.md) | 422 | `PlanningInputRevisions` | Record and withdraw dated adjustments on one capacity row in one command. |
| [CapacityAdjustmentResponse](../entities/CapacityAdjustmentResponse.md) | 443 | `BaseModel` | A recorded or withdrawn dated adjustment, with who recorded it. |
| [EffectiveCapacityDay](../entities/EffectiveCapacityDay.md) | 465 | `BaseModel` | One date of this row and of every row sharing its person, before and after the change. |
| [CapacityAdjustmentResult](../entities/CapacityAdjustmentResult.md) | 480 | `BaseModel` | Effective capacity for the changed dates and the adjustments the command records. |
| [CapacityTransferSource](../entities/CapacityTransferSource.md) | 502 | `BaseModel` | A capacity row that lends part of its availability percentage. |
| [CapacityTransferCommand](../entities/CapacityTransferCommand.md) | 509 | `PlanningInputRevisions` | Lend availability from one or more rows to a row of the same person for a bounded date range. |
| [CapacityTransferWithdrawal](../entities/CapacityTransferWithdrawal.md) | 541 | `PlanningInputRevisions` | Return the lent capacity of every row of one transfer together. |
| [CapacityTransferDay](../entities/CapacityTransferDay.md) | 554 | `BaseModel` | One date of one row of a transfer, before and after the command. |
| [CapacityTransferSide](../entities/CapacityTransferSide.md) | 564 | `BaseModel` | One row of a transfer: the target that receives or a source that lends. |
| [PersonCapacityDay](../entities/PersonCapacityDay.md) | 579 | `BaseModel` | The person's totals over every row of the same profile on one date. |
| [CapacityTransferResult](../entities/CapacityTransferResult.md) | 590 | `BaseModel` | Effective capacity of every row of a transfer, and the adjustments the command records or withdraws. |
| [CapacityTransferRecord](../entities/CapacityTransferRecord.md) | 616 | `BaseModel` | A recorded transfer: every row it changes and whether it is still active. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_clean_optional_text` | `(value: Optional[str]) -> Optional[str]` | — | Trim optional text values and normalize blanks to null. |
| `_dedupe_keywords` | `(values: list[Any]) -> list[str]` | — | Trim keyword strings and preserve first occurrence order. |
