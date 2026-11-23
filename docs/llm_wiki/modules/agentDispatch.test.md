# agentDispatch.test Module

**Path:** `frontend/src/features/agentDispatch.test.ts`

## Description

_Auto-generated from `frontend/src/features/agentDispatch.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/resources.en` | `englishResources` | — | compiler-dependent |
| `./agentDispatch` | `AgentDispatchFacts` | Declaration | erased |
| `./agentDispatch` | `AGENT_DISPATCH_LABEL_KEY`, `agentDispatchState`, `taskAgentDispatchState` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/agentDispatch.test.ts"]
    n1["frontend/src/features/agentDispatch.ts"]
    n2["frontend/src/i18n/resources.en.ts"]
    n0 --> n1
    n0 --> n2
    click n0 "../modules/agentDispatch.test.md"
    click n1 "../modules/agentDispatch.md"
    click n2 "../modules/resources.en.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [agentDispatch](../modules/agentDispatch.md) |
| Outbound | [resources.en](../modules/resources.en.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
