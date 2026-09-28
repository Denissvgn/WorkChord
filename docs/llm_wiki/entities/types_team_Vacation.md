# Vacation

**Location:** `frontend/src/types/team.ts:1`
**Kind:** Class
**Bases:** —
**Module:** [types_team](../modules/types_team.md)

## Description

_Auto-generated from `Vacation` in `frontend/src/types/team.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `start_date` | `string` | Yes | — | — |
| `end_date` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Vacation (frontend/src/types/team.ts)"]
    n1["VacationManager (frontend/src/components/team/VacationManager.tsx)"]
    n2["frontend/src/pages/CalendarPage.tsx"]
    n3["frontend/src/services/teamService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_team.md"
    click n1 "../modules/VacationManager.md"
    click n2 "../modules/CalendarPage.md"
    click n3 "../modules/teamService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_team](../modules/types_team.md) | 0 | `end_date`, `id`, `start_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `VacationManager` | type_reference | [VacationManager](../modules/VacationManager.md) | — |
| `CalendarPage` | import | [CalendarPage](../modules/CalendarPage.md) | — |
| `teamService` | import | [teamService](../modules/teamService.md) | — |
