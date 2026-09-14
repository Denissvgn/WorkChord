# template_service Module

**Path:** `backend/app/services/template_service.py`

## Description

Service for reusable work templates and built-in defaults.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.template` | `TemplateType`, `WorkTemplate` |
| `app.schemas.template` | `WorkTemplateCreate`, `WorkTemplateUpdate` |
| `sqlalchemy` | `Select`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/template.py"]
    n2["backend/app/routers/templates.py"]
    n3["backend/app/schemas/template.py"]
    n4["backend/app/services/template_service.py"]
    n5["backend/app/services/upgrade_service.py"]
    n0 --> n3
    n0 --> n4
    n2 --> n3
    n2 --> n4
    n4 --> n1
    n4 --> n3
    n5 --> n4
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/models_template.md"
    click n2 "../modules/templates.md"
    click n3 "../modules/schemas_template.md"
    click n4 "../modules/template_service.md"
    click n5 "../modules/upgrade_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [templates](../modules/templates.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [models_template](../modules/models_template.md) |
| Outbound | [schemas_template](../modules/schemas_template.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TemplateService](../entities/TemplateService.md) | 157 | — | Service for template CRUD and built-in template seeding. |
