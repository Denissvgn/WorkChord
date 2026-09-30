# GitHubSettingsPanel.test Module

**Path:** `frontend/src/components/settings/GitHubSettingsPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/GitHubSettingsPanel.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../../types/github` | `GitHubStatusAutomationRule` |
| `./GitHubSettingsPanel` | `GitHubSettingsPanel` |
| `@testing-library/react` | `fireEvent`, `screen`, `waitFor`, `within` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `githubServiceMock` |
| Module calls | `githubServiceMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/GitHubSettingsPanel.test.tsx"]
    n1["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/github.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/GitHubSettingsPanel.test.md"
    click n1 "../modules/GitHubSettingsPanel.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_github.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_github](../modules/types_github.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
