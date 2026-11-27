# TaskReassign.test Module

**Path:** `frontend/src/components/tasks/TaskReassign.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskReassign.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n`, `changeAppLanguage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `RoutingCheck`, `Task` | Declaration | erased |
| `./TaskReadView` | `TaskReadView` | — | compiler-dependent |
| `./TaskReassign` | `TaskReassign` | — | compiler-dependent |
| `./taskEditorContract` | `emptyTaskBrief` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `routing`, `task`, `noRoutingCheck` |
| Module calls | `service = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskEditorContract.ts"]
    n1["frontend/src/components/tasks/TaskReadView.tsx"]
    n2["frontend/src/components/tasks/TaskReassign.test.tsx"]
    n3["frontend/src/components/tasks/TaskReassign.tsx"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/task.ts"]
    n0 --> n6
    n1 --> n0
    n1 --> n3
    n1 --> n6
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n6
    n5 --> n4
    click n0 "../modules/taskEditorContract.md"
    click n1 "../modules/TaskReadView.md"
    click n2 "../modules/TaskReassign.test.md"
    click n3 "../modules/TaskReassign.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [TaskReadView](../modules/TaskReadView.md) |
| Outbound | [TaskReassign](../modules/TaskReassign.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
