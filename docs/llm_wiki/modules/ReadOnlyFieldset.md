# ReadOnlyFieldset Module

**Path:** `frontend/src/components/settings/ReadOnlyFieldset.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/ReadOnlyFieldset.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./sharedUnlock` | `useSettingsReadOnly` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ReadOnlyFieldset` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/EffortModifierCard.tsx"]
    n1["frontend/src/components/settings/ReadOnlyFieldset.tsx"]
    n2["frontend/src/components/settings/SchedulingPassCard.tsx"]
    n3["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n4["frontend/src/components/settings/sharedUnlock.ts"]
    n5["frontend/src/pages/SettingsPage.tsx"]
    n0 --> n1
    n1 --> n4
    n2 --> n1
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n5 --> n1
    n5 --> n3
    n5 --> n4
    click n0 "../modules/EffortModifierCard.md"
    click n1 "../modules/ReadOnlyFieldset.md"
    click n2 "../modules/SchedulingPassCard.md"
    click n3 "../modules/SchedulingRulesSettings.md"
    click n4 "../modules/sharedUnlock.md"
    click n5 "../modules/SettingsPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EffortModifierCard](../modules/EffortModifierCard.md) |
| Inbound | [SchedulingPassCard](../modules/SchedulingPassCard.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [sharedUnlock](../modules/sharedUnlock.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ReadOnlyFieldset` | `({ children, disabled = false }: { children: ReactNode; disabled?: boolean })` | — | Wraps editing controls so they are disabled while the surrounding settings |
