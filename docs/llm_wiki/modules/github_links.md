# github_links Module

**Path:** `backend/app/utils/github_links.py`

## Description

Parse GitHub URLs that trace delivery work: pull requests, issues, branches, commits and tags.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `dataclasses` | `dataclass` |
| `re` | `re` |
| `typing` | `Any`, `Optional` |
| `urllib.parse` | `urlparse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/schemas/agent.py"]
    n1["backend/app/services/agent_work_service.py"]
    n2["backend/app/services/external_link_service.py"]
    n3["backend/app/services/review_provenance.py"]
    n4["backend/app/utils/github_links.py"]
    n5["backend/tests/test_review_provenance.py"]
    n6["backend/tests/test_work_delivery_links.py"]
    n0 --> n4
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n4
    n3 --> n0
    n3 --> n4
    n5 --> n0
    n5 --> n1
    n5 --> n3
    n5 --> n4
    n6 --> n0
    n6 --> n1
    n6 --> n4
    click n0 "../modules/schemas_agent.md"
    click n1 "../modules/agent_work_service.md"
    click n2 "../modules/external_link_service.md"
    click n3 "../modules/review_provenance.md"
    click n4 "../modules/github_links.md"
    click n5 "../modules/test_review_provenance.md"
    click n6 "../modules/test_work_delivery_links.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [schemas_agent](../modules/schemas_agent.md) |
| Inbound | [agent_work_service](../modules/agent_work_service.md) |
| Inbound | [external_link_service](../modules/external_link_service.md) |
| Inbound | [review_provenance](../modules/review_provenance.md) |
| Inbound | [test_review_provenance](../modules/test_review_provenance.md) |
| Inbound | [test_work_delivery_links](../modules/test_work_delivery_links.md) |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [GitHubLinkError](../entities/GitHubLinkError.md) | 17 | `ValueError` | Raised when a URL is not a supported GitHub link. |
| [ParsedGitHubLink](../entities/ParsedGitHubLink.md) | 22 | — | Normalized GitHub link details ready for persistence. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_commit` | `(owner: str, repo: str, raw_sha: str) -> ParsedGitHubLink` | — | — |
| `parse_github_url` | `(raw_url: str) -> ParsedGitHubLink` | — | Parse a GitHub pull request, issue, branch, commit, or release tag URL. |
| `require_github_link` | `(raw_url: str, github_type: str) -> str` | — | Return the normalized URL when it is a GitHub link of the given type. |
