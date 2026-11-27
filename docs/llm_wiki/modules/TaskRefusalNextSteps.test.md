# TaskRefusalNextSteps.test Module

**Path:** `frontend/src/components/tasks/TaskRefusalNextSteps.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskRefusalNextSteps.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../i18n/i18n` | `i18n`, `ensureLanguageResources` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `RefusalNextStep`, `Task` | Declaration | erased |
| `../../utils/apiError` | `getApiNextStep` | — | compiler-dependent |
| `./TaskWorkPanel` | `TaskWorkPanel` | — | compiler-dependent |
| `./taskEditorContract` | `emptyTaskBrief` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `resolved`, `provenanceStep`, `ownerStep`, `candidateBlocker`, `publisherBlocker`, `recordable` |
| Module calls | `service = hoisted`, `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskEditorContract.ts"]
    n1["frontend/src/components/tasks/TaskRefusalNextSteps.test.tsx"]
    n2["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/features/identity/identityService.ts"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/types/task.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n0 --> n7
    n0 --> n8
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n2 --> n3
    n2 --> n7
    n2 --> n8
    n3 --> n4
    n6 --> n5
    n8 --> n7
    click n0 "../modules/taskEditorContract.md"
    click n1 "../modules/TaskRefusalNextSteps.test.md"
    click n2 "../modules/TaskWorkPanel.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/identityService.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/types_task.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
