# GitHubStatusService___init__

**Entry point:** `github_status_service.GitHubStatusService.__init__`
**Modules involved:** [config](../modules/config.md), [external_link_service](../modules/external_link_service.md), [github_status_service](../modules/github_status_service.md), [url_policy](../modules/url_policy.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `url_policy.normalize_provider_api_url`
3. `external_link_service.ExternalLinkService`

## Touches

- [config](../modules/config.md)
- [external_link_service](../modules/external_link_service.md)
- [github_status_service](../modules/github_status_service.md)
- [url_policy](../modules/url_policy.md)

## Behavior

This workflow starts at `github_status_service.GitHubStatusService.__init__`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
