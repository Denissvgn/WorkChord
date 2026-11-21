# DirectoryActor

**Location:** `frontend/src/components/team/directoryModel.ts:23`
**Kind:** Interface
**Bases:** —
**Module:** [directoryModel](../modules/directoryModel.md)

## Description

One agent actor as read from the roster: a profile can have several, for example a Worker and a Reviewer.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `actor` | `AgentActorRosterItem` | Yes | — | — |
| `role` | `DirectoryRole \| null` | Yes | — | — |
| `status` | `AgentStatus` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DirectoryActor (frontend/src/components/team/directoryModel.ts)"]
    n1["distinctRole (frontend/src/components/team/directoryModel.ts)"]
    n2["frontend/src/components/team/TeamDirectory.tsx"]
    n3["frontend/src/components/team/TeamProfileManager.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/directoryModel.md"
    click n1 "../modules/directoryModel.md"
    click n2 "../modules/TeamDirectory.md"
    click n3 "../modules/TeamProfileManager.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [directoryModel](../modules/directoryModel.md) | 0 | `actor`, `role`, `status` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `distinctRole` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `TeamDirectory` | import | [TeamDirectory](../modules/TeamDirectory.md) | — |
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
