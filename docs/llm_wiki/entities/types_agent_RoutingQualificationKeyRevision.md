# RoutingQualificationKeyRevision

**Location:** `frontend/src/types/agent.ts:330`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `RoutingQualificationKeyRevision` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `revision` | `number` | Yes | — | — |
| `action` | `'declare' \| 'revise' \| 'retire'` | Yes | — | — |
| `state` | `RoutingQualificationKeyState` | Yes | — | — |
| `label` | `string` | Yes | — | — |
| `description` | `string \| null` | Yes | — | — |
| `reason` | `string` | Yes | — | — |
| `actor_type` | `string` | Yes | — | — |
| `actor_id` | `number \| null` | Yes | — | — |
| `correlation_id` | `string \| null` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `action`, `actor_id`, `actor_type`, `correlation_id`, `created_at`, `description`, `label`, `reason`, `revision`, `state` |
