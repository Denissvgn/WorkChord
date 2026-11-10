# attentionRanking Module

**Path:** `frontend/src/features/overview/attentionRanking.ts`

## Description

_Auto-generated from `frontend/src/features/overview/attentionRanking.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `Task` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AttentionKind`, `AttentionSeverity`, `RankableAttention`, `compareAttentionRank`, `rankAttentionItems`, `rankAttentionTaskCandidates` |
| Constants | `severityRank`, `kindTieBreaker` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/overview/attentionRanking.test.ts"]
    n1["frontend/src/features/overview/attentionRanking.ts"]
    n2["frontend/src/pages/OverviewPage.tsx"]
    n3["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/attentionRanking.test.md"
    click n1 "../modules/attentionRanking.md"
    click n2 "../modules/OverviewPage.md"
    click n3 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [attentionRanking.test](../modules/attentionRanking.test.md) |
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AttentionSeverity](../entities/AttentionSeverity.md) | Type alias | 3 | `'critical' \| 'warning' \| 'advisory'` | — |
| [AttentionKind](../entities/AttentionKind.md) | Type alias | 5 | <pre><code>&#124; &#39;overdue&#39;&#10;    &#124; &#39;project&#45;risk&#39;&#10;    &#124; &#39;pace&#39;&#10;    &#124; &#39;project&#45;update&#39;&#10;    &#124; &#39;unassigned&#39;&#10;    &#124; &#39;intake&#39;</code></pre> | — |
| [RankableAttention](../entities/RankableAttention.md) | Type alias | 13 | <pre><code>&#123;&#10;    id&#58; string&#59;&#10;    kind&#58; AttentionKind&#59;&#10;    severity&#58; AttentionSeverity&#59;&#10;    urgency&#58; number&#59;&#10;    magnitude&#58; number&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `compareAttentionRank` | `(left: RankableAttention, right: RankableAttention)` | — | — |
| `rankAttentionItems` | `<Item extends RankableAttention>(items: readonly Item[])` | — | — |
| `rankAttentionTaskCandidates` | `(tasks: readonly Task[])` | — | — |
