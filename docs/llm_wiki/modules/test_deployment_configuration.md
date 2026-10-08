# test_deployment_configuration Module

**Path:** `backend/tests/test_deployment_configuration.py`

## Description

Deployment policy propagation and bounded acceptance artifact retention.

## Imports

| Source | Symbols |
|--------|---------|
| `pathlib` | `Path` |
| `pytest` | `pytest` |
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
| `test_mutation_version_policy_is_forwarded_with_safe_default` | `(filename, service)` | `@pytest.mark.parametrize('filename', ['docker-compose.yml', 'docker-compose.prod.yml'])`, `@pytest.mark.parametrize('service', ['backend', 'delivery-worker'])` | — |
| `test_self_hosted_acceptance_exports_receipts_even_on_failure` | `()` | — | — |
