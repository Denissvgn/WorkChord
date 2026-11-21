# TriageRow Module

**Path:** `frontend/src/components/triage/TriageRow.tsx`

## Description

_Auto-generated from `frontend/src/components/triage/TriageRow.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/triage` | `TriageItem` | Declaration | erased |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `./StatusPill` | `StatusPill` | — | compiler-dependent |
| `./triageUtils` | `isDueSnoozed`, `t` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `MessageSquare` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TriageRow` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/triage/StatusPill.tsx"]
    n1["frontend/src/components/triage/TriageList.tsx"]
    n2["frontend/src/components/triage/TriageRow.tsx"]
    n3["frontend/src/components/triage/triageUtils.ts"]
    n4["frontend/src/types/triage.ts"]
    n5["frontend/src/utils/formatDate.ts"]
    n0 --> n3
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n4
    click n0 "../modules/StatusPill.md"
    click n1 "../modules/TriageList.md"
    click n2 "../modules/TriageRow.md"
    click n3 "../modules/triageUtils.md"
    click n4 "../modules/types_triage.md"
    click n5 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TriageList](../modules/TriageList.md) |
| Outbound | [StatusPill](../modules/StatusPill.md) |
| Outbound | [triageUtils](../modules/triageUtils.md) |
| Outbound | [types_triage](../modules/types_triage.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TriageRowProps](../entities/TriageRowProps.md) | Interface | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TriageRow` | <pre><code>&#40;&#123;&#10;    item&#44;&#10;    isSelected&#44;&#10;    projectsById&#44;&#10;    iterationsById&#44;&#10;    onSelect&#44;&#10;&#125;&#58; TriageRowProps&#41;</code></pre> | — | — |
