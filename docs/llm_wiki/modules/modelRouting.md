# modelRouting Module

**Path:** `frontend/src/utils/modelRouting.ts`

## Description

_Auto-generated from `frontend/src/utils/modelRouting.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/agent` | `AgentCommandMetadata`, `TaskDifficultyAxes`, `TaskDifficultyBand`, `TaskReviewMode` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ASSESSMENT_REASON_CODES`, `AssessmentReasonCode`, `MODEL_AWARE_ROUTING_FEATURE`, `createAgentCommandMetadata`, `deriveDifficultyBand`, `formatRoutingCode`, `minimumReviewMode`, `parseRoutingTags`, `reviewModeMeets`, `toAgentAuditRationale` |
| Constants | `MODEL_AWARE_ROUTING_FEATURE`, `ASSESSMENT_REASON_CODES`, `ADVANCED_REASON_CODES`, `INDEPENDENT_REASON_CODES`, `STANDARD_REVIEW_REASON_CODES`, `REVIEW_ORDER`, `AGENT_AUDIT_RATIONALE_MAX_LENGTH`, `AGENT_AUDIT_RATIONALE_FALLBACK` |
| Module calls | `ADVANCED_REASON_CODES = Set`, `INDEPENDENT_REASON_CODES = Set`, `STANDARD_REVIEW_REASON_CODES = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["frontend/src/components/settings/QualificationKeysPanel.tsx"]
    n3["frontend/src/components/team/AgentModelAdministration.tsx"]
    n4["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n5["frontend/src/types/agent.ts"]
    n6["frontend/src/utils/modelRouting.test.ts"]
    n7["frontend/src/utils/modelRouting.ts"]
    n0 --> n5
    n0 --> n7
    n1 --> n0
    n1 --> n5
    n1 --> n7
    n2 --> n5
    n2 --> n7
    n3 --> n5
    n3 --> n7
    n4 --> n5
    n4 --> n7
    n6 --> n5
    n6 --> n7
    n7 --> n5
    click n0 "../modules/RoutingCandidateComparison.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/QualificationKeysPanel.md"
    click n3 "../modules/AgentModelAdministration.md"
    click n4 "../modules/ConnectAgentSteps.md"
    click n5 "../modules/types_agent.md"
    click n6 "../modules/modelRouting.test.md"
    click n7 "../modules/modelRouting.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoutingCandidateComparison](../modules/RoutingCandidateComparison.md) |
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [QualificationKeysPanel](../modules/QualificationKeysPanel.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Inbound | [modelRouting.test](../modules/modelRouting.test.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AssessmentReasonCode](../entities/modelRouting_AssessmentReasonCode.md) | Type alias | 25 | `typeof ASSESSMENT_REASON_CODES[number]` | — |

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
