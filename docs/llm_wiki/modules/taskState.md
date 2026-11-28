# taskState Module

**Path:** `frontend/src/utils/taskState.ts`

## Description

_Auto-generated from `frontend/src/utils/taskState.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/task` | `TaskDisplayedState`, `TaskStatus` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ALL_STATES`, `STOPPED_STATES`, `StoppedState`, `isEndedState`, `isStoppedState`, `stateOf` |
| Constants | `STOPPED_STATES`, `ALL_STATES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/utils/taskState.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/taskState.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (20) |
| Outbound | `frontend` (1) |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [StoppedState](../entities/StoppedState.md) | Type alias | 9 | `typeof STOPPED_STATES[number]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `stateOf` | `(task: { status: TaskStatus; displayed_state?: TaskDisplayedState \| string }) -> TaskDisplayedState` | — | What a task is shown as: the server's displayed state, or its stored status. |
| `isStoppedState` | `(state: string) -> state is StoppedState` | — | — |
| `isEndedState` | `(state: string)` | — | Canceled and superseded work has ended; postponed work is paused and comes back. |
