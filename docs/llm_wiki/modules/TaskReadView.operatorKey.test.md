# TaskReadView.operatorKey.test Module

**Path:** `frontend/src/components/tasks/TaskReadView.operatorKey.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskReadView.operatorKey.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `../../utils/adminAccess` | `ADMIN_API_KEY_STORAGE_KEY` | — | compiler-dependent |
| `./TaskReadView` | `TaskReadView` | — | compiler-dependent |
| `./taskEditorContract` | `emptyTaskBrief` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `task`, `identity`, `actions` |
| Module calls | `service = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskEditorContract.ts"]
    n1["frontend/src/components/tasks/TaskReadView.operatorKey.test.tsx"]
    n2["frontend/src/components/tasks/TaskReadView.tsx"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/features/identity/identityService.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/task.ts"]
    n7["frontend/src/utils/adminAccess.ts"]
    n0 --> n6
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n2 --> n0
    n2 --> n6
    n2 --> n7
    n3 --> n4
    click n0 "../modules/taskEditorContract.md"
    click n1 "../modules/TaskReadView.operatorKey.test.md"
    click n2 "../modules/TaskReadView.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/identityService.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_task.md"
    click n7 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [TaskReadView](../modules/TaskReadView.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
