# test_planning_input_context Module

**Path:** `backend/tests/test_planning_input_context.py`

## Description

Initial shared-input observations are complete, bounded and side-effect free.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `Authority`, `AuthorityError` |
| `app.commands` | `AggregateVersionConflict`, `PlanningConflict` |
| `app.config` | `get_settings` |
| `app.main` | `app` |
| `app.models.calendar` | `Calendar` |
| `app.models.capacity` | `ProfileAvailability` |
| `app.models.identity` | `CommandAudit` |
| `app.models.iteration` | `Iteration` |
| `app.models.outbound_webhook` | `OutboundWebhookEvent` |
| `app.models.recovery` | `ApplicationSnapshot` |
| `app.models.team_member` | `TeamMember`, `Vacation` |
| `app.schemas.calendar` | `CalendarCreate`, `CalendarUpdate` |
| `app.schemas.planning_inputs` | `PlanningInputRevisions` |
| `app.services.calendar_service` | `CalendarService` |
| `app.services.capacity_service` | `CapacityService` |
| `app.services.planning_input_context` | `observe_planning_input` |
| `datetime` | `date` |
| `httpx` | `httpx` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/test_planning_input_context.py"]
    n1 --> n0
    click n1 "../modules/test_planning_input_context.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (18) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 1 |

> All 18 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_initial_resource_and_revision_read_does_not_advance_or_emit` | *(async)* `(delivery_store)` | — | — |
| `test_supplied_empty_scope_detects_new_allocation_in_compatibility_mode` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_empty_scope_remains_valid_for_unused_input_in_strict_mode` | *(async)* `(delivery_store, monkeypatch)` | — | — |
| `test_stale_and_contradictory_contexts_roll_back_shared_input` | *(async)* `(delivery_store)` | — | — |
| `test_scope_overflow_is_explicit_instead_of_partial_context` | *(async)* `(delivery_store)` | — | — |
| `test_unprivileged_context_read_does_not_disclose_hidden_scope` | *(async)* `(managed_store)` | — | — |
| `test_profile_local_version_contract_ignores_iteration_header_context` | *(async)* `(delivery_store)` | — | — |
| `test_body_context_limits_and_positive_keys_match_header_contract` | `()` | — | — |
| `test_context_covers_each_shared_resource_and_new_member_target` | *(async)* `(delivery_store)` | — | — |
