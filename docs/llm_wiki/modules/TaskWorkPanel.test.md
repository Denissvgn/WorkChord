# TaskWorkPanel.test Module

**Path:** `frontend/src/components/tasks/TaskWorkPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskWorkPanel.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../../types/task` | `Task` |
| `./TaskWorkPanel` | `TaskWorkPanel` |
| `./taskEditorContract` | `emptyTaskBrief` |
| `@testing-library/react` | `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `task` |
| Module calls | `service = hoisted`, `mock`, `mock`, `describe`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/taskEditorContract.ts"]
    n1["frontend/src/components/tasks/TaskWorkPanel.test.tsx"]
    n2["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/task.ts"]
    n0 --> n4
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n4
    click n0 "../modules/taskEditorContract.md"
    click n1 "../modules/TaskWorkPanel.test.md"
    click n2 "../modules/TaskWorkPanel.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
