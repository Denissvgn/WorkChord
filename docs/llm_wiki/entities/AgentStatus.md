# AgentStatus

**Location:** `frontend/src/components/team/directoryModel.ts:16`
**Kind:** Interface
**Bases:** —
**Module:** [directoryModel](../modules/directoryModel.md)

## Description

What an agent's model and connection cells show.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `model` | `AgentModelBinding \| null \| undefined` | Yes | — | — |
| `connection` | `ConnectionState` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentStatus (frontend/src/components/team/directoryModel.ts)"]
    n1["agentStatus (frontend/src/components/team/directoryModel.ts)"]
    n2["statusKnown (frontend/src/components/team/directoryModel.ts)"]
    n3["frontend/src/components/team/TeamDirectory.tsx"]
    n4["frontend/src/components/team/TeamProfileManager.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/directoryModel.md"
    click n1 "../modules/directoryModel.md"
    click n2 "../modules/directoryModel.md"
    click n3 "../modules/TeamDirectory.md"
    click n4 "../modules/TeamProfileManager.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [directoryModel](../modules/directoryModel.md) | 0 | `connection`, `model` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentStatus` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `statusKnown` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `TeamDirectory` | import | [TeamDirectory](../modules/TeamDirectory.md) | — |
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
