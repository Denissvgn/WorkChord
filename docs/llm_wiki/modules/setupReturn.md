# setupReturn Module

**Path:** `frontend/src/features/firstRun/setupReturn.ts`

## Description

_Auto-generated from `frontend/src/features/firstRun/setupReturn.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `zustand` | `create` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SETUP_RETURN_KEY`, `useSetupReturn` |
| Constants | `SETUP_RETURN_KEY`, `useSetupReturn` |
| Module calls | `useSetupReturn = create` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/FirstRunLanding.tsx"]
    n1["frontend/src/features/firstRun/GetStartedFlow.test.tsx"]
    n2["frontend/src/features/firstRun/setupReturn.ts"]
    n3["frontend/src/features/firstRun/SetupReturnBar.tsx"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n3 --> n2
    click n0 "../modules/FirstRunLanding.md"
    click n1 "../modules/GetStartedFlow.test.md"
    click n2 "../modules/setupReturn.md"
    click n3 "../modules/SetupReturnBar.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [FirstRunLanding](../modules/FirstRunLanding.md) |
| Inbound | [GetStartedFlow.test](../modules/GetStartedFlow.test.md) |
| Inbound | [SetupReturnBar](../modules/SetupReturnBar.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SetupReturn](../entities/SetupReturn.md) | Interface | 35 | — | — |
