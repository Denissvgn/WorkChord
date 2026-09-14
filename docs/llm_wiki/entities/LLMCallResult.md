# LLMCallResult

**Location:** `backend/app/services/llm_service.py:42`
**Kind:** Class
**Bases:** —
**Module:** [llm_service](../modules/llm_service.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Normalized OpenAI-compatible chat completion result.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `str` | *required* | — |
| `finish_reason` | `Optional[str]` | `None` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `is_truncated` | `() -> bool` | `@property` | Whether the provider stopped because the token limit was reached. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LLMCallResult (backend/app/services/llm_service.py)"]
    n1["LLMService._call_llm_result (backend/app/services/llm_service.py)"]
    n2["LLMService._enhance_explanation (backend/app/services/llm_service.py)"]
    n3["LLMService._normalize_task_ai_response (backend/app/services/llm_service.py)"]
    n4["LLMService.draft_triage_task (backend/app/services/llm_service.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/llm_service.md"
    click n1 "../modules/llm_service.md"
    click n2 "../modules/llm_service.md"
    click n3 "../modules/llm_service.md"
    click n4 "../modules/llm_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [llm_service](../modules/llm_service.md) | 1 | `content`, `finish_reason` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `LLMService._call_llm_result` | call | [llm_service](../modules/llm_service.md) | 1 |
| `LLMService._call_llm_result` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._enhance_explanation` | call | [llm_service](../modules/llm_service.md) | 1 |
| `LLMService._enhance_explanation` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._normalize_task_ai_response` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService.draft_triage_task` | call | [llm_service](../modules/llm_service.md) | 1 |
