# ProjectForm.test Module

**Path:** `frontend/src/components/projects/ProjectForm.test.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectForm.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/project` | `Project` | Declaration | erased |
| `./ProjectForm` | `ProjectForm` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `axios` | `AxiosError` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `projects`, `planning`, `project` |
| Module calls | `projects = hoisted`, `mock`, `mock`, `mock`, `planning = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectForm.test.tsx"]
    n1["frontend/src/components/projects/ProjectForm.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/project.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/ProjectForm.test.md"
    click n1 "../modules/ProjectForm.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_project.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ProjectForm](../modules/ProjectForm.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_project](../modules/types_project.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
