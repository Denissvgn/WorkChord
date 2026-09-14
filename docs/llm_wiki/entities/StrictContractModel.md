# StrictContractModel

**Location:** `backend/app/autonomy/canonical.py:22`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [autonomy_canonical](../modules/autonomy_canonical.md)

## Description

Base class shared by immutable, extra-forbidden contracts.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |
| `frozen` | `True` | model_config |
| `str_strip_whitespace` | `True` | model_config |
| `validate_default` | `True` | model_config |
| `allow_inf_nan` | `False` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n1["BaseModel"]
    n2["AutonomyCharter (backend/app/autonomy/contracts/charter.py)"]
    n3["BootstrapActionManifest (backend/app/autonomy/contracts/charter.py)"]
    n4["BootstrapActionSlot (backend/app/autonomy/contracts/charter.py)"]
    n5["CharterVerificationReceipt (backend/app/autonomy/contracts/charter.py)"]
    n6["ExactResourceBinding (backend/app/autonomy/contracts/charter.py)"]
    n7["ExecutionBudget (backend/app/autonomy/contracts/charter.py)"]
    n8["ExecutionWindow (backend/app/autonomy/contracts/charter.py)"]
    n9["ImmutableInputBinding (backend/app/autonomy/contracts/charter.py)"]
    n10["MigrationPolicy (backend/app/autonomy/contracts/charter.py)"]
    n11["RevocationObservation (backend/app/autonomy/contracts/charter.py)"]
    n12["SignedAutonomyCharter (backend/app/autonomy/contracts/charter.py)"]
    n13["SignedBootstrapActionManifest (backend/app/autonomy/contracts/charter.py)"]
    n14["backend/app/autonomy/contracts/charter.py"]
    n15["backend/app/autonomy/contracts/postgresql/loader.py"]
    n16["backend/app/autonomy/contracts/topology.py"]
    n17["backend/app/autonomy/evidence.py"]
    n18["backend/app/autonomy/handoff.py"]
    n19["backend/app/autonomy/leases.py"]
    n20["backend/app/autonomy/orchestration.py"]
    n21["backend/app/autonomy/preflight.py"]
    n22["backend/app/autonomy/providers.py"]
    n23["backend/app/autonomy/server_acceptance.py"]
    n24["backend/app/autonomy/signing.py"]
    n25["backend/app/autonomy/status.py"]
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
    n14 --> n0
    n15 --> n0
    n16 --> n0
    n17 --> n0
    n18 --> n0
    n19 --> n0
    n20 --> n0
    n21 --> n0
    n22 --> n0
    n23 --> n0
    n24 --> n0
    n25 --> n0
    click n0 "../modules/autonomy_canonical.md"
    click n2 "../modules/charter.md"
    click n3 "../modules/charter.md"
    click n4 "../modules/charter.md"
    click n5 "../modules/charter.md"
    click n6 "../modules/charter.md"
    click n7 "../modules/charter.md"
    click n8 "../modules/charter.md"
    click n9 "../modules/charter.md"
    click n10 "../modules/charter.md"
    click n11 "../modules/charter.md"
    click n12 "../modules/charter.md"
    click n13 "../modules/charter.md"
    click n14 "../modules/charter.md"
    click n15 "../modules/loader.md"
    click n16 "../modules/topology.md"
    click n17 "../modules/evidence.md"
    click n18 "../modules/handoff.md"
    click n19 "../modules/leases.md"
    click n20 "../modules/orchestration.md"
    click n21 "../modules/preflight.md"
    click n22 "../modules/providers.md"
    click n23 "../modules/autonomy_server_acceptance.md"
    click n24 "../modules/signing.md"
    click n25 "../modules/status.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [autonomy_canonical](../modules/autonomy_canonical.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AutonomyCharter` | [charter](../modules/charter.md) |
| Subclass | `BootstrapActionManifest` | [charter](../modules/charter.md) |
| Subclass | `BootstrapActionSlot` | [charter](../modules/charter.md) |
| Subclass | `CharterVerificationReceipt` | [charter](../modules/charter.md) |
| Subclass | `ExactResourceBinding` | [charter](../modules/charter.md) |
| Subclass | `ExecutionBudget` | [charter](../modules/charter.md) |
| Subclass | `ExecutionWindow` | [charter](../modules/charter.md) |
| Subclass | `ImmutableInputBinding` | [charter](../modules/charter.md) |
| Subclass | `MigrationPolicy` | [charter](../modules/charter.md) |
| Subclass | `RevocationObservation` | [charter](../modules/charter.md) |
| Subclass | `SignedAutonomyCharter` | [charter](../modules/charter.md) |
| Subclass | `SignedBootstrapActionManifest` | [charter](../modules/charter.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `charter` | import | [charter](../modules/charter.md) | — |
| `loader` | import | [loader](../modules/loader.md) | — |
| `topology` | import | [topology](../modules/topology.md) | — |
| `evidence` | import | [evidence](../modules/evidence.md) | — |
| `handoff` | import | [handoff](../modules/handoff.md) | — |
| `leases` | import | [leases](../modules/leases.md) | — |
| `orchestration` | import | [orchestration](../modules/orchestration.md) | — |
| `preflight` | import | [preflight](../modules/preflight.md) | — |
| `providers` | import | [providers](../modules/providers.md) | — |
| `server_acceptance` | import | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | — |
| `signing` | import | [signing](../modules/signing.md) | — |
| `status` | import | [status](../modules/status.md) | — |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
