# TriageTaskDraftResponse

**Location:** `backend/app/schemas/triage.py:244`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_triage](../modules/schemas_triage.md)

## Description

_Auto-generated from `TriageTaskDraftResponse` in `backend/app/schemas/triage.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `brief` | `Optional[TaskBrief]` | `brief` | No | Yes | `None` | — | — | — |
| `triage_item_id` | `int` | `triage_item_id` | Yes | No | — | — | — | — |
| `suggested_title` | `str` | `suggested_title` | Yes | No | — | — | — | — |
| `suggested_description` | `str` | `suggested_description` | Yes | No | — | — | — | — |
| `suggested_checklist` | `list[str]` | `suggested_checklist` | No | No | factory: `list` | — | — | — |
| `acceptance_criteria` | `list[str]` | `acceptance_criteria` | No | No | factory: `list` | — | — | — |
| `risks` | `list[str]` | `risks` | No | No | factory: `list` | — | — | — |
| `template_id` | `Optional[int]` | `template_id` | No | Yes | `None` | — | — | — |
| `classification_suggestion_id` | `Optional[int]` | `classification_suggestion_id` | No | Yes | `None` | — | — | — |
| `is_fallback` | `bool` | `is_fallback` | No | No | `False` | — | — | — |
| `provider` | `Optional[str]` | `provider` | No | Yes | `None` | — | — | — |
| `model` | `Optional[str]` | `model` | No | Yes | `None` | — | — | — |
| `language` | `str` | `language` | No | No | `'en'` | — | — | — |
| `finish_reason` | `Optional[str]` | `finish_reason` | No | Yes | `None` | — | — | — |
| `is_truncated` | `bool` | `is_truncated` | No | No | `False` | — | — | — |
| `grounded_facts` | `list[dict[str, Any]]` | `grounded_facts` | No | No | factory: `list` | — | — | — |
| `implementation_notes` | `list[str]` | `implementation_notes` | No | No | factory: `list` | — | — | — |
| `open_questions` | `list[str]` | `open_questions` | No | No | factory: `list` | — | — | — |
| `ungrounded_suggestions` | `list[str]` | `ungrounded_suggestions` | No | No | factory: `list` | — | — | — |
| `warnings` | `list[str]` | `warnings` | No | No | factory: `list` | — | — | — |
| `rationale` | `Optional[str]` | `rationale` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageTaskDraftResponse (backend/app/schemas/triage.py)"]
    n1["BaseModel"]
    n2["draft_triage_task (backend/app/routers/triage.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["LLMService._triage_task_draft_fallback (backend/app/services/llm_service.py)"]
    n5["LLMService.draft_triage_task (backend/app/services/llm_service.py)"]
    n6["TriageService.draft_task (backend/app/services/triage_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_triage.md"
    click n2 "../modules/routers_triage.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/llm_service.md"
    click n5 "../modules/llm_service.md"
    click n6 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_triage](../modules/schemas_triage.md) | 0 | `acceptance_criteria`, `brief`, `classification_suggestion_id`, `finish_reason`, `grounded_facts`, `implementation_notes`, `is_fallback`, `is_truncated`, `language`, `model`, `open_questions`, `provider` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `draft_triage_task` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `LLMService._triage_task_draft_fallback` | call | [llm_service](../modules/llm_service.md) | 1 |
| `LLMService._triage_task_draft_fallback` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService.draft_triage_task` | call | [llm_service](../modules/llm_service.md) | 1 |
| `LLMService.draft_triage_task` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `TriageService.draft_task` | type_reference | [triage_service](../modules/triage_service.md) | — |
