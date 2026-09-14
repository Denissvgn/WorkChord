# AgentAccessPanel Module

**Path:** `frontend/src/components/settings/AgentAccessPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AgentAccessPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useAgentAccess` | `useAgentAccess` |
| `../../services/agentService` | `agentService` |
| `../../utils/agentAccess` | `clearAgentApiKey`, `setAgentApiKey` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/protectedQueries` | `protectedQueryRetry` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `@tanstack/react-query` | `useQuery`, `useQueryClient` |
| `lucide-react` | `AlertTriangle`, `CheckCircle2`, `KeyRound`, `ShieldCheck`, `Trash2` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AgentAccessPanel` |
| Constants | `AGENT_QUERY_KEYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/settings/AgentAccessPanel.test.tsx"]
    n3["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n4["frontend/src/hooks/useAgentAccess.ts"]
    n5["frontend/src/pages/SettingsPage.tsx"]
    n6["frontend/src/services/agentService.ts"]
    n7["frontend/src/utils/agentAccess.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n9["frontend/src/utils/protectedQueries.ts"]
    n2 --> n3
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n7
    n5 --> n3
    n9 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/AgentAccessPanel.test.md"
    click n3 "../modules/AgentAccessPanel.md"
    click n4 "../modules/useAgentAccess.md"
    click n5 "../modules/SettingsPage.md"
    click n6 "../modules/agentService.md"
    click n7 "../modules/agentAccess.md"
    click n8 "../modules/apiError.md"
    click n9 "../modules/protectedQueries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentAccessPanel.test](../modules/AgentAccessPanel.test.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [useAgentAccess](../modules/useAgentAccess.md) |
| Outbound | [agentService](../modules/agentService.md) |
| Outbound | [agentAccess](../modules/agentAccess.md) |
| Outbound | [apiError](../modules/apiError.md) |
| Outbound | [protectedQueries](../modules/protectedQueries.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AgentAccessPanel` | `()` | — | — |
