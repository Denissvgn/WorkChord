# useAgentAccess Module

**Path:** `frontend/src/hooks/useAgentAccess.ts`

## Description

_Auto-generated from `frontend/src/hooks/useAgentAccess.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../utils/agentAccess` | `AGENT_API_KEY_CHANGED_EVENT`, `hasAgentApiKey` | — | compiler-dependent |
| `react` | `useEffect`, `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useAgentAccess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n1["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n2["frontend/src/components/tasks/PipelineTaskEvidence.tsx"]
    n3["frontend/src/components/tasks/usePipeline.ts"]
    n4["frontend/src/components/team/AgentModelAdministration.tsx"]
    n5["frontend/src/components/team/TeamDirectory.tsx"]
    n6["frontend/src/hooks/useAgentAccess.ts"]
    n7["frontend/src/utils/agentAccess.ts"]
    n0 --> n6
    n1 --> n6
    n1 --> n7
    n2 --> n0
    n2 --> n6
    n3 --> n6
    n4 --> n6
    n5 --> n6
    n6 --> n7
    click n0 "../modules/TaskRoutingPanel.md"
    click n1 "../modules/AgentAccessPanel.md"
    click n2 "../modules/PipelineTaskEvidence.md"
    click n3 "../modules/usePipeline.md"
    click n4 "../modules/AgentModelAdministration.md"
    click n5 "../modules/TeamDirectory.md"
    click n6 "../modules/useAgentAccess.md"
    click n7 "../modules/agentAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [PipelineTaskEvidence](../modules/PipelineTaskEvidence.md) |
| Inbound | [usePipeline](../modules/usePipeline.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [TeamDirectory](../modules/TeamDirectory.md) |
| Outbound | [agentAccess](../modules/agentAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useAgentAccess` | `()` | — | — |
