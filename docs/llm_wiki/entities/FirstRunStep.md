# FirstRunStep

**Location:** `frontend/src/features/firstRun/firstRunSteps.ts:40`
**Kind:** Interface
**Bases:** —
**Module:** [firstRunSteps](../modules/firstRunSteps.md)

## Description

_Auto-generated from `FirstRunStep` in `frontend/src/features/firstRun/firstRunSteps.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `FirstRunStepId` | Yes | — | — |
| `number` | `number` | Yes | — | — |
| `done` | `boolean` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FirstRunStep (frontend/src/features/firstRun/firstRunSteps.ts)"]
    n1["firstRunSteps (frontend/src/features/firstRun/firstRunSteps.ts)"]
    n2["nextFirstRunStep (frontend/src/features/firstRun/firstRunSteps.ts)"]
    n3["frontend/src/features/firstRun/GetStartedPanel.tsx"]
    n4["frontend/src/features/firstRun/useFirstRunProgress.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/firstRunSteps.md"
    click n1 "../modules/firstRunSteps.md"
    click n2 "../modules/firstRunSteps.md"
    click n3 "../modules/GetStartedPanel.md"
    click n4 "../modules/useFirstRunProgress.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [firstRunSteps](../modules/firstRunSteps.md) | 0 | `done`, `id`, `number` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `firstRunSteps` | type_reference | [firstRunSteps](../modules/firstRunSteps.md) | — |
| `nextFirstRunStep` | type_reference | [firstRunSteps](../modules/firstRunSteps.md) | — |
| `GetStartedPanel` | import | [GetStartedPanel](../modules/GetStartedPanel.md) | — |
| `useFirstRunProgress` | import | [useFirstRunProgress](../modules/useFirstRunProgress.md) | — |
