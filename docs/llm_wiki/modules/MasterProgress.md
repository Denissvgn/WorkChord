# MasterProgress Module

**Path:** `frontend/src/components/ui/MasterProgress.tsx`

## Description

_Auto-generated from `frontend/src/components/ui/MasterProgress.tsx`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `MasterProgress` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/ui/MasterProgress.test.tsx"]
    n1["frontend/src/components/ui/MasterProgress.tsx"]
    n2["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n3["frontend/src/pages/PlanMasterPage.tsx"]
    n0 --> n1
    n2 --> n1
    n3 --> n1
    click n0 "../modules/MasterProgress.test.md"
    click n1 "../modules/MasterProgress.md"
    click n2 "../modules/AgentTeamSetupMasterPage.md"
    click n3 "../modules/PlanMasterPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [MasterProgress.test](../modules/MasterProgress.test.md) |
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [MasterProgressProps](../entities/MasterProgressProps.md) | Class | 1 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `MasterProgress` | `({     className = '',     completed,     label,     total,     valueText, }: MasterProgressProps)` | — | — |
