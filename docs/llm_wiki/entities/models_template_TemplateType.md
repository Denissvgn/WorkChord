# TemplateType

**Location:** `backend/app/models/template.py:13`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_template](../modules/models_template.md)

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
    n0["TemplateType (backend/app/models/template.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n4["TemplateService.list_templates (backend/app/services/template_service.py)"]
    n5["backend/app/services/triage_service.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/models_template.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/template_service.md"
    click n5 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_template](../modules/models_template.md) | 0 | `PROJECT`, `TASK`, `TRIAGE` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `TemplateService.list_templates` | type_reference | [template_service](../modules/template_service.md) | — |
| `triage_service` | import | [triage_service](../modules/triage_service.md) | — |
