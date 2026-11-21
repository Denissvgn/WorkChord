# projectStatusStyles Module

**Path:** `frontend/src/components/projects/projectStatusStyles.ts`

## Description

_Auto-generated from `frontend/src/components/projects/projectStatusStyles.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/project` | `ProjectMilestoneStatus`, `ProjectStatus` | Declaration | erased |
| `../ui/tone` | `PillTone` | Specifier | compiler-dependent |
| `../ui/tone` | `toneBorderClassName`, `wcPillClass` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectRecordStatus`, `projectHealthBadgeClassName`, `projectStatusBadgeClassName`, `projectStatusPillClassName` |
| Constants | `projectRecordStatusTone` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/InitiativeGroupHeader.tsx"]
    n1["frontend/src/components/projects/MilestonesSection.tsx"]
    n2["frontend/src/components/projects/projectStatusStyles.test.ts"]
    n3["frontend/src/components/projects/projectStatusStyles.ts"]
    n4["frontend/src/components/projects/RoadmapView.tsx"]
    n5["frontend/src/components/ui/tone.ts"]
    n6["frontend/src/pages/ProjectsPage.tsx"]
    n7["frontend/src/types/project.ts"]
    n0 --> n3
    n0 --> n7
    n1 --> n3
    n1 --> n7
    n2 --> n3
    n3 --> n5
    n3 --> n7
    n4 --> n0
    n4 --> n3
    n4 --> n7
    n6 --> n0
    n6 --> n3
    n6 --> n4
    n6 --> n7
    click n0 "../modules/InitiativeGroupHeader.md"
    click n1 "../modules/MilestonesSection.md"
    click n2 "../modules/projectStatusStyles.test.md"
    click n3 "../modules/projectStatusStyles.md"
    click n4 "../modules/RoadmapView.md"
    click n5 "../modules/tone.md"
    click n6 "../modules/ProjectsPage.md"
    click n7 "../modules/types_project.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InitiativeGroupHeader](../modules/InitiativeGroupHeader.md) |
| Inbound | [MilestonesSection](../modules/MilestonesSection.md) |
| Inbound | [projectStatusStyles.test](../modules/projectStatusStyles.test.md) |
| Inbound | [RoadmapView](../modules/RoadmapView.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [types_project](../modules/types_project.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectRecordStatus](../entities/ProjectRecordStatus.md) | Type alias | 8 | `ProjectStatus \| ProjectMilestoneStatus` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `projectStatusBadgeClassName` | `(status: ProjectRecordStatus)` | — | — |
| `projectStatusPillClassName` | `(status: ProjectRecordStatus)` | — | — |
| `projectHealthBadgeClassName` | `(health: string)` | — | The health badge colours shared by project rows and initiative headers. |
