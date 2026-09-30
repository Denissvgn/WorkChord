# agentAccess Module

**Path:** `frontend/src/utils/agentAccess.ts`

## Description

_Auto-generated from `frontend/src/utils/agentAccess.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AGENT_API_KEY_CHANGED_EVENT`, `AGENT_API_KEY_STORAGE_KEY`, `clearAgentApiKey`, `getAgentApiKey`, `hasAgentApiKey`, `setAgentApiKey` |
| Constants | `AGENT_API_KEY_STORAGE_KEY`, `AGENT_API_KEY_CHANGED_EVENT` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n1["frontend/src/features/identity/IdentityProvider.tsx"]
    n2["frontend/src/hooks/useAgentAccess.ts"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/utils/agentAccess.ts"]
    n0 --> n2
    n0 --> n4
    n1 --> n3
    n1 --> n4
    n2 --> n4
    n3 --> n4
    click n0 "../modules/AgentAccessPanel.md"
    click n1 "../modules/IdentityProvider.md"
    click n2 "../modules/useAgentAccess.md"
    click n3 "../modules/api.md"
    click n4 "../modules/agentAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [useAgentAccess](../modules/useAgentAccess.md) |
| Inbound | [api](../modules/api.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `getAgentApiKey` | `()` | — | — |
| `hasAgentApiKey` | `()` | — | — |
| `setAgentApiKey` | `(apiKey: string)` | — | — |
| `clearAgentApiKey` | `()` | — | — |
