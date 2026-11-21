# IdentitySubject

**Location:** `backend/app/models/identity.py:23`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_identity](../modules/models_identity.md)

## Description

_Auto-generated from `IdentitySubject` in `backend/app/models/identity.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `principal_id` | `Mapped[int]` | `mapped_column(ForeignKey('principals.id', ondelete='CASCADE'), index=True)` | — |
| `issuer` | `Mapped[str]` | `mapped_column(String(512), nullable=False)` | — |
| `subject` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IdentitySubject (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["acting_principal_id (backend/app/services/identity_service.py)"]
    n4["IdentityService.finish_login (backend/app/services/identity_service.py)"]
    n5["backend/tests/test_acceptance_attribution.py"]
    n6["managed_store (backend/tests/test_managed_authority.py)"]
    n7["test_issuer_subject_unique_without_name_or_ip_identity (backend/tests/test_managed_authority.py)"]
    n8["test_authenticated_manual_submission_and_assigned_agent_verdict (backend/tests/test_manual_review_provenance.py)"]
    n9["scripts/ci/serve_disposable_api.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/models_identity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/identity_service.md"
    click n4 "../modules/identity_service.md"
    click n5 "../modules/test_acceptance_attribution.md"
    click n6 "../modules/test_managed_authority.md"
    click n7 "../modules/test_managed_authority.md"
    click n8 "../modules/test_manual_review_provenance.md"
    click n9 "../modules/serve_disposable_api.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_identity](../modules/models_identity.md) | 0 | `created_at`, `id`, `issuer`, `principal_id`, `subject` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `acting_principal_id` | call | [identity_service](../modules/identity_service.md) | 1 |
| `IdentityService.finish_login` | call | [identity_service](../modules/identity_service.md) | 1 |
| `test_acceptance_attribution` | import | [test_acceptance_attribution](../modules/test_acceptance_attribution.md) | — |
| `managed_store` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |
| `test_issuer_subject_unique_without_name_or_ip_identity` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |
| `test_authenticated_manual_submission_and_assigned_agent_verdict` | call | [test_manual_review_provenance](../modules/test_manual_review_provenance.md) | 1 |
| `serve_disposable_api` | import | [serve_disposable_api](../modules/serve_disposable_api.md) | — |
