# reset_scheduling_rules

**Entry point:** `reset_scheduling_rules` (`http`)
**Source:** [routers_scheduling_rules](../modules/routers_scheduling_rules.md)
**Modules touched:** [routers_scheduling_rules](../modules/routers_scheduling_rules.md), [scheduling_rules_service](../modules/scheduling_rules_service.md), [schemas_scheduling_rules](../modules/schemas_scheduling_rules.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as reset_scheduling_rules
    participant p1 as get_rules_service
    participant p2 as SchedulingRulesService.get_instance
    participant p3 as SchedulingRulesService
    participant p4 as service.reset_to_defaults
    participant p5 as service.get_rules_as_dict
    participant p6 as SchedulingRulesResponse
    participant p7 as SchedulingRulesSchema
    participant p8 as logger.error
    participant p9 as HTTPException
    participant p10 as str
    p0->>p1: get_rules_service
    p1->>p2: SchedulingRulesService.get_instance
    p2->>p3: SchedulingRulesService
    p0-->>p4: service.reset_to_defaults
    p0-->>p5: service.get_rules_as_dict
    p0->>p6: SchedulingRulesResponse
    p0->>p7: SchedulingRulesSchema
    p0-->>p8: logger.error
    p0-->>p9: HTTPException
    p0-->>p10: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. reset_scheduling_rules"]
    s2["2. get_rules_service"]
    s3["3. SchedulingRulesService.get_instance"]
    s4["4. SchedulingRulesService"]
    s5["5. service.reset_to_defaults"]
    s6["6. service.get_rules_as_dict"]
    s7["7. SchedulingRulesResponse"]
    s8["8. SchedulingRulesSchema"]
    s9["9. logger.error"]
    s10["10. HTTPException"]
    s11["11. str"]
    s1 -->|"get_rules_service(data not statically known)"| s2
    s2 -->|"SchedulingRulesService.get_instance(data not statically known)"| s3
    s3 -->|"SchedulingRulesService(config_path)"| s4
    s1 -. "service.reset_to_defaults(data not statically known)" .-> s5
    s1 -. "service.get_rules_as_dict(data not statically known)" .-> s6
    s1 -->|"SchedulingRulesResponse(rules=SchedulingRulesSchema(...), source='defaults')"| s7
    s1 -->|"SchedulingRulesSchema(**=rules_dict)"| s8
    s1 -. "logger.error('Failed to reset scheduling rules', exc_info=True)" .-> s9
    s1 -. "HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=...)" .-> s10
    s1 -. "str(e)" .-> s11
    click s1 "../modules/routers_scheduling_rules.md"
    click s2 "../modules/routers_scheduling_rules.md"
    click s3 "../modules/scheduling_rules_service.md"
    click s4 "../modules/scheduling_rules_service.md"
    click s7 "../modules/schemas_scheduling_rules.md"
    click s8 "../modules/schemas_scheduling_rules.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `reset_scheduling_rules` | - | `status` | - | `SchedulingRulesResponse(...)` |
| `get_rules_service` | - | - | - | `SchedulingRulesService.get_instance(...)` |
| `SchedulingRulesService.get_instance` | `config_path: Optional[Path]` | `cls._instance`, `cls._instance` | `cls._instance` | `cls._instance` |
| `SchedulingRulesService` | - | - | - | - |
| `service.reset_to_defaults` | - | - | - | - |
| `service.get_rules_as_dict` | - | - | - | - |
| `SchedulingRulesResponse` | - | - | - | - |
| `SchedulingRulesSchema` | - | - | - | - |
| `logger.error` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| reset_scheduling_rules | get_rules_service | 71 | `get_rules_service(data not statically known)` |
| get_rules_service | SchedulingRulesService.get_instance | 20 | `SchedulingRulesService.get_instance(data not statically known)` |
| SchedulingRulesService.get_instance | SchedulingRulesService | 105 | `cls(config_path)` |
| reset_scheduling_rules | service.reset_to_defaults | 74 | `service.reset_to_defaults(data not statically known)` |
| reset_scheduling_rules | service.get_rules_as_dict | 75 | `service.get_rules_as_dict(data not statically known)` |
| reset_scheduling_rules | SchedulingRulesResponse | 77 | `SchedulingRulesResponse(rules=SchedulingRulesSchema(...), source='defaults')` |
| reset_scheduling_rules | SchedulingRulesSchema | 78 | `SchedulingRulesSchema(**=rules_dict)` |
| reset_scheduling_rules | logger.error | 82 | `logger.error('Failed to reset scheduling rules', exc_info=True)` |
| reset_scheduling_rules | HTTPException | 83 | `HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=...)` |
| reset_scheduling_rules | str | 85 | `str(e)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `reset_scheduling_rules` | `service.reset_to_defaults` | 74 |
| unresolved_call | `reset_scheduling_rules` | `service.get_rules_as_dict` | 75 |
| unresolved_call | `reset_scheduling_rules` | `logger.error` | 82 |
| external_call | `reset_scheduling_rules` | `HTTPException` | 83 |

## Behavior

This flow starts at `reset_scheduling_rules` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
