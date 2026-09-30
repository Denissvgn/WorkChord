# template_service Module

**Path:** `backend/app/services/template_service.py`

## Description

Service for reusable work templates and built-in defaults.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.models.template` | `TemplateType`, `WorkTemplate` |
| `app.schemas.template` | `WorkTemplateCreate`, `WorkTemplateUpdate` |
| `sqlalchemy` | `Select`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/template.py"]
    n3["backend/app/routers/templates.py"]
    n4["backend/app/schemas/template.py"]
    n5["backend/app/services/template_service.py"]
    n6["backend/app/services/upgrade_service.py"]
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n3 --> n4
    n3 --> n5
    n5 --> n0
    n5 --> n2
    n5 --> n4
    n6 --> n0
    n6 --> n5
    click n0 "../modules/commands.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_template.md"
    click n3 "../modules/templates.md"
    click n4 "../modules/schemas_template.md"
    click n5 "../modules/template_service.md"
    click n6 "../modules/upgrade_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [templates](../modules/templates.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_template](../modules/models_template.md) |
| Outbound | [schemas_template](../modules/schemas_template.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TemplateService](../entities/TemplateService.md) | 159 | — | Service for template CRUD and built-in template seeding. |
