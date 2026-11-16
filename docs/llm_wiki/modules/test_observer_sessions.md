# test_observer_sessions Module

**Path:** `backend/tests/test_observer_sessions.py`

## Description

Paired observer sessions read like their principal, change nothing, and renew within a cap.

## Imports

| Source | Symbols |
|--------|---------|
| `app.config` | `Settings`, `get_settings` |
| `app.models.user_session` | `UserSession` |
| `app.services.identity_service` | `digest` |
| `app.utils.time` | `as_utc`, `utc_now` |
| `base64` | `base64` |
| `datetime` | `timedelta` |
| `hashlib` | `hashlib` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `pytest_asyncio` | `pytest_asyncio` |
| `sqlalchemy` | `func`, `select` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client`, `managed_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/config.py"]
    n1["backend/app/models/user_session.py"]
    n2["backend/app/services/identity_service.py"]
    n3["backend/app/utils/time.py"]
    n4["backend/tests/test_agdash_link_provider.py"]
    n5["backend/tests/test_delivery_scenarios.py"]
    n6["backend/tests/test_managed_authority.py"]
    n7["backend/tests/test_observer_sessions.py"]
    n8["backend/tests/test_person_assignment_reads.py"]
    n9["backend/tests/test_team_topology_read.py"]
    n1 --> n3
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n6
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n5
    n8 --> n6
    n8 --> n7
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n5
    n9 --> n6
    n9 --> n7
    click n0 "../modules/config.md"
    click n1 "../modules/user_session.md"
    click n2 "../modules/identity_service.md"
    click n3 "../modules/time.md"
    click n4 "../modules/test_agdash_link_provider.md"
    click n5 "../modules/test_delivery_scenarios.md"
    click n6 "../modules/test_managed_authority.md"
    click n7 "../modules/test_observer_sessions.md"
    click n8 "../modules/test_person_assignment_reads.md"
    click n9 "../modules/test_team_topology_read.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_agdash_link_provider](../modules/test_agdash_link_provider.md) |
| Inbound | [test_person_assignment_reads](../modules/test_person_assignment_reads.md) |
| Inbound | [test_team_topology_read](../modules/test_team_topology_read.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [identity_service](../modules/identity_service.md) |
| Outbound | [time](../modules/time.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 2 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `local_store` | *(async)* `(delivery_store, monkeypatch)` | `@pytest_asyncio.fixture` | — |
| `bearer` | `(token)` | — | — |
| `start` | *(async)* `(access = 'observe', label = 'Desk reader')` | — | — |
| `exchange` | *(async)* `(connection)` | — | — |
| `approve_with` | *(async)* `(browser, connection, label = 'Desk reader')` | — | — |
| `pair_managed` | *(async)* `(token, csrf, label = 'Desk reader')` | — | — |
| `session_row` | *(async)* `(factory, token)` | — | — |
| `move_sign_in` | *(async)* `(factory, token, *, ago)` | — | — |
| `session_count` | *(async)* `(factory)` | — | — |
| `assert_read_only` | `(response)` | — | — |
| `test_managed_observer_reads_as_its_person_and_changes_nothing` | *(async)* `(managed_store)` | — | — |
| `test_observer_cannot_approve_pairings_or_travel_with_another_credential` | *(async)* `(managed_store)` | — | — |
| `test_observer_renewal_rotates_never_upgrades_and_stops_at_the_cap` | *(async)* `(managed_store)` | — | — |
| `test_person_renewal_keeps_the_sign_in_time_and_rotates_bearers` | *(async)* `(managed_store)` | — | — |
| `test_signed_in_cookie_rotation_shares_the_renewal_cap` | *(async)* `(managed_store)` | — | — |
| `test_trusted_local_pairs_observers_from_its_browser_and_can_revoke_them` | *(async)* `(local_store)` | — | — |
| `test_a_local_observer_stops_working_when_the_workspace_becomes_managed` | *(async)* `(local_store, monkeypatch)` | — | — |
| `test_renewal_caps_cannot_be_shorter_than_one_session` | `()` | — | — |
