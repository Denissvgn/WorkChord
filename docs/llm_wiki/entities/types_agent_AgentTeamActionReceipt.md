# AgentTeamActionReceipt

**Location:** `frontend/src/types/agent.ts:728`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamActionReceipt` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `action_id` | `string` | Yes | — | — |
| `action_digest` | `string` | Yes | — | — |
| `reconciliation_class` | `AgentTeamReconciliationClass` | Yes | — | — |
| `operation` | `string` | Yes | — | — |
| `actor_key` | `string` | Yes | — | — |
| `status` | `'pending' \| 'applied' \| 'no_change' \| 'blocked'` | Yes | — | — |
| `target_actor_id` | `number \| null` | Yes | — | — |
| `before_revision` | `number \| null` | Yes | — | — |
| `after_revision` | `number \| null` | Yes | — | — |
| `blocker_code` | `string \| null` | Yes | — | — |
| `next_action` | `string \| null` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `action_digest`, `action_id`, `actor_key`, `after_revision`, `before_revision`, `blocker_code`, `next_action`, `operation`, `reconciliation_class`, `status`, `target_actor_id` |
