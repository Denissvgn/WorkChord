# githubService Module

**Path:** `frontend/src/services/githubService.ts`

## Description

_Auto-generated from `frontend/src/services/githubService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/github` | `GitHubStatusAutomationRule`, `GitHubStatusAutomationRuleCreate`, `GitHubStatusAutomationRuleUpdate` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `githubService` |
| Constants | `githubService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/githubService.ts"]
    n3["frontend/src/types/github.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/GitHubSettingsPanel.md"
    click n1 "../modules/api.md"
    click n2 "../modules/githubService.md"
    click n3 "../modules/types_github.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_github](../modules/types_github.md) |
