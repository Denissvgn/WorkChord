# RequestSource

**Location:** `frontend/src/types/requestSource.ts:4`
**Kind:** Class
**Bases:** —
**Module:** [requestSource](../modules/requestSource.md)

## Description

_Auto-generated from `RequestSource` in `frontend/src/types/requestSource.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `title` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `source_type` | `RequestSourceType` | *required* | — |
| `source_name` | `string \| null` | *required* | — |
| `source_url` | `string \| null` | *required* | — |
| `external_key` | `string \| null` | *required* | — |
| `priority_hint` | `number \| null` | *required* | — |
| `created_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSource (frontend/src/types/requestSource.ts)"]
    n1["RequestSourceLinksPanel (frontend/src/components/requestSources/RequestSourceLinksPanel.tsx)"]
    n2["frontend/src/services/requestSourceService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/requestSource.md"
    click n1 "../modules/RequestSourceLinksPanel.md"
    click n2 "../modules/requestSourceService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [requestSource](../modules/requestSource.md) | 0 | `created_at`, `description`, `external_key`, `id`, `priority_hint`, `source_name`, `source_type`, `source_url`, `title` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RequestSourceLinksPanel` | type_reference | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) | — |
| `requestSourceService` | import | [requestSourceService](../modules/requestSourceService.md) | — |
