# schedulingRulesService Module

**Path:** `frontend/src/services/schedulingRulesService.ts`

## Description

_Auto-generated from `frontend/src/services/schedulingRulesService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/schedulingRules` | `SchedulingRules`, `SchedulingRulesResponse` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `schedulingRulesService` |
| Constants | `schedulingRulesService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n1["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/schedulingRulesService.ts"]
    n4["frontend/src/types/schedulingRules.ts"]
    n0 --> n3
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n3 --> n4
    click n0 "../modules/AdminAccessPanel.md"
    click n1 "../modules/SchedulingRulesSettings.md"
    click n2 "../modules/api.md"
    click n3 "../modules/schedulingRulesService.md"
    click n4 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |
