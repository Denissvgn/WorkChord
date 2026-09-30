# attentionRanking Module

**Path:** `frontend/src/features/overview/attentionRanking.ts`

## Description

_Auto-generated from `frontend/src/features/overview/attentionRanking.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `Task` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AttentionKind`, `AttentionSeverity`, `RankableAttention`, `compareAttentionRank`, `rankAttentionItems`, `rankAttentionTaskCandidates` |
| Constants | `severityRank`, `kindTieBreaker` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
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
| [AttentionSeverity](../entities/AttentionSeverity.md) | Type alias | 3 | — | — |
| [AttentionKind](../entities/AttentionKind.md) | Type alias | 5 | — | — |
| [RankableAttention](../entities/RankableAttention.md) | Type alias | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `compareAttentionRank` | `(left: RankableAttention, right: RankableAttention)` | — | — |
| `rankAttentionItems` | `(items: readonly Item[])` | — | — |
| `rankAttentionTaskCandidates` | `(tasks: readonly Task[])` | — | — |
