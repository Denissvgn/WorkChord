# GitHubWebhookService_process

**Entry point:** `github_webhook_service.GitHubWebhookService.process`
**Modules involved:** [commands](../modules/commands.md), [github_webhook_service](../modules/github_webhook_service.md), [language_service](../modules/language_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [schemas_github](../modules/schemas_github.md)

> Process one verified GitHub webhook payload.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_github.GitHubWebhookResponse`
2. `schemas_github.GitHubWebhookResponse`
3. `schemas_github.GitHubWebhookResponse`
4. `language_service.resolve_runtime_ui_language`
5. `schemas_github.GitHubWebhookResponse`
6. `outbound_webhook_service.emit_outbound_webhook_event`
7. `commands.commit_or_flush`
8. `schemas_github.GitHubWebhookResponse`
9. `outbound_webhook_service.emit_outbound_webhook_event`
10. `commands.commit_or_flush`
11. `schemas_github.GitHubWebhookResponse`

## Touches

- [commands](../modules/commands.md)
- [github_webhook_service](../modules/github_webhook_service.md)
- [language_service](../modules/language_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [schemas_github](../modules/schemas_github.md)

## Behavior

This workflow starts at `github_webhook_service.GitHubWebhookService.process`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
