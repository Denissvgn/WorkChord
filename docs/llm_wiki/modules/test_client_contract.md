# test_client_contract Module

**Path:** `backend/tests/test_client_contract.py`

## Description

Schema-derived compatibility, legacy payloads, and additive client behavior.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `Settings` |
| `app.schemas.agent` | `AgentActorCreate` |
| `app.schemas.agent_routing` | `AgentModelMutationReceipt` |
| `app.schemas.task` | `TaskStatusChange`, `TaskUpdate` |
| `app.schemas.triage` | `TriageConvertToTaskRequest` |
| `app.services.task_service` | `TaskVersionConflictError` |
| `copy` | `deepcopy` |
| `json` | `json` |
| `pathlib` | `Path` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `runpy` | `runpy` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/schemas/agent.py"]
    n2["backend/app/schemas/agent_routing.py"]
    n3["backend/app/schemas/task.py"]
    n4["backend/app/schemas/triage.py"]
    n5["backend/app/services/task_service.py"]
    n6["backend/tests/test_client_contract.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n4 --> n3
    n5 --> n3
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/config.md"
    click n1 "../modules/schemas_agent.md"
    click n2 "../modules/agent_routing.md"
    click n3 "../modules/schemas_task.md"
    click n4 "../modules/schemas_triage.md"
    click n5 "../modules/task_service.md"
    click n6 "../modules/test_client_contract.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [config](../modules/config.md) |
| Outbound | [schemas_agent](../modules/schemas_agent.md) |
| Outbound | [agent_routing](../modules/agent_routing.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [schemas_triage](../modules/schemas_triage.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_client_contract_is_current_and_deterministic` | `()` | — | — |
| `test_paged_readers_export_cursor_and_response_contracts` | `(path, schema_name, cursor_field)` | `@pytest.mark.parametrize('path,schema_name,cursor_field', PAGED_ROUTES)` | — |
| `test_missing_paged_reader_fails_contract_export` | `(monkeypatch, path, schema_name, cursor_field)` | `@pytest.mark.parametrize('path,schema_name,cursor_field', PAGED_ROUTES)` | — |
| `test_model_catalog_routes_accept_either_credential_header` | `(path, method, success_status, receipt)` | `@pytest.mark.parametrize('path,method,success_status,receipt', MODEL_CATALOG_ROUTES)` | — |
| `test_binding_and_preset_contracts_accept_either_credential_header` | `(path, method, status, response_schema)` | `@pytest.mark.parametrize('path,method,status,response_schema', [('/api/agent/model-bindings', 'get', '200', 'AgentModelBindingResponse'), ('/api/agent/model-bindings/{binding_id}', 'get', '200', 'AgentModelBindingResponse'), ('/api/agent/model-bindings', 'post', '201', 'AgentModelMutationReceipt'), ('/api/agent/model-bindings/{binding_id}', 'patch', '200', 'AgentModelMutationReceipt'), ('/api/agent/model-bindings/{binding_id}/disable', 'post', '200', 'AgentModelMutationReceipt'), ('/api/agent/profile-presets', 'get', '200', None)])` | — |
| `test_model_receipt_actor_is_an_agent_id_or_null_for_the_operator` | `()` | — | — |
| `test_supported_task_update_payloads` | `(payload)` | `@pytest.mark.parametrize('payload', [{'title': 'Legacy edit'}, {'title': 'Versioned edit', 'expected_version': 2}])` | — |
| `test_legacy_triage_target_and_additive_brief_input` | `()` | — | — |
| `test_unknown_actions_and_invalid_versions_do_not_succeed` | `()` | — | — |
| `test_conflict_fixture_uses_the_server_machine_code` | `()` | — | — |
| `test_public_skill_bundles_require_the_trusted_checksum` | `()` | — | — |
| `test_actor_provisioning_does_not_require_or_invent_runtime_binding` | `()` | — | — |
| `test_analytics_contract_adds_optional_scope_modes` | `(path)` | `@pytest.mark.parametrize('path', ['/api/tasks/delivery-metrics', '/api/tasks/execution-usage'])` | — |
| `test_metric_matches_exports_pagination_contract` | `()` | — | — |
| `test_planning_readiness_contract_includes_calendar_name` | `()` | — | — |
