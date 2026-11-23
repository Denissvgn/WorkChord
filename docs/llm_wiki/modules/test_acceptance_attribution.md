# test_acceptance_attribution Module

**Path:** `backend/tests/test_acceptance_attribution.py`

## Description

Every acceptance records who accepted it, so the work reads as accepted everywhere.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.models.identity` | `IdentitySubject`, `Principal`, `PrincipalProfileLink` |
| `app.models.task` | `Task` |
| `app.models.task_brief` | `TaskReviewRecord` |
| `app.models.team_member` | `TeamMemberProfile` |
| `app.schemas.task` | `TaskCreate` |
| `app.schemas.task_brief` | `TaskReviewWrite` |
| `app.schemas.task_domain` | `TaskActionRequest` |
| `app.services.delivery_metrics_service` | `DeliveryMetricsService` |
| `app.services.identity_service` | `LOCAL_PROFILE_ISSUER` |
| `app.services.task_brief_service` | `TaskBriefService` |
| `app.services.task_domain_service` | `TaskDomainService` |
| `app.services.task_service` | `TaskService` |
| `app.services.work_metrics` | `aggregate_metrics`, `task_signals` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client` |
| `tests.test_task_domain` | `human_context` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_acceptance_attribution.py"]
    n1 --> n0
    click n1 "../modules/test_acceptance_attribution.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `resolved_work` | *(async)* `(db, authority, project_id, owner_profile_id, title = 'Reviewed delivery')` | — | A resolved leaf task, executed under the given authority. |
| `accept` | `(task)` | — | — |
| `test_local_person_acceptance_records_the_acceptor_and_reads_accepted` | *(async)* `(delivery_store)` | — | — |
| `test_signed_in_acceptance_records_the_signed_in_person` | *(async)* `(delivery_store)` | — | — |
| `test_operator_acceptance_records_the_operator_only_with_an_accountable_override` | *(async)* `(delivery_store, override)` | `@pytest.mark.parametrize('override', [True, False])` | — |
