# github_status_automation_service Module

**Path:** `backend/app/services/github_status_automation_service.py`

## Description

GitHub status automation rule service.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.models.agent` | `TaskEvent` |
| `app.models.github` | `GitHubStatusAutomationRule` |
| `app.models.task` | `TaskStatus` |
| `app.schemas.github` | `GitHubStatusAutomationResult`, `GitHubStatusAutomationRuleCreate`, `GitHubStatusAutomationRuleUpdate` |
| `app.services.language_service` | `LanguageCode`, `backend_error_message`, `entity_not_found_message`, `invalid_status_transition_message`, `localized`, `resolve_runtime_ui_language` |
| `app.services.task_service` | `TaskService` |
| `collections` | `defaultdict` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/github.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/routers/github.py"]
    n5["backend/app/schemas/github.py"]
    n6["backend/app/services/github_status_automation_service.py"]
    n7["backend/app/services/github_webhook_service.py"]
    n8["backend/app/services/language_service.py"]
    n9["backend/app/services/task_service.py"]
    n10["backend/app/services/upgrade_service.py"]
    n0 --> n3
    n0 --> n9
    n1 --> n3
    n3 --> n1
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n6 --> n8
    n6 --> n9
    n7 --> n0
    n7 --> n1
    n7 --> n5
    n7 --> n6
    n7 --> n8
    n7 --> n9
    n9 --> n0
    n9 --> n1
    n9 --> n3
    n9 --> n8
    n10 --> n0
    n10 --> n6
    click n0 "../modules/commands.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_github.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/routers_github.md"
    click n5 "../modules/schemas_github.md"
    click n6 "../modules/github_status_automation_service.md"
    click n7 "../modules/github_webhook_service.md"
    click n8 "../modules/language_service.md"
    click n9 "../modules/task_service.md"
    click n10 "../modules/upgrade_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_github](../modules/routers_github.md) |
| Inbound | [github_webhook_service](../modules/github_webhook_service.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_github](../modules/models_github.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_github](../modules/schemas_github.md) |
| Outbound | [language_service](../modules/language_service.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [_SafeFormatDict](../entities/SafeFormatDict.md) | 70 | `defaultdict` | Leave unknown reason-template placeholders readable. |
| [GitHubStatusAutomationService](../entities/GitHubStatusAutomationService.md) | 77 | — | Manage and apply GitHub status automation rules. |
