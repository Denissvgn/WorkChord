# github Module

**Path:** `backend/app/schemas/github.py`

## Description

GitHub integration schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `datetime` |
| `pydantic` | `BaseModel`, `Field` |
| `typing` | `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/github.py"]
    n2["backend/app/routers/task_domain.py"]
    n3["backend/app/schemas/__init__.py"]
    n4["backend/app/schemas/github.py"]
    n5["backend/app/services/github_status_automation_service.py"]
    n6["backend/app/services/github_webhook_service.py"]
    n0 --> n4
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n4
    n3 --> n4
    n5 --> n4
    n6 --> n4
    n6 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_github.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/schemas_github.md"
    click n5 "../modules/github_status_automation_service.md"
    click n6 "../modules/github_webhook_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_github](../modules/routers_github.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [schemas___init__](../modules/schemas___init__.md) |
| Inbound | [github_status_automation_service](../modules/github_status_automation_service.md) |
| Inbound | [github_webhook_service](../modules/github_webhook_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GitHubAutomationEventType](../entities/schemas_github_GitHubAutomationEventType.md) | Type alias | 7 | `Literal['github_pr_opened', 'github_pr_reopened', 'github_pr_ready_for_review', 'github_pr_synchronize', 'github_pr_closed', 'github_pr_merged']` | — |
| [GitHubAutomationFromStatus](../entities/GitHubAutomationFromStatus.md) | Type alias | 15 | `Literal['planned', 'active', 'resolved', 'closed']` | — |
| [GitHubAutomationTargetStatus](../entities/schemas_github_GitHubAutomationTargetStatus.md) | Type alias | 16 | `Literal['active', 'resolved', 'closed']` | — |
| [GitHubAutomationOutcome](../entities/schemas_github_GitHubAutomationOutcome.md) | Type alias | 17 | `Literal['applied', 'skipped', 'failed']` | — |
| [GitHubStatusAutomationRuleBase](../entities/GitHubStatusAutomationRuleBase.md) | Pydantic model | 20 | `BaseModel` | Shared GitHub status automation rule fields. |
| [GitHubStatusAutomationRuleCreate](../entities/schemas_github_GitHubStatusAutomationRuleCreate.md) | Pydantic model | 33 | `GitHubStatusAutomationRuleBase` | Create a GitHub status automation rule. |
| [GitHubStatusAutomationRuleUpdate](../entities/schemas_github_GitHubStatusAutomationRuleUpdate.md) | Pydantic model | 37 | `BaseModel` | Update a GitHub status automation rule. |
| [GitHubStatusAutomationRuleResponse](../entities/GitHubStatusAutomationRuleResponse.md) | Pydantic model | 50 | `GitHubStatusAutomationRuleBase` | Response for one GitHub status automation rule. |
| [GitHubStatusAutomationResult](../entities/schemas_github_GitHubStatusAutomationResult.md) | Pydantic model | 61 | `BaseModel` | Result of applying one GitHub status automation rule. |
| [GitHubWebhookResponse](../entities/GitHubWebhookResponse.md) | Pydantic model | 72 | `BaseModel` | Response returned after receiving a GitHub webhook delivery. |
| [GitHubSubmissionReview](../entities/GitHubSubmissionReview.md) | Pydantic model | 86 | `BaseModel` | One review assignment bound to a submitted commit. |
| [GitHubPullSubmission](../entities/schemas_github_GitHubPullSubmission.md) | Pydantic model | 94 | `BaseModel` | One run's submitted commit for a pull request, with the review that saw it. |
| [GitHubPullChecks](../entities/GitHubPullChecks.md) | Pydantic model | 105 | `BaseModel` | Checks GitHub reported for the observed head commit. |
| [GitHubPullReview](../entities/GitHubPullReview.md) | Pydantic model | 114 | `BaseModel` | The WorkChord review state of the task, decided only by the independent reviewer. |
| [GitHubPullReconciliation](../entities/schemas_github_GitHubPullReconciliation.md) | Pydantic model | 121 | `BaseModel` | A linked pull request compared with what the task submitted. |
| [GitHubReplacementRole](../entities/GitHubReplacementRole.md) | Pydantic model | 146 | `BaseModel` | The replacement disposition the task takes part in. |
| [GitHubSuccessor](../entities/GitHubSuccessor.md) | Pydantic model | 154 | `BaseModel` | The task that replaced this one, with its own pull requests. |
| [GitHubReconciliationResponse](../entities/GitHubReconciliationResponse.md) | Pydantic model | 162 | `BaseModel` | What a task submitted against what GitHub shows now, and who acts next. |
