# ScopeIterationRecord

**Location:** `frontend/src/features/scope/workScope.ts:21`
**Kind:** Interface
**Bases:** —
**Module:** [workScope](../modules/workScope.md)

## Description

_Auto-generated from `ScopeIterationRecord` in `frontend/src/features/scope/workScope.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `project_id` | `number \| null` | No | — | — |
| `start_date` | `string` | Yes | — | — |
| `end_date` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ScopeIterationRecord (frontend/src/features/scope/workScope.ts)"]
    n1["frontend/src/features/firstRun/SampleProjectAction.tsx"]
    n2["frontend/src/features/scope/useWorkScope.ts"]
    n3["defaultIterationForProject (frontend/src/features/scope/workScope.ts)"]
    n4["resolveWorkScope (frontend/src/features/scope/workScope.ts)"]
    n5["frontend/src/store/iterationStore.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/workScope.md"
    click n1 "../modules/SampleProjectAction.md"
    click n2 "../modules/useWorkScope.md"
    click n3 "../modules/workScope.md"
    click n4 "../modules/workScope.md"
    click n5 "../modules/iterationStore.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [workScope](../modules/workScope.md) | 0 | `end_date`, `id`, `project_id`, `start_date` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SampleProjectAction` | import | [SampleProjectAction](../modules/SampleProjectAction.md) | — |
| `useWorkScope` | import | [useWorkScope](../modules/useWorkScope.md) | — |
| `defaultIterationForProject` | type_reference | [workScope](../modules/workScope.md) | — |
| `resolveWorkScope` | type_reference | [workScope](../modules/workScope.md) | — |
| `iterationStore` | import | [iterationStore](../modules/iterationStore.md) | — |
