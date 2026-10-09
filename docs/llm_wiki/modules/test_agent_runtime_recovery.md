# test_agent_runtime_recovery Module

**Path:** `backend/tests/test_agent_runtime_recovery.py`

## Description

SQLite and PostgreSQL scenarios use new peer processes for begin, resume, renew, terminal submission, independent review and PM recovery. Lost-response replay is represented by retrying the exact logical request after process exit. Expired fences and changed criterion revisions reject stale evidence; provisional lineage remains blocked until an explicit supervised PM reassignment in routing-off mode. Timeout cleanup kills only the owned peer process.

Separate-process protocol simulation; no provider or pilot acceptance implied.

## Imports

| Source | Symbols |
|--------|---------|
| `app` | `mcp_agent_tools` |
| `app.main` | `app` |
| `app.models.agent` | `AgentActor`, `AgentTaskAssignment`, `AgentRun` |
| `app.models.task` | `Task` |
| `app.schemas.task` | `TaskCreate`, `TaskUpdate` |
| `app.schemas.task_brief` | `BriefCriterion`, `BriefWrite`, `TaskBrief` |
| `app.services.agent_service` | `hash_api_key` |
| `app.services.agent_work_service` | `AgentConflictError` |
| `app.services.task_brief_service` | `TaskBriefService` |
| `app.services.task_service` | `TaskService` |
| `app.utils.time` | `utc_now` |
| `asyncio` | `asyncio` |
| `datetime` | `date`, `timedelta` |
| `httpx` | `httpx` |
| `json` | `json` |
| `os` | `os` |
| `pytest` | `pytest` |
| `sqlalchemy` | `select` |
| `sys` | `sys` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_agent_runtime_recovery.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/test_agent_runtime_recovery.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (1) |
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `peer` | *(async)* `(factory, key, action, *, body = None, idempotency_key = None, **extra)` | — | — |
| `fence` | `(receipt)` | — | — |
| `seed_work` | *(async)* `(factory, scenario)` | — | — |
| `begin_next` | *(async)* `(factory, key, logical_key)` | — | — |
| `nest_assigned_work` | *(async)* `(factory, scenario, task_id)` | — | — |
| `test_ancestor_deferral_blocks_assigned_begin_over_rest_and_mcp` | *(async)* `(delivery_store)` | — | — |
| `test_ancestor_edit_invalidates_live_worker_renew_submit_and_begin_replay` | *(async)* `(delivery_store)` | — | — |
| `review_assignment` | *(async)* `(factory, task_id, actor_id)` | — | — |
| `supervised_refresh` | *(async)* `(factory, scenario, task_id)` | — | A worker pauses; an explicit PM replaces provisional lineage in off mode. |
| `test_process_restart_ambiguous_replay_and_independent_rework` | *(async)* `(delivery_store)` | — | — |
| `test_process_restart_expired_fence_requeue_and_failure` | *(async)* `(delivery_store)` | — | — |
| `test_changed_criterion_invalidates_restarted_worker_evidence` | *(async)* `(delivery_store)` | — | — |