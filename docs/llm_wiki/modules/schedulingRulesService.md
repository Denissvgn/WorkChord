# schedulingRulesService Module

**Path:** `frontend/src/services/schedulingRulesService.ts`

## Description

_Auto-generated from `frontend/src/services/schedulingRulesService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/schedulingRules` | `SchedulingRules`, `SchedulingRulesResponse` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `schedulingRulesService` |
| Constants | `schedulingRulesService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/schedulingRulesService.ts"]
    n3["frontend/src/types/schedulingRules.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/SchedulingRulesSettings.md"
    click n1 "../modules/api.md"
    click n2 "../modules/schedulingRulesService.md"
    click n3 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |
