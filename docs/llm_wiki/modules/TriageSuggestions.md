# TriageSuggestions Module

**Path:** `frontend/src/components/triage/TriageSuggestions.tsx`

## Description

_Auto-generated from `frontend/src/components/triage/TriageSuggestions.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/triage` | `TriageClassificationSuggestion`, `TriageDuplicateSuggestion`, `TriageDuplicateSuggestionsResponse` | Declaration | erased |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `./triageUtils` | `formatSuggestionScore`, `t` | — | compiler-dependent |
| `lucide-react` | `CopyCheck`, `Loader2`, `Sparkles` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ClassificationPanel`, `DuplicateSuggestionsPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/triage/TriageDetailPanel.tsx"]
    n3["frontend/src/components/triage/TriageSuggestions.tsx"]
    n4["frontend/src/components/triage/triageUtils.ts"]
    n5["frontend/src/types/triage.ts"]
    n6["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n4 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/TriageDetailPanel.md"
    click n3 "../modules/TriageSuggestions.md"
    click n4 "../modules/triageUtils.md"
    click n5 "../modules/types_triage.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TriageDetailPanel](../modules/TriageDetailPanel.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [triageUtils](../modules/triageUtils.md) |
| Outbound | [types_triage](../modules/types_triage.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DuplicateSuggestionsPanelProps](../entities/DuplicateSuggestionsPanelProps.md) | Interface | 16 | — | — |
| [DuplicateSuggestionGroupProps](../entities/DuplicateSuggestionGroupProps.md) | Interface | 80 | — | — |
| [ClassificationPanelProps](../entities/ClassificationPanelProps.md) | Interface | 140 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DuplicateSuggestionsPanel` | <pre><code>&#40;&#123;&#10;    suggestions&#44;&#10;    isLoading&#44;&#10;    isError&#44;&#10;    error&#44;&#10;    onRetry&#44;&#10;    projectsById&#44;&#10;    iterationsById&#44;&#10;    onMarkSuggestion&#44;&#10;&#125;&#58; DuplicateSuggestionsPanelProps&#41;</code></pre> | — | — |
| `ClassificationPanel` | <pre><code>&#40;&#123;&#10;    suggestions&#44;&#10;    isLoading&#44;&#10;    isError&#44;&#10;    error&#44;&#10;    onRetry&#44;&#10;    onClassify&#44;&#10;    isClassifying&#44;&#10;    classifyError&#44;&#10;&#125;&#58; ClassificationPanelProps&#41;</code></pre> | — | — |
