# test_local_baseline Module

**Path:** `backend/tests/qualification/test_local_baseline.py`

## Description

Local measurements retain limits and cannot become formal certification.

## Imports

| Source | Symbols |
|--------|---------|
| `pytest` | `pytest` |
| `scripts.load.common` | `QualificationInputError` |
| `scripts.load.local_baseline` | `summarize` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 2 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `declaration` | `()` | — | — |
| `observation` | `(status = 200, code = None, latency = 10)` | — | — |
| `test_limits_are_observed_without_certification` | `()` | — | — |
| `test_unexpected_failures_and_budget_misses_remain_limitations` | `()` | — | — |
| `test_missing_or_mismatched_evidence_is_rejected` | `()` | — | — |
| `test_nonfinite_observation_is_rejected` | `()` | — | — |
