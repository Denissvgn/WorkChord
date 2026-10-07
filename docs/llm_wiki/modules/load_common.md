# common Module

**Path:** `scripts/load/common.py`

## Description

Shared, fail-closed contracts for the WorkChord load and qualification tools.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.autonomy.contracts.postgresql` | `ContractBundleError`, `PostgreSQLContractBundle`, `load_postgresql_contract_bundle` |
| `datetime` | `UTC`, `datetime` |
| `functools` | `lru_cache` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `typing` | `Any`, `Mapping` |
| `urllib.parse` | `urlsplit` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["scripts"]
    n2["scripts/load/common.py"]
    n1 --> n2
    n2 --> n0
    click n2 "../modules/load_common.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `scripts` (11) |
| Outbound | `backend` (1) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [QualificationInputError](../entities/QualificationInputError.md) | 34 | `ValueError` | A workload or evidence input is unsafe, stale, or incomplete. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `canonical_json_bytes` | `(value: Any) -> bytes` | — | — |
| `sha256_bytes` | `(value: bytes) -> str` | — | — |
| `sha256_file` | `(path: Path) -> str` | — | — |
| `seal_document` | `(payload: Mapping[str, Any]) -> dict[str, Any]` | — | — |
| `verify_document` | `(document: Mapping[str, Any]) -> str` | — | — |
| `read_json_object` | `(path: Path, *, sealed: bool = False) -> dict[str, Any]` | — | — |
| `contract_bundle` | `() -> PostgreSQLContractBundle` | `@lru_cache(maxsize=1)` | — |
| `contract_member_json` | `(member: str) -> dict[str, Any]` | — | — |
| `contract_member_sha256` | `(member: str) -> str` | — | — |
| `atomic_write_json` | `(path: Path, payload: Mapping[str, Any], *, sealed: bool = True, mode: int = 384) -> dict[str, Any]` | — | — |
| `capacity_contract` | `() -> dict[str, Any]` | — | — |
| `contract_sha256` | `() -> str` | — | — |
| `traffic_profile` | `(contract: Mapping[str, Any], profile_id: str) -> dict[str, Any]` | — | — |
| `utc_now_text` | `() -> str` | — | — |
| `authorized_base_url` | `(base_url: str, *, authorize_host: str, environment: str, production_authorization: str \| None, change_id: str \| None) -> str` | — | — |
