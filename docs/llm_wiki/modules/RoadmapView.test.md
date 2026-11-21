# RoadmapView.test Module

**Path:** `frontend/src/components/projects/RoadmapView.test.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/RoadmapView.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/project` | `Initiative`, `Project` | Declaration | erased |
| `./RoadmapView` | `RoadmapView` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `projectServiceMock`, `project`, `milestone` |
| Module calls | `projectServiceMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/RoadmapView.test.tsx"]
    n1["frontend/src/components/projects/RoadmapView.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/project.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/RoadmapView.test.md"
    click n1 "../modules/RoadmapView.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_project.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [RoadmapView](../modules/RoadmapView.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_project](../modules/types_project.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
