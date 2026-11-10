# RequestSourceLinkCreate

**Location:** `frontend/src/types/requestSource.ts:39`
**Kind:** Type alias
**Bases:** —
**Module:** [requestSource](../modules/requestSource.md)
**Target:**

```typescript
| {
        target_type: RequestSourceTargetType;
        target_id: number;
        request_source_id: number;
        request_source?: never;
    }
    | {
        target_type: RequestSourceTargetType;
        target_id: number;
        request_source: RequestSourceCreate;
        request_source_id?: never;
    }
```

## Description

_Auto-generated from `RequestSourceLinkCreate` in `frontend/src/types/requestSource.ts`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceLinkCreate (frontend/src/types/requestSource.ts)"]
    n1["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
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
| [requestSource](../modules/requestSource.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RequestSourceLinksPanel` | import | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) | — |
| `requestSourceService` | import | [requestSourceService](../modules/requestSourceService.md) | — |
