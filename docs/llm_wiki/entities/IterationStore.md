# IterationStore

**Location:** `frontend/src/store/iterationStore.ts:13`
**Kind:** Interface
**Bases:** —
**Module:** [iterationStore](../modules/iterationStore.md)

## Description

The iteration-only view of the work scope, for pages that still set the iteration with
their own control. The scope store holds the value; useWorkScope puts it in the URL.
In a component the iteration in the URL comes first, so a page shows the scope of its
URL from its first render, before the shell has remembered it.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `selectedIterationId` | `number` | Yes | — | — |
| `isBacklog` | `boolean` | Yes | — | — |
| `setSelectedIterationId` | `(id: number) => void` | Yes | — | — |
| `chooseDefaultIteration` | `(iterations: readonly ScopeIterationRecord[]) => void` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [iterationStore](../modules/iterationStore.md) | 0 | `chooseDefaultIteration`, `isBacklog`, `selectedIterationId`, `setSelectedIterationId` |
