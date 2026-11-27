# TaskPostponement.test Module

**Path:** `frontend/src/components/tasks/TaskPostponement.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskPostponement.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/MutationSuccessFeedback` | `MutationSuccessFeedback` | — | compiler-dependent |
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../i18n/i18n` | `i18n`, `ensureLanguageResources` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskPostponementRecord` | Declaration | erased |
| `./TaskWorkPanel` | `TaskWorkPanel` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `base`, `postponed` |
| Module calls | `service = hoisted`, `mock`, `mock`, `beforeEach`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskPostponement.test.tsx"]
    n1["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/identity/identityService.ts"]
    n4["frontend/src/features/MutationSuccessFeedback.tsx"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n1 --> n2
    n1 --> n7
    n2 --> n3
    n6 --> n5
    click n0 "../modules/TaskPostponement.test.md"
    click n1 "../modules/TaskWorkPanel.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/identityService.md"
    click n4 "../modules/MutationSuccessFeedback.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [MutationSuccessFeedback](../modules/MutationSuccessFeedback.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
