# saved_view_service Module

**Path:** `backend/app/services/saved_view_service.py`

## Description

Service for saved view persistence and filter payload compatibility.

Task dashboard cards count matching leaves. Personal ownership follows the durable principal after explicit guest transfer, retaining original session attribution. Legacy overdue predicates migrate to explicit iteration overflow with a disclosure note, while new overdue predicates mean open delivery already past its expected finish.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
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
    n0["backend/app/commands.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/models/saved_view.py"]
    n4["backend/app/routers/saved_views.py"]
    n5["backend/app/schemas/saved_view.py"]
    n6["backend/app/services/saved_view_service.py"]
    n7["backend/app/services/upgrade_service.py"]
    n8["backend/tests/test_saved_view_service.py"]
    n9["backend/tests/test_work_correctness.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n5
    n1 --> n6
    n4 --> n5
    n4 --> n6
    n6 --> n0
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n7 --> n0
    n7 --> n6
    n8 --> n5
    n8 --> n6
    n9 --> n0
    n9 --> n2
    n9 --> n6
    click n0 "../modules/commands.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/models_saved_view.md"
    click n4 "../modules/saved_views.md"
    click n5 "../modules/schemas_saved_view.md"
    click n6 "../modules/saved_view_service.md"
    click n7 "../modules/upgrade_service.md"
    click n8 "../modules/test_saved_view_service.md"
    click n9 "../modules/test_work_correctness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [saved_views](../modules/saved_views.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Inbound | [test_saved_view_service](../modules/test_saved_view_service.md) |
| Inbound | [test_work_correctness](../modules/test_work_correctness.md) |
| Outbound | [commands](../modules/commands.md) |
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
| [SavedViewPermissionError](../entities/SavedViewPermissionError.md) | 26 | `PermissionError` | Raised when a session cannot mutate a saved view. |
| [SavedViewValidationError](../entities/SavedViewValidationError.md) | 30 | `ValueError` | Raised when a saved view payload is invalid. |
| [SavedViewService](../entities/SavedViewService.md) | 174 | — | Service for saved view CRUD and compatibility-safe read models. |