"""Real-PostgreSQL small seed and resumability qualification."""

from __future__ import annotations

from argparse import Namespace
import os
from pathlib import Path
import socket
import subprocess
import sys
import time

import httpx
import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from app.services.upgrade_service import bootstrap_database_schema
from scripts.load.common import atomic_write_json, read_json_object, utc_now_text
from scripts.load.finalize import finalize_result
from scripts.load.seed import _target_identifier, seed_database


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_small_postgresql_seed_is_exact_and_resumable(
    postgres_database,
    configure_database,
    tmp_path: Path,
) -> None:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    args = Namespace(
        profile="small",
        seed=20260718,
        as_of=utc_now_text(),
        database_url=postgres_database.url,
        authorize_target=_target_identifier(postgres_database.url),
        checkpoint=tmp_path / "checkpoint.json",
        credentials=tmp_path / "credentials.json",
        manifest=tmp_path / "manifest.json",
        chunk_size=1000,
    )
    first = seed_database(args)
    second = seed_database(args)
    assert first["actual_table_rows"] == second["actual_table_rows"]
    assert first["actual_table_rows"]["tasks"] == 500
    assert first["actual_table_rows"]["agent_run_events"] == 4000
    assert first["hot_iteration_tasks"] == 50
    assert first["hot_project_linked_tasks"] >= 100
    assert first["qualification_eligible"] is False
    checkpoint = read_json_object(args.checkpoint, sealed=True)
    credentials = read_json_object(args.credentials, sealed=True)
    assert checkpoint["complete"] is True
    assert len(credentials["browsers"]) == 25
    assert len(credentials["agents"]) == 5

    external_metrics = {
        "pool_checkout_p95_ms": 0,
        "pool_checkout_p99_ms": 0,
        "pool_timeouts": 0,
        "steady_database_connections_percent": 0,
        "database_cpu_steady_percent": 0,
        "database_cpu_burst_percent": 0,
        "ordinary_lock_wait_p99_ms": 0,
        "deadlocks": 0,
        "web_rss_mib_per_replica_maximum": 0,
        "worker_rss_mib_per_replica_maximum": 0,
        "soak_memory_growth_hour_2_to_8_percent": 0,
        "delivery_oldest_ready_steady_seconds": 0,
        "delivery_oldest_ready_burst_seconds": 0,
        "delivery_ready_backlog_maximum": 0,
        "delivery_drain_to_steady_seconds": 0,
        "database_unready_detection_seconds": 0,
        "database_failover_seconds": 0,
        "database_failover_unexpected_attempt_failures_percent": 0,
        "replica_lag_steady_seconds": 0,
        "replica_lag_burst_seconds": 0,
        "wal_archive_rpo_lag_seconds": 0,
        "storage_used_steady_percent": 0,
        "storage_used_burst_percent": 0,
        "storage_latency_steady_p95_ms": 0,
        "storage_latency_burst_p95_ms": 0,
        "capacity_horizon_months": 12,
        "dead_tuple_or_bloat_percent_maximum": 0,
        "statistics_refresh_after_bulk_load_seconds": 0,
        "backup_rpo_seconds": 0,
        "restore_rto_seconds": 0,
        "backend_replica_reroute_seconds": 0,
        "backend_replica_unexpected_attempt_failures_percent": 0,
    }
    external_path = tmp_path / "test-external.json"
    integrity_path = tmp_path / "test-integrity.json"
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = int(listener.getsockname()[1])
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONPATH": str(REPOSITORY_ROOT / "backend"),
            "DATABASE_URL": postgres_database.url,
            "DATABASE_POSTGRESQL_REQUIRED": "true",
            "DATABASE_PROCESS_ROLE": "web",
            "DATABASE_SSL_MODE": "disable",
            "DEPLOYMENT_ENVIRONMENT": "test",
            "SESSION_COOKIE_SECURE": "false",
            "OUTBOUND_DELIVERY_WORKER_ENABLED": "false",
            "MAINTENANCE_MODE": "off",
        }
    )
    server_log_path = tmp_path / "small-load-server.log"
    server_log = server_log_path.open("wb")
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=REPOSITORY_ROOT / "backend",
        env=environment,
        stdout=server_log,
        stderr=subprocess.STDOUT,
    )
    base_url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            if server.poll() is not None:
                pytest.fail(f"Small-load uvicorn exited with {server.returncode}")
            try:
                if httpx.get(f"{base_url}/health/ready", timeout=0.5).status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            time.sleep(0.1)
        else:
            pytest.fail("Small-load uvicorn did not become ready")

        result_path = tmp_path / "small-load-result.json"
        completed = subprocess.run(
            [
                sys.executable,
                str(REPOSITORY_ROOT / "scripts/load/run.py"),
                "--profile",
                "mixed_peak_v1",
                "--phase",
                "small",
                "--duration-seconds",
                "30",
                "--rps",
                "2",
                "--virtual-users",
                "10",
                "--base-url",
                base_url,
                "--authorize-host",
                f"127.0.0.1:{port}",
                "--environment",
                "test",
                "--credentials",
                str(args.credentials),
                "--seed-manifest",
                str(args.manifest),
                "--defer-external-evidence",
                "--output",
                str(result_path),
            ],
            cwd=REPOSITORY_ROOT,
            env=environment,
            text=True,
            capture_output=True,
            timeout=60,
        )
        server_log.flush()
        assert completed.returncode == 0, (
            completed.stdout
            + completed.stderr
            + server_log_path.read_text(encoding="utf-8", errors="replace")
        )
        client_result = read_json_object(result_path, sealed=True)
        assert client_result["status"] == "incomplete"
        load_reference = {
            "run_id": client_result["run_id"],
            "sha256": client_result["document_sha256"],
            "created_at": client_result["created_at"],
        }
        atomic_write_json(
            external_path,
            {
                "kind": "workchord-external-qualification-metrics",
                "schema_version": 1,
                "phase": "small",
                "load_result": load_reference,
                "metrics": external_metrics,
            },
        )
        atomic_write_json(
            integrity_path,
            {
                "kind": "workchord-domain-integrity-evidence",
                "schema_version": 1,
                "load_result": load_reference,
                "failures": 0,
            },
        )
        finalized_path = tmp_path / "small-load-finalized.json"
        load_result = finalize_result(
            result_path,
            external_path,
            integrity_path,
            finalized_path,
        )
        assert load_result["status"] == "passed"
        assert load_result["traffic"]["completed_attempts"] == 60
        assert load_result["traffic"]["eligible_attempts"] == 60
        assert load_result["traffic"]["active_clients_peak"] == 10
        assert load_result["workload_evidence"]["client_mechanics"][
            "poll_guidance_parsed"
        ] > 0
        mechanics = load_result["workload_evidence"]["client_mechanics"]
        assert mechanics["poll_guidance_parsed"] == (
            mechanics["poll_guidance_respected"]
            + mechanics["poll_guidance_outstanding"]
        )
        assert mechanics["retry_attempts"] == 0
        assert load_result["gates"]["bounded_retry_contracts"]["status"] == (
            "passed"
        )
        assert load_result["gates"]["response_cardinality_conformance"][
            "status"
        ] == "passed"
    finally:
        server.terminate()
        try:
            server.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)
        server_log.close()
