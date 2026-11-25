"""Managed readiness stays status-only unless the readiness-detail token matches."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest
from starlette.requests import Request

from app import main

DETAIL = {
    "status": "ready",
    "database": {"connected": True, "schema_current": True},
    "migration_gate": {"clear": True},
}


def _request(headers: dict[str, str]) -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/health/ready",
            "headers": [
                (name.lower().encode("latin-1"), value.encode("latin-1"))
                for name, value in headers.items()
            ],
        }
    )


async def _readiness(
    monkeypatch: pytest.MonkeyPatch,
    *,
    auth_mode: str,
    token: str,
    headers: dict[str, str],
) -> dict:
    async def snapshot():
        return True, dict(DETAIL)

    monkeypatch.setattr(main, "readiness_snapshot", snapshot)
    monkeypatch.setattr(
        main,
        "get_settings",
        lambda: SimpleNamespace(
            workchord_auth_mode=auth_mode, readiness_detail_token=token
        ),
    )
    response = await main.readiness_check(_request(headers))
    assert response.status_code == 200
    return json.loads(response.body)


async def test_managed_readiness_reveals_details_to_the_matching_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = await _readiness(
        monkeypatch,
        auth_mode="managed",
        token="detail-secret",
        headers={"X-Readiness-Detail-Token": "detail-secret"},
    )
    assert payload == DETAIL


@pytest.mark.parametrize(
    ("token", "headers"),
    [
        ("detail-secret", {}),
        ("detail-secret", {"X-Readiness-Detail-Token": "wrong"}),
        ("detail-secret", {"X-Readiness-Detail-Token": ""}),
        ("", {"X-Readiness-Detail-Token": ""}),
        ("", {"X-Readiness-Detail-Token": "anything"}),
    ],
    ids=["absent", "wrong", "empty-header", "unset-empty-header", "unset"],
)
async def test_managed_readiness_stays_status_only_without_a_matching_token(
    monkeypatch: pytest.MonkeyPatch,
    token: str,
    headers: dict[str, str],
) -> None:
    payload = await _readiness(
        monkeypatch, auth_mode="managed", token=token, headers=headers
    )
    assert payload == {"status": "ready"}


async def test_trusted_local_readiness_keeps_its_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = await _readiness(
        monkeypatch, auth_mode="trusted_local", token="", headers={}
    )
    assert payload == DETAIL
