# StatusPill Module

**Path:** `frontend/src/components/triage/StatusPill.tsx`

## Description

_Auto-generated from `frontend/src/components/triage/StatusPill.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/triage` | `TriageItemStatus` | Declaration | erased |
| `./triageUtils` | `statusClassName`, `statusLabelKeys`, `t` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `StatusPill` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/triage/StatusPill.tsx"]
    n1["frontend/src/components/triage/TriageActionModal.tsx"]
    n2["frontend/src/components/triage/TriageDetailPanel.tsx"]
    n3["frontend/src/components/triage/TriageRow.tsx"]
    n4["frontend/src/components/triage/triageUtils.ts"]
    n5["frontend/src/types/triage.ts"]
    n0 --> n4
    n0 --> n5
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n3 --> n0
    n3 --> n4
    n3 --> n5
    n4 --> n5
    click n0 "../modules/StatusPill.md"
    click n1 "../modules/TriageActionModal.md"
    click n2 "../modules/TriageDetailPanel.md"
    click n3 "../modules/TriageRow.md"
    click n4 "../modules/triageUtils.md"
    click n5 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TriageActionModal](../modules/TriageActionModal.md) |
| Inbound | [TriageDetailPanel](../modules/TriageDetailPanel.md) |
| Inbound | [TriageRow](../modules/TriageRow.md) |
| Outbound | [triageUtils](../modules/triageUtils.md) |
| Outbound | [types_triage](../modules/types_triage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `StatusPill` | `({ status }: { status: TriageItemStatus })` | — | — |
