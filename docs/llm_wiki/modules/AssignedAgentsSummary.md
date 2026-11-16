# AssignedAgentsSummary Module

**Path:** `frontend/src/components/agent/AssignedAgentsSummary.tsx`

## Description

Read-only list of the agents assigned to a task, read with the person's own access and shown in the routing panel when the browser holds no agent key: each agent's name, purpose, state and declared model, with loading, empty and retryable error states.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/agentService` | `agentService` | — | compiler-dependent |
| `../../types/agent` | `AgentAssignmentReadItem` | Declaration | erased |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AssignedAgentsSummary` |
| Constants | `KNOWN_PURPOSES`, `KNOWN_STATES` |
| Module calls | `KNOWN_PURPOSES = Set`, `KNOWN_STATES = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/agent/AssignedAgentsSummary.test.tsx"]
    n1["frontend/src/components/agent/AssignedAgentsSummary.tsx"]
    n2["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/services/agentService.ts"]
    n5["frontend/src/types/agent.ts"]
    n6["frontend/src/utils/protectedQueries.ts"]
    n0 --> n1
    n0 --> n5
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n4 --> n5
    click n0 "../modules/AssignedAgentsSummary.test.md"
    click n1 "../modules/AssignedAgentsSummary.md"
    click n2 "../modules/TaskRoutingPanel.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/agentService.md"
    click n5 "../modules/types_agent.md"
    click n6 "../modules/protectedQueries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AssignedAgentsSummary.test](../modules/AssignedAgentsSummary.test.md) |
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [agentService](../modules/agentService.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [protectedQueries](../modules/protectedQueries.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AssignedAgentsSummary` | `({ taskId }: { taskId: number })` | — | Who holds a task, read with the person's own access: no agent key, no routing evidence. |
