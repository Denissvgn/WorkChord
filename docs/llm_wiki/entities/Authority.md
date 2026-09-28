# Authority

**Location:** `backend/app/authority.py:24`
**Kind:** Class
**Bases:** —
**Module:** [authority](../modules/authority.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

_Auto-generated from `Authority` in `backend/app/authority.py`._

Managed authority combines a durable principal, workspace/project roles, and actor scopes. ORM reads constrain related records and writes require the relevant action; review is distinct from execution. Trusted-local collaboration is an explicit deployment mode. Narrow internal identity resolution and verified system integrations are server-owned boundaries, not caller-provided identity claims.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `principal_id` | `int \| None` | *required* | — |
| `kind` | `str` | *required* | — |
| `workspace_role` | `str \| None` | `None` | — |
| `projects` | `dict[int, str]` | `field(default_factory=dict)` | — |
| `actor_id` | `int \| None` | `None` | — |
| `actor_role` | `str \| None` | `None` | — |
| `session_id` | `int \| None` | `None` | — |
| `profile_id` | `int \| None` | `None` | — |
| `source` | `str` | `'rest'` | — |
| `correlation_id` | `str` | `field(default_factory=lambda: uuid4().hex)` | — |
| `reason` | `str \| None` | `None` | — |
| `review_override` | `bool` | `False` | — |
| `local` | `bool` | `False` | — |
| `scopes` | `frozenset[str]` | `frozenset()` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `operator` | `()` | `@property` | — |
| `allows` | `(project_id, action = 'read')` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Authority (backend/app/authority.py)"]
    n1["resolve_http_identity (backend/app/http_authority.py)"]
    n2["backend/app/routers/identity.py"]
    n3["bind_verified_system (backend/app/services/identity_service.py)"]
    n4["IdentityService.context (backend/app/services/identity_service.py)"]
    n5["test_worker_bulk_sql_cannot_bypass_review_authority (backend/tests/test_managed_authority.py)"]
    n6["human_context (backend/tests/test_task_domain.py)"]
    n7["test_backlog_manual_execution_independent_review_and_reopen (backend/tests/test_task_domain.py)"]
    n8["test_managed_assigned_submission_and_independent_rework (backend/tests/test_task_domain.py)"]
    n9["test_rework_requires_fresh_progress_and_preserves_prior_evidence (backend/tests/test_task_domain.py)"]
    n10["test_blocked_metrics_do_not_hide_inaccessible_prerequisites (backend/tests/test_task_domain_integrity.py)"]
    n11["test_dependency_mutations_invalidate_evidence_without_erasing_history (backend/tests/test_task_domain_integrity.py)"]
    n12["test_repair_is_dry_by_default_and_does_not_invent_acceptance (backend/tests/test_work_correctness.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/authority.md"
    click n1 "../modules/http_authority.md"
    click n2 "../modules/routers_identity.md"
    click n3 "../modules/identity_service.md"
    click n4 "../modules/identity_service.md"
    click n5 "../modules/test_managed_authority.md"
    click n6 "../modules/test_task_domain.md"
    click n7 "../modules/test_task_domain.md"
    click n8 "../modules/test_task_domain.md"
    click n9 "../modules/test_task_domain.md"
    click n10 "../modules/test_task_domain_integrity.md"
    click n11 "../modules/test_task_domain_integrity.md"
    click n12 "../modules/test_work_correctness.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [authority](../modules/authority.md) | 2 | `actor_id`, `actor_role`, `correlation_id`, `kind`, `local`, `principal_id`, `profile_id`, `projects`, `reason`, `review_override`, `scopes`, `session_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `resolve_http_identity` | call | [http_authority](../modules/http_authority.md) | 3 |
| `identity` | import | [routers_identity](../modules/routers_identity.md) | — |
| `bind_verified_system` | call | [identity_service](../modules/identity_service.md) | 1 |
| `IdentityService.context` | call | [identity_service](../modules/identity_service.md) | 1 |
| `test_worker_bulk_sql_cannot_bypass_review_authority` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |
| `human_context` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
| `test_backlog_manual_execution_independent_review_and_reopen` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
| `test_managed_assigned_submission_and_independent_rework` | call | [test_task_domain](../modules/test_task_domain.md) | 2 |
| `test_rework_requires_fresh_progress_and_preserves_prior_evidence` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
| `test_blocked_metrics_do_not_hide_inaccessible_prerequisites` | call | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | 1 |
| `test_dependency_mutations_invalidate_evidence_without_erasing_history` | call | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | 1 |
| `test_repair_is_dry_by_default_and_does_not_invent_acceptance` | call | [test_work_correctness](../modules/test_work_correctness.md) | 1 |
