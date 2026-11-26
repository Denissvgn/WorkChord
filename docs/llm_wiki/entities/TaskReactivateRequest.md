# TaskReactivateRequest

**Location:** `backend/app/schemas/task_postponement.py:83`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task_postponement](../modules/schemas_task_postponement.md)

## Description

Return postponed work to planned, or to resolved when it was postponed after resolution.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `_reason` | field | reason | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_version` | `int` | `expected_version` | Yes | No | — | ge=1 | — | — |
| `reason` | `str` | `reason` | Yes | No | — | max_length=2000; min_length=1 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `_reason` | `(value: str) -> str` | `@field_validator('reason')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReactivateRequest (backend/app/schemas/task_postponement.py)"]
    n1["BaseModel"]
    n2["reactivate_task (backend/app/routers/task_domain.py)"]
    n3["test_cancel_and_reopen_keep_the_open_postponement (backend/tests/test_task_postponement.py)"]
    n4["test_deferred_and_postponed_are_independent (backend/tests/test_task_postponement.py)"]
    n5["test_only_a_pm_project_manager_or_operator_decides (backend/tests/test_task_postponement.py)"]
    n6["test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact (backend/tests/test_task_postponement.py)"]
    n7["test_summary_rolls_up_postponed_leaves (backend/tests/test_task_postponement.py)"]
    n8["test_work_an_open_postponement_waits_for_cannot_be_deleted (backend/tests/test_task_postponement.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/schemas_task_postponement.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/test_task_postponement.md"
    click n4 "../modules/test_task_postponement.md"
    click n5 "../modules/test_task_postponement.md"
    click n6 "../modules/test_task_postponement.md"
    click n7 "../modules/test_task_postponement.md"
    click n8 "../modules/test_task_postponement.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task_postponement](../modules/schemas_task_postponement.md) | 1 | `expected_version`, `reason` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `reactivate_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `test_cancel_and_reopen_keep_the_open_postponement` | call | [test_task_postponement](../modules/test_task_postponement.md) | 2 |
| `test_deferred_and_postponed_are_independent` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_only_a_pm_project_manager_or_operator_decides` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_summary_rolls_up_postponed_leaves` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_work_an_open_postponement_waits_for_cannot_be_deleted` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
