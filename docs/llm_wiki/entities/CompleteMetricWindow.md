# CompleteMetricWindow

**Location:** `backend/app/autonomy/providers.py:235`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [providers](../modules/providers.md)

## Description

_Auto-generated from `CompleteMetricWindow` in `backend/app/autonomy/providers.py`._

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `complete_window` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `metric_key` | `str` | `metric_key` | Yes | No | — | pattern=unknown (IDENTIFIER_PATTERN) | — | — |
| `starts_at` | `datetime` | `starts_at` | Yes | No | — | — | — | — |
| `ends_at` | `datetime` | `ends_at` | Yes | No | — | — | — | — |
| `expected_interval_seconds` | `int` | `expected_interval_seconds` | Yes | No | — | ge=1; le=3600 | — | — |
| `maximum_gap_seconds` | `int` | `maximum_gap_seconds` | Yes | No | — | ge=1; le=7200 | — | — |
| `samples` | `tuple[MetricSample, ...]` | `samples` | Yes | No | — | min_length=2; max_length=2000000 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `complete_window` | `() -> 'CompleteMetricWindow'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CompleteMetricWindow (backend/app/autonomy/providers.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["CompleteMetricWindow.complete_window (backend/app/autonomy/providers.py)"]
    n3["test_collector_windows_reject_metric_gaps_counter_resets_and_missing_replicas (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/providers.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/providers.md"
    click n3 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [providers](../modules/providers.md) | 1 | `ends_at`, `expected_interval_seconds`, `maximum_gap_seconds`, `metric_key`, `samples`, `starts_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CompleteMetricWindow.complete_window` | type_reference | [providers](../modules/providers.md) | — |
| `test_collector_windows_reject_metric_gaps_counter_resets_and_missing_replicas` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 2 |
