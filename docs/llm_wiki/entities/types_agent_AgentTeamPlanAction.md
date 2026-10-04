# AgentTeamPlanAction

**Location:** `frontend/src/types/agent.ts:701`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamPlanAction` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `action_id` | `string` | Yes | — | — |
| `action_digest` | `string` | Yes | — | — |
| `reconciliation_class` | `AgentTeamReconciliationClass` | Yes | — | — |
| `operation` | `string` | Yes | — | — |
| `actor_key` | `string` | Yes | — | — |
| `target_actor_id` | `number \| null` | Yes | — | — |
| `expected_object_revision` | `number \| null` | Yes | — | — |
| `expected_actor_revision` | `number \| null` | Yes | — | — |
| `before` | `Record<string, JsonValue> \| null` | Yes | — | — |
| `after` | `Record<string, JsonValue> \| null` | Yes | — | — |
| `preconditions` | `Record<string, JsonValue>` | Yes | — | — |
| `blocker_code` | `string \| null` | Yes | — | — |
| `requires_explicit_confirmation` | `boolean` | Yes | — | — |
| `authority_change` | `boolean` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamPlanAction (frontend/src/types/agent.ts)"]
    n1["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n1 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentTeamSetupMasterPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `action_digest`, `action_id`, `actor_key`, `after`, `authority_change`, `before`, `blocker_code`, `expected_actor_revision`, `expected_object_revision`, `operation`, `preconditions`, `reconciliation_class` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentTeamSetupMasterPage` | import | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) | — |
