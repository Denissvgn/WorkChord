# test_deployment_topology Module

**Path:** `backend/tests/database/test_deployment_topology.py`

## Description

Wave 3 deployment, security, backup, and reset contracts.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `json` | `json` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `shutil` | `shutil` |
| `subprocess` | `subprocess` |
| `yaml` | `yaml` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_yaml` | `(name: str)` | — | — |
| `test_github_actions_run_scripts_have_valid_bash_syntax` | `() -> None` | — | — |
| `test_executable_python_does_not_read_ignored_contract_sources` | `() -> None` | — | — |
| `test_local_compose_makes_postgresql_the_integration_database` | `() -> None` | — | — |
| `test_rehearsal_and_production_topologies_have_multiple_bounded_replicas` | `() -> None` | — | — |
| `test_self_hosted_server_acceptance_uses_internal_pinned_analogues` | `() -> None` | — | — |
| `test_public_proxy_keeps_detailed_readiness_and_metrics_internal` | `() -> None` | — | — |
| `test_security_and_recovery_scripts_are_fail_closed` | `() -> None` | — | — |
| `test_server_image_identity_is_baked_and_not_runtime_overridable` | `() -> None` | — | — |
| `test_cutover_runbook_names_authority_timers_and_point_of_no_return` | `() -> None` | — | — |
