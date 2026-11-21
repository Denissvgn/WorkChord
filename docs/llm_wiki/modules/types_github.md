# github Module

**Path:** `frontend/src/types/github.ts`

## Description

_Auto-generated from `frontend/src/types/github.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./task` | `TaskStatus` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `GitHubAutomationEventType`, `GitHubAutomationOutcome`, `GitHubAutomationTargetStatus`, `GitHubStatusAutomationResult`, `GitHubStatusAutomationRule`, `GitHubStatusAutomationRuleCreate`, `GitHubStatusAutomationRuleUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/GitHubSettingsPanel.test.tsx"]
    n1["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n2["frontend/src/i18n/seedDisplay.ts"]
    n3["frontend/src/pages/SettingsPage.labels.test.tsx"]
    n4["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n5["frontend/src/services/githubService.ts"]
    n6["frontend/src/types/github.ts"]
    n7["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n6
    n1 --> n2
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n2 --> n6
    n3 --> n6
    n4 --> n6
    n5 --> n6
    n6 --> n7
    click n0 "../modules/GitHubSettingsPanel.test.md"
    click n1 "../modules/GitHubSettingsPanel.md"
    click n2 "../modules/seedDisplay.md"
    click n3 "../modules/SettingsPage.labels.test.md"
    click n4 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n5 "../modules/githubService.md"
    click n6 "../modules/types_github.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GitHubSettingsPanel.test](../modules/GitHubSettingsPanel.test.md) |
| Inbound | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) |
| Inbound | [seedDisplay](../modules/seedDisplay.md) |
| Inbound | [SettingsPage.labels.test](../modules/SettingsPage.labels.test.md) |
| Inbound | [SettingsPage.readOnlyPanels.test](../modules/SettingsPage.readOnlyPanels.test.md) |
| Inbound | [githubService](../modules/githubService.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GitHubStatusAutomationRule](../entities/types_github_GitHubStatusAutomationRule.md) | Interface | 14 | — | — |
| [GitHubStatusAutomationRuleCreate](../entities/types_github_GitHubStatusAutomationRuleCreate.md) | Interface | 28 | — | — |
| [GitHubStatusAutomationResult](../entities/types_github_GitHubStatusAutomationResult.md) | Interface | 41 | — | — |
| [GitHubAutomationEventType](../entities/types_github_GitHubAutomationEventType.md) | Type alias | 3 | <pre><code>&#124; &#39;github&#95;pr&#95;opened&#39;&#10;    &#124; &#39;github&#95;pr&#95;reopened&#39;&#10;    &#124; &#39;github&#95;pr&#95;ready&#95;for&#95;review&#39;&#10;    &#124; &#39;github&#95;pr&#95;synchronize&#39;&#10;    &#124; &#39;github&#95;pr&#95;closed&#39;&#10;    &#124; &#39;github&#95;pr&#95;merged&#39;</code></pre> | — |
| [GitHubAutomationTargetStatus](../entities/types_github_GitHubAutomationTargetStatus.md) | Type alias | 11 | `Exclude<TaskStatus, 'planned'>` | — |
| [GitHubAutomationOutcome](../entities/types_github_GitHubAutomationOutcome.md) | Type alias | 12 | `'applied' \| 'skipped' \| 'failed'` | — |
| [GitHubStatusAutomationRuleUpdate](../entities/types_github_GitHubStatusAutomationRuleUpdate.md) | Type alias | 39 | `Partial<GitHubStatusAutomationRuleCreate>` | — |
