# ProjectRequestsTab Module

**Path:** `frontend/src/components/projects/ProjectRequestsTab.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectRequestsTab.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectRequestsTab` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectRequestsTab.tsx"]
    n1["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n2["frontend/src/pages/ProjectDetailPage.tsx"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/ProjectRequestsTab.md"
    click n1 "../modules/RequestSourceLinksPanel.md"
    click n2 "../modules/ProjectDetailPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectRequestsTab` | `({ projectId, count, onChanged }: { projectId: number; count: number; onChanged: () => void })` | — | — |
