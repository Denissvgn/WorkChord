# test_execution_working_dates Module

**Path:** `backend/tests/test_execution_working_dates.py`

## Description

Agent start decisions use the same declared working day as human work.

## Imports

| Source | Symbols |
|--------|---------|
| `app.main` | `app` |
| `app.models.agent` | `AgentActor` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.schemas.task` | `TaskCreate` |
| `app.schemas.task_domain` | `TaskActionRequest` |
| `app.services` | `agent_work_service`, `backlog_snapshot_service`, `work_metrics` |
| `app.services.task_domain_service` | `TaskDomainService` |
| `app.services.task_service` | `TaskService` |
| `app.utils` | `time` |
| `datetime` | `UTC`, `date`, `datetime`, `timedelta` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `tests.test_agent_runtime_recovery` | `seed_work` |
| `tests.test_delivery_scenarios` | `delivery_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_execution_working_dates.py"]
    n1 --> n0
    click n1 "../modules/test_execution_working_dates.md"
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
| `test_scheduled_agent_start_and_human_dates_reconcile` | *(async)* `(delivery_store, monkeypatch, zone, instant, future)` | `@pytest.mark.parametrize(('zone', 'instant', 'future'), [('Asia/Tokyo', '2026-01-20T23:30:00+00:00', False), ('America/Los_Angeles', '2026-01-21T00:30:00+00:00', False), ('America/Los_Angeles', '2026-03-08T09:59:00+00:00', False), ('America/Los_Angeles', '2026-03-09T06:30:00+00:00', False), ('Asia/Tokyo', '2026-01-20T23:30:00+00:00', True), ('America/Los_Angeles', '2026-01-21T00:30:00+00:00', True), ('America/Los_Angeles', '2026-03-09T06:30:00+00:00', True)])` | — |
