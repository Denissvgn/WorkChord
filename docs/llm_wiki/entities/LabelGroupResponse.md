# LabelGroupResponse

**Location:** `backend/app/schemas/label.py:92`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_label](../modules/schemas_label.md)

## Description

Schema for governed label group responses.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `key` | `str` | `key` | Yes | No | — | — | — | — |
| `name` | `str` | `name` | Yes | No | — | — | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `color` | `str` | `color` | Yes | No | — | — | — | — |
| `is_active` | `bool` | `is_active` | Yes | No | — | — | — | — |
| `sort_order` | `int` | `sort_order` | Yes | No | — | — | — | — |
| `seed_key` | `Optional[str]` | `seed_key` | No | Yes | `None` | — | — | — |
| `labels` | `list[LabelResponse]` | `labels` | No | No | factory: `list` | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `updated_at` | `datetime` | `updated_at` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LabelGroupResponse (backend/app/schemas/label.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["create_label_group (backend/app/routers/labels.py)"]
    n4["list_label_groups (backend/app/routers/labels.py)"]
    n5["update_label_group (backend/app/routers/labels.py)"]
    n6["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_label.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/labels.md"
    click n4 "../modules/labels.md"
    click n5 "../modules/labels.md"
    click n6 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_label](../modules/schemas_label.md) | 0 | `color`, `created_at`, `description`, `id`, `is_active`, `key`, `labels`, `name`, `seed_key`, `sort_order`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `create_label_group` | type_reference | [labels](../modules/labels.md) | — |
| `list_label_groups` | type_reference | [labels](../modules/labels.md) | — |
| `update_label_group` | type_reference | [labels](../modules/labels.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
