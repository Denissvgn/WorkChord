# AgentTeamActionReceipt

**Location:** `frontend/src/types/agent.ts:724`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamActionReceipt` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `action_id` | `string` | *required* | — |
| `action_digest` | `string` | *required* | — |
| `reconciliation_class` | `AgentTeamReconciliationClass` | *required* | — |
| `operation` | `string` | *required* | — |
| `actor_key` | `string` | *required* | — |
| `status` | `'pending' \| 'applied' \| 'no_change' \| 'blocked'` | *required* | — |
| `target_actor_id` | `number \| null` | *required* | — |
| `before_revision` | `number \| null` | *required* | — |
| `after_revision` | `number \| null` | *required* | — |
| `blocker_code` | `string \| null` | *required* | — |
| `next_action` | `string \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `action_digest`, `action_id`, `actor_key`, `after_revision`, `before_revision`, `blocker_code`, `next_action`, `operation`, `reconciliation_class`, `status`, `target_actor_id` |
