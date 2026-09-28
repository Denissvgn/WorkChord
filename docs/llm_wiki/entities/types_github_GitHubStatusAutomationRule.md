# GitHubStatusAutomationRule

**Location:** `frontend/src/types/github.ts:14`
**Kind:** Class
**Bases:** —
**Module:** [types_github](../modules/types_github.md)

## Description

_Auto-generated from `GitHubStatusAutomationRule` in `frontend/src/types/github.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `description` | `string \| null` | No | — | — |
| `enabled` | `boolean` | Yes | — | — |
| `github_event_type` | `GitHubAutomationEventType` | Yes | — | — |
| `from_status` | `TaskStatus \| null` | No | — | — |
| `target_status` | `GitHubAutomationTargetStatus` | Yes | — | — |
| `reason_template` | `string \| null` | No | — | — |
| `sort_order` | `number` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubStatusAutomationRule (frontend/src/types/github.ts)"]
    n1["frontend/src/components/settings/GitHubSettingsPanel.test.tsx"]
    n2["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n3["githubRuleDisplay (frontend/src/i18n/seedDisplay.ts)"]
    n4["frontend/src/services/githubService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_github.md"
    click n1 "../modules/GitHubSettingsPanel.test.md"
    click n2 "../modules/GitHubSettingsPanel.md"
    click n3 "../modules/seedDisplay.md"
    click n4 "../modules/githubService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_github](../modules/types_github.md) | 0 | `created_at`, `description`, `enabled`, `from_status`, `github_event_type`, `id`, `name`, `reason_template`, `sort_order`, `target_status`, `updated_at` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `GitHubSettingsPanel.test` | import | [GitHubSettingsPanel.test](../modules/GitHubSettingsPanel.test.md) | — |
| `GitHubSettingsPanel` | import | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) | — |
| `githubRuleDisplay` | type_reference | [seedDisplay](../modules/seedDisplay.md) | — |
| `githubService` | import | [githubService](../modules/githubService.md) | — |
