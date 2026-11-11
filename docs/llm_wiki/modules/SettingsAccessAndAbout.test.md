# SettingsAccessAndAbout.test Module

**Path:** `frontend/src/components/settings/SettingsAccessAndAbout.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/SettingsAccessAndAbout.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./AccessKeysSummary` | `AccessKeysSummary` | — | compiler-dependent |
| `./SettingsUnsavedBar` | `SettingsUnsavedBar` | — | compiler-dependent |
| `./SystemHealthPanel` | `SystemHealthPanel` | — | compiler-dependent |
| `./WithheldValuesNote` | `WithheldValuesNote` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `health` |
| Module calls | `health = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AccessKeysSummary.tsx"]
    n1["frontend/src/components/settings/SettingsAccessAndAbout.test.tsx"]
    n2["frontend/src/components/settings/SettingsUnsavedBar.tsx"]
    n3["frontend/src/components/settings/SystemHealthPanel.tsx"]
    n4["frontend/src/components/settings/WithheldValuesNote.tsx"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    click n0 "../modules/AccessKeysSummary.md"
    click n1 "../modules/SettingsAccessAndAbout.test.md"
    click n2 "../modules/SettingsUnsavedBar.md"
    click n3 "../modules/SystemHealthPanel.md"
    click n4 "../modules/WithheldValuesNote.md"
    click n5 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AccessKeysSummary](../modules/AccessKeysSummary.md) |
| Outbound | [SettingsUnsavedBar](../modules/SettingsUnsavedBar.md) |
| Outbound | [SystemHealthPanel](../modules/SystemHealthPanel.md) |
| Outbound | [WithheldValuesNote](../modules/WithheldValuesNote.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
