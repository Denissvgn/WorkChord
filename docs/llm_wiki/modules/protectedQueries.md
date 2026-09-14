# protectedQueries Module

**Path:** `frontend/src/utils/protectedQueries.ts`

## Description

_Auto-generated from `frontend/src/utils/protectedQueries.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./apiError` | `getApiErrorStatus` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `protectedQueryRetry` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n1["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n2["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n3["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n4["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n5["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n6["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n7["frontend/src/pages/AgentPipelinePage.tsx"]
    n8["frontend/src/utils/apiError.ts"]
    n9["frontend/src/utils/protectedQueries.ts"]
    n0 --> n8
    n0 --> n9
    n1 --> n8
    n1 --> n9
    n2 --> n8
    n2 --> n9
    n3 --> n9
    n4 --> n9
    n5 --> n9
    n6 --> n9
    n7 --> n0
    n7 --> n8
    n7 --> n9
    n9 --> n8
    click n0 "../modules/TaskRoutingPanel.md"
    click n1 "../modules/AgentAccessPanel.md"
    click n2 "../modules/AgentModelAdministration.md"
    click n3 "../modules/EmailSettingsPanel.md"
    click n4 "../modules/OutboundWebhooksPanel.md"
    click n5 "../modules/RuntimeConfigSettings.md"
    click n6 "../modules/SchedulingRulesSettings.md"
    click n7 "../modules/AgentPipelinePage.md"
    click n8 "../modules/apiError.md"
    click n9 "../modules/protectedQueries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Outbound | [apiError](../modules/apiError.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `protectedQueryRetry` | `(failureCount: number, error: unknown)` | — | — |
