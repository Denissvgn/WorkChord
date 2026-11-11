# seedDisplay Module

**Path:** `frontend/src/i18n/seedDisplay.ts`

## Description

_Auto-generated from `frontend/src/i18n/seedDisplay.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/github` | `GitHubStatusAutomationRule` | Declaration | erased |
| `../types/label` | `Label`, `LabelGroup` | Declaration | erased |
| `../types/savedView` | `SavedView`, `SavedViewDashboardCard` | Declaration | erased |
| `../types/template` | `WorkTemplate` | Declaration | erased |
| `./i18n` | `i18n` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `githubRuleDisplay`, `labelDisplay`, `labelGroupDisplay`, `savedViewDisplay`, `templateDisplay` |
| Constants | `templateBaselines`, `labelGroupBaselines`, `labelBaselines`, `savedViewBaselines`, `githubRuleBaselines` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/i18n/seedDisplay.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/seedDisplay.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (12) |
| Outbound | `frontend` (5) |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TemplateSeedBaseline](../entities/TemplateSeedBaseline.md) | Interface | 7 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `labelGroupDisplay` | `(group: LabelGroup \| { seed_key?: string \| null; name: string; description?: string \| null })` | — | — |
| `labelDisplay` | `(label: Label \| { seed_key?: string \| null; name: string; description?: string \| null })` | — | — |
| `templateDisplay` | `(template: WorkTemplate)` | — | — |
| `savedViewDisplay` | `(view: SavedView \| SavedViewDashboardCard)` | — | — |
| `githubRuleDisplay` | `(rule: GitHubStatusAutomationRule)` | — | — |
