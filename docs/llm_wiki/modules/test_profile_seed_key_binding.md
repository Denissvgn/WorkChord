# test_profile_seed_key_binding Module

**Path:** `backend/tests/test_profile_seed_key_binding.py`

## Description

Binding a seed key to an existing unkeyed planning profile keeps its history.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `PlanningConflict` |
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentTaskAssignment`, `AgentModelCatalogEntry` |
| `app.models.identity` | `CommandAudit` |
| `app.models.task` | `Task` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext` |
| `app.schemas.agent_team_setup` | `AgentTeamApplyRequest`, `AgentTeamMaster`, `AgentTeamPlanRequest` |
| `app.schemas.team` | `TeamMemberProfileSeedKeyBind` |
| `app.services.agent_team_setup_service` | `AgentTeamSetupService` |
| `app.services.team_service` | `TeamService` |
| `asyncio` | `asyncio` |
| `datetime` | `date` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_agent_team_setup` | `CapturingCredentialSink`, `example_payload`, `operator` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client`, `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_profile_seed_key_binding.py"]
    n1 --> n0
    click n1 "../modules/test_profile_seed_key_binding.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_unkeyed_agent` | *(async)* `(db, scenario, name, modes)` | — | — |
| `_snapshot` | *(async)* `(db, profile_ids)` | — | — |
| `test_bound_profile_is_connected_in_place_with_history_intact` | *(async)* `(delivery_store)` | — | — |
| `test_binding_refuses_keyed_duplicate_and_invalid_keys` | *(async)* `(delivery_store)` | — | — |
| `test_only_the_operator_can_bind_a_seed_key_over_http` | *(async)* `(managed_store)` | — | — |
| `_agent_attempt` | *(async)* `(factory, scenario, monkeypatch = None, role = 'pm')` | — | — |
| `test_agent_key_cannot_bind_a_seed_key_in_trusted_local_mode` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_agent_key_cannot_bind_a_seed_key_in_managed_mode` | *(async)* `(managed_store)` | — | — |
| `test_a_concurrent_binding_is_never_overwritten` | *(async)* `(delivery_store)` | — | — |
