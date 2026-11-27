# GitHubLinkError

**Location:** `backend/app/utils/github_links.py:17`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [github_links](../modules/github_links.md)

## Description

Raised when a URL is not a supported GitHub link.

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubLinkError (backend/app/utils/github_links.py)"]
    n1["ValueError"]
    n2["backend/app/services/agent_work_service.py"]
    n3["backend/app/services/external_link_service.py"]
    n4["backend/app/services/github_reconciliation_service.py"]
    n5["backend/app/services/manual_provenance_service.py"]
    n6["backend/app/services/review_provenance.py"]
    n7["backend/app/services/task_replacement_service.py"]
    n8["_commit (backend/app/utils/github_links.py)"]
    n9["parse_github_url (backend/app/utils/github_links.py)"]
    n10["require_github_link (backend/app/utils/github_links.py)"]
    n11["backend/tests/test_work_delivery_links.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/github_links.md"
    click n2 "../modules/agent_work_service.md"
    click n3 "../modules/external_link_service.md"
    click n4 "../modules/github_reconciliation_service.md"
    click n5 "../modules/manual_provenance_service.md"
    click n6 "../modules/review_provenance.md"
    click n7 "../modules/task_replacement_service.md"
    click n8 "../modules/github_links.md"
    click n9 "../modules/github_links.md"
    click n10 "../modules/github_links.md"
    click n11 "../modules/test_work_delivery_links.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [github_links](../modules/github_links.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent_work_service` | import | [agent_work_service](../modules/agent_work_service.md) | — |
| `external_link_service` | import | [external_link_service](../modules/external_link_service.md) | — |
| `github_reconciliation_service` | import | [github_reconciliation_service](../modules/github_reconciliation_service.md) | — |
| `manual_provenance_service` | import | [manual_provenance_service](../modules/manual_provenance_service.md) | — |
| `review_provenance` | import | [review_provenance](../modules/review_provenance.md) | — |
| `task_replacement_service` | import | [task_replacement_service](../modules/task_replacement_service.md) | — |
| `_commit` | call | [github_links](../modules/github_links.md) | 1 |
| `parse_github_url` | call | [github_links](../modules/github_links.md) | 4 |
| `require_github_link` | call | [github_links](../modules/github_links.md) | 1 |
| `test_work_delivery_links` | import | [test_work_delivery_links](../modules/test_work_delivery_links.md) | — |
