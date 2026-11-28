# ReviewHistory

**Location:** `backend/app/services/review_provenance.py:677`
**Kind:** Class
**Bases:** —
**Module:** [review_provenance](../modules/review_provenance.md)

**Decorators:** `@dataclass`

## Description

The attribution facts independent review reads for one task: every contributor and its publisher where known, the candidate under review, any manual execution record, and the reviewer profiles a handback requires. Under the project's different-review-publisher policy, a verifier's publisher is refused when it cannot be verified or matches a contributor, so the reviewing model never shares a publisher with the work. A missing manual fact is named rather than guessed.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `contributors` | `list[dict]` | *required* | — |
| `candidate` | `dict \| None` | *required* | — |
| `manual_execution` | `dict \| None` | `None` | — |
| `missing_manual_fact` | `str \| None` | `None` | — |
| `required_reviewer_profiles` | `tuple[int, ...] \| None` | `None` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `permits_profile` | `(profile_id)` | — | — |
| `publisher_blockers` | `(publisher)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReviewHistory (backend/app/services/review_provenance.py)"]
    n1["_attempt_history (backend/app/services/review_provenance.py)"]
    n2["_manual_history (backend/app/services/review_provenance.py)"]
    n3["_run_history (backend/app/services/review_provenance.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/review_provenance.md"
    click n1 "../modules/review_provenance.md"
    click n2 "../modules/review_provenance.md"
    click n3 "../modules/review_provenance.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [review_provenance](../modules/review_provenance.md) | 2 | `candidate`, `contributors`, `manual_execution`, `missing_manual_fact`, `required_reviewer_profiles` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_attempt_history` | call | [review_provenance](../modules/review_provenance.md) | 1 |
| `_manual_history` | call | [review_provenance](../modules/review_provenance.md) | 13 |
| `_run_history` | call | [review_provenance](../modules/review_provenance.md) | 4 |
