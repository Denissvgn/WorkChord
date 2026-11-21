# namedIteration Module

**Path:** `frontend/src/features/scope/namedIteration.ts`

## Description

_Auto-generated from `frontend/src/features/scope/namedIteration.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../navigation/scopeParams` | `parseScope` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `forgetCompletedSearchUnless`, `recordCompletedSearch`, `urlNamesIteration` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/scope/namedIteration.test.ts"]
    n1["frontend/src/features/scope/namedIteration.ts"]
    n2["frontend/src/features/scope/useWorkScope.ts"]
    n3["frontend/src/navigation/scopeParams.ts"]
    n4["frontend/src/pages/TasksPage.tsx"]
    n0 --> n1
    n1 --> n3
    n2 --> n1
    n2 --> n3
    n4 --> n1
    n4 --> n2
    click n0 "../modules/namedIteration.test.md"
    click n1 "../modules/namedIteration.md"
    click n2 "../modules/useWorkScope.md"
    click n3 "../modules/scopeParams.md"
    click n4 "../modules/TasksPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [namedIteration.test](../modules/namedIteration.test.md) |
| Inbound | [useWorkScope](../modules/useWorkScope.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [scopeParams](../modules/scopeParams.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `recordCompletedSearch` | `(search: string)` | — | The shell records the search it wrote after adding the scope to a URL that named no iteration. |
| `forgetCompletedSearchUnless` | `(search: string)` | — | The shell forgets the record once the URL has moved on to another search. |
| `urlNamesIteration` | `(search: string) -> boolean` | — | True when the URL names the iteration itself: a link, a reload or a scope already chosen. |
