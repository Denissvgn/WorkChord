# test_mutation_versions Module

**Path:** `backend/tests/test_mutation_versions.py`

## Description

Version rollout rejects missing inputs without weakening identity or rollback.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.authority` | `Authority` |
| `app.commands` | `command_transaction` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.mcp_server` | `_structured_tool_error` |
| `app.models.agent` | `AgentActor`, `AgentActor` |
| `app.models.iteration` | `Iteration` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.task` | `Task` |
| `app.mutation_versions` | `MissingMutationRevision`, `require_mutation_revision` |
| `app.schemas.agent_planning` | `AgentPlanningCommandContext`, `AgentScheduleCommand` |
| `app.services.agent_planning_service` | `AgentPlanningService` |
| `app.services.agent_service` | `AgentConflictError` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_mutation_versions.py"]
    n1 --> n0
    click n1 "../modules/test_mutation_versions.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `strict_versions` | `(monkeypatch)` | `@pytest.fixture(autouse=True)` | — |
| `test_missing_task_version_is_structured_and_rolls_back` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_aggregate_revision_required_for_import_and_structural_writes` | *(async)* `(delivery_store)` | — | — |
| `test_dependency_bulk_preview_and_partial_move_versions` | *(async)* `(delivery_store)` | — | — |
| `test_text_context_is_a_revision_bound_editing_base` | *(async)* `(delivery_store)` | — | — |
| `test_header_revision_context_is_validated_without_auth_bypass` | *(async)* `(delivery_store)` | — | — |
| `test_operator_web_commands_still_require_versions_and_offline_repair_is_explicit` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_mcp_mutation_uses_the_same_missing_version_policy` | *(async)* `(delivery_store)` | — | — |
| `test_strict_agent_schedule_accepts_verified_task_versions_and_input_digest` | *(async)* `(delivery_store)` | — | — |
