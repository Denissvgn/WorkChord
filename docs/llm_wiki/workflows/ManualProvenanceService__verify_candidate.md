# ManualProvenanceService__verify_candidate

**Entry point:** `manual_provenance_service.ManualProvenanceService._verify_candidate`
**Modules involved:** [github_links](../modules/github_links.md), [github_status_service](../modules/github_status_service.md), [manual_provenance_service](../modules/manual_provenance_service.md), [review_provenance](../modules/review_provenance.md)

> Refuse a candidate that the verdict-time check could never pass.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `review_provenance._submission_candidate`
2. `github_links.parse_github_url`
3. `github_links.parse_github_url`
4. `github_links.parse_github_url`
5. `github_links.parse_github_url`
6. `github_status_service.GitHubStatusService.from_runtime`

## Touches

- [github_links](../modules/github_links.md)
- [github_status_service](../modules/github_status_service.md)
- [manual_provenance_service](../modules/manual_provenance_service.md)
- [review_provenance](../modules/review_provenance.md)

## Behavior

This workflow starts at `manual_provenance_service.ManualProvenanceService._verify_candidate`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
