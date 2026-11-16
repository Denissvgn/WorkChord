# test_agdash_link_provider Module

**Path:** `backend/tests/test_agdash_link_provider.py`

## Description

agdash session links: a named provider, loopback display URLs for it alone, and no duplicates.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.external_link` | `ExternalLinkUpdate`, `TaskExternalLinkCreate` |
| `pydantic` | `ValidationError` |
| `pytest` | `pytest` |
| `tests.test_delivery_scenarios` | `delivery_store` |
| `tests.test_managed_authority` | `client` |
| `tests.test_observer_sessions` | `local_store` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/schemas/external_link.py"]
    n1["backend/tests/test_agdash_link_provider.py"]
    n2["backend/tests/test_delivery_scenarios.py"]
    n3["backend/tests/test_managed_authority.py"]
    n4["backend/tests/test_observer_sessions.py"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n4 --> n2
    n4 --> n3
    click n0 "../modules/schemas_external_link.md"
    click n1 "../modules/test_agdash_link_provider.md"
    click n2 "../modules/test_delivery_scenarios.md"
    click n3 "../modules/test_managed_authority.md"
    click n4 "../modules/test_observer_sessions.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [schemas_external_link](../modules/schemas_external_link.md) |
| Outbound | [test_delivery_scenarios](../modules/test_delivery_scenarios.md) |
| Outbound | [test_managed_authority](../modules/test_managed_authority.md) |
| Outbound | [test_observer_sessions](../modules/test_observer_sessions.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_an_agdash_link_may_open_on_the_observing_machine` | `(url)` | `@pytest.mark.parametrize('url', ['http://127.0.0.1:8730/s/1', 'http://localhost:8730/s/1', 'http://[::1]:8730/s/1', 'https://agdash.example/s/1'])` | — |
| `test_an_agdash_link_still_refuses_private_networks_credentials_and_other_schemes` | `(url)` | `@pytest.mark.parametrize('url', ['http://192.168.1.20:8730/s/1', 'http://user:secret@127.0.0.1/s/1', 'file:///tmp/s'])` | — |
| `test_other_providers_keep_refusing_loopback_links` | `()` | — | — |
| `test_a_session_link_is_created_once_and_updates_keep_the_url_rule` | *(async)* `(local_store)` | — | — |
