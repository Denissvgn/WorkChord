# LabelGroupCreate

**Location:** `backend/app/schemas/label.py:13`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_label](../modules/schemas_label.md)

## Description

Schema for creating a governed label group.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `key` | `str` | `key` | Yes | No | — | min_length=1; max_length=100; pattern=unknown (GROUP_KEY_PATTERN) | — | — |
| `name` | `str` | `name` | Yes | No | — | min_length=1; max_length=255 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `color` | `str` | `color` | No | No | `'#64748b'` | pattern=unknown (HEX_COLOR_PATTERN) | — | — |
| `is_active` | `bool` | `is_active` | No | No | `True` | — | — | — |
| `sort_order` | `int` | `sort_order` | No | No | `0` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LabelGroupCreate (backend/app/schemas/label.py)"]
    n1["BaseModel"]
    n2["create_label_group (backend/app/routers/labels.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["LabelService.create_group (backend/app/services/label_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_label.md"
    click n2 "../modules/labels.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/label_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_label](../modules/schemas_label.md) | 0 | `color`, `description`, `is_active`, `key`, `name`, `sort_order` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_label_group` | type_reference | [labels](../modules/labels.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `LabelService.create_group` | type_reference | [label_service](../modules/label_service.md) | — |
