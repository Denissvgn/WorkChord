# agentService.test Module

**Path:** `frontend/src/services/agentService.test.ts`

## Description

_Auto-generated from `frontend/src/services/agentService.test.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/agent` | `AgentCommandMetadata`, `AgentModelCatalogCreate`, `AgentTeamMaster`, `AgentTeamPlan`, `ModelAwareAgentTaskAssignmentCreate`, `TaskRoutingAssessmentCommand` |
| `./agentService` | `agentService` |
| `./api` | `api` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `mockedApi`, `metadata`, `expectedCommandConfig`, `catalogCommand`, `assessmentCommand`, `assignmentCommand`, `agentTeamMaster`, `agentTeamPlan` |
| Module calls | `mock`, `mockedApi = mocked`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/services/agentService.test.ts"]
    n1["frontend/src/services/agentService.ts"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/types/agent.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    click n0 "../modules/agentService.test.md"
    click n1 "../modules/agentService.md"
    click n2 "../modules/api.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [agentService](../modules/agentService.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
