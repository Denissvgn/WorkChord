# AuthorityError

**Location:** `backend/app/authority.py:14`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [authority](../modules/authority.md)

## Description

_Auto-generated from `AuthorityError` in `backend/app/authority.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code = 'permission_denied', message = 'You do not have permission for this action.', status = 403)` | — | — |
| `detail` | `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AuthorityError (backend/app/authority.py)"]
    n1["RuntimeError"]
    n2["_check_bulk_write (backend/app/authority.py)"]
    n3["authorize_domain_writes (backend/app/authority.py)"]
    n4["require_operator (backend/app/authority.py)"]
    n5["require_project (backend/app/authority.py)"]
    n6["scope_orm_operation (backend/app/authority.py)"]
    n7["lock_iterations (backend/app/commands.py)"]
    n8["enforce_http_authority (backend/app/http_authority.py)"]
    n9["resolve_http_identity (backend/app/http_authority.py)"]
    n10["authority_error (backend/app/main.py)"]
    n11["backend/app/mcp_server.py"]
    n12["bootstrap (backend/app/routers/identity.py)"]
    n13["link_profile (backend/app/routers/identity.py)"]
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
    click n0 "../modules/authority.md"
    click n2 "../modules/authority.md"
    click n3 "../modules/authority.md"
    click n4 "../modules/authority.md"
    click n5 "../modules/authority.md"
    click n6 "../modules/authority.md"
    click n7 "../modules/commands.md"
    click n8 "../modules/http_authority.md"
    click n9 "../modules/http_authority.md"
    click n10 "../modules/app_main.md"
    click n11 "../modules/mcp_server.md"
    click n12 "../modules/routers_identity.md"
    click n13 "../modules/routers_identity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [authority](../modules/authority.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_check_bulk_write` | call | [authority](../modules/authority.md) | 4 |
| `authorize_domain_writes` | call | [authority](../modules/authority.md) | 10 |
| `require_operator` | call | [authority](../modules/authority.md) | 1 |
| `require_project` | call | [authority](../modules/authority.md) | 2 |
| `scope_orm_operation` | call | [authority](../modules/authority.md) | 2 |
| `lock_iterations` | call | [commands](../modules/commands.md) | 1 |
| `enforce_http_authority` | call | [http_authority](../modules/http_authority.md) | 11 |
| `resolve_http_identity` | call | [http_authority](../modules/http_authority.md) | 11 |
| `authority_error` | type_reference | [app_main](../modules/app_main.md) | — |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `bootstrap` | call | [routers_identity](../modules/routers_identity.md) | 3 |
| `link_profile` | call | [routers_identity](../modules/routers_identity.md) | 2 |

> References: showing 12 of 60 logical references; 48 omitted by the 12-row generated summary limit.
