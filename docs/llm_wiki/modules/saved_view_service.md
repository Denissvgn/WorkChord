# saved_view_service Module

**Path:** `backend/app/services/saved_view_service.py`

## Description

Service for saved view persistence and filter payload compatibility.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.iteration` | `Iteration` |
| `app.models.saved_view` | `SavedView` |
| `app.schemas.saved_view` | `SavedViewCreate`, `SavedViewCreateRequest`, `SavedViewDashboardCardResponse`, `SavedViewDuplicateRequest`, `SavedViewResponse`, `SavedViewScope`, `SavedViewType`, `SavedViewUpdate`, `SavedViewUpdateRequest` |
| `datetime` | `date` |
| `math` | `isfinite` |
| `sqlalchemy` | `Select`, `or_`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/iteration.py"]
    n2["backend/app/models/saved_view.py"]
    n3["backend/app/routers/saved_views.py"]
    n4["backend/app/schemas/saved_view.py"]
    n5["backend/app/services/saved_view_service.py"]
    n6["backend/app/services/upgrade_service.py"]
    n7["backend/tests/test_saved_view_service.py"]
    n0 --> n4
    n0 --> n5
    n3 --> n4
    n3 --> n5
    n5 --> n1
    n5 --> n2
    n5 --> n4
    n6 --> n5
    n7 --> n4
    n7 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/models_iteration.md"
    click n2 "../modules/models_saved_view.md"
    click n3 "../modules/saved_views.md"
    click n4 "../modules/schemas_saved_view.md"
    click n5 "../modules/saved_view_service.md"
    click n6 "../modules/upgrade_service.md"
    click n7 "../modules/test_saved_view_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [saved_views](../modules/saved_views.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Inbound | [test_saved_view_service](../modules/test_saved_view_service.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_saved_view](../modules/models_saved_view.md) |
| Outbound | [schemas_saved_view](../modules/schemas_saved_view.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SavedViewPermissionError](../entities/SavedViewPermissionError.md) | 24 | `PermissionError` | Raised when a session cannot mutate a saved view. |
| [SavedViewValidationError](../entities/SavedViewValidationError.md) | 28 | `ValueError` | Raised when a saved view payload is invalid. |
| [SavedViewService](../entities/SavedViewService.md) | 171 | — | Service for saved view CRUD and compatibility-safe read models. |
