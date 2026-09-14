# github Module

**Path:** `backend/app/models/github.py`

## Description

GitHub integration models.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `Boolean`, `CheckConstraint`, `Index`, `Integer`, `String`, `Text` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/github.py"]
    n3["backend/app/services/github_status_automation_service.py"]
    n4["backend/app/utils/time.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_github.md"
    click n3 "../modules/github_status_automation_service.md"
    click n4 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [github_status_automation_service](../modules/github_status_automation_service.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [GitHubStatusAutomationRule](../entities/models_github_GitHubStatusAutomationRule.md) | 23 | `Base` | Opt-in rule that maps GitHub PR activity to task status changes. |
