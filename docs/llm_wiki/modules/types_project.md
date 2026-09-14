# project Module

**Path:** `frontend/src/types/project.ts`

## Description

_Auto-generated from `frontend/src/types/project.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./task` | `Task` |
| `./team` | `TeamMemberOption`, `TeamMemberProfileCompact` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Initiative`, `InitiativeCreate`, `InitiativeUpdate`, `Project`, `ProjectCreate`, `ProjectHealth`, `ProjectInitiativeSummary`, `ProjectMilestone`, `ProjectMilestoneCreateRequest`, `ProjectMilestoneDeleteResponse`, `ProjectMilestoneStatus`, `ProjectMilestoneSummary`, `ProjectMilestoneTaskGroup`, `ProjectMilestoneUpdateRequest`, `ProjectOwner`, `ProjectPortfolioSummary`, `ProjectProfileOwner`, `ProjectStatus`, `ProjectSummary`, `ProjectTargetDateRisk`, `ProjectTask`, `ProjectUpdate`, `ProjectUpdateEntry`, `ProjectUpdateEntryCreate`, `ProjectUpdateFreshness`, `RoadmapMilestonePage` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/InitiativeForm.tsx"]
    n1["frontend/src/components/projects/ProjectForm.tsx"]
    n2["frontend/src/components/projects/projectStatusStyles.ts"]
    n3["frontend/src/pages/OverviewPage.tsx"]
    n4["frontend/src/pages/ProjectDetailPage.tsx"]
    n5["frontend/src/pages/ProjectsPage.tsx"]
    n6["frontend/src/pages/RoadmapPage.tsx"]
    n7["frontend/src/pages/TriagePage.tsx"]
    n8["frontend/src/services/projectService.ts"]
    n9["frontend/src/types/project.ts"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/types/team.ts"]
    n0 --> n8
    n0 --> n9
    n1 --> n8
    n1 --> n9
    n2 --> n9
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n4 --> n1
    n4 --> n2
    n4 --> n8
    n4 --> n9
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n8
    n5 --> n9
    n6 --> n2
    n6 --> n8
    n6 --> n9
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n7 --> n11
    n8 --> n9
    n8 --> n10
    n9 --> n10
    n9 --> n11
    n10 --> n11
    click n0 "../modules/InitiativeForm.md"
    click n1 "../modules/ProjectForm.md"
    click n2 "../modules/projectStatusStyles.md"
    click n3 "../modules/OverviewPage.md"
    click n4 "../modules/ProjectDetailPage.md"
    click n5 "../modules/ProjectsPage.md"
    click n6 "../modules/RoadmapPage.md"
    click n7 "../modules/TriagePage.md"
    click n8 "../modules/projectService.md"
    click n9 "../modules/types_project.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InitiativeForm](../modules/InitiativeForm.md) |
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [projectStatusStyles](../modules/projectStatusStyles.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Inbound | [projectService](../modules/projectService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [types_team](../modules/types_team.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Initiative](../entities/types_project_Initiative.md) | Class | 12 | — | — |
| [InitiativeCreate](../entities/types_project_InitiativeCreate.md) | Class | 26 | — | — |
| [InitiativeUpdate](../entities/types_project_InitiativeUpdate.md) | Class | 35 | — | — |
| [ProjectInitiativeSummary](../entities/types_project_ProjectInitiativeSummary.md) | Class | 44 | — | — |
| [Project](../entities/types_project_Project.md) | Class | 55 | — | — |
| [ProjectCreate](../entities/types_project_ProjectCreate.md) | Class | 75 | — | — |
| [ProjectUpdate](../entities/types_project_ProjectUpdate.md) | Class | 88 | — | — |
| [ProjectUpdateEntry](../entities/types_project_ProjectUpdateEntry.md) | Class | 102 | — | — |
| [ProjectUpdateEntryCreate](../entities/types_project_ProjectUpdateEntryCreate.md) | Class | 115 | — | — |
| [ProjectMilestone](../entities/types_project_ProjectMilestone.md) | Class | 124 | — | — |
| [RoadmapMilestonePage](../entities/types_project_RoadmapMilestonePage.md) | Class | 137 | — | — |
| [ProjectMilestoneCreateRequest](../entities/types_project_ProjectMilestoneCreateRequest.md) | Class | 142 | — | — |
| [ProjectMilestoneUpdateRequest](../entities/ProjectMilestoneUpdateRequest.md) | Class | 151 | — | — |
| [ProjectMilestoneDeleteResponse](../entities/types_project_ProjectMilestoneDeleteResponse.md) | Class | 160 | — | — |
| [ProjectMilestoneSummary](../entities/types_project_ProjectMilestoneSummary.md) | Class | 166 | — | — |
| [ProjectMilestoneTaskGroup](../entities/types_project_ProjectMilestoneTaskGroup.md) | Class | 175 | — | — |
| [ProjectPortfolioSummary](../entities/types_project_ProjectPortfolioSummary.md) | Class | 187 | — | — |
| [ProjectSummary](../entities/types_project_ProjectSummary.md) | Class | 198 | — | — |
| [ProjectStatus](../entities/types_project_ProjectStatus.md) | Type alias | 4 | — | — |
| [ProjectHealth](../entities/types_project_ProjectHealth.md) | Type alias | 5 | — | — |
| [ProjectTargetDateRisk](../entities/types_project_ProjectTargetDateRisk.md) | Type alias | 6 | — | — |
| [ProjectUpdateFreshness](../entities/types_project_ProjectUpdateFreshness.md) | Type alias | 7 | — | — |
| [ProjectMilestoneStatus](../entities/types_project_ProjectMilestoneStatus.md) | Type alias | 8 | — | — |
| [ProjectOwner](../entities/ProjectOwner.md) | Type alias | 9 | — | — |
| [ProjectProfileOwner](../entities/ProjectProfileOwner.md) | Type alias | 10 | — | — |
| [ProjectTask](../entities/ProjectTask.md) | Type alias | 236 | — | — |
