# RequestSourceType

**Location:** `backend/app/schemas/request_source.py:20`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_request_source](../modules/schemas_request_source.md)

## Description

Supported lightweight request intake source types.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `CUSTOMER` | `'customer'` | — |
| `INTERNAL` | `'internal'` | — |
| `SUPPORT` | `'support'` | — |
| `EMAIL` | `'email'` | — |
| `WEB` | `'web'` | — |
| `IMPORT` | `'import'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceType (backend/app/schemas/request_source.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    click n0 "../modules/schemas_request_source.md"
    click n3 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_request_source](../modules/schemas_request_source.md) | 0 | `CUSTOMER`, `EMAIL`, `IMPORT`, `INTERNAL`, `SUPPORT`, `WEB` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
