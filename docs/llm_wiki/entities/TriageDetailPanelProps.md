# TriageDetailPanelProps

**Location:** `frontend/src/pages/TriagePage.tsx:1263`
**Kind:** Class
**Bases:** —
**Module:** [TriagePage](../modules/TriagePage.md)

## Description

_Auto-generated from `TriageDetailPanelProps` in `frontend/src/pages/TriagePage.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `item` | `TriageItem \| null` | Yes | — | — |
| `projectsById` | `Record<number, string>` | Yes | — | — |
| `iterationsById` | `Record<number, string>` | Yes | — | — |
| `canConvert` | `boolean` | Yes | — | — |
| `onAction` | `(action: TriageLifecycleAction, item: TriageItem) => void` | Yes | — | — |
| `onMarkSuggestion` | `(item: TriageItem, suggestion: TriageDuplicateSuggestion) => void` | Yes | — | — |
| `onConvert` | `(item: TriageItem) => void` | Yes | — | — |
| `onRequestLinksChanged` | `() => void` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TriagePage](../modules/TriagePage.md) | 0 | `canConvert`, `item`, `iterationsById`, `onAction`, `onConvert`, `onMarkSuggestion`, `onRequestLinksChanged`, `projectsById` |
