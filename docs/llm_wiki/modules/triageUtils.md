# triageUtils Module

**Path:** `frontend/src/components/triage/triageUtils.ts`

## Description

_Auto-generated from `frontend/src/components/triage/triageUtils.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../types/savedView` | `SavedView` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `../../types/triage` | `TriageItem`, `TriageItemStatus`, `TriageTaskDraftResponse` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AGENT_SOURCE_LABEL_KEYS`, `DuplicateActionDefaults`, `TriageLifecycleAction`, `flattenTasks`, `formatDraftDescription`, `formatSuggestionScore`, `getErrorMessage`, `isDueSnoozed`, `makeLookup`, `optionalText`, `parseOptionalNumber`, `statusClassName`, `statusLabelKeys`, `statusOptions`, `t`, `toLocalDateTimeInputValue`, `triageFiltersFromSavedView` |
| Constants | `t`, `statusOptions`, `statusLabelKeys`, `AGENT_SOURCE_LABEL_KEYS` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/triage/triageUtils.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/triageUtils.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (12) |
| Outbound | `frontend` (4) |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskListOption](../entities/TaskListOption.md) | Interface | 112 | — | — |
| [DuplicateActionDefaults](../entities/DuplicateActionDefaults.md) | Interface | 140 | — | — |
| [TriageLifecycleAction](../entities/TriageLifecycleAction.md) | Type alias | 132 | `'accept' \| 'decline' \| 'snooze' \| 'clarify' \| 'duplicate'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `statusClassName` | `(status: TriageItemStatus)` | — | — |
| `triageFiltersFromSavedView` | `(view: SavedView)` | — | — |
| `toLocalDateTimeInputValue` | `(date: Date)` | — | — |
| `optionalText` | `(value: string)` | — | — |
| `parseOptionalNumber` | `(value: string)` | — | — |
| `formatSuggestionScore` | `(score: number)` | — | — |
| `formatDraftDescription` | `(draft: TriageTaskDraftResponse)` | — | — |
| `isDueSnoozed` | `(item: TriageItem)` | — | — |
| `getErrorMessage` | `(error: unknown, fallback: string)` | — | — |
| `flattenTasks` | `(tasks: Task[] = [], depth = 0) -> TaskListOption[]` | — | — |
| `makeLookup` | `<T extends { id: number; name: string }>(items: T[])` | — | — |
