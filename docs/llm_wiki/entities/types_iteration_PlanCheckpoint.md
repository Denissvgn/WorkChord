# PlanCheckpoint

**Location:** `frontend/src/types/iteration.ts:103`
**Kind:** Interface
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `PlanCheckpoint` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `'iteration' \| 'team' \| 'work' \| 'blockers' \| 'schedule' \| 'review'` | Yes | — | — |
| `state` | `'done' \| 'warn' \| 'todo' \| 'blocked'` | Yes | — | — |
| `reason_codes` | `string[]` | Yes | — | — |
| `counts` | `Record<string, number>` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `counts`, `id`, `reason_codes`, `state` |
