# sampleProjectStore Module

**Path:** `frontend/src/features/firstRun/sampleProjectStore.ts`

## Description

_Auto-generated from `frontend/src/features/firstRun/sampleProjectStore.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./sampleProject` | `SampleManifest` | Declaration | erased |
| `zustand` | `create` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useSampleProject` |
| Constants | `STORAGE_KEY`, `useSampleProject` |
| Module calls | `useSampleProject = create` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/GetStartedPanel.test.tsx"]
    n1["frontend/src/features/firstRun/sampleProject.test.tsx"]
    n2["frontend/src/features/firstRun/sampleProject.ts"]
    n3["frontend/src/features/firstRun/SampleProjectAction.tsx"]
    n4["frontend/src/features/firstRun/sampleProjectStore.ts"]
    n5["frontend/src/features/firstRun/useGetStarted.ts"]
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n3 --> n4
    n4 --> n2
    n5 --> n4
    click n0 "../modules/GetStartedPanel.test.md"
    click n1 "../modules/sampleProject.test.md"
    click n2 "../modules/sampleProject.md"
    click n3 "../modules/SampleProjectAction.md"
    click n4 "../modules/sampleProjectStore.md"
    click n5 "../modules/useGetStarted.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GetStartedPanel.test](../modules/GetStartedPanel.test.md) |
| Inbound | [sampleProject.test](../modules/sampleProject.test.md) |
| Inbound | [SampleProjectAction](../modules/SampleProjectAction.md) |
| Inbound | [useGetStarted](../modules/useGetStarted.md) |
| Outbound | [sampleProject](../modules/sampleProject.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SampleState](../entities/SampleState.md) | Interface | 17 | — | — |
