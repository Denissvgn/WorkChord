# AgentTeamPlan

**Location:** `frontend/src/types/agent.ts:718`
**Kind:** Class
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

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamPlan (frontend/src/types/agent.ts)"]
    n1["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n2["frontend/src/services/agentService.test.ts"]
    n3["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentTeamSetupMasterPage.md"
    click n2 "../modules/agentService.test.md"
    click n3 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actions`, `blocker_codes`, `expected_topology_revision`, `manifest_digest`, `plan_digest`, `schema_version`, `topology_key` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentTeamSetupMasterPage` | import | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) | — |
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
