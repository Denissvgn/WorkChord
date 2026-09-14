# ImmutableContractArchive

**Location:** `backend/app/autonomy/contracts/postgresql/loader.py:142`
**Kind:** Class
**Bases:** `Protocol`
**Module:** [loader](../modules/loader.md)

**Decorators:** `@runtime_checkable`

## Description

Read exact charter-pinned immutable input bytes by logical key/digest.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `get_exact` | `(*, logical_key: str, expected_sha256: str) -> bytes` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ImmutableContractArchive (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n1["Protocol"]
    n2["load_postgresql_contract_bundle (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/loader.md"
    click n2 "../modules/loader.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [loader](../modules/loader.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Protocol` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `load_postgresql_contract_bundle` | type_reference | [loader](../modules/loader.md) | — |
