# projectStatusStyles Module

**Path:** `frontend/src/components/projects/projectStatusStyles.ts`

## Description

_Auto-generated from `frontend/src/components/projects/projectStatusStyles.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/project` | `ProjectMilestoneStatus`, `ProjectStatus` |
| `../ui/tone` | `toneBorderClassName`, `wcPillClass`, `PillTone` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectRecordStatus`, `projectStatusBadgeClassName`, `projectStatusPillClassName` |
| Constants | `projectRecordStatusTone` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/projectStatusStyles.test.ts"]
    n1["frontend/src/components/projects/projectStatusStyles.ts"]
    n2["frontend/src/components/ui/tone.ts"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n4["frontend/src/pages/ProjectsPage.tsx"]
    n5["frontend/src/pages/RoadmapPage.tsx"]
    n6["frontend/src/types/project.ts"]
    n0 --> n1
    n1 --> n2
    n1 --> n6
    n3 --> n1
    n3 --> n2
    n3 --> n6
    n4 --> n1
    n4 --> n6
    n5 --> n1
    n5 --> n6
    click n0 "../modules/projectStatusStyles.test.md"
    click n1 "../modules/projectStatusStyles.md"
    click n2 "../modules/tone.md"
    click n3 "../modules/ProjectDetailPage.md"
    click n4 "../modules/ProjectsPage.md"
    click n5 "../modules/RoadmapPage.md"
    click n6 "../modules/types_project.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [projectStatusStyles.test](../modules/projectStatusStyles.test.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [types_project](../modules/types_project.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectRecordStatus](../entities/ProjectRecordStatus.md) | Type alias | 8 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `projectStatusBadgeClassName` | `(status: ProjectRecordStatus)` | — | — |
| `projectStatusPillClassName` | `(status: ProjectRecordStatus)` | — | — |
