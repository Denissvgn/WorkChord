# AgentAccessPanel Module

**Path:** `frontend/src/components/settings/AgentAccessPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AgentAccessPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAgentAccess` | `useAgentAccess` | — | compiler-dependent |
| `../../services/agentService` | `agentService` | — | compiler-dependent |
| `../../utils/agentAccess` | `clearAgentApiKey`, `setAgentApiKey` | — | compiler-dependent |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `CheckCircle2`, `KeyRound`, `ShieldCheck`, `Trash2` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

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
