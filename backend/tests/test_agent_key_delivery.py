"""An operator can hand an agent its key without chat or an inherited shell."""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

import httpx
import pytest

from app import mcp_server
from app.agent_key_file import AgentKeyFileError, read_agent_key_file
from app.main import app as main_app
from app.routers import agent_connect


_PROVISION_SCRIPT = (
    Path(__file__).resolve().parents[2] / "scripts" / "api_keys" / "create_agent_actor.py"
)
_PROVISION_SPEC = importlib.util.spec_from_file_location(
    "workchord_create_agent_actor_key_file", _PROVISION_SCRIPT
)
assert _PROVISION_SPEC is not None and _PROVISION_SPEC.loader is not None
provision_actor = importlib.util.module_from_spec(_PROVISION_SPEC)
_PROVISION_SPEC.loader.exec_module(provision_actor)

posix_only = pytest.mark.skipif(os.name != "posix", reason="owner-only file modes are POSIX")


def _key_file(tmp_path: Path, content: str, mode: int = 0o600) -> Path:
    path = tmp_path / "agent.key"
    path.write_text(content, encoding="utf-8")
    path.chmod(mode)
    return path


# Key file reader


def test_key_file_returns_the_single_key_without_surrounding_whitespace(tmp_path: Path) -> None:
    assert read_agent_key_file(_key_file(tmp_path, "  wc_agent_example \n\n")) == "wc_agent_example"


@posix_only
def test_key_file_readable_by_others_is_refused_without_revealing_content(tmp_path: Path) -> None:
    path = _key_file(tmp_path, "wc_agent_secret_value\n", mode=0o644)
    with pytest.raises(AgentKeyFileError) as raised:
        read_agent_key_file(path)
    assert "chmod 600" in str(raised.value)
    assert "wc_agent_secret_value" not in str(raised.value)


@pytest.mark.parametrize("content", ["", "\n", "one\ntwo\n"])
def test_key_file_must_hold_exactly_one_key(tmp_path: Path, content: str) -> None:
    with pytest.raises(AgentKeyFileError, match="exactly one key"):
        read_agent_key_file(_key_file(tmp_path, content))


def test_missing_key_file_is_named(tmp_path: Path) -> None:
    with pytest.raises(AgentKeyFileError, match="does not exist"):
        read_agent_key_file(tmp_path / "absent.key")


# Stdio MCP startup


@pytest.fixture
def stdio_key_state(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(mcp_server.MCP_AGENT_API_KEY_ENV, raising=False)
    monkeypatch.delenv(mcp_server.MCP_AGENT_API_KEY_FILE_ENV, raising=False)
    monkeypatch.setattr(mcp_server, "_stdio_file_agent_key", None)
    return monkeypatch


def test_stdio_mcp_reads_its_key_from_the_configured_file(
    stdio_key_state: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    stdio_key_state.setenv(
        mcp_server.MCP_AGENT_API_KEY_FILE_ENV, str(_key_file(tmp_path, "wc_agent_from_file\n"))
    )
    assert mcp_server._load_stdio_agent_key() is True
    assert mcp_server._current_agent_key() == "wc_agent_from_file"


def test_stdio_mcp_key_variable_wins_over_the_key_file(
    stdio_key_state: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    stdio_key_state.setenv(mcp_server.MCP_AGENT_API_KEY_ENV, "wc_agent_from_env")
    stdio_key_state.setenv(
        mcp_server.MCP_AGENT_API_KEY_FILE_ENV, str(_key_file(tmp_path, "wc_agent_from_file\n"))
    )
    assert mcp_server._load_stdio_agent_key() is True
    assert mcp_server._current_agent_key() == "wc_agent_from_env"


def test_stdio_mcp_without_any_key_names_both_sources(
    stdio_key_state: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as raised:
        mcp_server.main(["--transport", "stdio"])
    assert raised.value.code == 2
    error = capsys.readouterr().err
    assert "MCP_AGENT_API_KEY" in error and "MCP_AGENT_API_KEY_FILE" in error


# Provisioning script


class _ActorResponse:
    def __enter__(self):
        return self

    def __exit__(self, *_args: Any) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(
            {"id": 7, "name": "desk-pm", "api_key": "wc_agent_one_time_value"}
        ).encode("utf-8")


def _run_provisioning(
    monkeypatch: pytest.MonkeyPatch, *args: str
) -> None:
    monkeypatch.setattr(provision_actor.request, "urlopen", lambda req, *, timeout: _ActorResponse())
    monkeypatch.setattr(
        sys,
        "argv",
        ["create_agent_actor.py", "--bootstrap-key", "bootstrap", "--name", "desk-pm", "--role", "pm", *args],
    )
    provision_actor.main()


@posix_only
def test_provisioning_writes_the_key_to_an_owner_only_file_and_prints_only_its_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    _run_provisioning(monkeypatch, "--key-file")

    key_file = tmp_path / "config" / "workchord" / "workchord-pm.key"
    assert key_file.read_text(encoding="utf-8") == "wc_agent_one_time_value\n"
    assert key_file.stat().st_mode & 0o777 == 0o600
    assert read_agent_key_file(key_file) == "wc_agent_one_time_value"
    captured = capsys.readouterr()
    assert "wc_agent_one_time_value" not in captured.out + captured.err
    assert f"AGENT_API_KEY_FILE={key_file}" in captured.out
    assert f"MCP_AGENT_API_KEY_FILE={key_file}" in captured.out


def test_provisioning_refuses_an_existing_key_file_before_creating_the_actor(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    existing = tmp_path / "taken.key"
    existing.write_text("old\n", encoding="utf-8")

    def unexpected(*_args: Any, **_kwargs: Any):
        raise AssertionError("the actor must not be created")

    monkeypatch.setattr(provision_actor.request, "urlopen", unexpected)
    monkeypatch.setattr(
        sys,
        "argv",
        ["create_agent_actor.py", "--bootstrap-key", "b", "--key-file", str(existing)],
    )
    with pytest.raises(SystemExit, match="already exists"):
        provision_actor.main()
    assert existing.read_text(encoding="utf-8") == "old\n"


def test_provisioning_refuses_a_key_file_inside_a_repository(tmp_path: Path) -> None:
    (tmp_path / "repo" / ".git").mkdir(parents=True)
    with pytest.raises(SystemExit, match="Git work tree"):
        provision_actor.check_key_file_target(tmp_path / "repo" / "keys" / "pm.key")


# Public connection hint


@pytest.mark.asyncio
async def test_connect_hint_is_public_secret_free_and_lists_role_scopes(
    deployed_agent_skill_release: Path,
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=main_app), base_url="http://workchord.test"
    ) as client:
        response = await client.get("/.well-known/workchord/agent-connect.json")

    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == "workchord-agent-connect/v1"
    assert body["capabilities_path"].endswith("/agent/capabilities")
    assert body["mcp_http_path"].endswith("/mcp")
    assert body["credential"]["anonymous_agent_access"] is False
    assert "AGENT_API_KEY_FILE" in body["credential"]["key_sources"]
    roles = {role["skill"]: role for role in body["roles"]}
    assert set(roles) == {"workchord-pm", "workchord-reviewer", "workchord-worker"}
    assert roles["workchord-pm"]["actor_role"] == "pm"
    assert "planning:write" in roles["workchord-pm"]["required_scopes"]
    def field_names(value: Any) -> set[str]:
        if isinstance(value, dict):
            return set(value).union(*(field_names(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(field_names(item) for item in value))
        return set()

    assert not {"api_key", "key", "token", "secret"} & field_names(body)


@pytest.mark.asyncio
async def test_connect_hint_still_answers_when_skill_artifacts_are_missing(tmp_path: Path) -> None:
    from app.services.agent_skill_bundle_service import AgentSkillBundleService

    async def missing_service() -> AgentSkillBundleService:
        return AgentSkillBundleService(tmp_path / "absent")

    main_app.dependency_overrides[agent_connect.get_agent_connect_bundle_service] = missing_service
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=main_app), base_url="http://workchord.test"
        ) as client:
            response = await client.get("/.well-known/workchord/agent-connect.json")
    finally:
        main_app.dependency_overrides.pop(agent_connect.get_agent_connect_bundle_service, None)

    assert response.status_code == 200
    assert response.json()["roles"] == []
