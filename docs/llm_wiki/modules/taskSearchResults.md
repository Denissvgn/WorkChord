# taskSearchResults Module

**Path:** `frontend/src/components/tasks/taskSearchResults.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskSearchResults.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `TaskReference` | Declaration | erased |
| `i18next` | `TFunction` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `taskSearchResultCopy` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.tsx"]
    n1["frontend/src/components/tasks/taskSearchResults.ts"]
    n2["frontend/src/types/task.ts"]
    n0 --> n1
    n1 --> n2
    click n0 "../modules/CommandMenu.md"
    click n1 "../modules/taskSearchResults.md"
    click n2 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `taskSearchResultCopy` | `(task: TaskReference, t: TFunction)` | — | The same task identity and project context in every global search result. |
