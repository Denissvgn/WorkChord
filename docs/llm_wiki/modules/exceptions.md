# exceptions Module

**Path:** `backend/app/utils/exceptions.py`

## Description

Exception handlers and error middleware.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.common` | `ErrorResponse`, `ErrorDetail` |
| `fastapi` | `FastAPI`, `Request`, `status` |
| `fastapi.responses` | `JSONResponse` |
| `pydantic` | `ValidationError` |
| `sqlalchemy.exc` | `IntegrityError` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/schemas/common.py"]
    n1["backend/app/utils/exceptions.py"]
    n1 --> n0
    click n0 "../modules/schemas_common.md"
    click n1 "../modules/exceptions.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [schemas_common](../modules/schemas_common.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [WorkChordException](../entities/WorkChordException.md) | 12 | `Exception` | Base exception for the application. |
| [NotFoundException](../entities/NotFoundException.md) | 20 | `WorkChordException` | Resource not found exception. |
| [ValidationException](../entities/ValidationException.md) | 29 | `WorkChordException` | Validation error exception. |
| [CircularDependencyException](../entities/CircularDependencyException.md) | 36 | `WorkChordException` | Circular dependency detected. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `setup_exception_handlers` | `(app: FastAPI)` | — | Setup custom exception handlers for the application. |
