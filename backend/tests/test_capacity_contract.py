"""Executable checks for the approved PostgreSQL capacity contract."""

from __future__ import annotations

import pytest

from app.autonomy.contracts.postgresql import (
    PostgreSQLContractBundle,
    load_postgresql_contract_bundle,
)


CAPACITY_CONTRACT_MEMBER = "postgresql-capacity-contract-v1.json"


@pytest.fixture(scope="module")
def postgresql_contract_bundle() -> PostgreSQLContractBundle:
    return load_postgresql_contract_bundle()


@pytest.fixture(scope="module")
def capacity_contract(
    postgresql_contract_bundle: PostgreSQLContractBundle,
) -> dict:
    contract = postgresql_contract_bundle.member_json(CAPACITY_CONTRACT_MEMBER)
    assert isinstance(contract, dict)
    return contract


@pytest.mark.contract
def test_database_contract_is_frozen(capacity_contract: dict) -> None:
    target = capacity_contract["database"]["target"]
    driver = capacity_contract["database"]["driver"]

    assert capacity_contract["status"] == "approved"
    assert target == {
        "major": 18,
        "reference_minor": "18.4",
        "supported_minor_policy": "current PostgreSQL 18 minor",
        "verified_on": "2026-07-18",
        "revalidate_on_or_before": "2026-08-13",
        "ci_image": "postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296",
        "encoding": "UTF8",
        "locale_provider": "builtin",
        "locale": "PG_UNICODE_FAST",
        "collation_version": "1",
        "collation_deterministic": True,
        "database_timezone": "UTC",
        "role_timezone": "UTC",
        "application_schema": "workchord",
        "search_path": ["workchord", "pg_catalog"],
        "public_schema_in_search_path": False,
    }
    assert driver["family"] == "psycopg"
    assert driver["major"] == 3
    assert driver["sync_sqlalchemy_url"] == driver["async_sqlalchemy_url"]
    assert capacity_contract["database"]["sqlite_policy"] == {
        "allowed_environments": ["development", "test"],
        "production_fallback_allowed": False,
    }


@pytest.mark.contract
def test_connection_budget_preserves_required_reserve(capacity_contract: dict) -> None:
    pooling = capacity_contract["database"]["pooling"]
    allocated = (
        pooling["web"]["maximum_connections"]
        + pooling["delivery_worker"]["maximum_connections"]
        + pooling["migration_operations_and_monitoring_reserve"]
    )

    assert allocated == pooling["application_and_operations_budget"] == 100
    assert allocated + pooling["maintenance_and_failover_reserve"] <= pooling[
        "database_max_connections"
    ]
    assert pooling["maintenance_and_failover_reserve"] / pooling[
        "database_max_connections"
    ] >= 0.30


@pytest.mark.contract
def test_identity_claim_cannot_be_read_as_authenticated_people(
    capacity_contract: dict,
) -> None:
    identity = capacity_contract["identity_claim"]
    assert identity["browser_identities"] == 1250
    assert identity["active_browser_sessions"] == 250
    assert identity["concurrent_agent_clients"] == 200
    assert identity["authenticated_people_claim"] is False
    assert identity["wording"] == (
        "1,250 opaque browser identities, 250 active browser sessions, and "
        "200 concurrent MCP/agent clients"
    )


@pytest.mark.contract
@pytest.mark.parametrize(
    ("profile_id", "read_weight", "write_weight"),
    [
        ("human_peak_v1", 80, 20),
        ("mixed_peak_v1", 59, 41),
    ],
)
def test_operation_manifests_have_exact_weights_and_shapes(
    capacity_contract: dict,
    profile_id: str,
    read_weight: int,
    write_weight: int,
) -> None:
    traffic = capacity_contract["traffic"]
    profile = next(
        profile for profile in traffic["profiles"] if profile["id"] == profile_id
    )
    operations = profile["operations"]

    assert sum(operation["weight_percent"] for operation in operations) == 100
    assert sum(
        operation["weight_percent"]
        for operation in operations
        if operation["classification"] == "read"
    ) == read_weight
    assert sum(
        operation["weight_percent"]
        for operation in operations
        if operation["classification"] == "write"
    ) == write_weight
    assert len({operation["id"] for operation in operations}) == len(operations)
    for operation in operations:
        assert operation["method"]
        assert operation["payload_profile"] in traffic["payload_profiles"]
        assert operation["response_profile"] in traffic["response_profiles"]
        assert operation["expected_statuses"]


@pytest.mark.contract
def test_surge_and_external_wait_are_explicit(capacity_contract: dict) -> None:
    profiles = {
        profile["id"]: profile for profile in capacity_contract["traffic"]["profiles"]
    }
    surge = profiles["connection_surge_v1"]
    llm = profiles["external_llm_wait_v1"]

    assert surge["virtual_users"] == 1000
    assert surge["operation_mix"] == "exactly mixed_peak_v1"
    assert surge["report_separately"] == [
        "active_clients",
        "open_connections",
        "in_flight_requests",
    ]
    assert llm["concurrent_calls"] == 25
    assert sum(item["weight_percent"] for item in llm["operations"]) == 100
    assert "no checked-out database connection" in llm["required_invariant"]


@pytest.mark.contract
def test_every_later_database_task_is_in_the_packaged_trace(
    postgresql_contract_bundle: PostgreSQLContractBundle,
) -> None:
    later_tasks = {
        "DBM-DEP-001",
        "DBM-CFG-001",
        "DBM-MIG-001",
        "DBM-MIG-002",
        "DBM-QA-002",
        "DBM-RUN-001",
        "DBM-RUN-002",
        "DBM-RUN-003",
        "DBM-PERF-001",
        "DBM-PERF-002",
        "DBM-WORK-001",
        "DBM-OBS-001",
        "DBM-MAINT-001",
        "DBM-DATA-001",
        "DBM-DATA-002",
        "DBM-DATA-003",
        "DBM-DEPLOY-001",
        "DBM-DEPLOY-002",
        "DBM-SEC-001",
        "DBM-BACKUP-001",
        "DBM-CUT-001",
        "DBM-QA-003",
        "DBM-SCALE-001",
        "DBM-RES-001",
        "DBM-DOC-001",
        "DBM-QUAL-001",
        "DBM-REHEARSE-001",
        "DBM-CUT-002",
        "DBM-DOC-002",
        "DBM-CLOSE-001",
    }
    assert set(postgresql_contract_bundle.manifest.trace.dbm_tasks) == later_tasks | {
        "DBM-CON-001",
        "DBM-QA-001",
    }
