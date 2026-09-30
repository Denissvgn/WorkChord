# sql_semantics Module

**Path:** `backend/app/sql_semantics.py`

## Description

Cross-dialect text matching rules for the supported SQLite/PostgreSQL window.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `sqlalchemy` | `func` |
| `typing` | `Any` |
| `unicodedata` | `unicodedata` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/label_service.py"]
    n1["backend/app/services/project_service.py"]
    n2["backend/app/services/request_source_service.py"]
    n3["backend/app/services/team_service.py"]
    n4["backend/app/services/triage_service.py"]
    n5["backend/app/sql_semantics.py"]
    n6["backend/tests/database/test_postgresql_concurrency.py"]
    n7["backend/tests/database/test_runtime_policy.py"]
    n0 --> n5
    n1 --> n2
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n2
    n4 --> n5
    n6 --> n5
    n7 --> n5
    click n0 "../modules/label_service.md"
    click n1 "../modules/project_service.md"
    click n2 "../modules/request_source_service.md"
    click n3 "../modules/team_service.md"
    click n4 "../modules/triage_service.md"
    click n5 "../modules/sql_semantics.md"
    click n6 "../modules/test_postgresql_concurrency.md"
    click n7 "../modules/test_runtime_policy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [label_service](../modules/label_service.md) |
| Inbound | [project_service](../modules/project_service.md) |
| Inbound | [request_source_service](../modules/request_source_service.md) |
| Inbound | [team_service](../modules/team_service.md) |
| Inbound | [triage_service](../modules/triage_service.md) |
| Inbound | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) |
| Inbound | [test_runtime_policy](../modules/test_runtime_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalize_text` | `(value: str) -> str` | — | Normalize user search input without database-collation assumptions. |
| `_escaped_like` | `(value: str) -> str` | — | — |
| `portable_contains` | `(column: Any, value: str) -> Any` | — | Return the frozen portable substring contract. |
| `portable_case_insensitive_equal` | `(column: Any, value: str) -> Any` | — | Match ASCII identifiers case-insensitively and Unicode identifiers exactly. |
