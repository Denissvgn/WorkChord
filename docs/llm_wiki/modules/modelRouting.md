# modelRouting Module

**Path:** `frontend/src/utils/modelRouting.ts`

## Description

_Auto-generated from `frontend/src/utils/modelRouting.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/agent` | `AgentCommandMetadata`, `TaskDifficultyAxes`, `TaskDifficultyBand`, `TaskReviewMode` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ASSESSMENT_REASON_CODES`, `AssessmentReasonCode`, `MODEL_AWARE_ROUTING_FEATURE`, `createAgentCommandMetadata`, `deriveDifficultyBand`, `formatRoutingCode`, `minimumReviewMode`, `parseRoutingTags`, `reviewModeMeets`, `toAgentAuditRationale` |
| Constants | `MODEL_AWARE_ROUTING_FEATURE`, `ASSESSMENT_REASON_CODES`, `ADVANCED_REASON_CODES`, `INDEPENDENT_REASON_CODES`, `STANDARD_REVIEW_REASON_CODES`, `REVIEW_ORDER`, `AGENT_AUDIT_RATIONALE_MAX_LENGTH`, `AGENT_AUDIT_RATIONALE_FALLBACK` |
| Module calls | `ADVANCED_REASON_CODES = Set`, `INDEPENDENT_REASON_CODES = Set`, `STANDARD_REVIEW_REASON_CODES = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n3["frontend/src/types/agent.ts"]
    n4["frontend/src/utils/modelRouting.test.ts"]
    n5["frontend/src/utils/modelRouting.ts"]
    n0 --> n3
    n0 --> n5
    n1 --> n0
    n1 --> n3
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n4 --> n3
    n4 --> n5
    n5 --> n3
    click n0 "../modules/RoutingCandidateComparison.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/AgentModelAdministration.md"
    click n3 "../modules/types_agent.md"
    click n4 "../modules/modelRouting.test.md"
    click n5 "../modules/modelRouting.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoutingCandidateComparison](../modules/RoutingCandidateComparison.md) |
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [modelRouting.test](../modules/modelRouting.test.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AssessmentReasonCode](../entities/modelRouting_AssessmentReasonCode.md) | Type alias | 25 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `deriveDifficultyBand` | `(axes: TaskDifficultyAxes, reasonCodes: readonly string[]) -> TaskDifficultyBand` | — | — |
| `minimumReviewMode` | `(axes: TaskDifficultyAxes, reasonCodes: readonly string[]) -> TaskReviewMode` | — | — |
| `reviewModeMeets` | `(actual: TaskReviewMode, minimum: TaskReviewMode)` | — | — |
| `parseRoutingTags` | `(value: string)` | — | — |
| `formatRoutingCode` | `(value: string)` | — | — |
| `toAgentAuditRationale` | `(rationale: string)` | — | — |
| `createAgentCommandMetadata` | `(rationale: string) -> AgentCommandMetadata` | — | — |
