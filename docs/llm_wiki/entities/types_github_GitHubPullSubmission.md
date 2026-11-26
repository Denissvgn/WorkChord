# GitHubPullSubmission

**Location:** `frontend/src/types/github.ts:50`
**Kind:** Interface
**Bases:** —
**Module:** [types_github](../modules/types_github.md)

## Description

One commit a worker run submitted for a pull request, with its run, commit and pull request links, submission time and the verification reviews requested for it.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `run_id` | `number` | Yes | — | — |
| `commit_sha` | `string` | Yes | — | — |
| `commit_url` | `string \| null` | No | — | — |
| `pr_url` | `string \| null` | No | — | — |
| `submitted_at` | `string \| null` | No | — | — |
| `reviews` | `{ assignment_id: number; actor_id?: number \| null; state: string }[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_github](../modules/types_github.md) | 0 | `commit_sha`, `commit_url`, `pr_url`, `reviews`, `run_id`, `submitted_at` |
