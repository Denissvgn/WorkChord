# ProviderAuditObservation

**Location:** `backend/app/autonomy/providers.py:96`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [providers](../modules/providers.md)

## Description

Separately credentialed read-only provider/audit observation.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `aware_observation_time` | field | observed_at | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `schema_version` | `Literal['workchord-provider-audit-observation-v1']` | `schema_version` | No | No | `'workchord-provider-audit-observation-v1'` | — | — | — |
| `collector_identity` | `Literal['pg-source-collector']` | `collector_identity` | No | No | `'pg-source-collector'` | — | — | — |
| `provider_request_id` | `str` | `provider_request_id` | Yes | No | — | max_length=512; min_length=1 | — | — |
| `provider_event_id` | `str` | `provider_event_id` | Yes | No | — | max_length=512; min_length=1 | — | — |
| `operation` | `str` | `operation` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `resource_ref` | `str` | `resource_ref` | Yes | No | — | max_length=2048; pattern=unknown (OPAQUE_REF_PATTERN) | — | — |
| `resource_generation_before` | `str` | `resource_generation_before` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `resource_generation_after` | `str` | `resource_generation_after` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `observed_at` | `datetime` | `observed_at` | Yes | No | — | — | — | — |
| `source_query_digest` | `str` | `source_query_digest` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `raw_audit_uri` | `str` | `raw_audit_uri` | Yes | No | — | max_length=2048; pattern=unknown (OPAQUE_REF_PATTERN) | — | — |
| `raw_audit_sha256` | `str` | `raw_audit_sha256` | Yes | No | — | pattern=unknown (SHA256_PATTERN) | — | — |
| `source_generation` | `str` | `source_generation` | Yes | No | — | max_length=255; min_length=1 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `aware_observation_time` | `(value: datetime) -> datetime` | `@field_validator('observed_at')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProviderAuditObservation (backend/app/autonomy/providers.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["correlate_provider_action (backend/app/autonomy/providers.py)"]
    n3["ProviderSourceCollector.collect_action (backend/app/autonomy/providers.py)"]
    n4["test_action_lease_binds_exact_attempt_target_generation_and_remote_key (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/providers.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/providers.md"
    click n3 "../modules/providers.md"
    click n4 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [providers](../modules/providers.md) | 1 | `collector_identity`, `observed_at`, `operation`, `provider_event_id`, `provider_request_id`, `raw_audit_sha256`, `raw_audit_uri`, `resource_generation_after`, `resource_generation_before`, `resource_ref`, `schema_version`, `source_generation` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `correlate_provider_action` | type_reference | [providers](../modules/providers.md) | — |
| `ProviderSourceCollector.collect_action` | type_reference | [providers](../modules/providers.md) | — |
| `test_action_lease_binds_exact_attempt_target_generation_and_remote_key` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
