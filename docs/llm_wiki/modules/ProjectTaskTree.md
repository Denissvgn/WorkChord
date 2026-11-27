# ProjectTaskTree Module

**Path:** `frontend/src/components/projects/ProjectTaskTree.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectTaskTree.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `../../utils/taskState` | `stateOf` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../tasks/TaskEditorDrawer` | `TaskEditorDrawer` | — | compiler-dependent |
| `../tasks/TaskRow` | `TaskRow` | — | compiler-dependent |
| `../tasks/TaskSelectionBar` | `TaskSelectionBar` | — | compiler-dependent |
| `../tasks/taskRowValues` | `getEffectiveEffort` | — | compiler-dependent |
| `../tasks/taskStateChip` | `taskStateChip` | — | compiler-dependent |
| `../tasks/useAgentRowFacts` | `agentRowValues`, `useAgentRowFacts` | — | compiler-dependent |
| `../tasks/useIterationRowData` | `useIterationRowData` | — | compiler-dependent |
| `../tasks/useTaskRowEdits` | `useTaskRowEdits` | — | compiler-dependent |
| `../tasks/useTaskSelection` | `useTaskSelection` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useCallback`, `useMemo`, `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectTaskSection`, `ProjectTaskTree` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/ProjectTaskTree.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectTaskSection](../entities/ProjectTaskSection.md) | Interface | 19 | — | — |
| [ProjectTaskTreeProps](../entities/ProjectTaskTreeProps.md) | Interface | 25 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectTaskTree` | `({ sections, dependencyTasks }: ProjectTaskTreeProps)` | — | — |
