# test_postponement_agent_tools Module

**Path:** `backend/tests/test_postponement_agent_tools.py`

## Description

A PM agent postpones, reactivates and reads postponed work with exactly the REST authority.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_server` |
| `app.agent_contract` | `agent_contract_features` |
| `app.models.agent` | `AgentActor`, `TaskEvent` |
| `app.models.identity` | `Principal`, `ProjectMembership` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.server_features` | `SERVER_FEATURES` |
| `app.services.agent_readiness` | `DEFAULT_AGENT_CAPABILITY_SLUGS` |
| `app.services.agent_service` | `hash_api_key` |
| `app.utils.time` | `utc_now` |
| `contextlib` | `asynccontextmanager` |
| `datetime` | `timedelta` |
| `httpx` | `httpx` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client`, `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_postponement_agent_tools.py"]
    n1 --> n0
    click n1 "../modules/test_postponement_agent_tools.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_agent` | *(async)* `(db, key, name, *, role = 'pm', scopes = WRITE, memberships)` | — | — |
| `team` | *(async)* `(managed_store)` | `@pytest.fixture` | One PM manages the work; every other credential differs in exactly one way. |
| `_nothing` | *(async)* `()` | `@asynccontextmanager` | — |
| `transport_api` | *(async)* `(transport, factory, monkeypatch)` | `@asynccontextmanager` | Call one command through REST or MCP; a refusal returns the error text instead of the result. |
| `_later` | `(days = 30)` | — | — |
| `_postpone` | `(call, key, task_id, version, receipt)` | — | — |
| `_reactivate` | `(call, key, task_id, version, receipt)` | — | — |
| `_read` | `(call, key, task_id)` | — | — |
| `_state` | *(async)* `(factory, task_id)` | — | — |
| `test_new_tools_declare_their_inputs_and_features_and_no_owner_decision_tool` | *(async)* `()` | — | — |
| `test_pm_postpones_reads_each_requirement_and_reactivates` | *(async)* `(team, transport, monkeypatch)` | `@pytest.mark.parametrize('transport', ['rest', 'mcp'])` | — |
| `test_rest_and_mcp_return_the_same_record_shape` | *(async)* `(team, monkeypatch)` | — | — |
| `test_an_mcp_retry_with_the_same_key_replays_the_receipt` | *(async)* `(team, monkeypatch)` | — | — |
| `test_other_credentials_cannot_postpone_or_reactivate` | *(async)* `(team, transport, key, monkeypatch)` | `@pytest.mark.parametrize('transport', ['rest', 'mcp'])`, `@pytest.mark.parametrize('key', [OTHER_PM_KEY, VIEWER_KEY, READER_KEY, WORKER_KEY, VERIFIER_KEY])` | — |
| `test_reading_a_postponement_needs_read_access_to_the_project` | *(async)* `(team, transport, monkeypatch)` | `@pytest.mark.parametrize('transport', ['rest', 'mcp'])` | — |
| `_tool` | *(async)* `(factory, monkeypatch, name, **arguments)` | — | — |
| `_rows` | `(tree)` | — | — |
| `test_postponed_work_is_listed_filtered_and_never_queued` | *(async)* `(team, monkeypatch)` | — | — |
