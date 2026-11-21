# ExternalLinkService_create_release_github_link

**Entry point:** `external_link_service.ExternalLinkService.create_release_github_link`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [external_link_service](../modules/external_link_service.md), [schemas_external_link](../modules/schemas_external_link.md)

> Parse and link a GitHub pull request, commit, branch, or tag to a release.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `schemas_external_link.ExternalLinkCreate`
3. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [external_link_service](../modules/external_link_service.md)
- [schemas_external_link](../modules/schemas_external_link.md)

## Behavior

The release must exist before the service normalizes the GitHub URL. It checks for a duplicate on that release, creates the link and emits the creation event inside the same transaction.
