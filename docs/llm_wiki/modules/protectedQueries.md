# protectedQueries Module

**Path:** `frontend/src/utils/protectedQueries.ts`

## Description

_Auto-generated from `frontend/src/utils/protectedQueries.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./apiError` | `getApiErrorStatus` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `protectedQueryRetry` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/AssignedAgentsSummary.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n3["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n4["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n5["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n6["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n7["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n8["frontend/src/pages/AgentPipelinePage.tsx"]
    n9["frontend/src/utils/apiError.ts"]
    n10["frontend/src/utils/protectedQueries.ts"]
    n0 --> n10
    n1 --> n0
    n1 --> n9
    n1 --> n10
    n2 --> n9
    n2 --> n10
    n3 --> n9
    n3 --> n10
    n4 --> n10
    n5 --> n10
    n6 --> n10
    n7 --> n10
    n8 --> n1
    n8 --> n9
    n8 --> n10
    n10 --> n9
    click n0 "../modules/AssignedAgentsSummary.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/AgentAccessPanel.md"
    click n3 "../modules/AgentModelAdministration.md"
    click n4 "../modules/EmailSettingsPanel.md"
    click n5 "../modules/OutboundWebhooksPanel.md"
    click n6 "../modules/RuntimeConfigSettings.md"
    click n7 "../modules/SchedulingRulesSettings.md"
    click n8 "../modules/AgentPipelinePage.md"
    click n9 "../modules/apiError.md"
    click n10 "../modules/protectedQueries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AssignedAgentsSummary](../modules/AssignedAgentsSummary.md) |
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
