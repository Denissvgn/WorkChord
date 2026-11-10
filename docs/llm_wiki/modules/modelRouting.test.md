# modelRouting.test Module

**Path:** `frontend/src/utils/modelRouting.test.ts`

## Description

_Auto-generated from `frontend/src/utils/modelRouting.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/agent` | `TaskDifficultyAxes` | Declaration | erased |
| `./modelRouting` | `createAgentCommandMetadata`, `deriveDifficultyBand`, `minimumReviewMode`, `reviewModeMeets`, `toAgentAuditRationale` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `routineAxes` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/types/agent.ts"]
    n1["frontend/src/utils/modelRouting.test.ts"]
    n2["frontend/src/utils/modelRouting.ts"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/modelRouting.test.md"
    click n2 "../modules/modelRouting.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [modelRouting](../modules/modelRouting.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
