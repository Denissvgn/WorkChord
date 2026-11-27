# test_plan_import_dry_run Module

**Path:** `backend/tests/test_plan_import_dry_run.py`

## Description

A plan import is reviewed under planning scope and applied exactly as reviewed.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_server` |
| `app.authority` | `Authority` |
| `app.commands` | `app.commands`, `command_transaction` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor` |
| `app.models.identity` | `Principal`, `ProjectMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task`, `TaskDependency` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile` |
| `app.query_limits` | `app.query_limits` |
| `app.routers.export` | `export`, `export` |
| `app.services` | `import_review_service`, `import_review_service` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.import_review_service` | `compose_review_digest`, `capture_import_state`, `diff_import_state`, `dry_run_import` |
| `asyncio` | `asyncio` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select`, `text` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_plan_import_dry_run.py"]
    n1 --> n0
    click n1 "../modules/test_plan_import_dry_run.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `plan_file` | `(project_id, *, title = 'Reviewed parent')` | — | — |
| `upload` | `(data)` | — | — |
| `add_agents` | *(async)* `(factory, scenario)` | — | A PM of the first project, a PM of the other project only, and a planning reader. |
| `persisted` | *(async)* `(factory)` | — | — |
| `client` | `(**headers)` | — | — |
| `dry_run` | *(async)* `(key, path, data)` | — | — |
| `test_dry_run_returns_the_exact_changes_and_writes_nothing` | *(async)* `(managed_store)` | — | — |
| `test_apply_with_the_digest_makes_exactly_the_reviewed_changes` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `test_concurrent_edit_or_changed_file_refuses_the_reviewed_write` | *(async)* `(managed_store)` | — | — |
| `test_a_change_set_that_differs_from_the_review_is_rolled_back` | *(async)* `(managed_store)` | — | — |
| `test_callers_without_planning_scope_or_from_another_team_are_refused` | *(async)* `(managed_store)` | — | — |
| `test_new_iteration_is_reviewed_and_applied_and_a_write_without_digest_is_unchanged` | *(async)* `(managed_store)` | — | — |
| `test_mcp_preview_matches_the_rest_dry_run` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `refuse_planning_reservation` | `(monkeypatch)` | — | Fail the test if a refusal is decided only after the workspace planning reservation. |
| `test_oversized_previews_are_refused_before_any_reservation` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `test_profiles_the_caller_cannot_read_are_refused_alike` | *(async)* `(managed_store)` | — | — |
| `test_a_planner_may_name_people_already_on_a_team_it_can_read` | *(async)* `(managed_store)` | — | — |
| `test_a_dry_run_over_its_budget_is_refused_and_rolled_back` | *(async)* `(managed_store, monkeypatch)` | — | — |
| `test_the_elevated_writer_cannot_commit_and_needs_a_preview_root` | *(async)* `(managed_store, monkeypatch)` | — | — |
