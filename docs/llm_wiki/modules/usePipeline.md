# usePipeline Module

**Path:** `frontend/src/components/tasks/usePipeline.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/usePipeline.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAdminAccess` | `useAdminAccess`, `useKeylessReader` | — | compiler-dependent |
| `../../hooks/useAgentAccess` | `useAgentAccess` | — | compiler-dependent |
| `../../services/agentService` | `agentService` | — | compiler-dependent |
| `../../types/agent` | `AgentPipeline` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorStatus` | — | compiler-dependent |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useMemo` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `usePipeline` |
| Constants | `EMPTY_PIPELINE` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/assigneeDisplay.test.tsx"]
    n1["frontend/src/components/tasks/PipelineView.tsx"]
    n2["frontend/src/components/tasks/usePipeline.ts"]
    n3["frontend/src/hooks/useAdminAccess.ts"]
    n4["frontend/src/hooks/useAgentAccess.ts"]
    n5["frontend/src/pages/OverviewPage.tsx"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/services/agentService.ts"]
    n8["frontend/src/types/agent.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n10["frontend/src/utils/protectedQueries.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n8
    n1 --> n2
    n2 --> n3
    n2 --> n4
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n5 --> n2
    n5 --> n9
    n6 --> n1
    n6 --> n2
    n7 --> n8
    n10 --> n9
    click n0 "../modules/assigneeDisplay.test.md"
    click n1 "../modules/PipelineView.md"
    click n2 "../modules/usePipeline.md"
    click n3 "../modules/useAdminAccess.md"
    click n4 "../modules/useAgentAccess.md"
    click n5 "../modules/OverviewPage.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/agentService.md"
    click n8 "../modules/types_agent.md"
    click n9 "../modules/apiError.md"
    click n10 "../modules/protectedQueries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [assigneeDisplay.test](../modules/assigneeDisplay.test.md) |
| Inbound | [PipelineView](../modules/PipelineView.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Outbound | [useAgentAccess](../modules/useAgentAccess.md) |
| Outbound | [agentService](../modules/agentService.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [apiError](../modules/apiError.md) |
| Outbound | [protectedQueries](../modules/protectedQueries.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `usePipeline` | `(enabled: boolean)` | — | — |
