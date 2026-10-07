# time_entries Module

**Path:** `backend/app/routers/time_entries.py`

## Description

Optional human-authored time records with private correction history. A router dependency marks serialized responses `Cache-Control: private, no-store`; the explicit CSV response carries the same directive. Authentication and domain error handlers retain their existing no-store protection.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.database` | `get_db` |
| `app.routers.task_domain` | `domain_result` |
| `app.schemas.time_entry` | `TimeEntryCreate`, `TimeEntryCorrection`, `TimeEntryVoid`, `TimeEntryResponse`, `TimeEntryPage`, `TimeRevisionPage`, `TimeEntryCapabilities` |
| `app.schemas.time_report` | `TimeReportPage` |
| `app.services.time_entry_service` | `TimeEntryService` |
| `app.services.time_report_service` | `TimeReportService` |
| `datetime` | `date` |
| `fastapi` | `APIRouter`, `Depends`, `Query` |
| `fastapi.responses` | `Response` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Annotated`, `Literal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/database.py"]
    n2["backend/app/main.py"]
    n3["backend/app/routers/task_domain.py"]
    n4["backend/app/routers/time_entries.py"]
    n5["backend/app/schemas/time_entry.py"]
    n6["backend/app/schemas/time_report.py"]
    n7["backend/app/services/time_entry_service.py"]
    n8["backend/app/services/time_report_service.py"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n3 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n7 --> n0
    n7 --> n5
    n8 --> n7
    click n0 "../modules/config.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/time_entries.md"
    click n5 "../modules/schemas_time_entry.md"
    click n6 "../modules/time_report.md"
    click n7 "../modules/time_entry_service.md"
    click n8 "../modules/time_report_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [app_main](../modules/app_main.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Outbound | [schemas_time_entry](../modules/schemas_time_entry.md) |
| Outbound | [time_report](../modules/time_report.md) |
| Outbound | [time_entry_service](../modules/time_entry_service.md) |
| Outbound | [time_report_service](../modules/time_report_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DB](../entities/time_entries_DB.md) | Type alias | 24 | `Annotated[AsyncSession, Depends(get_db, scope='function')]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `prevent_private_caching` | `(response: Response)` | — | — |
| `capabilities` | *(async)* `(db: DB)` | `@router.get('/capabilities', response_model=TimeEntryCapabilities)` | — |
| `list_entries` | *(async)* `(db: DB, project_id: int \| None = Query(default=None, ge=1), task_id: int \| None = Query(default=None, ge=1), start: date \| None = None, end: date \| None = None, after_id: int = Query(default=0, ge=0), upper_id: int \| None = Query(default=None, ge=0), limit: int = Query(default=50, ge=1, le=100), include_voided: bool = False)` | `@router.get('', response_model=TimeEntryPage)` | — |
| `create_entry` | *(async)* `(data: TimeEntryCreate, db: DB)` | `@router.post('', response_model=TimeEntryResponse, status_code=201)` | — |
| `report` | *(async)* `(db: DB, project_id: int = Query(ge=1), start: date = Query(), end: date = Query(), scope: Literal['mine', 'project'] = 'mine', after_id: int = Query(default=0, ge=0), upper_id: int \| None = Query(default=None, ge=0), limit: int = Query(default=50, ge=1, le=100))` | `@router.get('/report', response_model=TimeReportPage)` | — |
| `export` | *(async)* `(db: DB, project_id: int = Query(ge=1), start: date = Query(), end: date = Query(), scope: Literal['mine', 'project'] = 'mine', kind: Literal['totals', 'entries'] = 'totals')` | `@router.get('/export', response_class=Response, responses={200: {'description': 'Scoped recorded time CSV', 'content': {'text/csv': {'schema': {'type': 'string', 'format': 'binary'}}}}})` | — |
| `get_entry` | *(async)* `(entry_id: int, db: DB)` | `@router.get('/{entry_id}', response_model=TimeEntryResponse)` | — |
| `correct_entry` | *(async)* `(entry_id: int, data: TimeEntryCorrection, db: DB)` | `@router.put('/{entry_id}', response_model=TimeEntryResponse)` | — |
| `void_entry` | *(async)* `(entry_id: int, data: TimeEntryVoid, db: DB)` | `@router.post('/{entry_id}/void', response_model=TimeEntryResponse)` | — |
| `history` | *(async)* `(entry_id: int, db: DB, after_version: int = Query(default=0, ge=0), limit: int = Query(default=50, ge=1, le=100))` | `@router.get('/{entry_id}/history', response_model=TimeRevisionPage)` | — |
