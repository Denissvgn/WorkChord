# TriageConvertSource Module

**Path:** `frontend/src/components/triage/TriageConvertSource.tsx`

## Description

_Auto-generated from `frontend/src/components/triage/TriageConvertSource.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/triage` | `TriageItem` | Declaration | erased |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../../utils/safeUrl` | `sourceLinkHref` | — | compiler-dependent |
| `./TriageDetailPanel` | `InfoBlock` | — | compiler-dependent |
| `./triageUtils` | `t` | — | compiler-dependent |
| `lucide-react` | `ExternalLink` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TriageConvertSource` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n1["frontend/src/components/triage/TriageConvertSource.tsx"]
    n2["frontend/src/components/triage/TriageDetailPanel.tsx"]
    n3["frontend/src/components/triage/triageUtils.ts"]
    n4["frontend/src/types/triage.ts"]
    n5["frontend/src/utils/formatDate.ts"]
    n6["frontend/src/utils/safeUrl.ts"]
    n0 --> n1
    n0 --> n3
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n4
    click n0 "../modules/ConvertTriageDrawer.md"
    click n1 "../modules/TriageConvertSource.md"
    click n2 "../modules/TriageDetailPanel.md"
    click n3 "../modules/triageUtils.md"
    click n4 "../modules/types_triage.md"
    click n5 "../modules/formatDate.md"
    click n6 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) |
| Outbound | [TriageDetailPanel](../modules/TriageDetailPanel.md) |
| Outbound | [triageUtils](../modules/triageUtils.md) |
| Outbound | [types_triage](../modules/types_triage.md) |
| Outbound | [formatDate](../modules/formatDate.md) |
| Outbound | [safeUrl](../modules/safeUrl.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TriageConvertSource` | `({ item, projectsById, iterationsById }: { item: TriageItem; projectsById: Record<number, string>; iterationsById: Record<number, string> })` | — | — |
