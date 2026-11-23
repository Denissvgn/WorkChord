# ConvertTriageDrawerProps

**Location:** `frontend/src/components/triage/ConvertTriageDrawer.tsx:38`
**Kind:** Interface
**Bases:** —
**Module:** [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md)

## Description

_Auto-generated from `ConvertTriageDrawerProps` in `frontend/src/components/triage/ConvertTriageDrawer.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `item` | `TriageItem` | Yes | — | — |
| `projects` | `Project[]` | Yes | — | — |
| `iterations` | `Iteration[]` | Yes | — | — |
| `selectedIterationId` | `number` | Yes | — | — |
| `isSubmitting` | `boolean` | Yes | — | — |
| `error` | `string \| null` | No | — | — |
| `onSubmit` | `(payload: TriageConvertToTaskRequest) => void` | Yes | — | — |
| `onClose` | `() => void` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ConvertTriageDrawerProps (frontend/src/components/triage/ConvertTriageDrawer.tsx)"]
    n1["ConvertTriageDrawer (frontend/src/components/triage/ConvertTriageDrawer.tsx)"]
    n1 --> n0
    click n0 "../modules/ConvertTriageDrawer.md"
    click n1 "../modules/ConvertTriageDrawer.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) | 0 | `error`, `isSubmitting`, `item`, `iterations`, `onClose`, `onSubmit`, `projects`, `selectedIterationId` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ConvertTriageDrawer` | type_reference | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) | — |
