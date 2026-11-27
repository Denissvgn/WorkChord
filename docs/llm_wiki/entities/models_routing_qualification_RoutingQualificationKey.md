# RoutingQualificationKey

**Location:** `backend/app/models/routing_qualification.py:16`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_routing_qualification](../modules/models_routing_qualification.md)

## Description

One deployment-declared key that catalog entries and task requirements may name.

The key name never changes. Retiring keeps the row and its history, so a
later declaration under the same name continues the revision sequence.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `key` | `Mapped[str]` | `mapped_column(String(120), nullable=False)` | — |
| `label` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text)` | — |
| `state` | `Mapped[str]` | `mapped_column(String(20), default='active', nullable=False)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `retired_at` | `Mapped[Optional[datetime]]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `revisions` | `Mapped[list['RoutingQualificationKeyRevision']]` | `relationship('RoutingQualificationKeyRevision', back_populates='qualification_key', order_by='RoutingQualificationKeyRevision.revision')` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingQualificationKey (backend/app/models/routing_qualification.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["RoutingQualificationKeyService._bounded_usage (backend/app/services/routing_qualification_key_service.py)"]
    n4["RoutingQualificationKeyService._key (backend/app/services/routing_qualification_key_service.py)"]
    n5["RoutingQualificationKeyService._record (backend/app/services/routing_qualification_key_service.py)"]
    n6["RoutingQualificationKeyService._require_revision (backend/app/services/routing_qualification_key_service.py)"]
    n7["RoutingQualificationKeyService._response (backend/app/services/routing_qualification_key_service.py)"]
    n8["RoutingQualificationKeyService._result (backend/app/services/routing_qualification_key_service.py)"]
    n9["RoutingQualificationKeyService._retire_usage (backend/app/services/routing_qualification_key_service.py)"]
    n10["RoutingQualificationKeyService.declare (backend/app/services/routing_qualification_key_service.py)"]
    n11["RoutingQualificationKeyService.get_key (backend/app/services/routing_qualification_key_service.py)"]
    n12["RoutingQualificationKeyService.list_registry (backend/app/services/routing_qualification_key_service.py)"]
    n13["RoutingQualificationKeyService.retire (backend/app/services/routing_qualification_key_service.py)"]
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
    click n0 "../modules/models_routing_qualification.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/routing_qualification_key_service.md"
    click n4 "../modules/routing_qualification_key_service.md"
    click n5 "../modules/routing_qualification_key_service.md"
    click n6 "../modules/routing_qualification_key_service.md"
    click n7 "../modules/routing_qualification_key_service.md"
    click n8 "../modules/routing_qualification_key_service.md"
    click n9 "../modules/routing_qualification_key_service.md"
    click n10 "../modules/routing_qualification_key_service.md"
    click n11 "../modules/routing_qualification_key_service.md"
    click n12 "../modules/routing_qualification_key_service.md"
    click n13 "../modules/routing_qualification_key_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_routing_qualification](../modules/models_routing_qualification.md) | 0 | `created_at`, `description`, `id`, `key`, `label`, `retired_at`, `revision`, `revisions`, `state`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `RoutingQualificationKeyService._bounded_usage` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._key` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._record` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._require_revision` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._response` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._result` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._retire_usage` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService.declare` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService.get_key` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService.list_registry` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService.retire` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |

> References: showing 12 of 19 logical references; 7 omitted by the 12-row generated summary limit.
