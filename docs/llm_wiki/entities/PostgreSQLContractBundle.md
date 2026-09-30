# PostgreSQLContractBundle

**Location:** `backend/app/autonomy/contracts/postgresql/loader.py:153`
**Kind:** Class
**Bases:** —
**Module:** [loader](../modules/loader.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

_Auto-generated from `PostgreSQLContractBundle` in `backend/app/autonomy/contracts/postgresql/loader.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `manifest` | `PostgreSQLContractManifest` | *required* | — |
| `manifest_bytes` | `bytes` | *required* | — |
| `manifest_digest` | `str` | *required* | — |
| `members` | `dict[str, bytes]` | *required* | — |
| `archive_verified` | `bool` | *required* | — |
| `blocker_codes` | `tuple[str, ...]` | *required* | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `member_json` | `(path: str) -> object` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PostgreSQLContractBundle (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n1["backend/app/autonomy/contracts/postgresql/__init__.py"]
    n2["load_postgresql_contract_bundle (backend/app/autonomy/contracts/postgresql/loader.py)"]
    n3["evaluate_agent_preflight (backend/app/autonomy/preflight.py)"]
    n4["evaluate_status_amendment (backend/app/autonomy/status.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/loader.md"
    click n1 "../modules/postgresql___init__.md"
    click n2 "../modules/loader.md"
    click n3 "../modules/preflight.md"
    click n4 "../modules/status.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [loader](../modules/loader.md) | 1 | `archive_verified`, `blocker_codes`, `manifest`, `manifest_bytes`, `manifest_digest`, `members` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [postgresql___init__](../modules/postgresql___init__.md) | — |
| `load_postgresql_contract_bundle` | call | [loader](../modules/loader.md) | 1 |
| `load_postgresql_contract_bundle` | type_reference | [loader](../modules/loader.md) | — |
| `evaluate_agent_preflight` | type_reference | [preflight](../modules/preflight.md) | — |
| `evaluate_status_amendment` | type_reference | [status](../modules/status.md) | — |
