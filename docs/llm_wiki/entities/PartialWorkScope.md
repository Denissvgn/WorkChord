# PartialWorkScope

**Location:** `frontend/src/features/scope/workScope.ts:16`
**Kind:** Interface
**Bases:** —
**Module:** [workScope](../modules/workScope.md)

## Description

A scope that may be incomplete: read from the URL, remembered, or just chosen.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `project` | `ScopeProject \| null` | No | — | — |
| `iteration` | `ScopeIteration \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PartialWorkScope (frontend/src/features/scope/workScope.ts)"]
    n1["frontend/src/features/scope/scopeStore.ts"]
    n2["linkScope (frontend/src/features/scope/useScopeLink.ts)"]
    n3["useLinkScope (frontend/src/features/scope/useScopeLink.ts)"]
    n4["frontend/src/features/scope/useWorkScope.ts"]
    n5["isCompleteScope (frontend/src/features/scope/workScope.ts)"]
    n6["resolveWorkScope (frontend/src/features/scope/workScope.ts)"]
    n7["sameScope (frontend/src/features/scope/workScope.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/workScope.md"
    click n1 "../modules/scopeStore.md"
    click n2 "../modules/useScopeLink.md"
    click n3 "../modules/useScopeLink.md"
    click n4 "../modules/useWorkScope.md"
    click n5 "../modules/workScope.md"
    click n6 "../modules/workScope.md"
    click n7 "../modules/workScope.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [workScope](../modules/workScope.md) | 0 | `iteration`, `project` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `scopeStore` | import | [scopeStore](../modules/scopeStore.md) | — |
| `linkScope` | type_reference | [useScopeLink](../modules/useScopeLink.md) | — |
| `useLinkScope` | type_reference | [useScopeLink](../modules/useScopeLink.md) | — |
| `useWorkScope` | import | [useWorkScope](../modules/useWorkScope.md) | — |
| `isCompleteScope` | type_reference | [workScope](../modules/workScope.md) | — |
| `resolveWorkScope` | type_reference | [workScope](../modules/workScope.md) | — |
| `sameScope` | type_reference | [workScope](../modules/workScope.md) | — |
