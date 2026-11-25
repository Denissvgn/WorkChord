# test_routing_preview_team_scope Module

**Path:** `backend/tests/test_routing_preview_team_scope.py`

## Description

A team-bound PM's routing preview carries only its own team's operational rows.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.schemas.agent` | `ModelAwareAgentTaskAssignmentCreate` |
| `app.schemas.agent_routing` | `AgentRoutingPreviewCreate` |
| `app.services` | `agent_routing_service` |
| `app.services.agent_routing_service` | `AgentRoutingConflictError`, `AgentRoutingService` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.agent_team_setup_service` | `AgentTeamSetupConflictError` |
| `app.services.agent_work_service` | `AgentWorkService` |
| `app.services.task_service` | `TaskService` |
| `app.utils.time` | `utc_now` |
| `json` | `json` |
| `pytest` | `pytest` |
| `tests.support.transactions` | `reload_session_fixture` |
| `tests.test_agent_routing_service` | `_command_context` |
| `tests.test_agent_routing_wave6_qualification` | `_assessment_command`, `_dispatch` |
| `tests.test_agent_team_setup_qualification` | `default_candidate`, `provision_ready_topology`, `routing_base` |
| `tests.test_review_provenance` | `database_engines` |
| `tests.test_scoped_review_evidence` | `through` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_routing_preview_team_scope.py"]
    n1 --> n0
    click n1 "../modules/test_routing_preview_team_scope.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (19) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `restore_settings_cache` | `()` | `@pytest.fixture(autouse=True)` | — |
| `rows` | `(preview)` | — | — |
| `pairs` | `(items)` | — | — |
| `test_team_pm_preview_excludes_other_teams_rows_on_rest_and_mcp` | *(async)* `(db_session, db_session_factory, profile_factory, actor_factory, team_member_factory, task_factory, monkeypatch)` | `@database_engines`, `@pytest.mark.usefixtures('deployed_agent_skill_release', 'qualified_model_aware_routing_test_context')` | — |
| `test_publisher_independence_from_out_of_team_implementer_is_unchanged` | *(async)* `(db_session, db_session_factory, profile_factory, actor_factory, team_member_factory, task_factory, monkeypatch, shared_publisher)` | `@database_engines`, `@pytest.mark.parametrize('shared_publisher', [True, False])`, `@pytest.mark.usefixtures('deployed_agent_skill_release', 'qualified_model_aware_routing_test_context')` | — |
