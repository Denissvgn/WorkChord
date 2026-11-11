# teamService Module

**Path:** `frontend/src/services/teamService.ts`

## Description

_Auto-generated from `frontend/src/services/teamService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/team` | `MemberCapacity`, `MemberWorkload`, `TeamMember`, `TeamMemberCreate`, `TeamMemberOption`, `TeamMemberProfile`, `TeamMemberProfileCreate`, `TeamMemberProfileSkill`, `TeamMemberProfileSkillCreate`, `TeamMemberProfileSkillUpdate`, `TeamMemberProfileUpdate`, `Vacation`, `VacationCreate`, `VacationImportResponse` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |
| `./planningInputService` | `ObservedRevisions` | Specifier | compiler-dependent |
| `./planningInputService` | `revisionHeaders` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `teamService` |
| Constants | `teamService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/services/teamService.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/teamService.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (20) |
| Outbound | `frontend` (3) |

> All 23 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
