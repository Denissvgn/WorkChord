# Authority

**Location:** `backend/app/authority.py:24`
**Kind:** Class
**Bases:** —
**Module:** [authority](../modules/authority.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

_Auto-generated from `Authority` in `backend/app/authority.py`._

Managed authority combines a durable principal, workspace/project roles, and actor scopes. ORM reads constrain related records and writes require the relevant action; review is distinct from execution. Trusted-local collaboration is an explicit deployment mode. A read-only authority (a paired observer) is allowed reads only: `allows` refuses every other action and ORM writes under it are refused with no personal-record exemption. Narrow internal identity resolution and verified system integrations are server-owned boundaries, not caller-provided identity claims.

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
| `read_only` | `bool` | `False` | — |

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
    n5["test_local_person_acceptance_records_the_acceptor_and_reads_accepted (backend/tests/test_acceptance_attribution.py)"]
    n6["test_operator_acceptance_records_the_operator_only_with_an_accountable_override (backend/tests/test_acceptance_attribution.py)"]
    n7["test_signed_in_acceptance_records_the_signed_in_person (backend/tests/test_acceptance_attribution.py)"]
    n8["test_operator_rest_restore_reconciles_exact_allocation_membership (backend/tests/test_allocation_recovery.py)"]
    n9["test_scoped_manager_can_restore_another_eligible_person_without_profile_access (backend/tests/test_allocation_recovery.py)"]
    n10["test_workspace_reports_keep_authorization_and_recorded_backlog_scope (backend/tests/test_analytics_scopes.py)"]
    n11["test_hidden_person_protects_shared_master_without_leaking_their_identity (backend/tests/test_annual_calendar_coverage.py)"]
    n12["test_private_cross_year_commitment_warns_the_draft_and_holds_only_baseline_commit (backend/tests/test_annual_calendar_coverage.py)"]
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
    click n5 "../modules/test_acceptance_attribution.md"
    click n6 "../modules/test_acceptance_attribution.md"
    click n7 "../modules/test_acceptance_attribution.md"
    click n8 "../modules/test_allocation_recovery.md"
    click n9 "../modules/test_allocation_recovery.md"
    click n10 "../modules/test_analytics_scopes.md"
    click n11 "../modules/test_annual_calendar_coverage.md"
    click n12 "../modules/test_annual_calendar_coverage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [authority](../modules/authority.md) | 2 | `actor_id`, `actor_role`, `correlation_id`, `kind`, `local`, `principal_id`, `profile_id`, `projects`, `read_only`, `reason`, `review_override`, `scopes` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `resolve_http_identity` | call | [http_authority](../modules/http_authority.md) | 4 |
| `identity` | import | [routers_identity](../modules/routers_identity.md) | — |
| `bind_verified_system` | call | [identity_service](../modules/identity_service.md) | 1 |
| `IdentityService.context` | call | [identity_service](../modules/identity_service.md) | 1 |
| `test_local_person_acceptance_records_the_acceptor_and_reads_accepted` | call | [test_acceptance_attribution](../modules/test_acceptance_attribution.md) | 1 |
| `test_operator_acceptance_records_the_operator_only_with_an_accountable_override` | call | [test_acceptance_attribution](../modules/test_acceptance_attribution.md) | 1 |
| `test_signed_in_acceptance_records_the_signed_in_person` | call | [test_acceptance_attribution](../modules/test_acceptance_attribution.md) | 1 |
| `test_operator_rest_restore_reconciles_exact_allocation_membership` | call | [test_allocation_recovery](../modules/test_allocation_recovery.md) | 1 |
| `test_scoped_manager_can_restore_another_eligible_person_without_profile_access` | call | [test_allocation_recovery](../modules/test_allocation_recovery.md) | 1 |
| `test_workspace_reports_keep_authorization_and_recorded_backlog_scope` | call | [test_analytics_scopes](../modules/test_analytics_scopes.md) | 1 |
| `test_hidden_person_protects_shared_master_without_leaking_their_identity` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_private_cross_year_commitment_warns_the_draft_and_holds_only_baseline_commit` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |

> References: showing 12 of 52 logical references; 40 omitted by the 12-row generated summary limit.
