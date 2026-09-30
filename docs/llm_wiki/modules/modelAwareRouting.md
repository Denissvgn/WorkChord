# modelAwareRouting Module

**Path:** `frontend/src/test/fixtures/modelAwareRouting.ts`

## Description

_Auto-generated from `frontend/src/test/fixtures/modelAwareRouting.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/agent` | `AgentActorRosterItem`, `AgentRoutingCandidate`, `AgentRoutingExclusion`, `AgentRoutingPreviewResponse` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `eligibleRoutingCandidate`, `excludedRoutingCandidate`, `modelAwareRoutingPreview`, `modelAwareRoutingRoster` |
| Constants | `eligibleRoutingCandidate`, `excludedRoutingCandidate`, `modelAwareRoutingPreview`, `modelAwareRoutingRoster` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/RoutingCandidateComparison.test.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n3["frontend/src/types/agent.ts"]
    n0 --> n2
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/RoutingCandidateComparison.test.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/modelAwareRouting.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoutingCandidateComparison.test](../modules/RoutingCandidateComparison.test.md) |
| Inbound | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
