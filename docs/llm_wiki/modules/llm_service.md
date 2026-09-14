# llm_service Module

**Path:** `backend/app/services/llm_service.py`

## Description

LLM service for task formalization and schedule explanation.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `get_settings` |
| `app.schemas.gantt` | `SchedulingDecision`, `WorkloadIssue` |
| `app.schemas.llm` | `FormalizeResponse`, `SuggestedSubtask`, `ImproveDescriptionResponse`, `ExplainScheduleResponse`, `ScheduleDecisionExplanation`, `WorkloadAnalysis`, `GroundedAISuggestionResponse`, `GroundedFact` |
| `app.schemas.triage` | `TriageClassificationDraft`, `TriageTaskDraftResponse` |
| `app.services.language_service` | `AILanguageMode`, `LanguageCode`, `language_instruction`, `localized`, `normalize_ai_language_mode`, `normalize_language`, `resolve_ai_language` |
| `app.utils.url_policy` | `normalize_provider_api_url` |
| `collections` | `Counter` |
| `dataclasses` | `dataclass` |
| `httpx` | `httpx` |
| `json` | `json` |
| `logging` | `logging` |
| `re` | `re` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/routers/llm.py"]
    n2["backend/app/routers/triage.py"]
    n3["backend/app/schemas/gantt.py"]
    n4["backend/app/schemas/llm.py"]
    n5["backend/app/schemas/triage.py"]
    n6["backend/app/services/language_service.py"]
    n7["backend/app/services/llm_service.py"]
    n8["backend/app/services/triage_service.py"]
    n9["backend/app/utils/url_policy.py"]
    n1 --> n4
    n1 --> n7
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n6 --> n0
    n7 --> n0
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    n7 --> n9
    n8 --> n5
    n8 --> n7
    n9 --> n0
    click n0 "../modules/config.md"
    click n1 "../modules/routers_llm.md"
    click n2 "../modules/routers_triage.md"
    click n3 "../modules/schemas_gantt.md"
    click n4 "../modules/schemas_llm.md"
    click n5 "../modules/schemas_triage.md"
    click n6 "../modules/language_service.md"
    click n7 "../modules/llm_service.md"
    click n8 "../modules/triage_service.md"
    click n9 "../modules/url_policy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_llm](../modules/routers_llm.md) |
| Inbound | [routers_triage](../modules/routers_triage.md) |
| Inbound | [triage_service](../modules/triage_service.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [schemas_gantt](../modules/schemas_gantt.md) |
| Outbound | [schemas_llm](../modules/schemas_llm.md) |
| Outbound | [schemas_triage](../modules/schemas_triage.md) |
| Outbound | [language_service](../modules/language_service.md) |
| Outbound | [url_policy](../modules/url_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [LLMCallResult](../entities/LLMCallResult.md) | 42 | — | Normalized OpenAI-compatible chat completion result. |
| [LLMService](../entities/LLMService.md) | 54 | — | Service for LLM-powered features. |
