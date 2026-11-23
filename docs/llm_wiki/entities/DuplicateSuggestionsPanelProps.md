# DuplicateSuggestionsPanelProps

**Location:** `frontend/src/components/triage/TriageSuggestions.tsx:16`
**Kind:** Interface
**Bases:** —
**Module:** [TriageSuggestions](../modules/TriageSuggestions.md)

## Description

_Auto-generated from `DuplicateSuggestionsPanelProps` in `frontend/src/components/triage/TriageSuggestions.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `suggestions` | `TriageDuplicateSuggestionsResponse` | No | — | — |
| `isLoading` | `boolean` | Yes | — | — |
| `isError` | `boolean` | Yes | — | — |
| `error` | `unknown` | No | — | — |
| `onRetry` | `() => void` | Yes | — | — |
| `projectsById` | `Record<number, string>` | Yes | — | — |
| `iterationsById` | `Record<number, string>` | Yes | — | — |
| `onMarkSuggestion` | `(suggestion: TriageDuplicateSuggestion) => void` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DuplicateSuggestionsPanelProps (frontend/src/components/triage/TriageSuggestions.tsx)"]
    n1["DuplicateSuggestionsPanel (frontend/src/components/triage/TriageSuggestions.tsx)"]
    n1 --> n0
    click n0 "../modules/TriageSuggestions.md"
    click n1 "../modules/TriageSuggestions.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TriageSuggestions](../modules/TriageSuggestions.md) | 0 | `error`, `isError`, `isLoading`, `iterationsById`, `onMarkSuggestion`, `onRetry`, `projectsById`, `suggestions` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `DuplicateSuggestionsPanel` | type_reference | [TriageSuggestions](../modules/TriageSuggestions.md) | — |
