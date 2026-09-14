# AgentTeamMemberStatus

**Location:** `frontend/src/types/agent.ts:771`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamMemberStatus` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `actor_key` | `string` | *required* | — |
| `actor_id` | `number \| null` | *required* | — |
| `actor_name` | `string` | *required* | — |
| `display_name` | `string` | *required* | — |
| `role` | `AgentTeamRole` | *required* | — |
| `desired` | `boolean` | *required* | — |
| `configured` | `boolean` | *required* | — |
| `lifecycle_state` | `AgentTeamLifecycle` | *required* | — |
| `enabled` | `boolean` | *required* | — |
| `profile_key` | `string` | *required* | — |
| `profile_revision` | `string \| null` | *required* | — |
| `binding_revisions` | `Record<string, number>` | *required* | — |
| `skill_package` | `AgentTeamSkillPackage` | *required* | — |
| `package_acknowledged` | `boolean` | *required* | — |
| `credential_delivery_state` | `'pending' \| 'delivered' \| 'uncertain' \| 'not_required'` | *required* | — |
| `connection_state` | `'unobserved' \| 'observed' \| 'stale'` | *required* | — |
| `last_seen_at` | `string \| null` | *required* | — |
| `queued_assignments` | `number \| null` | *required* | — |
| `accepted_assignments` | `number \| null` | *required* | — |
| `running_runs` | `number \| null` | *required* | — |
| `runtime_ready` | `boolean` | *required* | — |
| `availability` | `'availability_unknown'` | *required* | — |
| `blocker_codes` | `string[]` | *required* | — |
| `handoff` | `AgentTeamRuntimeHandoff \| null` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `accepted_assignments`, `actor_id`, `actor_key`, `actor_name`, `availability`, `binding_revisions`, `blocker_codes`, `configured`, `connection_state`, `credential_delivery_state`, `desired`, `display_name` |
