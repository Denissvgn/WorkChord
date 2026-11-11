# MyWorkPage.test Module

**Path:** `frontend/src/pages/MyWorkPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/MyWorkPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/tasks/taskDraftStorage` | `writeTaskDraft` | — | compiler-dependent |
| `../components/tasks/taskEditorContract` | `buildTaskEditorDefaults` | — | compiler-dependent |
| `../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../types/task` | `Task` | Declaration | erased |
| `./MyWorkPage` | `MyWorkPage` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `api` |
| Module calls | `api = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `it`, `it`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskDraftStorage.ts"]
    n1["frontend/src/components/tasks/taskEditorContract.ts"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/pages/MyWorkPage.test.tsx"]
    n4["frontend/src/pages/MyWorkPage.tsx"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/task.ts"]
    n0 --> n1
    n1 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n4 --> n2
    n4 --> n6
    click n0 "../modules/taskDraftStorage.md"
    click n1 "../modules/taskEditorContract.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/MyWorkPage.test.md"
    click n4 "../modules/MyWorkPage.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [taskDraftStorage](../modules/taskDraftStorage.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
