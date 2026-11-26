# DeliveryPrerequisiteHold

**Location:** `frontend/src/types/github.ts:92`
**Kind:** Interface
**Bases:** —
**Module:** [types_github](../modules/types_github.md)

## Description

Why a prerequisite keeps its task from starting: a case (not_accepted, open_pull_request, merged_on_other_branch, merge_branch_unknown, closed_unmerged or not_observed), the reason, the next owner (project manager, worker or reviewer) and the action that owner takes.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `case` | `string` | Yes | — | — |
| `reason` | `string` | Yes | — | — |
| `next_owner` | `string` | Yes | — | — |
| `next_action` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_github](../modules/types_github.md) | 0 | `case`, `next_action`, `next_owner`, `reason` |
