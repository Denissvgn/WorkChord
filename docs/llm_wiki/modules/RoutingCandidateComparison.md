# RoutingCandidateComparison Module

**Path:** `frontend/src/components/agent/RoutingCandidateComparison.tsx`

## Description

_Auto-generated from `frontend/src/components/agent/RoutingCandidateComparison.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentActorRosterItem`, `AgentRoutingCandidate`, `AgentRoutingExclusion`, `AgentRoutingPreviewResponse` | Declaration | erased |
| `../../utils/modelRouting` | `formatRoutingCode` | — | compiler-dependent |
| `lucide-react` | `CheckCircle2`, `ShieldX` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RoutingCandidateComparison` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/agent/RoutingCandidateComparison.test.tsx"]
    n1["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n2["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n3["frontend/src/types/agent.ts"]
    n4["frontend/src/utils/modelRouting.ts"]
    n0 --> n1
    n1 --> n3
    n1 --> n4
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n4 --> n3
    click n0 "../modules/RoutingCandidateComparison.test.md"
    click n1 "../modules/RoutingCandidateComparison.md"
    click n2 "../modules/TaskRoutingPanel.md"
    click n3 "../modules/types_agent.md"
    click n4 "../modules/modelRouting.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoutingCandidateComparison.test](../modules/RoutingCandidateComparison.test.md) |
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [modelRouting](../modules/modelRouting.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RoutingCandidateComparisonProps](../entities/RoutingCandidateComparisonProps.md) | Interface | 15 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `RoutingCandidateComparison` | <pre><code>&#40;&#123;&#10;    preview&#44;&#10;    roster&#44;&#10;    selectedCandidateKey&#44;&#10;    onSelectCandidate&#44;&#10;    selectionDisabled &#61; false&#44;&#10;&#125;&#58; RoutingCandidateComparisonProps&#41;</code></pre> | — | — |
