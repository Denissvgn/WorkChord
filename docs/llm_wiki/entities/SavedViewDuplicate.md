# SavedViewDuplicate

**Location:** `frontend/src/types/savedView.ts:61`
**Kind:** Class
**Bases:** —
**Module:** [savedView](../modules/savedView.md)

## Description

_Auto-generated from `SavedViewDuplicate` in `frontend/src/types/savedView.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `scope` | `Exclude<SavedViewScope, 'system'>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewDuplicate (frontend/src/types/savedView.ts)"]
    n1["frontend/src/services/savedViewService.ts"]
    n1 --> n0
    click n0 "../modules/savedView.md"
    click n1 "../modules/savedViewService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [savedView](../modules/savedView.md) | 0 | `description`, `name`, `scope` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `savedViewService` | import | [savedViewService](../modules/savedViewService.md) | — |
