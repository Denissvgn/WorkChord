# ConnectIssue

**Location:** `frontend/src/features/agentTeamSetup/connectAgent.ts:154`
**Kind:** Interface
**Bases:** —
**Module:** [connectAgent](../modules/connectAgent.md)

## Description

_Auto-generated from `ConnectIssue` in `frontend/src/features/agentTeamSetup/connectAgent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `step` | `number` | Yes | — | — |
| `reason` | `ConnectIssueReason` | Yes | — | — |
| `code` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ConnectIssue (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n1["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n2["connectIssue (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/connectAgent.md"
    click n1 "../modules/ConnectAgentSteps.md"
    click n2 "../modules/connectAgent.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [connectAgent](../modules/connectAgent.md) | 0 | `code`, `reason`, `step` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ConnectAgentSteps` | import | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) | — |
| `connectIssue` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
