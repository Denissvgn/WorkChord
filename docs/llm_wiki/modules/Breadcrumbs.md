# Breadcrumbs Module

**Path:** `frontend/src/components/layout/Breadcrumbs.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/Breadcrumbs.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `lucide-react` | `ChevronRight` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Breadcrumbs` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/Breadcrumbs.tsx"]
    n1["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n2["frontend/src/pages/PlanMasterPage.tsx"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n4["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/Breadcrumbs.md"
    click n1 "../modules/AgentTeamSetupMasterPage.md"
    click n2 "../modules/PlanMasterPage.md"
    click n3 "../modules/ProjectDetailPage.md"
    click n4 "../modules/ProjectReleaseDetailPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [BreadcrumbItem](../entities/BreadcrumbItem.md) | Class | 5 | — | — |
| [BreadcrumbsProps](../entities/BreadcrumbsProps.md) | Class | 10 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `Breadcrumbs` | `({ items, label }: BreadcrumbsProps)` | — | — |
