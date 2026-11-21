# RosterState

**Location:** `frontend/src/components/team/directoryModel.ts:13`
**Kind:** Type alias
**Bases:** —
**Module:** [directoryModel](../modules/directoryModel.md)
**Target:**

```typescript
'loaded' | 'loading' | 'unavailable'
```

## Description

Loaded: the roster was read in this request. Loading: the first read is under way. Unavailable: no key, or the read failed.

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RosterState (frontend/src/components/team/directoryModel.ts)"]
    n1["agentStatus (frontend/src/components/team/directoryModel.ts)"]
    n2["buildDirectory (frontend/src/components/team/directoryModel.ts)"]
    n3["frontend/src/components/team/TeamDirectory.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/directoryModel.md"
    click n1 "../modules/directoryModel.md"
    click n2 "../modules/directoryModel.md"
    click n3 "../modules/TeamDirectory.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [directoryModel](../modules/directoryModel.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentStatus` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `buildDirectory` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `TeamDirectory` | import | [TeamDirectory](../modules/TeamDirectory.md) | — |
