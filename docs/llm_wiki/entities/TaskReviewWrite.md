# TaskReviewWrite

**Location:** `backend/app/schemas/task_brief.py:84`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_brief](../modules/schemas_task_brief.md)

## Description

_Auto-generated from `TaskReviewWrite` in `backend/app/schemas/task_brief.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_version` | `int` | `expected_version` | Yes | No | — | ge=1 | — | — |
| `brief_revision` | `int` | `brief_revision` | Yes | No | — | ge=0 | — | — |
| `artifact_revision` | `int` | `artifact_revision` | Yes | No | — | ge=0 | — | — |
| `verdict` | `Literal['accept', 'reject']` | `verdict` | Yes | No | — | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | max_length=8000; min_length=1 | — | — |
| `evidence` | `str` | `evidence` | No | No | `''` | max_length=8000 | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReviewWrite (backend/app/schemas/task_brief.py)"]
    n1["BaseModel"]
    n2["review_task (backend/app/routers/task_domain.py)"]
    n3["TaskBriefService.review (backend/app/services/task_brief_service.py)"]
    n4["test_operator_acceptance_records_the_operator_only_with_an_accountable_override (backend/tests/test_acceptance_attribution.py)"]
    n5["test_signed_in_acceptance_records_the_signed_in_person (backend/tests/test_acceptance_attribution.py)"]
    n6["accepted_work (backend/tests/test_delivery_metrics.py)"]
    n7["test_backlog_manual_execution_independent_review_and_reopen (backend/tests/test_task_domain.py)"]
    n8["test_rework_requires_fresh_progress_and_preserves_prior_evidence (backend/tests/test_task_domain.py)"]
    n9["test_dependency_mutations_invalidate_evidence_without_erasing_history (backend/tests/test_task_domain_integrity.py)"]
    n10["test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact (backend/tests/test_task_postponement.py)"]
    n11["_accept (backend/tests/test_task_reactivation.py)"]
    n0 --> n1
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
    click n0 "../modules/schemas_task_brief.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/task_brief_service.md"
    click n4 "../modules/test_acceptance_attribution.md"
    click n5 "../modules/test_acceptance_attribution.md"
    click n6 "../modules/test_delivery_metrics.md"
    click n7 "../modules/test_task_domain.md"
    click n8 "../modules/test_task_domain.md"
    click n9 "../modules/test_task_domain_integrity.md"
    click n10 "../modules/test_task_postponement.md"
    click n11 "../modules/test_task_reactivation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_brief](../modules/schemas_task_brief.md) | 0 | `artifact_revision`, `brief_revision`, `evidence`, `expected_version`, `reason`, `verdict` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `review_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `TaskBriefService.review` | type_reference | [task_brief_service](../modules/task_brief_service.md) | — |
| `test_operator_acceptance_records_the_operator_only_with_an_accountable_override` | call | [test_acceptance_attribution](../modules/test_acceptance_attribution.md) | 2 |
| `test_signed_in_acceptance_records_the_signed_in_person` | call | [test_acceptance_attribution](../modules/test_acceptance_attribution.md) | 1 |
| `accepted_work` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 1 |
| `test_backlog_manual_execution_independent_review_and_reopen` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
| `test_rework_requires_fresh_progress_and_preserves_prior_evidence` | call | [test_task_domain](../modules/test_task_domain.md) | 2 |
| `test_dependency_mutations_invalidate_evidence_without_erasing_history` | call | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | 1 |
| `test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `_accept` | call | [test_task_reactivation](../modules/test_task_reactivation.md) | 1 |
