# SavedViewUpdate

**Location:** `frontend/src/types/savedView.ts:52`
**Kind:** Class
**Bases:** —
**Module:** [savedView](../modules/savedView.md)

## Description

_Auto-generated from `SavedViewUpdate` in `frontend/src/types/savedView.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `view_type` | `SavedViewType` | *required* | — |
| `scope` | `Exclude<SavedViewScope, 'system'>` | *required* | — |
| `filters_json` | `Record<string, unknown>` | *required* | — |
| `sort_json` | `Record<string, unknown>` | *required* | — |
| `columns_json` | `Record<string, unknown>` | *required* | — |
| `schema_version` | `number` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewUpdate (frontend/src/types/savedView.ts)"]
    n1["frontend/src/services/savedViewService.ts"]
    n1 --> n0
    click n0 "../modules/savedView.md"
    click n1 "../modules/savedViewService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [savedView](../modules/savedView.md) | 0 | `columns_json`, `description`, `filters_json`, `name`, `schema_version`, `scope`, `sort_json`, `view_type` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `savedViewService` | import | [savedViewService](../modules/savedViewService.md) | — |
