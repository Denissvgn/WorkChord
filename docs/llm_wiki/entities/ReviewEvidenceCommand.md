# ReviewEvidenceCommand

**Location:** `backend/app/schemas/review_evidence.py:64`
**Kind:** Type alias
**Bases:** —
**Module:** [schemas_review_evidence](../modules/schemas_review_evidence.md)
**Target:** `Annotated[ReviewEvidenceIssue \| ReviewEvidenceRevocation, Field(discriminator='action')]`

## Description

_Auto-generated from `ReviewEvidenceCommand` in `backend/app/schemas/review_evidence.py`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReviewEvidenceCommand (backend/app/schemas/review_evidence.py)"]
    n1["attest_review_evidence (backend/app/routers/agent_catalog.py)"]
    n2["backend/app/services/review_evidence.py"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/schemas_review_evidence.md"
    click n1 "../modules/agent_catalog.md"
    click n2 "../modules/services_review_evidence.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_review_evidence](../modules/schemas_review_evidence.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `attest_review_evidence` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `review_evidence` | import | [services_review_evidence](../modules/services_review_evidence.md) | — |
