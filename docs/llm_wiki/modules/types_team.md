# team Module

**Path:** `frontend/src/types/team.ts`

## Description

_Auto-generated from `frontend/src/types/team.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AssigneeRecommendation`, `MemberCapacity`, `MemberWorkload`, `TeamMember`, `TeamMemberAssignmentMode`, `TeamMemberCreate`, `TeamMemberOption`, `TeamMemberProfile`, `TeamMemberProfileCompact`, `TeamMemberProfileCreate`, `TeamMemberProfileKind`, `TeamMemberProfileSkill`, `TeamMemberProfileSkillCreate`, `TeamMemberProfileSkillUpdate`, `TeamMemberProfileUpdate`, `Vacation`, `VacationCreate`, `VacationImportError`, `VacationImportResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/types/team.ts"]
    n0 --> n1
    click n1 "../modules/types_team.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (19) |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Vacation](../entities/types_team_Vacation.md) | Class | 1 | — | — |
| [VacationCreate](../entities/types_team_VacationCreate.md) | Class | 7 | — | — |
| [VacationImportError](../entities/types_team_VacationImportError.md) | Class | 12 | — | — |
| [VacationImportResponse](../entities/types_team_VacationImportResponse.md) | Class | 17 | — | — |
| [TeamMemberProfileSkill](../entities/types_team_TeamMemberProfileSkill.md) | Class | 24 | — | — |
| [TeamMemberProfileSkillCreate](../entities/types_team_TeamMemberProfileSkillCreate.md) | Class | 39 | — | — |
| [TeamMemberProfile](../entities/types_team_TeamMemberProfile.md) | Class | 60 | — | — |
| [TeamMemberProfileCompact](../entities/types_team_TeamMemberProfileCompact.md) | Class | 76 | — | — |
| [TeamMemberProfileCreate](../entities/types_team_TeamMemberProfileCreate.md) | Class | 87 | — | — |
| [TeamMemberProfileUpdate](../entities/types_team_TeamMemberProfileUpdate.md) | Class | 99 | — | — |
| [TeamMember](../entities/types_team_TeamMember.md) | Class | 110 | — | — |
| [TeamMemberOption](../entities/TeamMemberOption.md) | Class | 124 | — | — |
| [TeamMemberCreate](../entities/types_team_TeamMemberCreate.md) | Class | 133 | — | — |
| [MemberWorkload](../entities/types_team_MemberWorkload.md) | Class | 143 | — | — |
| [MemberCapacity](../entities/types_team_MemberCapacity.md) | Class | 154 | — | Detailed capacity breakdown from GET /team-members/{id}/capacity. |
| [AssigneeRecommendation](../entities/AssigneeRecommendation.md) | Class | 164 | — | — |
| [TeamMemberProfileSkillUpdate](../entities/types_team_TeamMemberProfileSkillUpdate.md) | Type alias | 50 | — | — |
| [TeamMemberProfileKind](../entities/TeamMemberProfileKind.md) | Type alias | 52 | — | — |
| [TeamMemberAssignmentMode](../entities/TeamMemberAssignmentMode.md) | Type alias | 54 | — | — |
