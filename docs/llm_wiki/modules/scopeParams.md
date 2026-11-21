# scopeParams Module

**Path:** `frontend/src/navigation/scopeParams.ts`

## Description

_Auto-generated from `frontend/src/navigation/scopeParams.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `formatScope`, `parseScope` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/SampleProjectAction.tsx"]
    n1["frontend/src/features/scope/namedIteration.ts"]
    n2["frontend/src/features/scope/useScopeLink.ts"]
    n3["frontend/src/features/scope/useWorkScope.ts"]
    n4["frontend/src/features/scope/workScope.ts"]
    n5["frontend/src/navigation/scopeParams.check.test.ts"]
    n6["frontend/src/navigation/scopeParams.ts"]
    n7["frontend/src/store/iterationStore.ts"]
    n0 --> n3
    n0 --> n4
    n0 --> n6
    n1 --> n6
    n2 --> n4
    n2 --> n6
    n3 --> n1
    n3 --> n4
    n3 --> n6
    n4 --> n6
    n5 --> n6
    n7 --> n4
    n7 --> n6
    click n0 "../modules/SampleProjectAction.md"
    click n1 "../modules/namedIteration.md"
    click n2 "../modules/useScopeLink.md"
    click n3 "../modules/useWorkScope.md"
    click n4 "../modules/workScope.md"
    click n5 "../modules/scopeParams.check.test.md"
    click n6 "../modules/scopeParams.md"
    click n7 "../modules/iterationStore.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SampleProjectAction](../modules/SampleProjectAction.md) |
| Inbound | [namedIteration](../modules/namedIteration.md) |
| Inbound | [useScopeLink](../modules/useScopeLink.md) |
| Inbound | [useWorkScope](../modules/useWorkScope.md) |
| Inbound | [workScope](../modules/workScope.md) |
| Inbound | [scopeParams.check.test](../modules/scopeParams.check.test.md) |
| Inbound | [iterationStore](../modules/iterationStore.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Scope](../entities/scopeParams_Scope.md) | Type alias | 1 | `{ project: number \| 'all'; iteration: number \| 'backlog' }` | — |
| [ParsedScope](../entities/scopeParams_ParsedScope.md) | Type alias | 2 | `Partial<Scope>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `parseScope` | `(search: string) -> ParsedScope` | — | — |
| `formatScope` | `(scope: Scope, search: string) -> string` | — | — |
