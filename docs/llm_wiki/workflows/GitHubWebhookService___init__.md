# GitHubWebhookService___init__

**Entry point:** `github_webhook_service.GitHubWebhookService.__init__`
**Modules involved:** [config](../modules/config.md), [github_status_automation_service](../modules/github_status_automation_service.md), [github_status_service](../modules/github_status_service.md), [github_webhook_service](../modules/github_webhook_service.md), [task_service](../modules/task_service.md), [triage_service](../modules/triage_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `task_service.TaskService`
3. `triage_service.TriageService`
4. `github_status_service.GitHubStatusService`
5. `github_status_automation_service.GitHubStatusAutomationService`

## Touches

- [config](../modules/config.md)
- [github_status_automation_service](../modules/github_status_automation_service.md)
- [github_status_service](../modules/github_status_service.md)
- [github_webhook_service](../modules/github_webhook_service.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `github_webhook_service.GitHubWebhookService.__init__`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
