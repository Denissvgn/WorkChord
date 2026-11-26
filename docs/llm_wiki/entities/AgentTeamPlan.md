# AgentTeamPlan

**Location:** `frontend/src/types/agent.ts:748`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamPlan` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `schema_version` | `'agent-team-reconciliation-plan-v1'` | Yes | — | — |
| `topology_key` | `string` | Yes | — | — |
| `expected_topology_revision` | `number` | Yes | — | — |
| `manifest_digest` | `string` | Yes | — | — |
| `plan_digest` | `string` | Yes | — | — |
| `actions` | `AgentTeamPlanAction[]` | Yes | — | — |
| `blocker_codes` | `string[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamPlan (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n2["frontend/src/components/team/ConnectAgentSteps.test.tsx"]
    n3["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n4["frontend/src/services/agentService.test.ts"]
    n5["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentManifestWorkflow.md"
    click n2 "../modules/ConnectAgentSteps.test.md"
    click n3 "../modules/ConnectAgentSteps.md"
    click n4 "../modules/agentService.test.md"
    click n5 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actions`, `blocker_codes`, `expected_topology_revision`, `manifest_digest`, `plan_digest`, `schema_version`, `topology_key` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentManifestWorkflow` | import | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) | — |
| `ConnectAgentSteps.test` | import | [ConnectAgentSteps.test](../modules/ConnectAgentSteps.test.md) | — |
| `ConnectAgentSteps` | import | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) | — |
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
