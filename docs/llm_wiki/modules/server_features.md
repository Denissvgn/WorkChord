# server_features Module

**Path:** `backend/app/server_features.py`

## Description

Server features a client can detect before it holds a credential.

A client such as a read-only dashboard reads this list from ``GET /api/auth/me``
to choose what to use, instead of comparing versions or commits. A name is
stable once published; a server without a feature does not list it.

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/identity.py"]
    n1["backend/app/server_features.py"]
    n2["backend/tests/test_delivery_prerequisite_tools.py"]
    n3["backend/tests/test_postponement_agent_tools.py"]
    n4["backend/tests/test_server_features.py"]
    n0 --> n1
    n2 --> n1
    n3 --> n1
    n4 --> n0
    n4 --> n1
    click n0 "../modules/routers_identity.md"
    click n1 "../modules/server_features.md"
    click n2 "../modules/test_delivery_prerequisite_tools.md"
    click n3 "../modules/test_postponement_agent_tools.md"
    click n4 "../modules/test_server_features.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_identity](../modules/routers_identity.md) |
| Inbound | [test_delivery_prerequisite_tools](../modules/test_delivery_prerequisite_tools.md) |
| Inbound | [test_postponement_agent_tools](../modules/test_postponement_agent_tools.md) |
| Inbound | [test_server_features](../modules/test_server_features.md) |
