"""Calibration contracts: submitted, approved and read under deployment-operator authority."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime, timedelta
from typing import Any

import httpx
import pytest
from fastapi import FastAPI
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.main import app as main_app
from app.models.agent import AgentActor, TaskEvent
from app.models.identity import Principal, WorkspaceAuthorityState
from app.models.routing_calibration import RoutingCalibrationContractRevision
from app.models.routing_qualification import RoutingQualificationKey
from app.schemas.routing_calibration import RoutingCalibrationContractSubmit, RoutingCalibrationContractTerms
from app.services.agent_service import hash_api_key

SUBMITTER_KEY = "calibration-submitter-key"
APPROVER_KEY = "calibration-approver-key"
READER_KEY = "calibration-reader-key"
CONTRACTS = "/api/agent/routing-calibration-contracts"


def _terms(**overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "qualification_keys": ["qualified.schema-review", "backend-python"],
        "sample_bounds": {"minimum_samples": 20, "maximum_samples": 500, "maximum_age_days": 180},
        "decay": {"method": "exponential", "days": 60},
        "bias_review": {
            "reviewer": "Routing review board",
            "reviewed_at": "2026-11-20T10:00:00Z",
            "findings": "Samples over-represent short tasks from one team.",
            "mitigations": "Weight each team equally before comparing models.",
        },
        "approver": "Head of delivery",
    }
    values.update(overrides)
    return values


def _headers(api_key: str, command_key: str | None = None, reason: str = "Operator calibration change.") -> dict[str, str]:
    headers = {"X-Agent-API-Key": api_key}
    if command_key is not None:
        headers.update(
            {
                "Idempotency-Key": command_key,
                "X-Agent-Rationale": reason,
                "X-Correlation-ID": f"correlation-{command_key}",
            }
        )
    return headers


async def _client(app: FastAPI, db: AsyncSession) -> httpx.AsyncClient:
    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://workchord.test")


async def _setup(db: AsyncSession) -> None:
    db.add_all(
        [
            AgentActor(
                name="calibration-submitter",
                display_name="Calibration Submitter",
                api_key_hash=hash_api_key(SUBMITTER_KEY),
                scopes='["admin"]',
                enabled=True,
                role="pm",
            ),
            AgentActor(
                name="calibration-approver",
                display_name="Calibration Approver",
                api_key_hash=hash_api_key(APPROVER_KEY),
                scopes='["admin"]',
                enabled=True,
                role="pm",
            ),
            AgentActor(
                name="calibration-reader",
                display_name="Calibration Reader",
                api_key_hash=hash_api_key(READER_KEY),
                scopes='["planning:read"]',
                enabled=True,
                role="pm",
            ),
            RoutingQualificationKey(key="qualified.schema-review", label="Schema review"),
        ]
    )
    await db.commit()


def test_the_schema_refuses_terms_without_sample_bounds_decay_bias_review_or_approver() -> None:
    complete = {"key": "default", **_terms()}
    assert RoutingCalibrationContractSubmit.model_validate(complete).qualification_keys == [
        "backend-python", "qualified.schema-review"
    ]
    for field in ("sample_bounds", "decay", "bias_review", "approver", "qualification_keys"):
        incomplete = deepcopy(complete)
        del incomplete[field]
        with pytest.raises(ValidationError, match=field):
            RoutingCalibrationContractSubmit.model_validate(incomplete)
    for field in ("reviewer", "reviewed_at", "findings"):
        incomplete = deepcopy(complete)
        del incomplete["bias_review"][field]
        with pytest.raises(ValidationError, match=field):
            RoutingCalibrationContractSubmit.model_validate(incomplete)
    invalid = [
        {"approver": "   "},
        {"qualification_keys": []},
        {"qualification_keys": ["backend-python", "Backend-Python"]},
        {"sample_bounds": {"minimum_samples": 50, "maximum_samples": 10, "maximum_age_days": 30}},
        {"sample_bounds": {"minimum_samples": 0, "maximum_samples": 10, "maximum_age_days": 30}},
        {"decay": {"method": "none", "days": 30}},
        {"decay": {"method": "linear", "days": 365}},
        {"bias_review": {**complete["bias_review"], "reviewed_at": "2026-11-20T10:00:00"}},
        {"bias_review": {**complete["bias_review"], "findings": " "}},
        {"bias_review": {**complete["bias_review"], "reviewed_at": 1795000000}},
        {"bias_review": {**complete["bias_review"], "reviewed_at": 1795000000.5}},
        {"unknown_term": True},
    ]
    for overrides in invalid:
        with pytest.raises(ValidationError):
            RoutingCalibrationContractSubmit.model_validate({**complete, **overrides})


def test_the_terms_digest_is_canonical() -> None:
    first = RoutingCalibrationContractTerms.model_validate(_terms())
    # The same instant written with another offset is the same terms.
    offset = RoutingCalibrationContractTerms.model_validate(
        _terms(bias_review={**_terms()["bias_review"], "reviewed_at": "2026-11-20T12:00:00+02:00"})
    )
    assert offset.bias_review.reviewed_at == datetime(2026, 11, 20, 10, tzinfo=UTC)
    assert offset.stored()["bias_review"]["reviewed_at"] == first.stored()["bias_review"]["reviewed_at"]
    assert offset.digest() == first.digest()
    reordered = RoutingCalibrationContractTerms.model_validate(
        _terms(qualification_keys=["backend-python", "qualified.schema-review"])
    )
    assert first.digest() == reordered.digest()
    assert first.digest() != RoutingCalibrationContractTerms.model_validate(
        _terms(decay={"method": "window", "days": 60})
    ).digest()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_a_contract_is_submitted_approved_and_every_revision_is_kept(
    db_session: AsyncSession,
) -> None:
    await _setup(db_session)
    client = await _client(main_app, db_session)
    try:
        empty = await client.get(CONTRACTS, headers=_headers(READER_KEY))
        assert empty.status_code == 200
        assert empty.json() == {
            "schema_version": "routing-calibration-contract-v1",
            "approved_contract_exists": False,
            "performance_history_use": "advisory",
            "contracts": [],
        }

        # Reading needs planning:read; submitting and approving need operator authority.
        denied = await client.post(CONTRACTS, headers=_headers(READER_KEY, "reader-submit"), json={"key": "default", **_terms()})
        assert denied.status_code == 403
        for method, path, body in (
            ("PUT", f"{CONTRACTS}/absent", {"expected_revision": 1, **_terms()}),
            ("POST", f"{CONTRACTS}/absent/approve", {"expected_revision": 1, "expected_terms_digest": "0" * 64, "approved_as": "Head of delivery"}),
        ):
            probe = await client.request(method, path, headers=_headers(READER_KEY, f"probe-{method}"), json=body)
            assert probe.status_code == 403, (method, probe.text)

        # The API refuses incomplete terms and keys outside the vocabulary.
        incomplete = {"key": "default", **_terms()}
        del incomplete["bias_review"]
        refused = await client.post(CONTRACTS, headers=_headers(SUBMITTER_KEY, "incomplete"), json=incomplete)
        assert refused.status_code == 422
        unknown = await client.post(
            CONTRACTS,
            headers=_headers(SUBMITTER_KEY, "unknown-key"),
            json={"key": "default", **_terms(qualification_keys=["qualified.other"])},
        )
        assert unknown.status_code == 422
        assert "Unknown routing skill key: qualified.other" in unknown.text
        future = (datetime.now(UTC) + timedelta(days=2)).isoformat()
        future_review = await client.post(
            CONTRACTS,
            headers=_headers(SUBMITTER_KEY, "future-review"),
            json={"key": "default", **_terms(bias_review={**_terms()["bias_review"], "reviewed_at": future})},
        )
        assert future_review.status_code == 422
        assert "bias_review.reviewed_at must not be in the future" in future_review.text
        # A missing reason is refused before anything is stored.
        no_reason = await client.post(
            CONTRACTS,
            headers={"X-Agent-API-Key": SUBMITTER_KEY, "Idempotency-Key": "no-reason", "X-Correlation-ID": "c"},
            json={"key": "default", **_terms()},
        )
        assert no_reason.status_code in {400, 422}
        assert (await client.get(CONTRACTS, headers=_headers(READER_KEY))).json()["contracts"] == []

        submitted = await client.post(
            CONTRACTS,
            headers=_headers(SUBMITTER_KEY, "submit-default", "Calibrate schema review on recent outcomes."),
            json={"key": "Default", **_terms()},
        )
        assert submitted.status_code == 201, submitted.text
        receipt = submitted.json()
        assert receipt["target_type"] == "routing_calibration_contract"
        assert receipt["authoritative_revision"] == 1
        contract = receipt["result"]
        assert (contract["key"], contract["state"], contract["approved_by"]) == ("default", "submitted", None)
        assert contract["terms"]["qualification_keys"] == ["backend-python", "qualified.schema-review"]
        digest = contract["terms_digest"]
        replay = await client.post(
            CONTRACTS,
            headers=_headers(SUBMITTER_KEY, "submit-default", "Calibrate schema review on recent outcomes."),
            json={"key": "Default", **_terms()},
        )
        assert replay.status_code == 201 and replay.json() == receipt
        exists = await client.post(CONTRACTS, headers=_headers(SUBMITTER_KEY, "submit-again"), json={"key": "default", **_terms()})
        assert exists.status_code == 409
        assert exists.json()["detail"]["code"] == "routing_calibration_contract_exists"
        listed = (await client.get(CONTRACTS, headers=_headers(READER_KEY))).json()
        assert listed["approved_contract_exists"] is False

        def approve_body(revision: int, terms_digest: str = digest, approved_as: str = "Head of delivery") -> dict[str, Any]:
            return {"expected_revision": revision, "expected_terms_digest": terms_digest, "approved_as": approved_as}

        # A reader cannot approve, and an approval names the declared approver.
        missing_approver = await client.post(
            f"{CONTRACTS}/default/approve",
            headers=_headers(APPROVER_KEY, "approve-unnamed"),
            json={"expected_revision": 1, "expected_terms_digest": digest},
        )
        assert missing_approver.status_code == 422
        reader = await client.post(
            f"{CONTRACTS}/default/approve", headers=_headers(READER_KEY, "reader-approve"), json=approve_body(1)
        )
        assert reader.status_code == 403
        for body, code in (
            (approve_body(2), "routing_calibration_contract_revision_conflict"),
            (approve_body(1, "f" * 64), "routing_calibration_contract_terms_mismatch"),
            (approve_body(1, approved_as="Someone else"), "routing_calibration_contract_approver_mismatch"),
        ):
            conflict = await client.post(
                f"{CONTRACTS}/default/approve", headers=_headers(APPROVER_KEY, f"approve-{code}"), json=body
            )
            assert conflict.status_code == 409
            assert conflict.json()["detail"]["code"] == code

        approved = await client.post(
            f"{CONTRACTS}/default/approve",
            headers=_headers(APPROVER_KEY, "approve-default", "Bias review findings are mitigated."),
            json=approve_body(1),
        )
        assert approved.status_code == 200, approved.text
        result = approved.json()["result"]
        assert approved.json()["authoritative_revision"] == 2
        assert result["state"] == "approved"
        assert result["approval_reason"] == "Bias review findings are mitigated."
        # approved_by is the authenticated principal; approved_as is the declared approver.
        assert result["approved_by"]["actor_type"] == "agent"
        assert result["approved_by"] != result["submitted_by"]
        assert result["approved_as"] == "Head of delivery"
        assert result["terms_digest"] == digest
        again = await client.post(
            f"{CONTRACTS}/default/approve", headers=_headers(APPROVER_KEY, "approve-twice"), json=approve_body(2)
        )
        assert again.status_code == 409
        assert again.json()["detail"]["code"] == "routing_calibration_contract_already_approved"
        assert (await client.get(CONTRACTS, headers=_headers(READER_KEY))).json()["approved_contract_exists"] is True

        # New terms are a new revision and the earlier approval lapses until approved again.
        revised = await client.put(
            f"{CONTRACTS}/default",
            headers=_headers(APPROVER_KEY, "revise-default", "Shorter half-life after the review."),
            json={"expected_revision": 2, **_terms(decay={"method": "exponential", "days": 30})},
        )
        assert revised.status_code == 200, revised.text
        assert revised.json()["authoritative_revision"] == 3
        assert revised.json()["result"]["state"] == "submitted"
        assert revised.json()["result"]["approved_at"] is None
        assert revised.json()["result"]["approved_as"] is None
        new_digest = revised.json()["result"]["terms_digest"]
        assert new_digest != digest
        assert (await client.get(CONTRACTS, headers=_headers(READER_KEY))).json()["approved_contract_exists"] is False
        unchanged = await client.put(
            f"{CONTRACTS}/default",
            headers=_headers(APPROVER_KEY, "revise-unchanged"),
            json={"expected_revision": 3, **_terms(decay={"method": "exponential", "days": 30})},
        )
        assert unchanged.status_code == 409
        assert unchanged.json()["detail"]["code"] == "routing_calibration_contract_no_change"
        # The principal that submitted the new terms may approve them; approved_by records it honestly.
        reapproved = await client.post(
            f"{CONTRACTS}/default/approve",
            headers=_headers(APPROVER_KEY, "reapprove-default", "The shorter half-life is reviewed."),
            json=approve_body(3, new_digest),
        )
        assert reapproved.status_code == 200, reapproved.text
        assert reapproved.json()["result"]["approved_by"] == reapproved.json()["result"]["submitted_by"]

        detail = (await client.get(f"{CONTRACTS}/default", headers=_headers(READER_KEY))).json()
        assert [(item["revision"], item["action"], item["state"], item["reason"]) for item in detail["revisions"]] == [
            (1, "submit", "submitted", "Calibrate schema review on recent outcomes."),
            (2, "approve", "approved", "Bias review findings are mitigated."),
            (3, "submit", "submitted", "Shorter half-life after the review."),
            (4, "approve", "approved", "The shorter half-life is reviewed."),
        ]
        assert [item["terms_digest"] for item in detail["revisions"]] == [digest, digest, new_digest, new_digest]
        assert [item["approved_as"] for item in detail["revisions"]] == [
            None, "Head of delivery", None, "Head of delivery"
        ]
        assert detail["revisions"][0]["terms"]["decay"] == {"method": "exponential", "days": 60}
        assert (await client.get(f"{CONTRACTS}/absent", headers=_headers(READER_KEY))).status_code == 404

        events = (await db_session.execute(
            select(TaskEvent)
            .where(TaskEvent.event_type == "agent.routing_calibration_contract_changed")
            .order_by(TaskEvent.id)
        )).scalars().all()
        payloads = [json.loads(event.payload) for event in events]
        assert [(p["action"], p["authoritative_revision"], p["state"]) for p in payloads] == [
            ("submit", 1, "submitted"), ("approve", 2, "approved"), ("submit", 3, "submitted"), ("approve", 4, "approved")
        ]
        assert len((await db_session.execute(select(RoutingCalibrationContractRevision))).scalars().all()) == 4
    finally:
        main_app.dependency_overrides.clear()
        await client.aclose()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_approval_refuses_terms_naming_a_key_retired_since_submission(db_session: AsyncSession) -> None:
    await _setup(db_session)
    client = await _client(main_app, db_session)
    try:
        submitted = await client.post(
            CONTRACTS, headers=_headers(SUBMITTER_KEY, "submit-retiring"), json={"key": "default", **_terms()}
        )
        assert submitted.status_code == 201, submitted.text
        key = (await db_session.execute(select(RoutingQualificationKey))).scalar_one()
        key.state = "retired"
        await db_session.commit()
        approved = await client.post(
            f"{CONTRACTS}/default/approve",
            headers=_headers(APPROVER_KEY, "approve-retired"),
            json={
                "expected_revision": 1,
                "expected_terms_digest": submitted.json()["result"]["terms_digest"],
                "approved_as": "Head of delivery",
            },
        )
        assert approved.status_code == 422
        assert "qualified.schema-review" in approved.text
        assert (await client.get(f"{CONTRACTS}/default", headers=_headers(READER_KEY))).json()["state"] == "submitted"
    finally:
        main_app.dependency_overrides.clear()
        await client.aclose()


async def _operator_state(db: AsyncSession) -> None:
    if await db.get(WorkspaceAuthorityState, 1) is None:
        operator = Principal(kind="system", display_name="Operator API")
        db.add(operator)
        await db.flush()
        db.add(WorkspaceAuthorityState(id=1, operator_principal_id=operator.id))
        await db.commit()


def _command(key: str) -> dict[str, str]:
    return {
        "Idempotency-Key": key,
        "X-Agent-Rationale": "Operator calibration decision.",
        "X-Correlation-ID": key,
    }


@pytest.mark.sqlite
@pytest.mark.asyncio
@pytest.mark.parametrize("auth_mode", ["managed", "trusted_local"])
async def test_the_operator_admin_key_submits_and_approves_and_is_recorded_as_the_operator(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    auth_mode: str,
) -> None:
    await _setup(db_session)
    await _operator_state(db_session)
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "calibration-operator-key")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", auth_mode)
    get_settings.cache_clear()
    client = await _client(main_app, db_session)
    operator_headers = {"X-Admin-API-Key": "calibration-operator-key"}
    try:
        anonymous = await client.post(CONTRACTS, headers=_command("anonymous"), json={"key": "default", **_terms()})
        assert anonymous.status_code == 401
        submitted = await client.post(
            CONTRACTS, headers={**operator_headers, **_command(f"submit-{auth_mode}")}, json={"key": "default", **_terms()}
        )
        assert submitted.status_code == 201, submitted.text
        assert submitted.json()["actor_id"] is None
        assert submitted.json()["result"]["submitted_by"] == {"actor_type": "operator", "actor_id": None}
        approved = await client.post(
            f"{CONTRACTS}/default/approve",
            headers={**operator_headers, **_command(f"approve-{auth_mode}")},
            json={
                "expected_revision": 1,
                "expected_terms_digest": submitted.json()["result"]["terms_digest"],
                "approved_as": "Head of delivery",
            },
        )
        assert approved.status_code == 200, approved.text
        result = approved.json()["result"]
        assert result["approved_by"] == {"actor_type": "operator", "actor_id": None}
        assert result["approved_as"] == "Head of delivery"
        assert (await client.get(CONTRACTS, headers=operator_headers)).json()["approved_contract_exists"] is True
    finally:
        main_app.dependency_overrides.clear()
        get_settings.cache_clear()
        await client.aclose()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_in_managed_mode_only_an_agent_with_an_operator_membership_approves(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from app.models.identity import WorkspaceMembership

    await _setup(db_session)
    member_key = "calibration-member-operator-key"
    member = AgentActor(
        name="calibration-member-operator",
        display_name="Calibration Member Operator",
        api_key_hash=hash_api_key(member_key),
        scopes='["admin"]',
        enabled=True,
        role="pm",
    )
    db_session.add(member)
    await db_session.flush()
    principal = Principal(kind="agent", display_name=member.display_name, agent_actor_id=member.id)
    db_session.add(principal)
    await db_session.flush()
    db_session.add(WorkspaceMembership(principal_id=principal.id, role="operator"))
    await db_session.commit()
    member_id = member.id
    await _operator_state(db_session)
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "calibration-operator-key")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    client = await _client(main_app, db_session)
    try:
        submitted = await client.post(
            CONTRACTS,
            headers={"X-Admin-API-Key": "calibration-operator-key", **_command("managed-submit")},
            json={"key": "default", **_terms()},
        )
        assert submitted.status_code == 201, submitted.text
        body = {
            "expected_revision": 1,
            "expected_terms_digest": submitted.json()["result"]["terms_digest"],
            "approved_as": "Head of delivery",
        }
        # An admin-scoped agent without an operator membership is refused.
        refused = await client.post(
            f"{CONTRACTS}/default/approve", headers=_headers(APPROVER_KEY, "managed-no-membership"), json=body
        )
        assert refused.status_code == 403, refused.text
        approved = await client.post(
            f"{CONTRACTS}/default/approve", headers=_headers(member_key, "managed-member"), json=body
        )
        assert approved.status_code == 200, approved.text
        assert approved.json()["result"]["approved_by"] == {"actor_type": "agent", "actor_id": member_id}
    finally:
        main_app.dependency_overrides.clear()
        get_settings.cache_clear()
        await client.aclose()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_a_key_named_by_a_contract_cannot_be_retired(db_session: AsyncSession) -> None:
    await _setup(db_session)
    client = await _client(main_app, db_session)
    keys = "/api/agent/routing-qualification-keys"
    try:
        submitted = await client.post(
            CONTRACTS, headers=_headers(SUBMITTER_KEY, "submit-named"), json={"key": "default", **_terms()}
        )
        assert submitted.status_code == 201, submitted.text
        detail = (await client.get(f"{keys}/qualified.schema-review", headers=_headers(READER_KEY))).json()
        assert detail["usage"]["calibration_contracts"] == [{"key": "default", "state": "submitted"}]
        refused = await client.post(
            f"{keys}/qualified.schema-review/retire",
            headers=_headers(SUBMITTER_KEY, "retire-named"),
            json={"expected_revision": 1},
        )
        assert refused.status_code == 409
        assert refused.json()["detail"]["code"] == "routing_qualification_key_in_use"
        assert refused.json()["detail"]["calibration_contracts"] == [{"key": "default", "state": "submitted"}]

        # Once the terms no longer name the key, it can be retired.
        revised = await client.put(
            f"{CONTRACTS}/default",
            headers=_headers(SUBMITTER_KEY, "revise-unnamed"),
            json={"expected_revision": 1, **_terms(qualification_keys=["backend-python"])},
        )
        assert revised.status_code == 200, revised.text
        retired = await client.post(
            f"{keys}/qualified.schema-review/retire",
            headers=_headers(SUBMITTER_KEY, "retire-unnamed"),
            json={"expected_revision": 1},
        )
        assert retired.status_code == 200, retired.text
    finally:
        main_app.dependency_overrides.clear()
        await client.aclose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
@pytest.mark.asyncio
async def test_contracts_are_submitted_approved_and_read_on_postgresql(postgres_database, configure_database) -> None:
    from alembic import command as alembic_command
    from sqlalchemy import create_engine
    from sqlalchemy.ext.asyncio import AsyncSession as Session, create_async_engine

    from app.schemas.agent_planning import AgentPlanningCommandContext
    from app.schemas.routing_calibration import RoutingCalibrationContractApprove
    from app.schemas.routing_qualification import RoutingQualificationKeyRetire
    from app.services.agent_model_catalog_service import AgentModelConflictError
    from app.services.routing_calibration_contract_service import (
        RoutingCalibrationContractService,
        approved_calibration_contract_count,
    )
    from app.services.routing_qualification_key_service import RoutingQualificationKeyService
    from app.services.upgrade_service import alembic_config

    configure_database(postgres_database.url)
    sync_engine = create_engine(postgres_database.url)
    with sync_engine.connect() as connection:
        alembic_command.upgrade(alembic_config(connection=connection), "head")
    sync_engine.dispose()
    engine = create_async_engine(postgres_database.url)

    def context(key: str) -> AgentPlanningCommandContext:
        return AgentPlanningCommandContext(idempotency_key=key, rationale="Calibration decision.", correlation_id=key)

    try:
        async with Session(engine, expire_on_commit=False) as db:
            submitter = AgentActor(name="pg-submitter", display_name="Submitter", api_key_hash="pg-s",
                                   scopes='["admin"]', enabled=True, role="pm")
            approver = AgentActor(name="pg-approver", display_name="Approver", api_key_hash="pg-a",
                                  scopes='["admin"]', enabled=True, role="pm")
            db.add_all([submitter, approver, RoutingQualificationKey(key="qualified.schema-review", label="Schema")])
            await db.commit()
            service = RoutingCalibrationContractService(db)
            receipt = await service.submit(
                submitter, RoutingCalibrationContractSubmit.model_validate({"key": "default", **_terms()}),
                command=context("pg-submit"),
            )
            digest = receipt.result["terms_digest"]
            assert await approved_calibration_contract_count(db) == 0
            with pytest.raises(AgentModelConflictError) as wrong:
                await service.approve(
                    "default", approver,
                    RoutingCalibrationContractApprove(
                        expected_revision=1, expected_terms_digest=digest, approved_as="Someone else"
                    ),
                    command=context("pg-wrong"),
                )
            assert wrong.value.code == "routing_calibration_contract_approver_mismatch"
            # The refusal rolled back the session, which expires loaded rows.
            await db.refresh(submitter)
            await db.refresh(approver)
            approved = await service.approve(
                "default", approver,
                RoutingCalibrationContractApprove(
                    expected_revision=1, expected_terms_digest=digest, approved_as="Head of delivery"
                ),
                command=context("pg-approve"),
            )
            assert approved.authoritative_revision == 2
            assert await approved_calibration_contract_count(db) == 1
            detail = await service.get_contract(approver, "default")
            assert [(item.action, item.actor_id, item.approved_as) for item in detail.revisions] == [
                ("submit", submitter.id, None), ("approve", approver.id, "Head of delivery")
            ]
            assert detail.terms.bias_review.reviewed_at == datetime(2026, 11, 20, 10, tzinfo=UTC)

            # An approved contract keeps the key it names from being retired.
            with pytest.raises(AgentModelConflictError) as in_use:
                await RoutingQualificationKeyService(db).retire(
                    "qualified.schema-review", submitter, RoutingQualificationKeyRetire(expected_revision=1),
                    command=context("pg-retire"),
                )
            assert in_use.value.code == "routing_qualification_key_in_use"
            assert in_use.value.context["calibration_contracts"] == [{"key": "default", "state": "approved"}]
    finally:
        await engine.dispose()
