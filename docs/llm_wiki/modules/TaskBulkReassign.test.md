# TaskBulkReassign.test Module

**Path:** `frontend/src/components/tasks/TaskBulkReassign.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBulkReassign.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/MutationSuccessFeedback` | `MutationSuccessFeedback` | — | compiler-dependent |
| `../../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `RoutingCheck`, `TaskBulkOperationRequest` | Declaration | erased |
| `./TaskBulkOperationsPanel` | `TaskBulkOperationsPanel` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `selected`, `before`, `after` |
| Module calls | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n1["frontend/src/components/tasks/TaskBulkReassign.test.tsx"]
    n2["frontend/src/features/MutationSuccessFeedback.tsx"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/task.ts"]
    n0 --> n5
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n4 --> n3
    click n0 "../modules/TaskBulkOperationsPanel.md"
    click n1 "../modules/TaskBulkReassign.test.md"
    click n2 "../modules/MutationSuccessFeedback.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) |
| Outbound | [MutationSuccessFeedback](../modules/MutationSuccessFeedback.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
