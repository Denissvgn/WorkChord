# TaskBriefEditor.test Module

**Path:** `frontend/src/components/tasks/TaskBriefEditor.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBriefEditor.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./TaskBriefEditor` | `TaskBriefEditor` | — | compiler-dependent |
| `./taskEditorContract` | `buildTaskEditorDefaults`, `emptyTaskBrief`, `toTaskCreate` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskBriefEditor.test.tsx"]
    n1["frontend/src/components/tasks/TaskBriefEditor.tsx"]
    n2["frontend/src/components/tasks/taskEditorContract.ts"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    click n0 "../modules/TaskBriefEditor.test.md"
    click n1 "../modules/TaskBriefEditor.md"
    click n2 "../modules/taskEditorContract.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskBriefEditor](../modules/TaskBriefEditor.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
