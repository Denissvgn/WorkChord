# BlockedServerAcceptance

**Location:** `backend/app/autonomy/server_acceptance.py:260`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md)

## Description

_Auto-generated from `BlockedServerAcceptance` in `backend/app/autonomy/server_acceptance.py`._

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `canonical_blocked_result` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `schema_version` | `Literal['workchord-self-hosted-server-acceptance-v1']` | `schema_version` | No | No | `'workchord-self-hosted-server-acceptance-v1'` | — | — | — |
| `decision` | `Literal['SELF-HOSTED-SERVER-BLOCKED']` | `decision` | No | No | `'SELF-HOSTED-SERVER-BLOCKED'` | — | — | — |
| `evaluated_at` | `datetime` | `evaluated_at` | Yes | No | — | — | — | — |
| `source_revision` | `str` | `source_revision` | Yes | No | — | — | — | — |
| `release_fingerprint` | `str` | `release_fingerprint` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `blocker_code` | `str` | `blocker_code` | Yes | No | — | pattern=unknown (IDENTIFIER_PATTERN) | — | — |
| `cause_kind` | `str \| None` | `cause_kind` | No | Yes | `None` | pattern=unknown (IDENTIFIER_PATTERN) | — | — |
| `accepted_as_production_evidence` | `Literal[False]` | `accepted_as_production_evidence` | No | No | `False` | — | — | — |
| `accepted_as_zero_human_evidence` | `Literal[False]` | `accepted_as_zero_human_evidence` | No | No | `False` | — | — | — |
| `production_autonomy_qualified` | `Literal[False]` | `production_autonomy_qualified` | No | No | `False` | — | — | — |
| `production_gates_satisfied` | `Literal[False]` | `production_gates_satisfied` | No | No | `False` | — | — | — |
| `production_program_decision` | `Literal['NO-SHIP']` | `production_program_decision` | No | No | `'NO-SHIP'` | — | — | — |
| `receipt_digest` | `str` | `receipt_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `canonical_blocked_result` | `() -> 'BlockedServerAcceptance'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["BlockedServerAcceptance (backend/app/autonomy/server_acceptance.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["backend/app/autonomy/acceptance_artifacts.py"]
    n3["BlockedServerAcceptance.canonical_blocked_result (backend/app/autonomy/server_acceptance.py)"]
    n4["build_blocked_result (backend/app/autonomy/server_acceptance.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/autonomy_server_acceptance.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/acceptance_artifacts.md"
    click n3 "../modules/autonomy_server_acceptance.md"
    click n4 "../modules/autonomy_server_acceptance.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 1 | `accepted_as_production_evidence`, `accepted_as_zero_human_evidence`, `blocker_code`, `cause_kind`, `decision`, `evaluated_at`, `production_autonomy_qualified`, `production_gates_satisfied`, `production_program_decision`, `receipt_digest`, `release_fingerprint`, `schema_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `acceptance_artifacts` | import | [acceptance_artifacts](../modules/acceptance_artifacts.md) | — |
| `BlockedServerAcceptance.canonical_blocked_result` | type_reference | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | — |
| `build_blocked_result` | call | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | 1 |
| `build_blocked_result` | type_reference | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) | — |
