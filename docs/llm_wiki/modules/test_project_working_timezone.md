# test_project_working_timezone Module

**Path:** `backend/tests/test_project_working_timezone.py`

## Description

Declared project working zones survive transport and drive local work dates.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority` |
| `app.main` | `app` |
| `app.models.identity` | `WorkspaceMembership` |
| `app.schemas.project` | `ProjectCreate` |
| `app.schemas.task` | `TaskCreate` |
| `app.schemas.task_domain` | `TaskActionRequest` |
| `app.services` | `work_metrics` |
| `app.services.project_service` | `ProjectService` |
| `app.services.task_domain_service` | `TaskDomainService` |
| `app.services.task_service` | `TaskService` |
| `app.services.work_metrics` | `task_signals`, `working_today` |
| `app.utils` | `time` |
| `datetime` | `UTC`, `date`, `datetime` |
| `httpx` | `httpx` |
| `pytest` | `pytest` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store`, `client` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_project_working_timezone.py"]
    n1 --> n0
    click n1 "../modules/test_project_working_timezone.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_managed_creation_read_and_update_preserve_declared_zone` | *(async)* `(managed_store, zone)` | `@pytest.mark.parametrize('zone', ['Asia/Tokyo', 'America/Los_Angeles'])` | — |
| `test_project_zone_drives_actual_manual_day_and_metric_day` | *(async)* `(managed_store, monkeypatch, zone, expected)` | `@pytest.mark.parametrize(('zone', 'expected'), [('Asia/Tokyo', date(2026, 1, 21)), ('America/Los_Angeles', date(2026, 1, 20))])` | — |
