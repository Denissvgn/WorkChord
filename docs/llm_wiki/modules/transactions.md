# transactions Module

**Path:** `backend/tests/support/transactions.py`

## Description

Explicit persisted-state reads after rollback in multi-command scenarios.

## Imports

| Source | Symbols |
|--------|---------|
| `sqlalchemy` | `inspect` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/tests/support/transactions.py"]
    n1["backend/tests/test_agent_routing_service.py"]
    n2["backend/tests/test_agent_routing_wave6_qualification.py"]
    n3["backend/tests/test_agent_team_setup_qualification.py"]
    n4["backend/tests/test_review_provenance.py"]
    n5["backend/tests/test_routing_preview_focus.py"]
    n6["backend/tests/test_routing_preview_team_scope.py"]
    n7["backend/tests/test_scoped_review_evidence.py"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n7
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n4
    click n0 "../modules/transactions.md"
    click n1 "../modules/test_agent_routing_service.md"
    click n2 "../modules/test_agent_routing_wave6_qualification.md"
    click n3 "../modules/test_agent_team_setup_qualification.md"
    click n4 "../modules/test_review_provenance.md"
    click n5 "../modules/test_routing_preview_focus.md"
    click n6 "../modules/test_routing_preview_team_scope.md"
    click n7 "../modules/test_scoped_review_evidence.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_agent_routing_service](../modules/test_agent_routing_service.md) |
| Inbound | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) |
| Inbound | [test_agent_team_setup_qualification](../modules/test_agent_team_setup_qualification.md) |
| Inbound | [test_review_provenance](../modules/test_review_provenance.md) |
| Inbound | [test_routing_preview_focus](../modules/test_routing_preview_focus.md) |
| Inbound | [test_routing_preview_team_scope](../modules/test_routing_preview_team_scope.md) |
| Inbound | [test_scoped_review_evidence](../modules/test_scoped_review_evidence.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `reload_session_fixture` | *(async)* `(db)` | — | Reload retained fixture objects instead of triggering async lazy I/O in assertions. |
