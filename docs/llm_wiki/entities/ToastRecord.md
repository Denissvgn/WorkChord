# ToastRecord

**Location:** `frontend/src/components/feedback/ToastProvider.tsx:13`
**Kind:** Interface
**Bases:** `Required<Pick<ToastInput, 'message' | 'tone' | 'durationMs'>>`
**Module:** [ToastProvider](../modules/ToastProvider.md)

## Description

_Auto-generated from `ToastRecord` in `frontend/src/components/feedback/ToastProvider.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `key` | `string` | Yes | — | — |
| `title` | `string` | No | — | — |
| `actionLabel` | `string` | No | — | — |
| `onAction` | `() => void \| Promise<void>` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ToastRecord (frontend/src/components/feedback/ToastProvider.tsx)"]
    n1["Required#60;Pick#60;ToastInput, 'message' | 'tone' | 'durationMs'#62;#62;"]
    n0 --> n1
    click n0 "../modules/ToastProvider.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [ToastProvider](../modules/ToastProvider.md) | 0 | `actionLabel`, `id`, `key`, `onAction`, `title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Required<Pick<ToastInput, 'message' \| 'tone' \| 'durationMs'>>` | — |
