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
    n3["frontend/src/pages/destinationEmptyStates.test.tsx"]
    n4["frontend/src/pages/TeamPage.transport.test.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/utils/agentAccess.ts"]
    n0 --> n2
    n0 --> n6
    n1 --> n5
    n1 --> n6
    n2 --> n6
    n3 --> n5
    n3 --> n6
    n4 --> n1
    n4 --> n5
    n4 --> n6
    n5 --> n6
    click n0 "../modules/AgentAccessPanel.md"
    click n1 "../modules/IdentityProvider.md"
    click n2 "../modules/useAgentAccess.md"
    click n3 "../modules/destinationEmptyStates.test.md"
    click n4 "../modules/TeamPage.transport.test.md"
    click n5 "../modules/api.md"
    click n6 "../modules/agentAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [useAgentAccess](../modules/useAgentAccess.md) |
| Inbound | [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md) |
| Inbound | [TeamPage.transport.test](../modules/TeamPage.transport.test.md) |
| Inbound | [api](../modules/api.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `getAgentApiKey` | `()` | — | — |
| `hasAgentApiKey` | `()` | — | — |
| `setAgentApiKey` | `(apiKey: string)` | — | — |
| `clearAgentApiKey` | `()` | — | — |
