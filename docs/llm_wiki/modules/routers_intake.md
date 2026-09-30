# intake Module

**Path:** `backend/app/routers/intake.py`

## Description

Controlled external intake API router.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `get_db` |
| `app.schemas.intake` | `WebIntakeRequest` |
| `app.schemas.triage` | `TriageItemResponse` |
| `app.services.session_service` | `get_client_ip` |
| `app.services.system_settings_service` | `RuntimeSettingsService` |
| `app.services.web_intake_service` | `WebIntakeConfigurationError`, `WebIntakeRateLimitError`, `WebIntakeService`, `WebIntakeUnauthorizedError` |
| `fastapi` | `APIRouter`, `Body`, `Depends`, `Header`, `HTTPException`, `Request`, `status` |
| `pydantic` | `ValidationError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Annotated`, `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/main.py"]
    n2["backend/app/routers/__init__.py"]
    n3["backend/app/routers/intake.py"]
    n4["backend/app/schemas/intake.py"]
    n5["backend/app/schemas/triage.py"]
    n6["backend/app/services/session_service.py"]
    n7["backend/app/services/system_settings_service.py"]
    n8["backend/app/services/web_intake_service.py"]
    n1 --> n0
    n1 --> n3
    n2 --> n3
    n3 --> n0
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n6 --> n0
    n8 --> n4
    n8 --> n5
    click n0 "../modules/app_database.md"
    click n1 "../modules/app_main.md"
    click n2 "../modules/routers___init__.md"
    click n3 "../modules/routers_intake.md"
    click n4 "../modules/schemas_intake.md"
    click n5 "../modules/schemas_triage.md"
    click n6 "../modules/session_service.md"
    click n7 "../modules/system_settings_service.md"
    click n8 "../modules/web_intake_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [routers___init__](../modules/routers___init__.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [schemas_intake](../modules/schemas_intake.md) |
| Outbound | [schemas_triage](../modules/schemas_triage.md) |
| Outbound | [session_service](../modules/session_service.md) |
| Outbound | [system_settings_service](../modules/system_settings_service.md) |
| Outbound | [web_intake_service](../modules/web_intake_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `get_web_intake_service` | *(async)* `(db: Annotated[AsyncSession, Depends(get_db, scope='function')]) -> WebIntakeService` | — | Dependency for controlled web intake. |
| `create_web_intake_item` | *(async)* `(request: Request, raw_data: Annotated[Any, Body(...)], service: Annotated[WebIntakeService, Depends(get_web_intake_service)], authorization: Annotated[Optional[str], Header(alias='Authorization')] = None)` | `@router.post('/intake/web', response_model=TriageItemResponse, status_code=status.HTTP_201_CREATED)` | Create a triage item from a controlled external web/form intake payload. |
