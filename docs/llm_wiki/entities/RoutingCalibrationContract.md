# RoutingCalibrationContract

**Location:** `backend/app/models/routing_calibration.py:29`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_routing_calibration](../modules/models_routing_calibration.md)

## Description

The current revision of one named calibration contract.

Its terms are complete on every revision. Submitting new terms makes the
contract ``submitted`` again, so an approval always covers exactly the
terms the approver read.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `key` | `Mapped[str]` | `mapped_column(String(120), nullable=False)` | — |
| `schema_version` | `Mapped[str]` | `mapped_column(String(60), nullable=False)` | — |
| `state` | `Mapped[str]` | `mapped_column(String(20), default='submitted', nullable=False)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `terms` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, nullable=False)` | — |
| `terms_digest` | `Mapped[str]` | `mapped_column(String(64), nullable=False)` | — |
| `submitted_by_actor_type` | `Mapped[str]` | `mapped_column(String(50), nullable=False)` | — |
| `submitted_by_actor_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('agent_actors.id'), nullable=True)` | — |
| `submitted_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `approved_by_actor_type` | `Mapped[Optional[str]]` | `mapped_column(String(50), nullable=True)` | — |
| `approved_by_actor_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('agent_actors.id'), nullable=True)` | — |
| `approved_at` | `Mapped[Optional[datetime]]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `approval_reason` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `approved_as` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `revisions` | `Mapped[list['RoutingCalibrationContractRevision']]` | `relationship('RoutingCalibrationContractRevision', back_populates='contract', order_by='RoutingCalibrationContractRevision.revision')` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingCalibrationContract (backend/app/models/routing_calibration.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["RoutingCalibrationContractService._contract (backend/app/services/routing_calibration_contract_service.py)"]
    n4["RoutingCalibrationContractService._record (backend/app/services/routing_calibration_contract_service.py)"]
    n5["RoutingCalibrationContractService._require_revision (backend/app/services/routing_calibration_contract_service.py)"]
    n6["RoutingCalibrationContractService._response (backend/app/services/routing_calibration_contract_service.py)"]
    n7["RoutingCalibrationContractService._result (backend/app/services/routing_calibration_contract_service.py)"]
    n8["RoutingCalibrationContractService._submitted_by (backend/app/services/routing_calibration_contract_service.py)"]
    n9["RoutingCalibrationContractService._validated_terms (backend/app/services/routing_calibration_contract_service.py)"]
    n10["RoutingCalibrationContractService.approve (backend/app/services/routing_calibration_contract_service.py)"]
    n11["RoutingCalibrationContractService.get_contract (backend/app/services/routing_calibration_contract_service.py)"]
    n12["RoutingCalibrationContractService.list_contracts (backend/app/services/routing_calibration_contract_service.py)"]
    n13["RoutingCalibrationContractService.revise (backend/app/services/routing_calibration_contract_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/models_routing_calibration.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/routing_calibration_contract_service.md"
    click n4 "../modules/routing_calibration_contract_service.md"
    click n5 "../modules/routing_calibration_contract_service.md"
    click n6 "../modules/routing_calibration_contract_service.md"
    click n7 "../modules/routing_calibration_contract_service.md"
    click n8 "../modules/routing_calibration_contract_service.md"
    click n9 "../modules/routing_calibration_contract_service.md"
    click n10 "../modules/routing_calibration_contract_service.md"
    click n11 "../modules/routing_calibration_contract_service.md"
    click n12 "../modules/routing_calibration_contract_service.md"
    click n13 "../modules/routing_calibration_contract_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_routing_calibration](../modules/models_routing_calibration.md) | 0 | `approval_reason`, `approved_as`, `approved_at`, `approved_by_actor_id`, `approved_by_actor_type`, `created_at`, `id`, `key`, `revision`, `revisions`, `schema_version`, `state` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `RoutingCalibrationContractService._contract` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService._record` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService._require_revision` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService._response` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService._result` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService._submitted_by` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService._validated_terms` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService.approve` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService.get_contract` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService.list_contracts` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |
| `RoutingCalibrationContractService.revise` | type_reference | [routing_calibration_contract_service](../modules/routing_calibration_contract_service.md) | — |

> References: showing 12 of 16 logical references; 4 omitted by the 12-row generated summary limit.
