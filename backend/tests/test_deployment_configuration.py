"""Deployment policy propagation and bounded acceptance artifact retention."""

from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("filename", ["docker-compose.yml", "docker-compose.prod.yml"])
@pytest.mark.parametrize("service", ["backend", "delivery-worker"])
def test_mutation_version_policy_is_forwarded_with_safe_default(filename, service):
    definition = yaml.safe_load((ROOT / filename).read_text())
    environment = definition["services"][service]["environment"]
    if isinstance(environment, list):
        environment = dict(value.split("=", 1) for value in environment)
    assert environment.get("STRICT_MUTATION_VERSIONS") == "${STRICT_MUTATION_VERSIONS:-false}"


def test_self_hosted_acceptance_exports_receipts_even_on_failure():
    workflow = yaml.safe_load((ROOT / ".github/workflows/deployment-acceptance.yml").read_text())
    steps = workflow["jobs"]["server-acceptance"]["steps"]
    exports = [step for step in steps if step.get("uses", "").startswith("actions/upload-artifact@")]
    assert exports, "The ephemeral runner must retain bounded verification evidence"
    for step in exports:
        assert step.get("if") == "always()"
        paths = step["with"]["path"].splitlines()
        assert all(path.startswith(".runtime/autonomy/reports/") for path in paths)
        assert not any("server.env" in path or path.endswith("/**") for path in paths)
    paths = [path for step in exports for path in step["with"]["path"].splitlines()]
    assert ".runtime/autonomy/reports/latest.json" in paths
    assert ".runtime/autonomy/reports/trusted-signer-public-key.b64" in paths
