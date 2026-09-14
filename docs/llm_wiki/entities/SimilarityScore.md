# SimilarityScore

**Location:** `backend/app/utils/text_similarity.py:32`
**Kind:** Class
**Bases:** —
**Module:** [text_similarity](../modules/text_similarity.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Score returned for a similarity document.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `key` | `str` | *required* | — |
| `score` | `float` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SimilarityScore (backend/app/utils/text_similarity.py)"]
    n1["BM25Similarity.score (backend/app/utils/text_similarity.py)"]
    n1 --> n0
    click n0 "../modules/text_similarity.md"
    click n1 "../modules/text_similarity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [text_similarity](../modules/text_similarity.md) | 0 | `key`, `score` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `BM25Similarity.score` | call | [text_similarity](../modules/text_similarity.md) | 2 |
| `BM25Similarity.score` | type_reference | [text_similarity](../modules/text_similarity.md) | — |
