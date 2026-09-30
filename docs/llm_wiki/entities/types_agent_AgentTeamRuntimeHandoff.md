# AgentTeamRuntimeHandoff

**Location:** `frontend/src/types/agent.ts:753`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamRuntimeHandoff` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `schema_version` | `'agent-team-runtime-handoff-v1'` | Yes | — | — |
| `topology_key` | `string` | Yes | — | — |
| `topology_revision` | `number` | Yes | — | — |
| `actor_key` | `string` | Yes | — | — |
| `actor_id` | `number` | Yes | — | — |
| `role` | `AgentTeamRole` | Yes | — | — |
| `server_url` | `string` | Yes | — | — |
| `required_server_features` | `string[]` | Yes | — | — |
| `skill_package` | `AgentTeamSkillPackage` | Yes | — | — |
| `profile_key` | `string` | Yes | — | — |
| `profile_revision` | `string` | Yes | — | — |
| `model_binding_revisions` | `Record<string, number>` | Yes | — | — |
| `supported_assignment_modes` | `string[]` | Yes | — | — |
| `startup_instructions` | `string[]` | Yes | — | — |
| `credential_ref` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `actor_key`, `credential_ref`, `model_binding_revisions`, `profile_key`, `profile_revision`, `required_server_features`, `role`, `schema_version`, `server_url`, `skill_package`, `startup_instructions` |
