# BM25Similarity

**Location:** `backend/app/utils/text_similarity.py:38`
**Kind:** Class
**Bases:** —
**Module:** [text_similarity](../modules/text_similarity.md)

## Description

Small BM25-style scorer for in-memory candidate sets.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(k1: float = 1.5, b: float = 0.75)` | — | — |
| `fit` | `(documents: list[SimilarityDocument]) -> None` | — | Build the scorer index from documents. |
| `score` | `(query: str) -> list[SimilarityScore]` | — | Score indexed documents against a query. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["BM25Similarity (backend/app/utils/text_similarity.py)"]
    n1["TriageService.get_duplicate_suggestions (backend/app/services/triage_service.py)"]
    n1 --> n0
    click n0 "../modules/text_similarity.md"
    click n1 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [text_similarity](../modules/text_similarity.md) | 3 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TriageService.get_duplicate_suggestions` | call | [triage_service](../modules/triage_service.md) | 1 |
