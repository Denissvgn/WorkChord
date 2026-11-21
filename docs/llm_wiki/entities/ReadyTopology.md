# ReadyTopology

**Location:** `backend/tests/test_agent_team_setup_qualification.py:331`
**Kind:** Class
**Bases:** —
**Module:** [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

_Auto-generated from `ReadyTopology` in `backend/tests/test_agent_team_setup_qualification.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `manifest` | `AgentTeamMaster` | *required* | — |
| `sink` | `CapturingCredentialSink` | *required* | — |
| `service` | `AgentTeamSetupService` | *required* | — |
| `actors` | `dict[str, AgentActor]` | *required* | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReadyTopology (backend/tests/test_agent_team_setup_qualification.py)"]
    n1["provision_ready_topology (backend/tests/test_agent_team_setup_qualification.py)"]
    n2["routing_base (backend/tests/test_agent_team_setup_qualification.py)"]
    n3["test_scoped_source_packet_from_submission_through_verdict (backend/tests/test_scoped_review_evidence.py)"]
    n4["topology_with_two_reviewers (backend/tests/test_supervised_shadow_rework.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/test_agent_team_setup_qualification.md"
    click n1 "../modules/test_agent_team_setup_qualification.md"
    click n2 "../modules/test_agent_team_setup_qualification.md"
    click n3 "../modules/test_scoped_review_evidence.md"
    click n4 "../modules/test_supervised_shadow_rework.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 0 | `actors`, `manifest`, `service`, `sink` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `provision_ready_topology` | call | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | 1 |
| `provision_ready_topology` | type_reference | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | — |
| `routing_base` | type_reference | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) | — |
| `test_scoped_source_packet_from_submission_through_verdict` | call | [test_scoped_review_evidence](../modules/test_scoped_review_evidence.md) | 1 |
| `topology_with_two_reviewers` | call | [test_supervised_shadow_rework](../modules/test_supervised_shadow_rework.md) | 1 |
