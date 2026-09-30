# external_link Module

**Path:** `backend/app/models/external_link.py`

## Description

External link model for delivery traceability.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `enum` | `Enum` |
| `sqlalchemy` | `CheckConstraint`, `Index`, `Integer`, `JSON`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/external_link.py"]
    n3["backend/app/models/release.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/services/external_link_service.py"]
    n6["backend/app/services/github_status_service.py"]
    n7["backend/app/services/github_webhook_service.py"]
    n8["backend/app/utils/time.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n8
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n8
    n4 --> n0
    n4 --> n2
    n4 --> n8
    n5 --> n2
    n5 --> n4
    n6 --> n2
    n6 --> n5
    n7 --> n2
    n7 --> n6
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_external_link.md"
    click n3 "../modules/models_release.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/external_link_service.md"
    click n6 "../modules/github_status_service.md"
    click n7 "../modules/github_webhook_service.md"
    click n8 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [models_release](../modules/models_release.md) |
| Inbound | [models_task](../modules/models_task.md) |
| Inbound | [external_link_service](../modules/external_link_service.md) |
| Inbound | [github_status_service](../modules/github_status_service.md) |
| Inbound | [github_webhook_service](../modules/github_webhook_service.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ExternalLinkEntityType](../entities/models_external_link_ExternalLinkEntityType.md) | Enum | 13 | `str`, `Enum` | Supported internal entity types for external links. |
| [ExternalLinkProvider](../entities/models_external_link_ExternalLinkProvider.md) | Enum | 20 | `str`, `Enum` | Supported external link providers. |
| [ExternalLink](../entities/models_external_link_ExternalLink.md) | Class | 29 | `Base` | Generic link from an internal entity to an external delivery artifact. |
