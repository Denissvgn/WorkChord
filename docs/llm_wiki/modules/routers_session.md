# session Module

**Path:** `backend/app/routers/session.py`

## Description

Browser identity lifecycle API.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `get_db` |
| `app.models.user_session` | `UserSession` |
| `app.schemas.common` | `MessageResponse` |
| `app.schemas.session` | `UserSession` |
| `app.services` | `session_service` |
| `fastapi` | `APIRouter`, `Depends`, `Response` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Annotated` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/main.py"]
    n2["backend/app/models/user_session.py"]
    n3["backend/app/routers/__init__.py"]
    n4["backend/app/routers/session.py"]
    n5["backend/app/schemas/common.py"]
    n6["backend/app/schemas/session.py"]
    n7["backend/app/services/session_service.py"]
    n1 --> n0
    n1 --> n4
    n2 --> n0
    n3 --> n4
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n7 --> n0
    n7 --> n2
    click n0 "../modules/app_database.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/user_session.md"
    click n3 "../modules/routers___init__.md"
    click n4 "../modules/routers_session.md"
    click n5 "../modules/schemas_common.md"
    click n6 "../modules/schemas_session.md"
    click n7 "../modules/session_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [routers___init__](../modules/routers___init__.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [schemas_common](../modules/schemas_common.md) |
| Outbound | [schemas_session](../modules/schemas_session.md) |
| Outbound | [session_service](../modules/session_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `whoami` | *(async)* `(current_session: Annotated[UserSession, Depends(session_service.get_current_session)]) -> UserSession` | `@router.get('/session/whoami', response_model=UserSessionSchema)` | Return privacy-safe attribution for the current opaque browser session. |
| `rotate_session` | *(async)* `(response: Response, current_session: Annotated[UserSession, Depends(session_service.get_current_session)], db: Annotated[AsyncSession, Depends(get_db, scope='function')]) -> UserSession` | `@router.post('/session/rotate', response_model=UserSessionSchema)` | Rotate the browser token without changing saved-view ownership. |
| `revoke_session` | *(async)* `(response: Response, current_session: Annotated[UserSession, Depends(session_service.get_current_session)], db: Annotated[AsyncSession, Depends(get_db, scope='function')]) -> MessageResponse` | `@router.delete('/session', response_model=MessageResponse)` | Revoke the current browser identity. |
