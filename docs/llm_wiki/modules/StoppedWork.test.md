# StoppedWork.test Module

**Path:** `frontend/src/components/tasks/StoppedWork.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/StoppedWork.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/MutationSuccessFeedback` | `MutationSuccessFeedback` | — | compiler-dependent |
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../i18n/i18n` | `i18n`, `ensureLanguageResources` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `../../utils/taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `../../utils/taskFilters` | `filterTaskBySearch`, `filterTaskWithChildren` | — | compiler-dependent |
| `./StatusChangeControl` | `StatusChangeControl` | — | compiler-dependent |
| `./TaskFiltersBar` | `TaskFilters` | Specifier | compiler-dependent |
| `./TaskFiltersBar` | `TaskFiltersBar` | — | compiler-dependent |
| `./TaskRow` | `TaskRow` | — | compiler-dependent |
| `./TaskSupersedeForm` | `TaskSupersedeForm` | — | compiler-dependent |
| `./TaskWorkPanel` | `TaskWorkPanel` | — | compiler-dependent |
| `./taskStateChip` | `taskStateChip` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `base` |
| Module calls | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/StoppedWork.test.tsx"]
    n1 --> n0
    click n1 "../modules/StoppedWork.test.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
