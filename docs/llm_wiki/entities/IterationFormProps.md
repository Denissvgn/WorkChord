# IterationFormProps

**Location:** `frontend/src/components/iteration/IterationForm.tsx:24`
**Kind:** Interface
**Bases:** —
**Module:** [IterationForm](../modules/IterationForm.md)

## Description

_Auto-generated from `IterationFormProps` in `frontend/src/components/iteration/IterationForm.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `initialData` | `Iteration` | No | — | — |
| `lockedProject` | <pre><code>&#123;&#10;        id&#58; number&#59;&#10;        name&#58; string&#59;&#10;    &#125;</code></pre> | No | — | — |
| `hideProjectScope` | `boolean` | No | — | — |
| `onSuccess` | `(iteration?: Iteration, iterations?: Iteration[]) => void` | Yes | — | — |
| `onCancel` | `() => void` | Yes | — | — |
| `onStateChange` | `(state: { dirty: boolean; pending: boolean }) => void` | No | — | — |

## Methods

*No declared methods.*

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
