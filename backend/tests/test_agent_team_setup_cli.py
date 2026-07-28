"""No-network contract coverage for the agent-team setup CLI."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "api_keys"
    / "setup_agent_team.py"
)
SPEC = importlib.util.spec_from_file_location(
    "workchord_setup_agent_team",
    SCRIPT_PATH,
)
assert SPEC is not None and SPEC.loader is not None
setup_agent_team = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup_agent_team)


def test_cli_apply_sends_only_exact_actions_and_audit_headers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path = tmp_path / "master.json"
    plan_path = tmp_path / "plan.json"
    manifest = {
        "schema_version": "agent-team-master-v1",
        "topology_key": "delivery-team",
    }
    plan = {
        "expected_topology_revision": 3,
        "plan_digest": "a" * 64,
        "actions": [
            {"action_id": "safe-update-worker"},
            {"action_id": "propose-disable-retired"},
        ],
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    captured: dict[str, Any] = {}

    def fake_call_api(**kwargs: Any) -> dict[str, Any]:
        captured.update(kwargs)
        return {"status": "partial"}

    monkeypatch.setattr(setup_agent_team, "call_api", fake_call_api)
    args = SimpleNamespace(
        manifest=manifest_path,
        plan=plan_path,
        approve=["safe-update-worker"],
        confirm=["safe-update-worker"],
        base_url="http://workchord.test/",
        api_prefix="api",
        admin_key="operator-key",
        timeout=4.0,
        idempotency_key="setup-cli-idempotency",
        rationale="Approve one exact worker update",
        correlation_id="setup-cli-correlation",
    )

    assert setup_agent_team.run_apply(args) == {"status": "partial"}
    assert captured["url"] == (
        "http://workchord.test/api/agent/team-setup/apply"
    )
    assert captured["payload"] == {
        "manifest": manifest,
        "expected_topology_revision": 3,
        "plan_digest": "a" * 64,
        "approved_action_ids": ["safe-update-worker"],
        "confirmed_action_ids": ["safe-update-worker"],
    }
    assert captured["headers"] == {
        "Idempotency-Key": "setup-cli-idempotency",
        "X-Agent-Rationale": "Approve one exact worker update",
        "X-Correlation-ID": "setup-cli-correlation",
    }
    assert "operator-key" not in json.dumps(captured["payload"])


def test_cli_refuses_unknown_or_implicitly_confirmed_actions(
    tmp_path: Path,
) -> None:
    manifest_path = tmp_path / "master.json"
    plan_path = tmp_path / "plan.json"
    manifest_path.write_text("{}", encoding="utf-8")
    plan_path.write_text(
        json.dumps(
            {
                "expected_topology_revision": 0,
                "plan_digest": "b" * 64,
                "actions": [{"action_id": "create-primary-pm"}],
            }
        ),
        encoding="utf-8",
    )
    common = {
        "manifest": manifest_path,
        "plan": plan_path,
        "base_url": "http://workchord.test",
        "api_prefix": "/api",
        "admin_key": "operator-key",
        "timeout": 4.0,
        "idempotency_key": "setup-cli-idempotency",
        "rationale": "Apply setup",
        "correlation_id": "setup-cli-correlation",
    }

    with pytest.raises(SystemExit, match="not present"):
        setup_agent_team.run_apply(
            SimpleNamespace(
                **common,
                approve=["unknown-action"],
                confirm=[],
            )
        )
    with pytest.raises(SystemExit, match="must also be approved"):
        setup_agent_team.run_apply(
            SimpleNamespace(
                **common,
                approve=["create-primary-pm"],
                confirm=["other-action"],
            )
        )
