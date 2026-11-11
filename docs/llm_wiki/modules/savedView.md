# savedView Module

**Path:** `frontend/src/types/savedView.ts`

## Description

_Auto-generated from `frontend/src/types/savedView.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SavedView`, `SavedViewCreate`, `SavedViewDashboardCard`, `SavedViewDuplicate`, `SavedViewListParams`, `SavedViewScope`, `SavedViewType`, `SavedViewUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/types/savedView.ts"]
    n0 --> n1
    click n1 "../modules/savedView.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (13) |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SavedView](../entities/savedView_SavedView.md) | Interface | 4 | — | — |
| [SavedViewDashboardCard](../entities/SavedViewDashboardCard.md) | Interface | 24 | — | — |
| [SavedViewListParams](../entities/SavedViewListParams.md) | Interface | 37 | — | — |
| [SavedViewCreate](../entities/savedView_SavedViewCreate.md) | Interface | 41 | — | — |
| [SavedViewUpdate](../entities/savedView_SavedViewUpdate.md) | Interface | 52 | — | — |
| [SavedViewDuplicate](../entities/SavedViewDuplicate.md) | Interface | 63 | — | — |
| [SavedViewType](../entities/savedView_SavedViewType.md) | Type alias | 1 | `'tasks' \| 'projects' \| 'triage'` | — |
| [SavedViewScope](../entities/savedView_SavedViewScope.md) | Type alias | 2 | `'personal' \| 'shared' \| 'system'` | — |
