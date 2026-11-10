# TaskDiscussion.test Module

**Path:** `frontend/src/components/tasks/TaskDiscussion.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskDiscussion.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./TaskDiscussion` | `TaskDiscussion` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service` |
| Module calls | `service = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskDiscussion.test.tsx"]
    n1["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    click n0 "../modules/TaskDiscussion.test.md"
    click n1 "../modules/TaskDiscussion.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
