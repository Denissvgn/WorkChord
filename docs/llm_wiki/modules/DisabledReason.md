# DisabledReason Module

**Path:** `frontend/src/components/common/DisabledReason.tsx`

## Description

_Auto-generated from `frontend/src/components/common/DisabledReason.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `clsx` | `clsx` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DisabledReason` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/DisabledReason.tsx"]
    n1["frontend/src/components/iteration/IterationImportDialog.tsx"]
    n2["frontend/src/components/releases/ReleaseForm.tsx"]
    n3["frontend/src/components/team/ImportTeamModal.tsx"]
    n4["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n5["frontend/src/pages/CalendarPage.tsx"]
    n6["frontend/src/pages/ProjectDetailPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n6 --> n2
    click n0 "../modules/DisabledReason.md"
    click n1 "../modules/IterationImportDialog.md"
    click n2 "../modules/ReleaseForm.md"
    click n3 "../modules/ImportTeamModal.md"
    click n4 "../modules/AgentTeamSetupMasterPage.md"
    click n5 "../modules/CalendarPage.md"
    click n6 "../modules/ProjectDetailPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationImportDialog](../modules/IterationImportDialog.md) |
| Inbound | [ReleaseForm](../modules/ReleaseForm.md) |
| Inbound | [ImportTeamModal](../modules/ImportTeamModal.md) |
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DisabledReason` | `({ reason, className }: { reason?: string \| null \| false; className?: string })` | — | Says, next to a disabled button, what would enable it. Renders nothing when there is no reason. |
