# useTaskRowEdits Module

**Path:** `frontend/src/components/tasks/useTaskRowEdits.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/useTaskRowEdits.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../features/taskTransitions` | `canTransition` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskStatus` | Declaration | erased |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `./TaskRow` | `TaskRowAssigneeOption` | Declaration | erased |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `assigneeOptionsFrom`, `useAssigneeOptions`, `useTaskRowEdits` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/useTaskRowEdits.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/useTaskRowEdits.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (5) |
| Outbound | `frontend` (7) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RowTarget](../entities/RowTarget.md) | Type alias | 11 | `{ id: number; title: string; status: TaskStatus; version: number }` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `assigneeOptionsFrom` | `(members: TeamMember[]) -> TaskRowAssigneeOption[]` | — | The picker options for an iteration's team: the same people and agents, with their kind, on every surface. |
| `useAssigneeOptions` | `(iterationId: number \| null)` | — | The people and agents a task in this iteration can be given to; empty without an iteration. |
| `useTaskRowEdits` | `()` | — | Inline writes for a task row: a status move and a new assignee, each reversible from the toast. |
