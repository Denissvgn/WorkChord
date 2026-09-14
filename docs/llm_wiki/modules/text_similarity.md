# text_similarity Module

**Path:** `backend/app/utils/text_similarity.py`

## Description

Lightweight text similarity helpers for advisory search.

## Imports

| Source | Symbols |
|--------|---------|
| `collections` | `Counter` |
| `dataclasses` | `dataclass` |
| `math` | `math` |
| `re` | `re` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/triage_service.py"]
    n1["backend/app/utils/text_similarity.py"]
    n0 --> n1
    click n0 "../modules/triage_service.md"
    click n1 "../modules/text_similarity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [triage_service](../modules/triage_service.md) |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SimilarityDocument](../entities/SimilarityDocument.md) | 25 | — | Document used by the BM25 similarity scorer. |
| [SimilarityScore](../entities/SimilarityScore.md) | 32 | — | Score returned for a similarity document. |
| [BM25Similarity](../entities/BM25Similarity.md) | 38 | — | Small BM25-style scorer for in-memory candidate sets. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalize_text` | `(value: str \| None) -> str` | — | Normalize text for exact comparisons. |
| `tokenize_text` | `(value: str \| None) -> list[str]` | — | Tokenize text for BM25 scoring. |
