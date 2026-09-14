# ServerAcceptanceError

**Location:** `backend/app/autonomy/server_acceptance.py:43`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md)

## Description

A sanitized, stable failure from one server-acceptance predicate.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code: str, *, cause: BaseException \| None = None) -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ServerAcceptanceError (backend/app/autonomy/server_acceptance.py)"]
    n1["RuntimeError"]
    n2["_probe_application (backend/app/autonomy/server_acceptance.py)"]
    n3["build_blocked_result (backend/app/autonomy/server_acceptance.py)"]
    n4["OpenBaoTransitClient._request (backend/app/autonomy/server_acceptance.py)"]
    n5["OpenBaoTransitClient.probe (backend/app/autonomy/server_acceptance.py)"]
    n6["OpenBaoTransitClient.sign_and_verify (backend/app/autonomy/server_acceptance.py)"]
    n7["run_server_acceptance (backend/app/autonomy/server_acceptance.py)"]
    n8["S3ObjectLockClient._request (backend/app/autonomy/server_acceptance.py)"]
    n9["S3ObjectLockClient.probe_ready (backend/app/autonomy/server_acceptance.py)"]
    n10["S3ObjectLockClient.store_locked (backend/app/autonomy/server_acceptance.py)"]
    n11["ValkeyCasClient.probe (backend/app/autonomy/server_acceptance.py)"]
    n12["_required (backend/app/cli/server_acceptance.py)"]
    n13["main (backend/app/cli/server_acceptance.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/autonomy_server_acceptance.md"
    click n2 "../modules/autonomy_server_acceptance.md"
    click n3 "../modules/autonomy_server_acceptance.md"
    click n4 "../modules/autonomy_server_acceptance.md"
    click n5 "../modules/autonomy_server_acceptance.md"
    click n6 "../modules/autonomy_server_acceptance.md"
    click n7 "../modules/autonomy_server_acceptance.md"
    click n8 "../modules/autonomy_server_acceptance.md"
    click n9 "../modules/autonomy_server_acceptance.md"
    click n10 "../modules/autonomy_server_acceptance.md"
    click n11 "../modules/autonomy_server_acceptance.md"
    click n12 "../modules/cli_server_acceptance.md"
    click n13 "../modules/cli_server_acceptance.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_probe_application` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 9 |
| `build_blocked_result` | type_reference | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | — |
| `OpenBaoTransitClient._request` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 2 |
| `OpenBaoTransitClient.probe` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 6 |
| `OpenBaoTransitClient.sign_and_verify` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 3 |
| `run_server_acceptance` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 7 |
| `S3ObjectLockClient._request` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 1 |
| `S3ObjectLockClient.probe_ready` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 2 |
| `S3ObjectLockClient.store_locked` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 9 |
| `ValkeyCasClient.probe` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 7 |
| `_required` | call | [cli_server_acceptance](../modules/cli_server_acceptance.md) | 1 |
| `main` | call | [cli_server_acceptance](../modules/cli_server_acceptance.md) | 2 |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
