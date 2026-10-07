# QualificationInputError

**Location:** `scripts/load/common.py:34`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [load_common](../modules/load_common.md)

## Description

A workload or evidence input is unsafe, stale, or incomplete.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["QualificationInputError (scripts/load/common.py)"]
    n1["ValueError"]
    n2["_authorized_database_url (scripts/load/collect.py)"]
    n3["_derive (scripts/load/collect.py)"]
    n4["_evidence_metrics (scripts/load/collect.py)"]
    n5["_one (scripts/load/collect.py)"]
    n6["_timestamp (scripts/load/collect.py)"]
    n7["authorized_base_url (scripts/load/common.py)"]
    n8["capacity_contract (scripts/load/common.py)"]
    n9["contract_bundle (scripts/load/common.py)"]
    n10["contract_member_json (scripts/load/common.py)"]
    n11["contract_member_sha256 (scripts/load/common.py)"]
    n12["read_json_object (scripts/load/common.py)"]
    n13["seal_document (scripts/load/common.py)"]
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
    click n0 "../modules/load_common.md"
    click n2 "../modules/collect.md"
    click n3 "../modules/collect.md"
    click n4 "../modules/collect.md"
    click n5 "../modules/collect.md"
    click n6 "../modules/collect.md"
    click n7 "../modules/load_common.md"
    click n8 "../modules/load_common.md"
    click n9 "../modules/load_common.md"
    click n10 "../modules/load_common.md"
    click n11 "../modules/load_common.md"
    click n12 "../modules/load_common.md"
    click n13 "../modules/load_common.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [load_common](../modules/load_common.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_authorized_database_url` | call | [collect](../modules/collect.md) | 5 |
| `_derive` | call | [collect](../modules/collect.md) | 9 |
| `_evidence_metrics` | call | [collect](../modules/collect.md) | 2 |
| `_one` | call | [collect](../modules/collect.md) | 1 |
| `_timestamp` | call | [collect](../modules/collect.md) | 1 |
| `authorized_base_url` | call | [load_common](../modules/load_common.md) | 6 |
| `capacity_contract` | call | [load_common](../modules/load_common.md) | 1 |
| `contract_bundle` | call | [load_common](../modules/load_common.md) | 1 |
| `contract_member_json` | call | [load_common](../modules/load_common.md) | 2 |
| `contract_member_sha256` | call | [load_common](../modules/load_common.md) | 1 |
| `read_json_object` | call | [load_common](../modules/load_common.md) | 2 |
| `seal_document` | call | [load_common](../modules/load_common.md) | 1 |

> References: showing 12 of 57 logical references; 45 omitted by the 12-row generated summary limit.
