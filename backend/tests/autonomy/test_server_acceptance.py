"""Self-hosted server acceptance contract and adapter tests."""

from __future__ import annotations

import base64
import json
from datetime import UTC, datetime, timedelta
from io import BytesIO

import httpx
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from pydantic import ValidationError

from app.autonomy.canonical import canonical_json_bytes, sha256_hex
from app.autonomy.server_acceptance import (
    ApplicationAcceptance,
    CasAcceptance,
    LockedAcceptanceObject,
    ObjectStoreAcceptance,
    OpenBaoTransitClient,
    S3ObjectLockClient,
    ServerAcceptanceCandidate,
    ServerAcceptanceConfig,
    ServerAcceptanceError,
    ServerAcceptanceReceipt,
    TransitSignerAcceptance,
    ValkeyCasClient,
    _read_resp,
    _signed_report_payload,
    build_blocked_result,
    run_server_acceptance,
    verify_receipt_current_build,
    verify_receipt_trusted_signer,
)
from app.autonomy.status import ResolvedStatusEvidence
from app.build_identity import (
    BackendBuildIdentity,
    load_backend_build_identity,
    package_artifact_digest,
)
from app.cli.server_acceptance import _emit, main as server_acceptance_main


NOW = datetime.now(UTC).replace(microsecond=0)
SOURCE_REVISION = "a" * 40
DIGEST = "b" * 64
PRIVATE_KEY = Ed25519PrivateKey.from_private_bytes(b"\x07" * 32)
PUBLIC_KEY_BYTES = PRIVATE_KEY.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)
PUBLIC_KEY_BASE64 = base64.b64encode(PUBLIC_KEY_BYTES).decode("ascii")


def _build_identity() -> BackendBuildIdentity:
    return BackendBuildIdentity(
        source_revision=SOURCE_REVISION,
        artifact_digest="c" * 64,
        expected_frontend_artifact_digest="d" * 64,
    )


def _signature(payload: bytes, *, version: int = 2) -> str:
    encoded = base64.b64encode(PRIVATE_KEY.sign(payload)).decode("ascii")
    return f"vault:v{version}:{encoded}"


def _candidate() -> ServerAcceptanceCandidate:
    values = {
        "evaluated_at": NOW,
        "source_revision": SOURCE_REVISION,
        "release_fingerprint": sha256_hex(f"git-revision:{SOURCE_REVISION}"),
        "contract_manifest_digest": DIGEST,
        "application": ApplicationAcceptance(
            backend_url="http://backend:8001",
            gateway_url="http://frontend",
            status="ready",
            database_backend="postgresql",
            database_login_role="workchord_runtime",
            database_connected=True,
            schema_current=True,
            migration_gate_clear=True,
            current_revision="20260719_0033",
            expected_revision="20260719_0033",
            backend_source_revision=SOURCE_REVISION,
            gateway_source_revision=SOURCE_REVISION,
            backend_artifact_digest="c" * 64,
            gateway_artifact_digest="d" * 64,
            expected_gateway_artifact_digest="d" * 64,
            backend_contract_manifest_digest=DIGEST,
        ),
        "signer": TransitSignerAcceptance(
            key_ref="transit:workchord-server-acceptance",
            key_type="ed25519",
            key_version=2,
            public_key_base64=PUBLIC_KEY_BASE64,
            public_key_sha256=sha256_hex(PUBLIC_KEY_BYTES),
            exportable=False,
            plaintext_backup_allowed=False,
            round_trip_verified=True,
        ),
        "object_store": ObjectStoreAcceptance(
            endpoint="http://minio:9000",
            bucket="workchord-server-acceptance",
            ready=True,
        ),
        "cas": CasAcceptance(
            endpoint="valkey:6379",
            append_only_enabled=True,
            local_aof_fsync_confirmed=True,
            first_writer_won=True,
            independent_competing_writer=True,
            competing_writer_rejected=True,
            stored_value_verified=True,
        ),
    }
    preliminary = ServerAcceptanceCandidate.model_construct(
        **values,
        report_digest="0" * 64,
    )
    unsigned = preliminary.model_dump(mode="json", exclude={"report_digest"})
    return ServerAcceptanceCandidate(**values, report_digest=sha256_hex(unsigned))


def _receipt() -> ServerAcceptanceReceipt:
    candidate = _candidate()
    candidate_signature = _signature(canonical_json_bytes(candidate))
    stored_payload = _signed_report_payload(candidate, candidate_signature)
    values = {
        "candidate": candidate,
        "valid_until": NOW + timedelta(hours=12),
        "remote_signature": candidate_signature,
        "signature_verified": True,
        "evidence_object": LockedAcceptanceObject(
            bucket="workchord-server-acceptance",
            object_key=(
                f"server-acceptance/{candidate.release_fingerprint}/"
                f"{candidate.report_digest}.signed.json"
            ),
            version_id="version-1",
            object_sha256=sha256_hex(stored_payload),
            lock_mode="COMPLIANCE",
            retain_until=NOW + timedelta(days=1),
            delete_response_status=204,
            exact_bytes_verified=True,
            exact_version_delete_blocked=True,
        ),
        "receipt_signature_verified": True,
    }
    preliminary = ServerAcceptanceReceipt.model_construct(
        **values,
        receipt_signature="vault:v2:cGxhY2Vob2xkZXI=",
        receipt_digest="0" * 64,
    )
    claims = preliminary.model_dump(
        mode="json",
        exclude={"receipt_signature", "receipt_digest"},
    )
    receipt_signature = _signature(canonical_json_bytes(claims))
    signed_values = {**values, "receipt_signature": receipt_signature}
    signed = ServerAcceptanceReceipt.model_construct(
        **signed_values,
        receipt_digest="0" * 64,
    )
    unsigned = signed.model_dump(mode="json", exclude={"receipt_digest"})
    return ServerAcceptanceReceipt(
        **signed_values,
        receipt_digest=sha256_hex(unsigned),
    )


def test_server_receipt_is_nonproduction_and_cannot_enter_status_evidence() -> None:
    receipt = _receipt()

    assert receipt.decision == "SELF-HOSTED-SERVER-ACCEPTED"
    assert receipt.accepted_as_production_evidence is False
    assert receipt.accepted_as_zero_human_evidence is False
    assert receipt.production_autonomy_qualified is False
    assert receipt.production_gates_satisfied is False
    assert receipt.production_program_decision == "NO-SHIP"

    with pytest.raises(ValidationError):
        ResolvedStatusEvidence.model_validate(receipt.model_dump(mode="json"))

    tampered = receipt.model_dump(mode="json")
    tampered["production_gates_satisfied"] = True
    with pytest.raises(ValidationError):
        ServerAcceptanceReceipt.model_validate(tampered)


def test_receipt_round_trips_through_offline_cli_verification(
    tmp_path,
    capsys,
    monkeypatch,
) -> None:
    receipt_path = tmp_path / "receipt.json"
    public_key_path = tmp_path / "trusted-signer-public-key.b64"
    receipt_path.write_text(_receipt().model_dump_json(), encoding="utf-8")
    public_key_path.write_text(PUBLIC_KEY_BASE64 + "\n", encoding="utf-8")
    monkeypatch.setattr(
        "app.cli.server_acceptance.load_backend_build_identity",
        _build_identity,
    )

    assert (
        server_acceptance_main(
            [
                "--verify-receipt",
                str(receipt_path),
                "--trusted-signer-public-key-file",
                str(public_key_path),
            ]
        )
        == 0
    )
    assert "SELF-HOSTED-SERVER-RECEIPT-VERIFIED" in capsys.readouterr().out

    tampered = json.loads(receipt_path.read_text(encoding="utf-8"))
    tampered["evidence_object"]["object_sha256"] = "f" * 64
    receipt_path.write_text(json.dumps(tampered), encoding="utf-8")
    assert (
        server_acceptance_main(
            [
                "--verify-receipt",
                str(receipt_path),
                "--trusted-signer-public-key-file",
                str(public_key_path),
            ]
        )
        == 2
    )


def test_offline_verification_rejects_untrusted_embedded_signer(
    tmp_path,
    capsys,
    monkeypatch,
) -> None:
    receipt_path = tmp_path / "receipt.json"
    public_key_path = tmp_path / "trusted-signer-public-key.b64"
    receipt_path.write_text(_receipt().model_dump_json(), encoding="utf-8")
    other_key = Ed25519PrivateKey.generate().public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    public_key_path.write_text(
        base64.b64encode(other_key).decode("ascii") + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "app.cli.server_acceptance.load_backend_build_identity",
        _build_identity,
    )

    assert (
        server_acceptance_main(
            [
                "--verify-receipt",
                str(receipt_path),
                "--trusted-signer-public-key-file",
                str(public_key_path),
            ]
        )
        == 2
    )
    assert "SELF-HOSTED-SERVER-RECEIPT-INVALID" in capsys.readouterr().out


def test_receipt_output_is_atomically_host_readable(tmp_path, capsys) -> None:
    output = tmp_path / "latest.json"

    _emit('{"decision":"SELF-HOSTED-SERVER-ACCEPTED"}\n', output)

    assert output.read_text(encoding="utf-8").endswith("\n")
    assert output.stat().st_mode & 0o777 == 0o644
    assert not list(tmp_path.glob(".latest.json.*.tmp"))
    assert "SELF-HOSTED-SERVER-ACCEPTED" in capsys.readouterr().out


def test_baked_build_identity_hashes_stable_package_members(tmp_path) -> None:
    package_root = tmp_path / "app"
    package_root.mkdir()
    (package_root / "module.py").write_text("value = 1\n", encoding="utf-8")
    first = package_artifact_digest(package_root)
    cache = package_root / "__pycache__"
    cache.mkdir()
    (cache / "module.pyc").write_bytes(b"ignored")

    assert package_artifact_digest(package_root) == first

    (package_root / "module.py").write_text("value = 2\n", encoding="utf-8")
    assert package_artifact_digest(package_root) != first

    identity_path = tmp_path / "workchord-build.json"
    identity_path.write_text(
        BackendBuildIdentity(
            source_revision=SOURCE_REVISION,
            artifact_digest=first,
            expected_frontend_artifact_digest="d" * 64,
        ).model_dump_json(),
        encoding="utf-8",
    )
    assert load_backend_build_identity(identity_path).artifact_digest == first


def test_receipt_verification_rejects_expiry_and_different_build() -> None:
    receipt = _receipt()

    verify_receipt_trusted_signer(receipt, PUBLIC_KEY_BASE64)
    verify_receipt_current_build(
        receipt,
        _build_identity(),
        verified_at=NOW + timedelta(hours=1),
    )

    with pytest.raises(ValueError, match="expired"):
        verify_receipt_current_build(
            receipt,
            _build_identity(),
            verified_at=receipt.valid_until + timedelta(seconds=1),
        )
    with pytest.raises(ValueError, match="backend artifact differs"):
        verify_receipt_current_build(
            receipt,
            _build_identity().model_copy(
                update={"artifact_digest": "e" * 64}
            ),
            verified_at=NOW + timedelta(hours=1),
        )


def test_receipt_rejects_different_locked_object_location() -> None:
    receipt = _receipt()
    with pytest.raises(ValidationError, match="different bucket"):
        ServerAcceptanceReceipt.model_validate(
            {
                **receipt.model_dump(mode="json"),
                "evidence_object": {
                    **receipt.evidence_object.model_dump(mode="json"),
                    "bucket": "different-bucket",
                },
            }
        )

    with pytest.raises(ValidationError, match="does not bind"):
        ServerAcceptanceReceipt.model_validate(
            {
                **receipt.model_dump(mode="json"),
                "evidence_object": {
                    **receipt.evidence_object.model_dump(mode="json"),
                    "object_key": "unrelated/report.json",
                },
            }
        )


def test_blocked_result_is_digest_bound_and_preserves_boundary() -> None:
    result = build_blocked_result(
        source_revision=SOURCE_REVISION,
        evaluated_at=NOW,
        error=ServerAcceptanceError(
            "object-store-not-ready",
            cause=TimeoutError(),
        ),
    )

    assert result.decision == "SELF-HOSTED-SERVER-BLOCKED"
    assert result.blocker_code == "object-store-not-ready"
    assert result.cause_kind == "TimeoutError"
    assert result.production_program_decision == "NO-SHIP"
    assert result.accepted_as_production_evidence is False


def test_server_acceptance_rejects_production_before_network_access() -> None:
    config = ServerAcceptanceConfig(
        deployment_environment="production",
        backend_url="http://backend:8001",
        gateway_url="http://frontend",
        signer_url="http://openbao:8200",
        signer_token="not-recorded",
        signer_key="workchord-server-acceptance",
        trusted_signer_public_key_base64=PUBLIC_KEY_BASE64,
        object_store_url="http://minio:9000",
        object_store_access_key="not-recorded",
        object_store_secret_key="not-recorded",
        object_store_bucket="workchord-server-acceptance",
        object_store_region="us-east-1",
        valkey_host="valkey",
        valkey_port=6379,
    )

    with pytest.raises(
        ServerAcceptanceError,
        match="self-hosted-profile-requires-development",
    ):
        run_server_acceptance(config, evaluated_at=NOW)


def test_server_acceptance_success_path_seals_final_receipt(
    monkeypatch,
) -> None:
    from app.autonomy.contracts.postgresql import load_postgresql_contract_bundle

    bundle = load_postgresql_contract_bundle()
    application = _candidate().application.model_copy(
        update={"backend_contract_manifest_digest": bundle.manifest_digest}
    )
    signer_fact = _candidate().signer
    object_store_fact = _candidate().object_store
    cas_fact = _candidate().cas

    class ObjectStore:
        def __init__(self, **_kwargs) -> None:
            return None

        def probe_ready(self, _bucket: str) -> ObjectStoreAcceptance:
            return object_store_fact

        def store_locked(
            self,
            *,
            bucket: str,
            object_key: str,
            payload: bytes,
            evaluated_at: datetime,
        ) -> LockedAcceptanceObject:
            return LockedAcceptanceObject(
                bucket=bucket,
                object_key=object_key,
                version_id="version-1",
                object_sha256=sha256_hex(payload),
                lock_mode="COMPLIANCE",
                retain_until=evaluated_at + timedelta(days=1),
                delete_response_status=403,
                exact_bytes_verified=True,
                exact_version_delete_blocked=True,
            )

        def close(self) -> None:
            return None

    class Signer:
        def __init__(self, **_kwargs) -> None:
            return None

        def probe(self) -> TransitSignerAcceptance:
            return signer_fact

        def sign_and_verify(
            self,
            payload: bytes,
            *,
            signer: TransitSignerAcceptance,
        ) -> str:
            assert signer == signer_fact
            return _signature(payload)

        def close(self) -> None:
            return None

    class Cas:
        def __init__(self, **_kwargs) -> None:
            return None

        def probe(self, **_kwargs) -> CasAcceptance:
            return cas_fact

    monkeypatch.setattr(
        "app.autonomy.server_acceptance._probe_application",
        lambda *_args, **_kwargs: application,
    )
    monkeypatch.setattr(
        "app.autonomy.server_acceptance.load_backend_build_identity",
        _build_identity,
    )
    monkeypatch.setattr(
        "app.autonomy.server_acceptance.S3ObjectLockClient",
        ObjectStore,
    )
    monkeypatch.setattr(
        "app.autonomy.server_acceptance.OpenBaoTransitClient",
        Signer,
    )
    monkeypatch.setattr(
        "app.autonomy.server_acceptance.ValkeyCasClient",
        Cas,
    )

    receipt = run_server_acceptance(
        ServerAcceptanceConfig(
            deployment_environment="development",
            backend_url="http://backend:8001",
            gateway_url="http://frontend",
            signer_url="http://openbao:8200",
            signer_token="not-recorded",
            signer_key="workchord-server-acceptance",
            trusted_signer_public_key_base64=PUBLIC_KEY_BASE64,
            object_store_url="http://minio:9000",
            object_store_access_key="not-recorded",
            object_store_secret_key="not-recorded",
            object_store_bucket="workchord-server-acceptance",
            object_store_region="us-east-1",
            valkey_host="valkey",
            valkey_port=6379,
        ),
        evaluated_at=NOW,
    )

    assert receipt.decision == "SELF-HOSTED-SERVER-ACCEPTED"
    assert receipt.candidate.contract_manifest_digest == bundle.manifest_digest
    assert receipt.receipt_signature_verified is True
    assert receipt.evidence_object.object_sha256 == sha256_hex(
        _signed_report_payload(
            receipt.candidate,
            receipt.remote_signature,
        )
    )


def test_openbao_transit_requires_nonexportable_key_and_verifies_signature() -> None:
    seen_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_paths.append(request.url.path)
        if request.url.path == "/v1/sys/health":
            return httpx.Response(
                200,
                json={"initialized": True, "sealed": False},
            )
        if request.url.path == "/v1/transit/keys/workchord-server-acceptance":
            return httpx.Response(
                200,
                json={
                    "data": {
                        "type": "ed25519",
                        "latest_version": 2,
                        "exportable": False,
                        "allow_plaintext_backup": False,
                        "keys": {
                            "2": {
                                "public_key": PUBLIC_KEY_BASE64,
                            }
                        },
                    }
                },
            )
        if request.url.path == "/v1/transit/sign/workchord-server-acceptance":
            request_payload = json.loads(request.content)
            decoded = base64.b64decode(request_payload["input"])
            return httpx.Response(
                200,
                json={"data": {"signature": _signature(decoded)}},
            )
        if request.url.path == "/v1/transit/verify/workchord-server-acceptance":
            return httpx.Response(200, json={"data": {"valid": True}})
        raise AssertionError(request.url)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = OpenBaoTransitClient(
        base_url="http://openbao:8200",
        token="not-recorded",
        key_name="workchord-server-acceptance",
        timeout_seconds=1,
        client=http_client,
    )
    try:
        fact, signature = client.probe_and_sign(b"candidate")
    finally:
        http_client.close()

    assert fact.key_version == 2
    assert fact.exportable is False
    assert fact.plaintext_backup_allowed is False
    assert signature == _signature(b"candidate")
    assert seen_paths[-1] == "/v1/transit/verify/workchord-server-acceptance"


def test_minio_adapter_proves_locked_exact_version_survives_delete() -> None:
    payload = b'{"accepted":true}'
    delete_seen = False

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal delete_seen
        if request.url.path == "/minio/health/ready":
            return httpx.Response(200)
        assert request.headers["authorization"].startswith("AWS4-HMAC-SHA256 ")
        assert request.url.path.endswith("/report.signed.json")
        if request.method == "PUT":
            assert request.content == payload
            return httpx.Response(200, headers={"x-amz-version-id": "version-1"})
        assert request.url.params["versionId"] == "version-1"
        if request.method == "GET":
            return httpx.Response(200, content=payload)
        if request.method == "HEAD":
            return httpx.Response(
                200,
                headers={
                    "x-amz-object-lock-mode": "COMPLIANCE",
                    "x-amz-object-lock-retain-until-date": (
                        NOW + timedelta(days=1)
                    ).isoformat(),
                },
            )
        if request.method == "DELETE":
            delete_seen = True
            return httpx.Response(204)
        raise AssertionError(request.method)

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = S3ObjectLockClient(
        endpoint="http://minio:9000",
        access_key="not-recorded",
        secret_key="not-recorded",
        region="us-east-1",
        timeout_seconds=1,
        client=http_client,
    )
    try:
        ready = client.probe_ready("workchord-server-acceptance")
        stored = client.store_locked(
            bucket="workchord-server-acceptance",
            object_key="server-acceptance/report.signed.json",
            payload=payload,
            evaluated_at=NOW,
        )
    finally:
        http_client.close()

    assert ready.ready is True
    assert stored.object_sha256 == sha256_hex(payload)
    assert stored.exact_version_delete_blocked is True
    assert delete_seen is True


def test_valkey_probe_uses_independent_writer_and_confirms_aof(
    monkeypatch,
) -> None:
    nonce = sha256_hex(f"{DIGEST}:{NOW.isoformat()}")
    winner = f"winner:{nonce}".encode()
    persistence = b"# Persistence\r\naof_enabled:1\r\n"

    def bulk(value: bytes) -> bytes:
        return f"${len(value)}\r\n".encode() + value + b"\r\n"

    first_responses = (
        b"+PONG\r\n"
        + bulk(persistence)
        + b"+OK\r\n"
        + b"*2\r\n:1\r\n:0\r\n"
        + b":1\r\n"
        + b"*2\r\n:1\r\n:0\r\n"
    )
    competing_responses = b"$-1\r\n" + bulk(winner)

    class Duplex:
        def __init__(self, responses: bytes) -> None:
            self.responses = BytesIO(responses)
            self.writes = BytesIO()

        def write(self, value: bytes) -> int:
            return self.writes.write(value)

        def flush(self) -> None:
            return None

        def readline(self) -> bytes:
            return self.responses.readline()

        def read(self, length: int) -> bytes:
            return self.responses.read(length)

    class Connection:
        def __init__(self, responses: bytes) -> None:
            self.stream = Duplex(responses)

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        def settimeout(self, _timeout: float) -> None:
            return None

        def makefile(self, _mode: str):
            return self.stream

    connections = iter(
        (Connection(first_responses), Connection(competing_responses))
    )
    opened = []

    def connect(*_args, **_kwargs):
        connection = next(connections)
        opened.append(connection)
        return connection

    monkeypatch.setattr(
        "app.autonomy.server_acceptance.socket.create_connection",
        connect,
    )

    result = ValkeyCasClient(
        host="valkey",
        port=6379,
        timeout_seconds=1,
    ).probe(release_fingerprint=DIGEST, evaluated_at=NOW)

    assert len(opened) == 2
    assert result.independent_competing_writer is True
    assert result.local_aof_fsync_confirmed is True


@pytest.mark.parametrize(
    ("wire", "expected"),
    [
        (b"+PONG\r\n", "PONG"),
        (b"$5\r\nvalue\r\n", b"value"),
        (b"$-1\r\n", None),
        (b":2\r\n", 2),
    ],
)
def test_resp_parser_handles_acceptance_reply_shapes(
    wire: bytes,
    expected: object,
) -> None:
    assert _read_resp(BytesIO(wire)) == expected
