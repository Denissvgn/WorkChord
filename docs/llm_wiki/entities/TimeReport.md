# TimeReport

**Location:** `frontend/src/services/timeEntryService.ts:10`
**Kind:** Interface
**Bases:** —
**Module:** [timeEntryService](../modules/timeEntryService.md)

## Description

_Auto-generated from `TimeReport` in `frontend/src/services/timeEntryService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `project_id` | `number` | Yes | — | — |
| `scope` | `'mine' \| 'project'` | Yes | — | — |
| `start` | `string` | Yes | — | — |
| `end` | `string` | Yes | — | — |
| `upper_id` | `number` | Yes | — | — |
| `has_more` | `boolean` | Yes | — | — |
| `next_after_id` | `number \| null` | Yes | — | — |
| `can_view_project_totals` | `boolean` | Yes | — | — |
| `items` | <pre><code>&#123; task&#95;id&#58; number&#59; task&#95;title&#58; string &#124; null&#59; recorded&#95;minutes&#58; number &#124; null&#59; entry&#95;count&#58; number&#59;&#10;        estimate&#95;hours&#58; number &#124; null&#59; estimate&#95;state&#58; &#39;known&#39; &#124; &#39;unknown&#39; &#124; &#39;unavailable&#39; &#125;&#91;&#93;</code></pre> | Yes | — | — |
| `totals` | <pre><code>&#123; task&#95;count&#58; number&#59; tasks&#95;with&#95;records&#58; number&#59; recorded&#95;minutes&#58; number &#124; null&#59;&#10;        project&#95;work&#95;minutes&#58; number &#124; null&#59; known&#95;estimate&#95;hours&#58; number &#124; null&#59; tasks&#95;with&#95;estimates&#58; number &#125;</code></pre> | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [timeEntryService](../modules/timeEntryService.md) | 0 | `can_view_project_totals`, `end`, `has_more`, `items`, `next_after_id`, `project_id`, `scope`, `start`, `totals`, `upper_id` |
