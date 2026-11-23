# AtRiskTaskReasons Module

**Path:** `frontend/src/components/tasks/AtRiskTaskReasons.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/AtRiskTaskReasons.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/atRiskReasons` | `atRiskReasons` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AtRiskTaskReasons` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/AtRiskTaskReasons.tsx"]
    n1["frontend/src/features/planningMasters/atRiskReasons.ts"]
    n2["frontend/src/pages/TasksPage.tsx"]
    n3["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/AtRiskTaskReasons.md"
    click n1 "../modules/atRiskReasons.md"
    click n2 "../modules/TasksPage.md"
    click n3 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [atRiskReasons](../modules/atRiskReasons.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AtRiskTaskReasons` | `({ task }: { task: Task })` | — | The reasons an opened task is at risk, shown while the Tasks list is filtered to at-risk work. |
