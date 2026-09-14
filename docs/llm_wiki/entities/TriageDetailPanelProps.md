# TriageDetailPanelProps

**Location:** `frontend/src/pages/TriagePage.tsx:1246`
**Kind:** Class
**Bases:** —
**Module:** [TriagePage](../modules/TriagePage.md)

## Description

_Auto-generated from `TriageDetailPanelProps` in `frontend/src/pages/TriagePage.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `item` | `TriageItem \| null` | *required* | — |
| `projectsById` | `Record<number, string>` | *required* | — |
| `iterationsById` | `Record<number, string>` | *required* | — |
| `canConvert` | `boolean` | *required* | — |
| `onAction` | `(action: TriageLifecycleAction, item: TriageItem) => void` | *required* | — |
| `onMarkSuggestion` | `(item: TriageItem, suggestion: TriageDuplicateSuggestion) => void` | *required* | — |
| `onConvert` | `(item: TriageItem) => void` | *required* | — |
| `onRequestLinksChanged` | `() => void` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TriagePage](../modules/TriagePage.md) | 0 | `canConvert`, `item`, `iterationsById`, `onAction`, `onConvert`, `onMarkSuggestion`, `onRequestLinksChanged`, `projectsById` |
