# sql_semantics Module

**Path:** `backend/app/sql_semantics.py`

## Description

Cross-dialect SQL expressions for the supported SQLite/PostgreSQL window.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `sqlalchemy` | `JSON`, `cast`, `func` |
| `typing` | `Any` |
| `unicodedata` | `unicodedata` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/discussion_service.py"]
    n1["backend/app/services/execution_reconciliation.py"]
    n2["backend/app/services/label_service.py"]
    n3["backend/app/services/project_service.py"]
    n4["backend/app/services/request_source_service.py"]
    n5["backend/app/services/task_detail_service.py"]
    n6["backend/app/services/team_service.py"]
    n7["backend/app/services/triage_service.py"]
    n8["backend/app/services/work_metrics.py"]
    n9["backend/app/sql_semantics.py"]
    n10["backend/tests/database/test_postgresql_concurrency.py"]
    n11["backend/tests/database/test_runtime_policy.py"]
    n0 --> n9
    n1 --> n9
    n2 --> n9
    n3 --> n4
    n3 --> n8
    n3 --> n9
    n4 --> n9
    n5 --> n9
    n6 --> n8
    n6 --> n9
    n7 --> n4
    n7 --> n9
    n8 --> n9
    n10 --> n9
    n11 --> n9
    click n0 "../modules/discussion_service.md"
    click n1 "../modules/execution_reconciliation.md"
    click n2 "../modules/label_service.md"
    click n3 "../modules/project_service.md"
    click n4 "../modules/request_source_service.md"
    click n5 "../modules/task_detail_service.md"
    click n6 "../modules/team_service.md"
    click n7 "../modules/triage_service.md"
    click n8 "../modules/services_work_metrics.md"
    click n9 "../modules/sql_semantics.md"
    click n10 "../modules/test_postgresql_concurrency.md"
    click n11 "../modules/test_runtime_policy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [discussion_service](../modules/discussion_service.md) |
| Inbound | [execution_reconciliation](../modules/execution_reconciliation.md) |
| Inbound | [label_service](../modules/label_service.md) |
| Inbound | [project_service](../modules/project_service.md) |
| Inbound | [request_source_service](../modules/request_source_service.md) |
| Inbound | [task_detail_service](../modules/task_detail_service.md) |
| Inbound | [team_service](../modules/team_service.md) |
| Inbound | [triage_service](../modules/triage_service.md) |
| Inbound | [services_work_metrics](../modules/services_work_metrics.md) |
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
| `json_text_field` | `(db, column, *path, integer = False)` | — | Task event payloads are historical text on both supported databases. |
