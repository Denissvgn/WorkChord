# routing_calibration Module

**Path:** `backend/app/models/routing_calibration.py`

## Description

Calibration contracts that state when performance history may inform routing.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `JSON`, `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/routing_calibration.py"]
    n3["backend/app/services/routing_calibration_contract_service.py"]
    n4["backend/app/services/routing_qualification_key_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/test_agent_routing_service.py"]
    n7["backend/tests/test_routing_calibration_contracts.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n5
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n4 --> n2
    n4 --> n5
    n6 --> n2
    n6 --> n4
    n7 --> n0
    n7 --> n2
    n7 --> n3
    n7 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_routing_calibration.md"
    click n3 "../modules/routing_calibration_contract_service.md"
    click n4 "../modules/routing_qualification_key_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_agent_routing_service.md"
    click n7 "../modules/test_routing_calibration_contracts.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) |
| Inbound | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) |
| Inbound | [test_agent_routing_service](../modules/test_agent_routing_service.md) |
| Inbound | [test_routing_calibration_contracts](../modules/test_routing_calibration_contracts.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [RoutingCalibrationContract](../entities/RoutingCalibrationContract.md) | 29 | `Base` | The current revision of one named calibration contract. |
| [RoutingCalibrationContractRevision](../entities/RoutingCalibrationContractRevision.md) | 82 | `Base` | The terms and state a contract had after one submit or approve command, and why. |
