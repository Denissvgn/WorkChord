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
    n0["backend"]
    n1["backend/app/models/external_link.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/models_external_link.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (13) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ExternalLinkEntityType](../entities/models_external_link_ExternalLinkEntityType.md) | Enum | 13 | `str`, `Enum` | Supported internal entity types for external links. |
| [ExternalLinkProvider](../entities/models_external_link_ExternalLinkProvider.md) | Enum | 20 | `str`, `Enum` | Supported external link providers. |
| [ExternalLink](../entities/models_external_link_ExternalLink.md) | Class | 30 | `Base` | Generic link from an internal entity to an external delivery artifact. |
