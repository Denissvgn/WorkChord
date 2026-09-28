# triage Module

**Path:** `backend/app/schemas/triage.py`

## Description

Triage item schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.task` | `TaskResponse` |
| `app.schemas.task_brief` | `TaskBrief` |
| `app.services.task_brief_service` | `render_brief` |
| `datetime` | `datetime` |
| `enum` | `Enum` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `computed_field`, `field_validator`, `model_validator` |
| `typing` | `Any`, `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/schemas/triage.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/schemas_triage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (13) |
| Outbound | `backend` (3) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TriageItemStatus](../entities/schemas_triage_TriageItemStatus.md) | Enum | 12 | `str`, `Enum` | Triage item lifecycle status. |
| [TriageItemCreate](../entities/schemas_triage_TriageItemCreate.md) | Pydantic model | 33 | `BaseModel` | Schema for creating a triage item. |
| [TriageItemUpdate](../entities/schemas_triage_TriageItemUpdate.md) | Pydantic model | 69 | `BaseModel` | Schema for updating a triage item. |
| [TriageItemResponse](../entities/TriageItemResponse.md) | Pydantic model | 105 | `BaseModel` | Schema for triage item response. |
| [TriageActionRequest](../entities/schemas_triage_TriageActionRequest.md) | Pydantic model | 137 | `BaseModel` | Request for simple triage status actions. |
| [TriageSnoozeRequest](../entities/schemas_triage_TriageSnoozeRequest.md) | Pydantic model | 142 | `BaseModel` | Request for snoozing a triage item. |
| [TriageDuplicateRequest](../entities/schemas_triage_TriageDuplicateRequest.md) | Pydantic model | 148 | `BaseModel` | Request for marking a triage item as duplicate. |
| [TriageDuplicateSuggestion](../entities/schemas_triage_TriageDuplicateSuggestion.md) | Pydantic model | 165 | `BaseModel` | Candidate duplicate returned by advisory duplicate search. |
| [TriageDuplicateSuggestionsResponse](../entities/schemas_triage_TriageDuplicateSuggestionsResponse.md) | Pydantic model | 182 | `BaseModel` | Response for advisory duplicate suggestions. |
| [TriageClassificationDraft](../entities/TriageClassificationDraft.md) | Pydantic model | 189 | `BaseModel` | Internal normalized triage classification draft before persistence. |
| [TriageClassificationSuggestionResponse](../entities/TriageClassificationSuggestionResponse.md) | Pydantic model | 209 | `BaseModel` | Stored advisory classification suggestion for a triage item. |
| [TriageTaskDraftRequest](../entities/schemas_triage_TriageTaskDraftRequest.md) | Pydantic model | 234 | `BaseModel` | Request for transient AI-assisted triage task drafting. |
| [TriageTaskDraftResponse](../entities/schemas_triage_TriageTaskDraftResponse.md) | Pydantic model | 244 | `BaseModel` | — |
| [TriageConvertToTaskRequest](../entities/schemas_triage_TriageConvertToTaskRequest.md) | Pydantic model | 269 | `BaseModel` | — |
| [TriageConvertToBacklogRequest](../entities/TriageConvertToBacklogRequest.md) | Pydantic model | 294 | `TriageConvertToTaskRequest` | Explicit project backlog destination; the legacy iteration contract stays required. |
| [TriageConvertToTaskResponse](../entities/schemas_triage_TriageConvertToTaskResponse.md) | Pydantic model | 301 | `BaseModel` | Response for triage item conversion. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `current_triage_brief` | `(description, metadata)` | — | — |
