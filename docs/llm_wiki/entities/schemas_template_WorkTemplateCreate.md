# WorkTemplateCreate

**Location:** `backend/app/schemas/template.py:23`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_template](../modules/schemas_template.md)

## Description

Schema for creating a reusable work template.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_brief_payload` | field | default_payload | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `str` | `name` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `template_type` | `TemplateType` | `template_type` | Yes | No | — | — | — | — |
| `default_title` | `Optional[str]` | `default_title` | No | Yes | `None` | max_length=500; min_length=1 | — | — |
| `default_description` | `Optional[str]` | `default_description` | No | Yes | `None` | — | — | — |
| `default_priority` | `Optional[int]` | `default_priority` | No | Yes | `None` | ge=1; le=10 | — | — |
| `default_effort_days` | `Optional[float]` | `default_effort_days` | No | Yes | `None` | ge=0.1 | — | — |
| `default_labels` | `list[str]` | `default_labels` | No | No | factory: `list` | — | — | — |
| `default_checklist` | `list[str]` | `default_checklist` | No | No | factory: `list` | — | — | — |
| `default_payload` | `dict[str, Any]` | `default_payload` | No | No | factory: `dict` | — | — | — |
| `is_active` | `bool` | `is_active` | No | No | `True` | — | — | — |
| `sort_order` | `int` | `sort_order` | No | No | `0` | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_brief_payload` | `(value)` | `@field_validator('default_payload')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkTemplateCreate (backend/app/schemas/template.py)"]
    n1["BaseModel"]
    n2["create_template (backend/app/routers/templates.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["TemplateService.create (backend/app/services/template_service.py)"]
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
| [schemas_template](../modules/schemas_template.md) | 1 | `default_checklist`, `default_description`, `default_effort_days`, `default_labels`, `default_payload`, `default_priority`, `default_title`, `description`, `is_active`, `name`, `sort_order`, `template_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_template` | type_reference | [templates](../modules/templates.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TemplateService.create` | type_reference | [template_service](../modules/template_service.md) | — |
