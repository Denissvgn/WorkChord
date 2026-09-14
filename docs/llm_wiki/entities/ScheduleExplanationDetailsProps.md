# ScheduleExplanationDetailsProps

**Location:** `frontend/src/components/gantt/ScheduleExplanationDetails.tsx:12`
**Kind:** Class
**Bases:** —
**Module:** [ScheduleExplanationDetails](../modules/ScheduleExplanationDetails.md)

## Description

_Auto-generated from `ScheduleExplanationDetailsProps` in `frontend/src/components/gantt/ScheduleExplanationDetails.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `decisions` | `ScheduleDecisionExplanation[]` | *required* | — |
| `taskLookup` | `Map<number, GanttTask>` | *required* | — |
| `memberVacations` | `Record<number, string[]>` | *required* | — |
| `workloadBalanced` | `boolean` | *required* | — |
| `workloadIssues` | `string[]` | *required* | — |
| `onOpenTask` | `(task: GanttTask) => void` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ScheduleExplanationDetailsProps (frontend/src/components/gantt/ScheduleExplanationDetails.tsx)"]
    n1["ScheduleExplanationDetails (frontend/src/components/gantt/ScheduleExplanationDetails.tsx)"]
    n1 --> n0
    click n0 "../modules/ScheduleExplanationDetails.md"
    click n1 "../modules/ScheduleExplanationDetails.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [ScheduleExplanationDetails](../modules/ScheduleExplanationDetails.md) | 0 | `decisions`, `memberVacations`, `onOpenTask`, `taskLookup`, `workloadBalanced`, `workloadIssues` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ScheduleExplanationDetails` | type_reference | [ScheduleExplanationDetails](../modules/ScheduleExplanationDetails.md) | — |
