# SchedulingRulesResponse

**Location:** `frontend/src/types/schedulingRules.ts:53`
**Kind:** Interface
**Bases:** —
**Module:** [schedulingRules](../modules/schedulingRules.md)

## Description

_Auto-generated from `SchedulingRulesResponse` in `frontend/src/types/schedulingRules.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `rules` | `SchedulingRules` | Yes | — | — |
| `source` | `'yaml' \| 'database' \| 'defaults'` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SchedulingRulesResponse (frontend/src/types/schedulingRules.ts)"]
    n1["frontend/src/components/settings/SchedulingRulesSettings.test.tsx"]
    n2["frontend/src/pages/SettingsPage.labels.test.tsx"]
    n3["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n4["frontend/src/services/schedulingRulesService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schedulingRules.md"
    click n1 "../modules/SchedulingRulesSettings.test.md"
    click n2 "../modules/SettingsPage.labels.test.md"
    click n3 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n4 "../modules/schedulingRulesService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schedulingRules](../modules/schedulingRules.md) | 0 | `rules`, `source` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SchedulingRulesSettings.test` | import | [SchedulingRulesSettings.test](../modules/SchedulingRulesSettings.test.md) | — |
| `SettingsPage.labels.test` | import | [SettingsPage.labels.test](../modules/SettingsPage.labels.test.md) | — |
| `SettingsPage.readOnlyPanels.test` | import | [SettingsPage.readOnlyPanels.test](../modules/SettingsPage.readOnlyPanels.test.md) | — |
| `schedulingRulesService` | import | [schedulingRulesService](../modules/schedulingRulesService.md) | — |
