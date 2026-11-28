# BranchDraft

**Location:** `frontend/src/components/tasks/DeliveryDependencies.tsx:23`
**Kind:** Interface
**Bases:** —
**Module:** [DeliveryDependencies](../modules/DeliveryDependencies.md)

## Description

A target-branch edit in progress for one prerequisite edge: the edge id, the typed text and the branch it started from. It is kept in session storage for at most a day and dropped when malformed, so a task view that remounts on a new version does not lose or misattribute an unsaved edit.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `edge` | `number` | Yes | — | — |
| `draft` | `string` | Yes | — | — |
| `base` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [DeliveryDependencies](../modules/DeliveryDependencies.md) | 0 | `base`, `draft`, `edge` |
