# TriageActionModalProps

**Location:** `frontend/src/pages/TriagePage.tsx:408`
**Kind:** Class
**Bases:** —
**Module:** [TriagePage](../modules/TriagePage.md)

## Description

_Auto-generated from `TriageActionModalProps` in `frontend/src/pages/TriagePage.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `action` | `TriageLifecycleAction` | *required* | — |
| `item` | `TriageItem` | *required* | — |
| `allTriageItems` | `TriageItem[]` | *required* | — |
| `iterations` | `Iteration[]` | *required* | — |
| `selectedIterationId` | `number` | *required* | — |
| `defaultSnooze` | `string` | *required* | — |
| `defaultDuplicate` | `DuplicateActionDefaults` | *required* | — |
| `isSubmitting` | `boolean` | *required* | — |
| `error` | `string \| null` | *required* | — |
| `onSubmit` | `(payload: TriageActionRequest \| TriageSnoozeRequest \| TriageDuplicateRequest) => void` | *required* | — |
| `onClose` | `() => void` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TriagePage](../modules/TriagePage.md) | 0 | `action`, `allTriageItems`, `defaultDuplicate`, `defaultSnooze`, `error`, `isSubmitting`, `item`, `iterations`, `onClose`, `onSubmit`, `selectedIterationId` |
