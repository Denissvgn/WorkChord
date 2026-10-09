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
| `test_boundary_code_requires_its_contracted_status` | `(status)` | `@pytest.mark.parametrize('status', [200, 204, 400, 403, 404, 429, 500, 503])` | — |
| `test_success_and_boundary_responses_require_consistent_codes` | `(status, code)` | `@pytest.mark.parametrize('status,code', [(200, 'other_error'), (413, None), (413, 'other_error')])` | — |
| `test_ordinary_success_passes_and_undeclared_boundary_is_unexpected` | `()` | — | — |
| `test_malformed_http_status_is_rejected` | `(status)` | `@pytest.mark.parametrize('status', [None, True, 200.0, '200', 99, 600])` | — |
| `test_missing_or_mismatched_evidence_is_rejected` | `()` | — | — |
| `test_nonfinite_observation_is_rejected` | `()` | — | — |
| `test_frozen_operation_coverage_cannot_omit_slow_or_missing_reads` | `()` | — | — |
| `test_duplicate_client_cannot_stand_in_for_declared_concurrency` | `()` | — | — |
