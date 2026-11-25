# test_routing_preview_size Module

**Path:** `backend/tests/test_routing_preview_size.py`

## Description

The routed decision, its defaults, and its digest share one exact canonical byte budget.

The budget counts canonical packet bytes of the validated response. MCP framing and
HTTP headers are outside it, so raw transport sizes are not asserted here.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.models.agent` | `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentTaskAssignment` |
| `app.models.iteration` | `Iteration` |
| `app.schemas` | `agent_routing` |
| `app.schemas.agent_routing` | `AgentRoutingPreviewResponse` |
| `app.services` | `agent_routing_service` |
| `app.services.agent_routing_policy` | `MAX_ROUTING_CANDIDATES`, `MAX_ROUTING_EXCLUSIONS`, `MAX_ROUTING_PACKET_BYTES`, `canonical_routing_json_bytes` |
| `app.services.agent_routing_service` | `AgentRoutingService` |
| `app.services.agent_service` | `hash_api_key` |
| `app.utils.time` | `utc_now` |
| `json` | `json` |
| `pytest` | `pytest` |
| `tests.test_agent_routing_service` | `_assessment_command`, `_command_context` |
| `tests.test_agent_team_setup_qualification` | `provision_ready_topology`, `routing_base` |
| `tests.test_review_provenance` | `database_engines` |
| `tests.test_scoped_review_evidence` | `through` |
| `tests.test_team_pm_dispatch` | `db_session_factory` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_routing_preview_size.py"]
    n1 --> n0
    click n1 "../modules/test_routing_preview_size.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `restore_settings_cache` | `()` | `@pytest.fixture(autouse=True)` | — |
| `trimmed_rows` | `(preview)` | — | Rows the trim loop dropped, beyond the omissions the row bounds alone cause. |
| `test_preview_bounds_final_rest_and_mcp_decisions` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, actor_factory, monkeypatch, record_property, primary)` | `@database_engines`, `@pytest.mark.parametrize('primary', ['rest', 'mcp'])`, `@pytest.mark.usefixtures('deployed_agent_skill_release', 'qualified_model_aware_routing_test_context')` | — |
| `test_preview_trim_attempts_track_rows_dropped` | *(async)* `(db_session, db_session_factory, team_member_factory, task_factory, actor_factory, monkeypatch, record_property)` | `@database_engines`, `@pytest.mark.usefixtures('deployed_agent_skill_release', 'qualified_model_aware_routing_test_context')` | — |
