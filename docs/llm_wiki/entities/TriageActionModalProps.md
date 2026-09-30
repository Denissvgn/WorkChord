# TriageActionModalProps

**Location:** `frontend/src/pages/TriagePage.tsx:410`
**Kind:** Class
**Bases:** —
**Module:** [TriagePage](../modules/TriagePage.md)

## Description

_Auto-generated from `TriageActionModalProps` in `frontend/src/pages/TriagePage.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `action` | `TriageLifecycleAction` | Yes | — | — |
| `item` | `TriageItem` | Yes | — | — |
| `allTriageItems` | `TriageItem[]` | Yes | — | — |
| `iterations` | `Iteration[]` | Yes | — | — |
| `selectedIterationId` | `number` | Yes | — | — |
| `defaultSnooze` | `string` | Yes | — | — |
| `defaultDuplicate` | `DuplicateActionDefaults` | No | — | — |
| `isSubmitting` | `boolean` | Yes | — | — |
| `error` | `string \| null` | No | — | — |
| `onSubmit` | `(payload: TriageActionRequest \| TriageSnoozeRequest \| TriageDuplicateRequest) => void` | Yes | — | — |
| `onClose` | `() => void` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TriagePage](../modules/TriagePage.md) | 0 | `action`, `allTriageItems`, `defaultDuplicate`, `defaultSnooze`, `error`, `isSubmitting`, `item`, `iterations`, `onClose`, `onSubmit`, `selectedIterationId` |
