# CloseoutContractError

**Location:** `scripts/ci/check_model_aware_routing_closeout.py:51`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md)

## Description

Raised when closure evidence is incomplete, stale, or overclaimed.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CloseoutContractError (scripts/ci/check_model_aware_routing_closeout.py)"]
    n1["RuntimeError"]
    n2["_evidence_path (scripts/ci/check_model_aware_routing_closeout.py)"]
    n3["_exact_ids (scripts/ci/check_model_aware_routing_closeout.py)"]
    n4["_load_json (scripts/ci/check_model_aware_routing_closeout.py)"]
    n5["_require_tracked (scripts/ci/check_model_aware_routing_closeout.py)"]
    n6["_validate_external_truth (scripts/ci/check_model_aware_routing_closeout.py)"]
    n7["_validate_master (scripts/ci/check_model_aware_routing_closeout.py)"]
    n8["_validate_versions (scripts/ci/check_model_aware_routing_closeout.py)"]
    n9["validate_closeout (scripts/ci/check_model_aware_routing_closeout.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/check_model_aware_routing_closeout.md"
    click n2 "../modules/check_model_aware_routing_closeout.md"
    click n3 "../modules/check_model_aware_routing_closeout.md"
    click n4 "../modules/check_model_aware_routing_closeout.md"
    click n5 "../modules/check_model_aware_routing_closeout.md"
    click n6 "../modules/check_model_aware_routing_closeout.md"
    click n7 "../modules/check_model_aware_routing_closeout.md"
    click n8 "../modules/check_model_aware_routing_closeout.md"
    click n9 "../modules/check_model_aware_routing_closeout.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_evidence_path` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 3 |
| `_exact_ids` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 7 |
| `_load_json` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 2 |
| `_require_tracked` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 1 |
| `_validate_external_truth` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 1 |
| `_validate_master` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 5 |
| `_validate_versions` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 9 |
| `validate_closeout` | call | [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md) | 2 |
