# RoutingDecision

**Location:** `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx:49`
**Kind:** Interface
**Bases:** —
**Module:** [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md)

## Description

A dry run that found tasks whose reviewer would no longer fit; nothing was written. It keeps the
versions it was read at, and what it was read for, so a changed selection or choice drops it.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `signature` | `string` | Yes | — | — |
| `items` | `RoutingChangeItem[]` | Yes | — | — |
| `canKeep` | `boolean` | Yes | — | — |
| `versions` | `TaskBulkOperationResponse['task_versions']` | Yes | — | — |
| `revisions` | `TaskBulkOperationResponse['input_revisions']` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) | 0 | `canKeep`, `items`, `revisions`, `signature`, `versions` |
