# ScenarioBase

**Location:** `backend/tests/test_agent_routing_wave6_qualification.py:86`
**Kind:** Class
**Bases:** —
**Module:** [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

_Auto-generated from `ScenarioBase` in `backend/tests/test_agent_routing_wave6_qualification.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `pm` | `AgentActor` | *required* | — |
| `task` | `Task` | *required* | — |
| `profile` | `TeamMemberProfile` | *required* | — |
| `member` | `TeamMember` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ScenarioBase (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n1["_create_assessment_with_parity (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n2["_dispatch (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n3["_preview_with_parity (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n4["_seed_base (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n5["routing_base (backend/tests/test_agent_team_setup_qualification.py)"]
    n6["test_setup_scenario_09_live_roster_and_routing_matrix_is_topology_bound (backend/tests/test_agent_team_setup_qualification.py)"]
    n7["test_setup_scenario_10_feature_off_preserves_setup_and_work_evidence (backend/tests/test_agent_team_setup_qualification.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/test_agent_routing_wave6_qualification.md"
    click n1 "../modules/test_agent_routing_wave6_qualification.md"
    click n2 "../modules/test_agent_routing_wave6_qualification.md"
    click n3 "../modules/test_agent_routing_wave6_qualification.md"
    click n4 "../modules/test_agent_routing_wave6_qualification.md"
    click n5 "../modules/test_agent_team_setup_qualification.md"
    click n6 "../modules/test_agent_team_setup_qualification.md"
    click n7 "../modules/test_agent_team_setup_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 0 | `member`, `pm`, `profile`, `task` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_create_assessment_with_parity` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `_dispatch` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `_preview_with_parity` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `_seed_base` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |
| `_seed_base` | type_reference | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | — |
| `routing_base` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `routing_base` | type_reference | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | — |
| `test_setup_scenario_09_live_roster_and_routing_matrix_is_topology_bound` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `test_setup_scenario_10_feature_off_preserves_setup_and_work_evidence` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
