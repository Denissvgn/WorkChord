# identityService Module

**Path:** `frontend/src/features/identity/identityService.ts`

## Description

_Auto-generated from `frontend/src/features/identity/identityService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AccountSession`, `WorkProfile`, `WorkspaceIdentity`, `identityService` |
| Constants | `identityService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/identity/identityService.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/identityService.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (22) |
| Outbound | `frontend` (1) |

> All 23 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkProfile](../entities/WorkProfile.md) | Interface | 4 | — | A linked profile is verified; a trusted-local session's own choice is not. |
| [WorkspaceIdentity](../entities/WorkspaceIdentity.md) | Interface | 6 | — | — |
| [AccountSession](../entities/AccountSession.md) | Interface | 24 | — | One session of this account, or on a trusted-local server, one paired reader. |
