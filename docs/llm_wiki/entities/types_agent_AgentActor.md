# AgentActor

**Location:** `frontend/src/types/agent.ts:100`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentActor` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `display_name` | `string` | Yes | — | — |
| `scopes` | `string[]` | Yes | — | — |
| `enabled` | `boolean` | Yes | — | — |
| `lifecycle_state` | `'active' \| 'onboarding' \| 'disabled'` | No | — | — |
| `role` | `AgentActorRole \| string` | Yes | — | — |
| `profile_id` | `number \| null` | Yes | — | — |
| `work_policy` | `string` | Yes | — | — |
| `max_parallel_work` | `number` | Yes | — | — |
| `queue_revision` | `number` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `last_seen_at` | `string \| null` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentActor (frontend/src/types/agent.ts)"]
    n1["AgentActorRosterItem (frontend/src/types/agent.ts)"]
    n2["frontend/src/components/settings/AgentModelAdministration.test.tsx"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/types_agent.md"
    click n2 "../modules/AgentModelAdministration.test.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `created_at`, `display_name`, `enabled`, `id`, `last_seen_at`, `lifecycle_state`, `max_parallel_work`, `name`, `profile_id`, `queue_revision`, `role`, `scopes` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `AgentActorRosterItem` | [types_agent](../modules/types_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentModelAdministration.test` | import | [AgentModelAdministration.test](../modules/AgentModelAdministration.test.md) | — |
