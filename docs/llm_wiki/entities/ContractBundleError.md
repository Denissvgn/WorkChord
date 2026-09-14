# ContractBundleError

**Location:** `backend/app/autonomy/contracts/postgresql/loader.py:148`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [loader](../modules/loader.md)

## Description

_Auto-generated from `ContractBundleError` in `backend/app/autonomy/contracts/postgresql/loader.py`._

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ContractBundleError (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n1["ValueError"]
    n2["backend/app/autonomy/contracts/postgresql/__init__.py"]
    n3["_validate_machine_semantics (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n4["load_postgresql_contract_bundle (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n5["PostgreSQLContractBundle.member_json (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/loader.md"
    click n2 "../modules/postgresql___init__.md"
    click n3 "../modules/loader.md"
    click n4 "../modules/loader.md"
    click n5 "../modules/loader.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [loader](../modules/loader.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [postgresql___init__](../modules/postgresql___init__.md) | — |
| `_validate_machine_semantics` | call | [loader](../modules/loader.md) | 14 |
| `load_postgresql_contract_bundle` | call | [loader](../modules/loader.md) | 9 |
| `PostgreSQLContractBundle.member_json` | call | [loader](../modules/loader.md) | 2 |
