# native_session_service Module

**Path:** `backend/app/services/native_session_service.py`

## Description

Owns proof-bound native session creation and browser approval. Public start/exchange paths require bounded inputs; approval requires a human session and normal browser request integrity. The exchange checks current account/session validity, locks the principal before the approving session, and atomically consumes the connection while issuing an opaque bearer session.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority` |
| `app.commands` | `atomic_command` |
| `app.config` | `get_settings` |
| `app.models.identity` | `Principal` |
| `app.models.native_connection` | `NativeConnection` |
| `app.models.user_session` | `UserSession` |
| `app.services.identity_service` | `IdentityService`, `digest`, `require_identity_writes` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `base64` | `base64` |
| `datetime` | `timedelta` |
| `hashlib` | `hashlib` |
| `secrets` | `secrets` |
| `sqlalchemy` | `delete`, `func`, `select`, `update` |
| `urllib.parse` | `urlencode` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/config.py"]
    n3["backend/app/models/identity.py"]
    n4["backend/app/models/native_connection.py"]
    n5["backend/app/models/user_session.py"]
    n6["backend/app/routers/identity.py"]
    n7["backend/app/services/identity_service.py"]
    n8["backend/app/services/native_session_service.py"]
    n9["backend/app/utils/time.py"]
    n0 --> n2
    n0 --> n3
    n1 --> n0
    n3 --> n9
    n4 --> n9
    n5 --> n3
    n5 --> n9
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n7
    n8 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/config.md"
    click n3 "../modules/models_identity.md"
    click n4 "../modules/native_connection.md"
    click n5 "../modules/user_session.md"
    click n6 "../modules/routers_identity.md"
    click n7 "../modules/identity_service.md"
    click n8 "../modules/native_session_service.md"
    click n9 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_identity](../modules/routers_identity.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [native_connection](../modules/native_connection.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [identity_service](../modules/identity_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [NativeSessionService](../entities/NativeSessionService.md) | 21 | — | — |