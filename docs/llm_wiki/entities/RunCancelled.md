# RunCancelled

**Location:** `scripts/ci/ci_runtime.py:32`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [ci_runtime](../modules/ci_runtime.md)

## Description

A cancellation signal was observed. The runner persists cancellation and performs bounded cleanup instead of claiming a completed run.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RunCancelled (scripts/ci/ci_runtime.py)"]
    n1["RuntimeError"]
    n2["RunReceipt.check_budget (scripts/ci/ci_runtime.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/ci_runtime.md"
    click n2 "../modules/ci_runtime.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [ci_runtime](../modules/ci_runtime.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RunReceipt.check_budget` | call | [ci_runtime](../modules/ci_runtime.md) | 1 |
