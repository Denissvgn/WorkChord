# WorkTemplateUpdate

**Location:** `backend/app/schemas/template.py:34`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_template](../modules/schemas_template.md)

## Description

Schema for updating a reusable work template.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `Optional[str]` | `name` | No | Yes | `None` | min_length=1; max_length=255 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `template_type` | `Optional[TemplateType]` | `template_type` | No | Yes | `None` | — | — | — |
| `default_title` | `Optional[str]` | `default_title` | No | Yes | `None` | min_length=1; max_length=500 | — | — |
| `default_description` | `Optional[str]` | `default_description` | No | Yes | `None` | — | — | — |
| `default_priority` | `Optional[int]` | `default_priority` | No | Yes | `None` | ge=1; le=10 | — | — |
| `default_effort_days` | `Optional[float]` | `default_effort_days` | No | Yes | `None` | ge=0.1 | — | — |
| `default_labels` | `Optional[list[str]]` | `default_labels` | No | Yes | `None` | — | — | — |
| `default_checklist` | `Optional[list[str]]` | `default_checklist` | No | Yes | `None` | — | — | — |
| `default_payload` | `Optional[dict[str, Any]]` | `default_payload` | No | Yes | `None` | — | — | — |
| `is_active` | `Optional[bool]` | `is_active` | No | Yes | `None` | — | — | — |
| `sort_order` | `Optional[int]` | `sort_order` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkTemplateUpdate (backend/app/schemas/template.py)"]
    n1["BaseModel"]
    n2["update_template (backend/app/routers/templates.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["TemplateService.update (backend/app/services/template_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_template.md"
    click n2 "../modules/templates.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/template_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_template](../modules/schemas_template.md) | 0 | `default_checklist`, `default_description`, `default_effort_days`, `default_labels`, `default_payload`, `default_priority`, `default_title`, `description`, `is_active`, `name`, `sort_order`, `template_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_template` | type_reference | [templates](../modules/templates.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TemplateService.update` | type_reference | [template_service](../modules/template_service.md) | — |
