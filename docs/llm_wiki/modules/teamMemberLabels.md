# teamMemberLabels Module

**Path:** `frontend/src/utils/teamMemberLabels.ts`

## Description

_Auto-generated from `frontend/src/utils/teamMemberLabels.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../i18n/i18n` | `i18n` |
| `../types/team` | `TeamMemberOption`, `TeamMemberProfileCompact` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `formatOwnerLabel`, `formatPortfolioOwnerLabel`, `formatTeamMemberLabel`, `formatTeamMemberProfileLabel` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/InitiativeForm.tsx"]
    n1["frontend/src/components/projects/ProjectForm.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n4["frontend/src/pages/ProjectsPage.tsx"]
    n5["frontend/src/pages/RoadmapPage.tsx"]
    n6["frontend/src/types/team.ts"]
    n7["frontend/src/utils/teamMemberLabels.ts"]
    n0 --> n7
    n1 --> n7
    n3 --> n1
    n3 --> n2
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n7
    n5 --> n2
    n5 --> n7
    n7 --> n2
    n7 --> n6
    click n0 "../modules/InitiativeForm.md"
    click n1 "../modules/ProjectForm.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/ProjectDetailPage.md"
    click n4 "../modules/ProjectsPage.md"
    click n5 "../modules/RoadmapPage.md"
    click n6 "../modules/types_team.md"
    click n7 "../modules/teamMemberLabels.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InitiativeForm](../modules/InitiativeForm.md) |
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_team](../modules/types_team.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TeamMemberLabelSource](../entities/TeamMemberLabelSource.md) | Type alias | 6 | — | — |
| [TeamMemberProfileLabelSource](../entities/TeamMemberProfileLabelSource.md) | Type alias | 7 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `formatTeamMemberLabel` | `(member: TeamMemberLabelSource)` | — | — |
| `formatOwnerLabel` | `(owner: TeamMemberLabelSource \| null, ownerId: number \| null, emptyLabel: string)` | — | — |
| `formatTeamMemberProfileLabel` | `(profile: TeamMemberProfileLabelSource)` | — | — |
| `formatPortfolioOwnerLabel` | `(ownerProfile: TeamMemberProfileLabelSource \| null, legacyOwner: TeamMemberLabelSource \| null, legacyOwnerId: number \| null, emptyLabel: string)` | — | — |
