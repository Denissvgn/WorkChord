# AgentTeamRuntimeHandoff

**Location:** `frontend/src/types/agent.ts:753`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamRuntimeHandoff` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `schema_version` | `'agent-team-runtime-handoff-v1'` | *required* | — |
| `topology_key` | `string` | *required* | — |
| `topology_revision` | `number` | *required* | — |
| `actor_key` | `string` | *required* | — |
| `actor_id` | `number` | *required* | — |
| `role` | `AgentTeamRole` | *required* | — |
| `server_url` | `string` | *required* | — |
| `required_server_features` | `string[]` | *required* | — |
| `skill_package` | `AgentTeamSkillPackage` | *required* | — |
| `profile_key` | `string` | *required* | — |
| `profile_revision` | `string` | *required* | — |
| `model_binding_revisions` | `Record<string, number>` | *required* | — |
| `supported_assignment_modes` | `string[]` | *required* | — |
| `startup_instructions` | `string[]` | *required* | — |
| `credential_ref` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `actor_key`, `credential_ref`, `model_binding_revisions`, `profile_key`, `profile_revision`, `required_server_features`, `role`, `schema_version`, `server_url`, `skill_package`, `startup_instructions` |
