# WorkTemplate

**Location:** `backend/app/models/template.py:20`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_template](../modules/models_template.md)

## Description

Reusable defaults for creating tasks, projects, or triage items.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `seed_key` | `Mapped[Optional[str]]` | `mapped_column(String(100), nullable=True, unique=True, index=True)` | — |
| `template_type` | `Mapped[str]` | `mapped_column(String(50), nullable=False, index=True)` | — |
| `default_title` | `Mapped[Optional[str]]` | `mapped_column(String(500), nullable=True)` | — |
| `default_description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `default_priority` | `Mapped[Optional[int]]` | `mapped_column(Integer, nullable=True)` | — |
| `default_effort_days` | `Mapped[Optional[float]]` | `mapped_column(Float, nullable=True)` | — |
| `default_labels` | `Mapped[list[str]]` | `mapped_column(JSON, default=list, nullable=False)` | — |
| `default_checklist` | `Mapped[list[str]]` | `mapped_column(JSON, default=list, nullable=False)` | — |
| `default_payload` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `is_active` | `Mapped[bool]` | `mapped_column(Boolean, default=True, nullable=False, index=True)` | — |
| `sort_order` | `Mapped[int]` | `mapped_column(Integer, default=0, nullable=False, index=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False, index=True)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkTemplate (backend/app/models/template.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["TemplateService.create (backend/app/services/template_service.py)"]
    n4["TemplateService.get_by_id (backend/app/services/template_service.py)"]
    n5["TemplateService.list_templates (backend/app/services/template_service.py)"]
    n6["TemplateService.seed_default_templates (backend/app/services/template_service.py)"]
    n7["TemplateService.update (backend/app/services/template_service.py)"]
    n8["TriageService._get_task_draft_template (backend/app/services/triage_service.py)"]
    n9["TriageService._task_template_context (backend/app/services/triage_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/models_template.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/template_service.md"
    click n4 "../modules/template_service.md"
    click n5 "../modules/template_service.md"
    click n6 "../modules/template_service.md"
    click n7 "../modules/template_service.md"
    click n8 "../modules/triage_service.md"
    click n9 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_template](../modules/models_template.md) | 0 | `created_at`, `default_checklist`, `default_description`, `default_effort_days`, `default_labels`, `default_payload`, `default_priority`, `default_title`, `description`, `id`, `is_active`, `name` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `TemplateService.create` | call | [template_service](../modules/template_service.md) | 1 |
| `TemplateService.create` | type_reference | [template_service](../modules/template_service.md) | — |
| `TemplateService.get_by_id` | type_reference | [template_service](../modules/template_service.md) | — |
| `TemplateService.list_templates` | type_reference | [template_service](../modules/template_service.md) | — |
| `TemplateService.seed_default_templates` | call | [template_service](../modules/template_service.md) | 1 |
| `TemplateService.seed_default_templates` | type_reference | [template_service](../modules/template_service.md) | — |
| `TemplateService.update` | type_reference | [template_service](../modules/template_service.md) | — |
| `TriageService._get_task_draft_template` | type_reference | [triage_service](../modules/triage_service.md) | — |
| `TriageService._task_template_context` | type_reference | [triage_service](../modules/triage_service.md) | — |
