# TemplateService

**Location:** `backend/app/services/template_service.py:159`
**Kind:** Class
**Bases:** —
**Module:** [template_service](../modules/template_service.md)

## Description

Service for template CRUD and built-in template seeding.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db: AsyncSession)` | — | — |
| `_enum_value` | `(value)` | — | Normalize Pydantic enum values before assigning to string columns. |
| `_query` | `() -> Select` | — | Build the base template query. |
| `seed_default_templates` | *(async)* `() -> list[WorkTemplate]` | — | Insert missing built-ins and safely upgrade unchanged legacy defaults. |
| `list_templates` | *(async)* `(template_type: Optional[TemplateType \| str] = None, include_inactive: bool = False) -> Sequence[WorkTemplate]` | — | List templates ordered for create-form selection. |
| `get_by_id` | *(async)* `(template_id: int) -> Optional[WorkTemplate]` | — | Get a template by ID. |
| `create` | *(async)* `(data: WorkTemplateCreate) -> WorkTemplate` | — | Create a user-managed template. |
| `update` | *(async)* `(template_id: int, data: WorkTemplateUpdate) -> Optional[WorkTemplate]` | — | Apply a partial template update. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TemplateService (backend/app/services/template_service.py)"]
    n1["list_templates (backend/app/mcp_agent_tools.py)"]
    n2["create_template (backend/app/routers/templates.py)"]
    n3["get_template (backend/app/routers/templates.py)"]
    n4["get_template_service (backend/app/routers/templates.py)"]
    n5["list_templates (backend/app/routers/templates.py)"]
    n6["update_template (backend/app/routers/templates.py)"]
    n7["run_post_migration_repairs (backend/app/services/upgrade_service.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/template_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/templates.md"
    click n3 "../modules/templates.md"
    click n4 "../modules/templates.md"
    click n5 "../modules/templates.md"
    click n6 "../modules/templates.md"
    click n7 "../modules/upgrade_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [template_service](../modules/template_service.md) | 8 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_templates` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `create_template` | type_reference | [templates](../modules/templates.md) | — |
| `get_template` | type_reference | [templates](../modules/templates.md) | — |
| `get_template_service` | call | [templates](../modules/templates.md) | 1 |
| `get_template_service` | type_reference | [templates](../modules/templates.md) | — |
| `list_templates` | type_reference | [templates](../modules/templates.md) | — |
| `update_template` | type_reference | [templates](../modules/templates.md) | — |
| `run_post_migration_repairs` | call | [upgrade_service](../modules/upgrade_service.md) | 1 |
