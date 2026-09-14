# __init__ Module

**Path:** `backend/app/autonomy/contracts/postgresql/__init__.py`

## Description

Installed PostgreSQL autonomous-program contract bundle.

## Imports

| Source | Symbols |
|--------|---------|
| `app.autonomy.contracts.postgresql.loader` | `ContractBundleError`, `PostgreSQLContractBundle`, `load_postgresql_contract_bundle` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/contracts/postgresql/__init__.py"]
    n1["backend/app/autonomy/contracts/postgresql/loader.py"]
    n2["backend/app/autonomy/server_acceptance.py"]
    n3["backend/app/cli/agent_preflight.py"]
    n4["backend/app/main.py"]
    n5["backend/tests/autonomy/test_autonomy_foundation.py"]
    n6["backend/tests/autonomy/test_server_acceptance.py"]
    n7["backend/tests/database/test_runtime_policy.py"]
    n8["backend/tests/test_capacity_contract.py"]
    n9["scripts/load/common.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n6 --> n2
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/postgresql___init__.md"
    click n1 "../modules/loader.md"
    click n2 "../modules/autonomy_server_acceptance.md"
    click n3 "../modules/agent_preflight.md"
    click n4 "../modules/app_main.md"
    click n5 "../modules/test_autonomy_foundation.md"
    click n6 "../modules/test_server_acceptance.md"
    click n7 "../modules/test_runtime_policy.md"
    click n8 "../modules/test_capacity_contract.md"
    click n9 "../modules/load_common.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [autonomy_server_acceptance](../modules/autonomy_server_acceptance.md) |
| Inbound | [agent_preflight](../modules/agent_preflight.md) |
| Inbound | [app_main](../modules/app_main.md) |
| Inbound | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) |
| Inbound | [test_server_acceptance](../modules/test_server_acceptance.md) |
| Inbound | [test_runtime_policy](../modules/test_runtime_policy.md) |
| Inbound | [test_capacity_contract](../modules/test_capacity_contract.md) |
| Inbound | [load_common](../modules/load_common.md) |
| Outbound | [loader](../modules/loader.md) |
