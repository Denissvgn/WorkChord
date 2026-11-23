# Breadcrumbs Module

**Path:** `frontend/src/components/layout/Breadcrumbs.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/Breadcrumbs.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `lucide-react` | `ChevronRight` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Breadcrumbs` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/Breadcrumbs.tsx"]
    n1["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n2["frontend/src/features/scope/useScopeLink.ts"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n4["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n0 --> n2
    n1 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/Breadcrumbs.md"
    click n1 "../modules/AgentManifestWorkflow.md"
    click n2 "../modules/useScopeLink.md"
    click n3 "../modules/ProjectDetailPage.md"
    click n4 "../modules/ProjectReleaseDetailPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [BreadcrumbItem](../entities/BreadcrumbItem.md) | Interface | 6 | — | — |
| [BreadcrumbsProps](../entities/BreadcrumbsProps.md) | Interface | 11 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `Breadcrumbs` | `({ items, label }: BreadcrumbsProps)` | — | — |
