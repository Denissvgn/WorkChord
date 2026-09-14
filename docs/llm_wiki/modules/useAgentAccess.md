# useAgentAccess Module

**Path:** `frontend/src/hooks/useAgentAccess.ts`

## Description

_Auto-generated from `frontend/src/hooks/useAgentAccess.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../utils/agentAccess` | `AGENT_API_KEY_CHANGED_EVENT`, `hasAgentApiKey` |
| `react` | `useEffect`, `useState` |

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
    n2["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n3["frontend/src/hooks/useAgentAccess.ts"]
    n4["frontend/src/pages/AgentPipelinePage.tsx"]
    n5["frontend/src/utils/agentAccess.ts"]
    n0 --> n3
    n1 --> n3
    n1 --> n5
    n2 --> n3
    n3 --> n5
    n4 --> n0
    n4 --> n3
    click n0 "../modules/TaskRoutingPanel.md"
    click n1 "../modules/AgentAccessPanel.md"
    click n2 "../modules/AgentModelAdministration.md"
    click n3 "../modules/useAgentAccess.md"
    click n4 "../modules/AgentPipelinePage.md"
    click n5 "../modules/agentAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Outbound | [agentAccess](../modules/agentAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useAgentAccess` | `()` | — | — |
