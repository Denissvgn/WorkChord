# executionUsageService Module

**Path:** `frontend/src/services/executionUsageService.ts`

## Description

_Auto-generated from `frontend/src/services/executionUsageService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/executionUsage` | `ExecutionUsageSummary` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `executionUsageService` |
| Constants | `executionUsageService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/analytics/ExecutionUsagePanel.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/executionUsageService.ts"]
    n3["frontend/src/types/executionUsage.ts"]
    n0 --> n2
    n2 --> n1
    n2 --> n3
    click n0 "../modules/ExecutionUsagePanel.md"
    click n1 "../modules/api.md"
    click n2 "../modules/executionUsageService.md"
    click n3 "../modules/executionUsage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ExecutionUsagePanel](../modules/ExecutionUsagePanel.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [executionUsage](../modules/executionUsage.md) |
