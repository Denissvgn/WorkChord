# SignedAgentPreflightReport

**Location:** `backend/app/autonomy/preflight.py:118`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [preflight](../modules/preflight.md)

## Description

_Auto-generated from `SignedAgentPreflightReport` in `backend/app/autonomy/preflight.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `report` | `AgentPreflightReport` | `report` | Yes | No | — | — | — | — |
| `signature` | `DetachedSignatureEnvelope` | `signature` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SignedAgentPreflightReport (backend/app/autonomy/preflight.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["sign_agent_preflight (backend/app/autonomy/preflight.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/preflight.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/preflight.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [preflight](../modules/preflight.md) | 0 | `report`, `signature` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `sign_agent_preflight` | call | [preflight](../modules/preflight.md) | 1 |
| `sign_agent_preflight` | type_reference | [preflight](../modules/preflight.md) | — |
