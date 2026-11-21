# RememberedScope

**Location:** `frontend/src/features/scope/scopeStore.ts:10`
**Kind:** Interface
**Bases:** —
**Module:** [scopeStore](../modules/scopeStore.md)

## Description

_Auto-generated from `RememberedScope` in `frontend/src/features/scope/scopeStore.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `project` | `ScopeProject \| null` | Yes | — | — |
| `iteration` | `ScopeIteration \| null` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RememberedScope (frontend/src/features/scope/scopeStore.ts)"]
    n1["ScopeStore (frontend/src/features/scope/scopeStore.ts)"]
    n2["linkScope (frontend/src/features/scope/useScopeLink.ts)"]
    n3["frontend/src/features/scope/useWorkScope.ts"]
    n4["frontend/src/store/iterationStore.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/scopeStore.md"
    click n1 "../modules/scopeStore.md"
    click n2 "../modules/useScopeLink.md"
    click n3 "../modules/useWorkScope.md"
    click n4 "../modules/iterationStore.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [scopeStore](../modules/scopeStore.md) | 0 | `iteration`, `project` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `ScopeStore` | [scopeStore](../modules/scopeStore.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `linkScope` | type_reference | [useScopeLink](../modules/useScopeLink.md) | — |
| `useWorkScope` | import | [useWorkScope](../modules/useWorkScope.md) | — |
| `iterationStore` | import | [iterationStore](../modules/iterationStore.md) | — |
