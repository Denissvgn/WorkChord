# TemplateType

**Location:** `backend/app/schemas/template.py:9`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_template](../modules/schemas_template.md)

## Description

Template target type.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `TASK` | `'task'` | — |
| `PROJECT` | `'project'` | — |
| `TRIAGE` | `'triage'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TemplateType (backend/app/schemas/template.py)"]
    n1["Enum"]
    n2["str"]
    n3["list_templates (backend/app/mcp_agent_tools.py)"]
    n4["list_templates (backend/app/routers/templates.py)"]
    n5["backend/app/schemas/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_template.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/templates.md"
    click n5 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_template](../modules/schemas_template.md) | 0 | `PROJECT`, `TASK`, `TRIAGE` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_templates` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `list_templates` | type_reference | [templates](../modules/templates.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
