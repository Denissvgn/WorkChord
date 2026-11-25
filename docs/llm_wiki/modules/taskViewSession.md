# taskViewSession Module

**Path:** `frontend/src/components/tasks/taskViewSession.ts`

## Description

Memory-only state of the task view's panels (prerequisite list open, branch conflict notice shown, catch-up finished), held for as long as the drawer is open and scoped to the signed-in person and task. The task view remounts on every task version change, so the panels read and update this state instead of keeping their own.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `react` | `useCallback`, `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `EMPTY_TASK_VIEW_SESSION`, `TaskViewSession`, `TaskViewSessionUpdate`, `useTaskViewSession` |
| Constants | `EMPTY_TASK_VIEW_SESSION` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/DeliveryDependencies.test.tsx"]
    n1["frontend/src/components/tasks/DeliveryDependencies.tsx"]
    n2["frontend/src/components/tasks/GitHubReconciliationPanel.test.tsx"]
    n3["frontend/src/components/tasks/GitHubReconciliationPanel.tsx"]
    n4["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n5["frontend/src/components/tasks/TaskReadView.tsx"]
    n6["frontend/src/components/tasks/taskViewSession.ts"]
    n0 --> n1
    n0 --> n6
    n1 --> n6
    n2 --> n3
    n2 --> n6
    n3 --> n6
    n4 --> n5
    n4 --> n6
    n5 --> n1
    n5 --> n3
    n5 --> n6
    click n0 "../modules/DeliveryDependencies.test.md"
    click n1 "../modules/DeliveryDependencies.md"
    click n2 "../modules/GitHubReconciliationPanel.test.md"
    click n3 "../modules/GitHubReconciliationPanel.md"
    click n4 "../modules/TaskEditorDrawer.md"
    click n5 "../modules/TaskReadView.md"
    click n6 "../modules/taskViewSession.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryDependencies.test](../modules/DeliveryDependencies.test.md) |
| Inbound | [DeliveryDependencies](../modules/DeliveryDependencies.md) |
| Inbound | [GitHubReconciliationPanel.test](../modules/GitHubReconciliationPanel.test.md) |
| Inbound | [GitHubReconciliationPanel](../modules/GitHubReconciliationPanel.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Inbound | [TaskReadView](../modules/TaskReadView.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskViewSession](../entities/TaskViewSession.md) | Interface | 7 | — | What a person was doing in the task view's panels. The view remounts whenever the task version |
| [TaskViewSessionUpdate](../entities/TaskViewSessionUpdate.md) | Type alias | 8 | `(patch: Partial<TaskViewSession>) => void` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useTaskViewSession` | `(scope: string \| null)` | — | Session state keyed by the signed-in person and task, so it never carries to another person or task. |
