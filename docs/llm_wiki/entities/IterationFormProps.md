# IterationFormProps

**Location:** `frontend/src/components/iteration/IterationForm.tsx:20`
**Kind:** Class
**Bases:** —
**Module:** [IterationForm](../modules/IterationForm.md)

## Description

_Auto-generated from `IterationFormProps` in `frontend/src/components/iteration/IterationForm.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `initialData` | `Iteration` | *required* | — |
| `lockedProject` | `{         id: number;         name: string;     }` | *required* | — |
| `hideProjectScope` | `boolean` | *required* | — |
| `onSuccess` | `(iteration?: Iteration, iterations?: Iteration[]) => void` | *required* | — |
| `onCancel` | `() => void` | *required* | — |
| `onStateChange` | `(state: { dirty: boolean; pending: boolean }) => void` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationFormProps (frontend/src/components/iteration/IterationForm.tsx)"]
    n1["IterationForm (frontend/src/components/iteration/IterationForm.tsx)"]
    n1 --> n0
    click n0 "../modules/IterationForm.md"
    click n1 "../modules/IterationForm.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [IterationForm](../modules/IterationForm.md) | 0 | `hideProjectScope`, `initialData`, `lockedProject`, `onCancel`, `onStateChange`, `onSuccess` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `IterationForm` | type_reference | [IterationForm](../modules/IterationForm.md) | — |
