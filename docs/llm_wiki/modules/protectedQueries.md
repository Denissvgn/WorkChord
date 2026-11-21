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
    n3["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n4["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n5["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n6["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n7["frontend/src/components/tasks/PipelineTaskEvidence.tsx"]
    n8["frontend/src/components/tasks/usePipeline.ts"]
    n9["frontend/src/components/team/AgentModelAdministration.tsx"]
    n10["frontend/src/utils/apiError.ts"]
    n11["frontend/src/utils/protectedQueries.ts"]
    n0 --> n11
    n1 --> n0
    n1 --> n10
    n1 --> n11
    n2 --> n10
    n2 --> n11
    n3 --> n11
    n4 --> n11
    n5 --> n11
    n6 --> n11
    n7 --> n1
    n7 --> n10
    n7 --> n11
    n8 --> n10
    n8 --> n11
    n9 --> n10
    n9 --> n11
    n11 --> n10
    click n0 "../modules/AssignedAgentsSummary.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/AgentAccessPanel.md"
    click n3 "../modules/EmailSettingsPanel.md"
    click n4 "../modules/OutboundWebhooksPanel.md"
    click n5 "../modules/RuntimeConfigSettings.md"
    click n6 "../modules/SchedulingRulesSettings.md"
    click n7 "../modules/PipelineTaskEvidence.md"
    click n8 "../modules/usePipeline.md"
    click n9 "../modules/AgentModelAdministration.md"
    click n10 "../modules/apiError.md"
    click n11 "../modules/protectedQueries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AssignedAgentsSummary](../modules/AssignedAgentsSummary.md) |
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [PipelineTaskEvidence](../modules/PipelineTaskEvidence.md) |
| Inbound | [usePipeline](../modules/usePipeline.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Outbound | [apiError](../modules/apiError.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `protectedQueryRetry` | `(failureCount: number, error: unknown)` | — | — |
