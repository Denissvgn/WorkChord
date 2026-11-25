# AsyncBarrier

**Location:** `backend/tests/support/faults.py:45`
**Kind:** Class
**Bases:** —
**Module:** [faults](../modules/faults.md)

## Description

Reusable asyncio barrier for controlled concurrency interleavings.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(participants: int) -> None` | — | — |
| `wait` | *(async)* `() -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AsyncBarrier (backend/tests/support/faults.py)"]
    n1["test_a_catch_up_racing_the_closure_webhook_records_the_closure_once (backend/tests/database/test_github_closure_concurrency.py)"]
    n2["test_two_racing_catch_ups_record_the_closure_once (backend/tests/database/test_github_closure_concurrency.py)"]
    n3["test_postgresql_race_matrix_preserves_all_invariants (backend/tests/database/test_postgresql_concurrency.py)"]
    n4["backend/tests/support/__init__.py"]
    n5["test_async_barrier_controls_interleaving (backend/tests/test_database_harness.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/faults.md"
    click n1 "../modules/test_github_closure_concurrency.md"
    click n2 "../modules/test_github_closure_concurrency.md"
    click n3 "../modules/test_postgresql_concurrency.md"
    click n4 "../modules/support___init__.md"
    click n5 "../modules/test_database_harness.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [faults](../modules/faults.md) | 2 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_a_catch_up_racing_the_closure_webhook_records_the_closure_once` | call | [test_github_closure_concurrency](../modules/test_github_closure_concurrency.md) | 2 |
| `test_two_racing_catch_ups_record_the_closure_once` | call | [test_github_closure_concurrency](../modules/test_github_closure_concurrency.md) | 1 |
| `test_postgresql_race_matrix_preserves_all_invariants` | call | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) | 8 |
| `__init__` | import | [support___init__](../modules/support___init__.md) | — |
| `test_async_barrier_controls_interleaving` | call | [test_database_harness](../modules/test_database_harness.md) | 1 |
