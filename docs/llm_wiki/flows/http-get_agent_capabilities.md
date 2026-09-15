# get_agent_capabilities

**Entry point:** `get_agent_capabilities` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [agent_contract](../modules/agent_contract.md), [agent_routing_rollout](../modules/agent_routing_rollout.md), [agent_service](../modules/agent_service.md), and 4 more

**Complete modules touched:**

- [agent_contract](../modules/agent_contract.md)
- [agent_routing_rollout](../modules/agent_routing_rollout.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [config](../modules/config.md)
- [routers_agent](../modules/routers_agent.md)
- [schemas_agent](../modules/schemas_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_agent_capabilities
    participant p1 as AgentRoutingRolloutService().status
    participant p2 as AgentRoutingRolloutService
    participant p3 as AgentTeamSetupService(…).routing_readiness
    participant p4 as AgentTeamSetupService
    participant p5 as (…).status
    participant p6 as agent_contract_features
    participant p7 as ValueError
    participant p8 as features.insert
    participant p9 as features.index
    participant p10 as get_settings
    participant p11 as Settings
    participant p12 as actor_has_scope
    participant p13 as actor_scopes
    participant p14 as json.loads
    participant p15 as isinstance
    participant p16 as SkillBundleCatalogResponse.model_validate_json
    participant p17 as bundle_service.catalog_payload
    participant p18 as logger.warning
    participant p19 as features.append
    participant p20 as settings.api_prefix.rstrip
    participant p21 as AgentCapabilitiesResponse
    participant p22 as service.actor_response
    participant p23 as rollout_status.as_dict
    p0-->>p1: AgentRoutingRolloutService().status
    p0->>p2: AgentRoutingRolloutService
    p0-->>p3: AgentTeamSetupService(…).routing_readiness
    p0->>p4: AgentTeamSetupService
    p0-->>p5: (…).status
    p0->>p2: AgentRoutingRolloutService
    p0->>p2: AgentRoutingRolloutService
    p0->>p6: agent_contract_features
    p6-->>p7: ValueError
    p6-->>p8: features.insert
    p6-->>p9: features.index
    p0->>p10: get_settings
    p10->>p11: Settings
    p0->>p12: actor_has_scope
    p12->>p13: actor_scopes
    p13-->>p14: json.loads
    p13-->>p15: isinstance
    p0-->>p16: SkillBundleCatalogResponse.model_validate_json
    p0-->>p17: bundle_service.catalog_payload
    p0-->>p18: logger.warning
    p0-->>p19: features.append
    p0-->>p20: settings.api_prefix.rstrip
    p0->>p21: AgentCapabilitiesResponse
    p0-->>p22: service.actor_response
    p0->>p13: actor_scopes
    p0-->>p23: rollout_status.as_dict
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_agent_capabilities"]
    s2["2. AgentRoutingRolloutService().status"]
    s3["3. AgentRoutingRolloutService"]
    s4["4. AgentTeamSetupService(…).routing_readiness"]
    s5["5. AgentTeamSetupService"]
    s6["6. (…).status"]
    s7["7. AgentRoutingRolloutService"]
    s8["8. AgentRoutingRolloutService"]
    s9["9. agent_contract_features"]
    s10["10. ValueError"]
    s11["11. features.insert"]
    s12["12. features.index"]
    s1 -. "AgentRoutingRolloutService().status(data not statically known)" .-> s2
    s1 -->|"AgentRoutingRolloutService(data not statically known)"| s3
    s1 -. "AgentTeamSetupService(…).routing_readiness(actor)" .-> s4
    s1 -->|"AgentTeamSetupService(service.db)"| s5
    s1 -. "(…).status(data not statically known)" .-> s6
    s1 -->|"AgentRoutingRolloutService(data not statically known)"| s7
    s1 -->|"AgentRoutingRolloutService(topology_readiness=topology_readiness)"| s8
    s1 -->|"agent_contract_features(include_skill_bundles=False, model_aware_routing_mode=rollout_status.effective_mode.value)"| s9
    s9 -. "ValueError('Unsupported model-aware routing mode')" .-> s10
    s9 -. "features.insert(..., MODEL_AWARE_ROUTING_FEATURE)" .-> s11
    s9 -. "features.index('actor-roster-v1')" .-> s12
    b0["mutation features.append"]
    s1 -. "mutation features.append" .-> b0
    b1["mutation features.insert"]
    s9 -. "mutation features.insert" .-> b1
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/agent_routing_rollout.md"
    click s5 "../modules/agent_team_setup_service.md"
    click s7 "../modules/agent_routing_rollout.md"
    click s8 "../modules/agent_routing_rollout.md"
    click s9 "../modules/agent_contract.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_agent_capabilities` | `request: Request`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentWorkService, Depends(get_agent_work_service)]`, `bundle_service: Annotated[AgentSkillBundleService, Depends(get_agent_skill_bundle_service)]` | `SkillBundleArtifactError` | `recommended_skills[...]` | `AgentCapabilitiesResponse(...)` |
| `AgentRoutingRolloutService().status` | - | - | - | - |
| `AgentRoutingRolloutService` | - | - | - | - |
| `AgentTeamSetupService(…).routing_readiness` | - | - | - | - |
| `AgentTeamSetupService` | - | - | - | - |
| `(…).status` | - | - | - | - |
| `AgentRoutingRolloutService` | - | - | - | - |
| `AgentRoutingRolloutService` | - | - | - | - |
| `agent_contract_features` | `include_skill_bundles: bool`, `model_aware_routing_mode: str` | `AGENT_CONTRACT_FEATURES`, `SKILL_BUNDLES_FEATURE`, `MODEL_AWARE_ROUTING_FEATURE` | - | `features` |
| `ValueError` | - | - | - | - |
| `features.insert` | - | - | - | - |
| `features.index` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_agent_capabilities | AgentRoutingRolloutService().status | 337 | `AgentRoutingRolloutService().status(data not statically known)` |
| get_agent_capabilities | AgentRoutingRolloutService | 337 | `AgentRoutingRolloutService(data not statically known)` |
| get_agent_capabilities | AgentTeamSetupService(…).routing_readiness | 339 | `AgentTeamSetupService(service.db).routing_readiness(actor)` |
| get_agent_capabilities | AgentTeamSetupService | 339 | `AgentTeamSetupService(service.db)` |
| get_agent_capabilities | (…).status | 342 | `(AgentRoutingRolloutService() if topology_readiness.status == AgentRoutingTopologyReadinessStatus.UNAVAILABLE else AgentRoutingRolloutService(topology_readiness=topology_readiness)).status(data not statically known)` |
| get_agent_capabilities | AgentRoutingRolloutService | 343 | `AgentRoutingRolloutService(data not statically known)` |
| get_agent_capabilities | AgentRoutingRolloutService | 346 | `AgentRoutingRolloutService(topology_readiness=topology_readiness)` |
| get_agent_capabilities | agent_contract_features | 350 | `agent_contract_features(include_skill_bundles=False, model_aware_routing_mode=rollout_status.effective_mode.value)` |
| agent_contract_features | ValueError | 41 | `ValueError('Unsupported model-aware routing mode')` |
| agent_contract_features | features.insert | 49 | `features.insert(..., MODEL_AWARE_ROUTING_FEATURE)` |
| agent_contract_features | features.index | 50 | `features.index('actor-roster-v1')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `features.append` | `get_agent_capabilities` | 370 |
| mutation | `features.insert` | `agent_contract_features` | 49 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_agent_capabilities` | `AgentRoutingRolloutService().status` | 337 |
| unresolved_call | `get_agent_capabilities` | `AgentTeamSetupService(service.db).routing_readiness` | 339 |
| unresolved_call | `get_agent_capabilities` | `(AgentRoutingRolloutService() if topology_readiness.status == AgentRoutingTopologyReadinessStatus.UNAVAILABLE else AgentRoutingRolloutService(topology_readiness=topology_readiness)).status` | 342 |
| external_call | `agent_contract_features` | `ValueError` | 41 |
| unresolved_call | `agent_contract_features` | `features.index` | 50 |
| step_limit | `get_agent_capabilities` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_agent_capabilities` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
