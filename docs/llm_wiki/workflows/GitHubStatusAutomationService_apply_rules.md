# GitHubStatusAutomationService_apply_rules

**Entry point:** `github_status_automation_service.GitHubStatusAutomationService.apply_rules`
**Modules involved:** [github_status_automation_service](../modules/github_status_automation_service.md), [language_service](../modules/language_service.md), [models_task](../modules/models_task.md), [schemas_github](../modules/schemas_github.md)

> Apply enabled rules for a matched GitHub webhook event.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `language_service.resolve_runtime_ui_language`
2. `schemas_github.GitHubStatusAutomationResult`
3. `language_service.entity_not_found_message`
4. `schemas_github.GitHubStatusAutomationResult`
5. `language_service.backend_error_message`
6. `schemas_github.GitHubStatusAutomationResult`
7. `language_service.backend_error_message`
8. `schemas_github.GitHubStatusAutomationResult`
9. `language_service.backend_error_message`
10. `models_task.TaskStatus`
11. `schemas_github.GitHubStatusAutomationResult`
12. `language_service.invalid_status_transition_message`
13. `schemas_github.GitHubStatusAutomationResult`
14. `schemas_github.GitHubStatusAutomationResult`

## Touches

- [github_status_automation_service](../modules/github_status_automation_service.md)
- [language_service](../modules/language_service.md)
- [models_task](../modules/models_task.md)
- [schemas_github](../modules/schemas_github.md)

## Behavior

This workflow starts at `github_status_automation_service.GitHubStatusAutomationService.apply_rules`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
