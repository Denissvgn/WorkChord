# identityContext Module

**Path:** `frontend/src/features/identity/identityContext.ts`

## Description

_Auto-generated from `frontend/src/features/identity/identityContext.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./identityService` | `WorkspaceIdentity` |
| `react` | `createContext`, `useContext` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IdentityContext`, `useIdentity` |
| Constants | `IdentityContext` |
| Module calls | `IdentityContext = createContext` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/identity/identityContext.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/identityContext.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (12) |
| Outbound | `frontend` (1) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IdentityContextValue](../entities/IdentityContextValue.md) | Type alias | 4 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useIdentity` | `()` | — | — |
