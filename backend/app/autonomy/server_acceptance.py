"""Container-backed acceptance for a self-hosted WorkChord server.

This module is intentionally separate from ``AutonomousEvidence`` and the
PostgreSQL G1-G15 status evaluator.  A receipt proves only that one exact
checkout ran with the bundled non-production service analogues.
"""

from __future__ import annotations

import base64
import hmac
import socket
from binascii import Error as Base64Error
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import BinaryIO, Literal
from urllib.parse import quote, urlsplit

import httpx
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from pydantic import Field, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)
from app.build_identity import (
    BackendBuildIdentity,
    BuildIdentity,
    load_backend_build_identity,
)


SHA256_PATTERN = r"^[0-9a-f]{64}$"
REVISION_PATTERN = r"^[0-9a-f]{40,64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"


class ServerAcceptanceError(RuntimeError):
    """A sanitized, stable failure from one server-acceptance predicate."""

    def __init__(self, code: str, *, cause: BaseException | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.cause_kind = type(cause).__name__ if cause is not None else None


class ApplicationAcceptance(StrictContractModel):
    backend_url: str = Field(pattern=r"^https?://[^@\s]+$")
    gateway_url: str = Field(pattern=r"^https?://[^@\s]+$")
    status: Literal["ready"]
    database_backend: Literal["postgresql"]
    database_login_role: Literal["workchord_runtime"]
    database_connected: Literal[True] = True
    schema_current: Literal[True] = True
    migration_gate_clear: Literal[True] = True
    current_revision: str = Field(pattern=IDENTIFIER_PATTERN)
    expected_revision: str = Field(pattern=IDENTIFIER_PATTERN)
    backend_source_revision: str = Field(pattern=REVISION_PATTERN)
    gateway_source_revision: str = Field(pattern=REVISION_PATTERN)
    backend_artifact_digest: str = Field(pattern=SHA256_PATTERN)
    gateway_artifact_digest: str = Field(pattern=SHA256_PATTERN)
    expected_gateway_artifact_digest: str = Field(pattern=SHA256_PATTERN)
    backend_contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def exact_revision(self) -> "ApplicationAcceptance":
        if self.current_revision != self.expected_revision:
            raise ValueError("Application schema is not at the packaged revision")
        if self.backend_source_revision != self.gateway_source_revision:
            raise ValueError("Backend and gateway source revisions differ")
        if self.gateway_artifact_digest != self.expected_gateway_artifact_digest:
            raise ValueError("Gateway artifact differs from the backend build")
        return self


class TransitSignerAcceptance(StrictContractModel):
    implementation: Literal["openbao-transit"] = "openbao-transit"
    key_ref: str = Field(pattern=IDENTIFIER_PATTERN)
    key_type: Literal["ed25519"]
    key_version: int = Field(ge=1)
    public_key_base64: str = Field(pattern=r"^[A-Za-z0-9+/]+={0,2}$")
    public_key_sha256: str = Field(pattern=SHA256_PATTERN)
    exportable: Literal[False] = False
    plaintext_backup_allowed: Literal[False] = False
    round_trip_verified: Literal[True] = True

    @model_validator(mode="after")
    def public_key_bound(self) -> "TransitSignerAcceptance":
        try:
            public_key = base64.b64decode(
                self.public_key_base64,
                validate=True,
            )
        except (Base64Error, ValueError) as exc:
            raise ValueError("Transit public key is not canonical base64") from exc
        if len(public_key) != 32:
            raise ValueError("Transit Ed25519 public key must be 32 bytes")
        if sha256_hex(public_key) != self.public_key_sha256:
            raise ValueError("Transit public-key fingerprint mismatch")
        return self


class ObjectStoreAcceptance(StrictContractModel):
    implementation: Literal["minio-s3-object-lock"] = "minio-s3-object-lock"
    endpoint: str = Field(pattern=r"^https?://[^@\s]+$")
    bucket: str = Field(pattern=r"^[a-z0-9][a-z0-9.-]{1,62}$")
    ready: Literal[True] = True


class CasAcceptance(StrictContractModel):
    implementation: Literal["valkey-aof-cas"] = "valkey-aof-cas"
    endpoint: str = Field(pattern=r"^[a-zA-Z0-9.-]+:[0-9]{1,5}$")
    append_only_enabled: Literal[True] = True
    local_aof_fsync_confirmed: Literal[True] = True
    first_writer_won: Literal[True] = True
    independent_competing_writer: Literal[True] = True
    competing_writer_rejected: Literal[True] = True
    stored_value_verified: Literal[True] = True


class ServerAcceptanceCandidate(StrictContractModel):
    schema_version: Literal["workchord-self-hosted-server-candidate-v1"] = (
        "workchord-self-hosted-server-candidate-v1"
    )
    profile: Literal["self-hosted-server-v1"] = "self-hosted-server-v1"
    evidence_scope: Literal["self-hosted-server-only"] = "self-hosted-server-only"
    evaluated_at: datetime
    source_revision: str = Field(pattern=REVISION_PATTERN)
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    application: ApplicationAcceptance
    signer: TransitSignerAcceptance
    object_store: ObjectStoreAcceptance
    cas: CasAcceptance
    production_mutation_allowed: Literal[False] = False
    accepted_as_production_evidence: Literal[False] = False
    accepted_as_zero_human_evidence: Literal[False] = False
    production_autonomy_qualified: Literal[False] = False
    production_gates_satisfied: Literal[False] = False
    production_program_decision: Literal["NO-SHIP"] = "NO-SHIP"
    report_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def canonical_candidate(self) -> "ServerAcceptanceCandidate":
        if self.evaluated_at.tzinfo is None or self.evaluated_at.utcoffset() is None:
            raise ValueError("Acceptance clock must be timezone-aware")
        expected_fingerprint = sha256_hex(f"git-revision:{self.source_revision}")
        if self.release_fingerprint != expected_fingerprint:
            raise ValueError("Release fingerprint does not bind the source revision")
        if (
            self.application.backend_source_revision != self.source_revision
            or self.application.gateway_source_revision != self.source_revision
        ):
            raise ValueError("Application images do not bind the source revision")
        if (
            self.application.backend_contract_manifest_digest
            != self.contract_manifest_digest
        ):
            raise ValueError("Backend contract bundle differs from the candidate")
        unsigned = self.model_dump(mode="json", exclude={"report_digest"})
        if self.report_digest != sha256_hex(unsigned):
            raise ValueError("Server acceptance candidate digest mismatch")
        ensure_secret_free(self)
        return self


class LockedAcceptanceObject(StrictContractModel):
    implementation: Literal["minio-s3-object-lock"] = "minio-s3-object-lock"
    bucket: str = Field(pattern=r"^[a-z0-9][a-z0-9.-]{1,62}$")
    object_key: str = Field(min_length=1, max_length=1024)
    version_id: str = Field(min_length=1, max_length=1024)
    object_sha256: str = Field(pattern=SHA256_PATTERN)
    lock_mode: Literal["COMPLIANCE"]
    retain_until: datetime
    delete_response_status: int = Field(ge=200, le=499)
    exact_bytes_verified: Literal[True] = True
    exact_version_delete_blocked: Literal[True] = True

    @model_validator(mode="after")
    def aware_retention(self) -> "LockedAcceptanceObject":
        if self.retain_until.tzinfo is None or self.retain_until.utcoffset() is None:
            raise ValueError("Object retention clock must be timezone-aware")
        return self


class ServerAcceptanceReceipt(StrictContractModel):
    schema_version: Literal["workchord-self-hosted-server-acceptance-v1"] = (
        "workchord-self-hosted-server-acceptance-v1"
    )
    decision: Literal["SELF-HOSTED-SERVER-ACCEPTED"] = (
        "SELF-HOSTED-SERVER-ACCEPTED"
    )
    candidate: ServerAcceptanceCandidate
    valid_until: datetime
    remote_signature: str = Field(pattern=r"^vault:v[1-9][0-9]*:[A-Za-z0-9+/=]+$")
    signature_verified: Literal[True] = True
    evidence_object: LockedAcceptanceObject
    receipt_signature: str = Field(
        pattern=r"^vault:v[1-9][0-9]*:[A-Za-z0-9+/=]+$"
    )
    receipt_signature_verified: Literal[True] = True
    accepted_as_production_evidence: Literal[False] = False
    accepted_as_zero_human_evidence: Literal[False] = False
    production_autonomy_qualified: Literal[False] = False
    production_gates_satisfied: Literal[False] = False
    production_program_decision: Literal["NO-SHIP"] = "NO-SHIP"
    receipt_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def canonical_receipt(self) -> "ServerAcceptanceReceipt":
        if self.valid_until.tzinfo is None or self.valid_until.utcoffset() is None:
            raise ValueError("Receipt validity clock must be timezone-aware")
        if self.valid_until <= self.candidate.evaluated_at:
            raise ValueError("Receipt validity horizon is not in the future")
        if self.evidence_object.retain_until <= self.candidate.evaluated_at:
            raise ValueError("Acceptance object retention is already expired")
        if self.valid_until > self.evidence_object.retain_until:
            raise ValueError("Receipt outlives its locked evidence")
        expected_object_key = (
            f"server-acceptance/{self.candidate.release_fingerprint}/"
            f"{self.candidate.report_digest}.signed.json"
        )
        if self.evidence_object.bucket != self.candidate.object_store.bucket:
            raise ValueError("Evidence object is stored in a different bucket")
        if self.evidence_object.object_key != expected_object_key:
            raise ValueError("Evidence object key does not bind the candidate")
        candidate_payload = canonical_json_bytes(self.candidate)
        _verify_transit_signature(
            self.candidate.signer,
            candidate_payload,
            self.remote_signature,
        )
        stored_payload = _signed_report_payload(
            self.candidate,
            self.remote_signature,
        )
        if self.evidence_object.object_sha256 != sha256_hex(stored_payload):
            raise ValueError("Evidence-object digest does not bind the signed report")
        receipt_claims = self.model_dump(
            mode="json",
            exclude={"receipt_signature", "receipt_digest"},
        )
        _verify_transit_signature(
            self.candidate.signer,
            canonical_json_bytes(receipt_claims),
            self.receipt_signature,
        )
        unsigned = self.model_dump(mode="json", exclude={"receipt_digest"})
        if self.receipt_digest != sha256_hex(unsigned):
            raise ValueError("Server acceptance receipt digest mismatch")
        ensure_secret_free(self)
        return self


class BlockedServerAcceptance(StrictContractModel):
    schema_version: Literal["workchord-self-hosted-server-acceptance-v1"] = (
        "workchord-self-hosted-server-acceptance-v1"
    )
    decision: Literal["SELF-HOSTED-SERVER-BLOCKED"] = "SELF-HOSTED-SERVER-BLOCKED"
    evaluated_at: datetime
    source_revision: str
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    blocker_code: str = Field(pattern=IDENTIFIER_PATTERN)
    cause_kind: str | None = Field(default=None, pattern=IDENTIFIER_PATTERN)
    accepted_as_production_evidence: Literal[False] = False
    accepted_as_zero_human_evidence: Literal[False] = False
    production_autonomy_qualified: Literal[False] = False
    production_gates_satisfied: Literal[False] = False
    production_program_decision: Literal["NO-SHIP"] = "NO-SHIP"
    receipt_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def canonical_blocked_result(self) -> "BlockedServerAcceptance":
        if self.evaluated_at.tzinfo is None or self.evaluated_at.utcoffset() is None:
            raise ValueError("Acceptance clock must be timezone-aware")
        unsigned = self.model_dump(mode="json", exclude={"receipt_digest"})
        if self.receipt_digest != sha256_hex(unsigned):
            raise ValueError("Blocked acceptance digest mismatch")
        ensure_secret_free(self)
        return self


@dataclass(frozen=True)
class ServerAcceptanceConfig:
    """Runtime inputs, including credentials that never enter a receipt."""

    deployment_environment: str
    backend_url: str
    gateway_url: str
    signer_url: str
    signer_token: str
    signer_key: str
    trusted_signer_public_key_base64: str
    object_store_url: str
    object_store_access_key: str
    object_store_secret_key: str
    object_store_bucket: str
    object_store_region: str
    valkey_host: str
    valkey_port: int
    timeout_seconds: float = 10.0


class OpenBaoTransitClient:
    """Small HTTP adapter for the OpenBao/Vault-compatible Transit API."""

    def __init__(
        self,
        *,
        base_url: str,
        token: str,
        key_name: str,
        timeout_seconds: float,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.key_name = key_name
        self._client = client or httpx.Client(
            timeout=timeout_seconds,
            trust_env=False,
        )
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        try:
            response = self._client.request(
                method,
                f"{self.base_url}{path}",
                headers={
                    "X-Vault-Request": "true",
                    "X-Vault-Token": self.token,
                },
                json=payload,
            )
            response.raise_for_status()
            value = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ServerAcceptanceError("remote-signer-unavailable", cause=exc) from exc
        if not isinstance(value, dict):
            raise ServerAcceptanceError("remote-signer-response-invalid")
        return value

    def probe(self) -> TransitSignerAcceptance:
        health = self._request("GET", "/v1/sys/health")
        if health.get("initialized") is not True or health.get("sealed") is not False:
            raise ServerAcceptanceError("remote-signer-not-ready")

        key_response = self._request(
            "GET",
            f"/v1/transit/keys/{quote(self.key_name, safe='')}",
        )
        key_data = key_response.get("data")
        if not isinstance(key_data, dict):
            raise ServerAcceptanceError("remote-signer-key-response-invalid")
        if (
            key_data.get("type") != "ed25519"
            or key_data.get("exportable") is not False
            or key_data.get("allow_plaintext_backup") is not False
        ):
            raise ServerAcceptanceError("remote-signer-key-policy-invalid")
        latest_version = key_data.get("latest_version")
        if not isinstance(latest_version, int) or latest_version < 1:
            raise ServerAcceptanceError("remote-signer-key-version-invalid")
        versions = key_data.get("keys")
        version = (
            versions.get(str(latest_version))
            if isinstance(versions, dict)
            else None
        )
        public_key_base64 = (
            version.get("public_key")
            if isinstance(version, dict)
            else None
        )
        if not isinstance(public_key_base64, str):
            raise ServerAcceptanceError("remote-signer-public-key-missing")
        try:
            public_key = base64.b64decode(public_key_base64, validate=True)
            fact = TransitSignerAcceptance(
                key_ref=f"transit:{self.key_name}",
                key_type="ed25519",
                key_version=latest_version,
                public_key_base64=public_key_base64,
                public_key_sha256=sha256_hex(public_key),
                exportable=False,
                plaintext_backup_allowed=False,
                round_trip_verified=True,
            )
        except (Base64Error, ValueError) as exc:
            raise ServerAcceptanceError(
                "remote-signer-public-key-invalid",
                cause=exc,
            ) from exc
        return fact

    def sign_and_verify(
        self,
        payload: bytes,
        *,
        signer: TransitSignerAcceptance,
    ) -> str:
        encoded = base64.b64encode(payload).decode("ascii")
        signature_response = self._request(
            "POST",
            f"/v1/transit/sign/{quote(self.key_name, safe='')}",
            payload={"input": encoded},
        )
        signature_data = signature_response.get("data")
        signature = (
            signature_data.get("signature")
            if isinstance(signature_data, dict)
            else None
        )
        if not isinstance(signature, str):
            raise ServerAcceptanceError("remote-signature-missing")
        verify_response = self._request(
            "POST",
            f"/v1/transit/verify/{quote(self.key_name, safe='')}",
            payload={"input": encoded, "signature": signature},
        )
        verify_data = verify_response.get("data")
        if not isinstance(verify_data, dict) or verify_data.get("valid") is not True:
            raise ServerAcceptanceError("remote-signature-round-trip-failed")
        try:
            _verify_transit_signature(signer, payload, signature)
        except ValueError as exc:
            raise ServerAcceptanceError(
                "remote-signature-offline-verification-failed",
                cause=exc,
            ) from exc
        return signature

    def probe_and_sign(
        self,
        payload: bytes,
    ) -> tuple[TransitSignerAcceptance, str]:
        """Compatibility helper for callers that need one probe/sign operation."""

        signer = self.probe()
        return signer, self.sign_and_verify(payload, signer=signer)


class S3ObjectLockClient:
    """Path-style S3 client with only the operations required by acceptance."""

    def __init__(
        self,
        *,
        endpoint: str,
        access_key: str,
        secret_key: str,
        region: str,
        timeout_seconds: float,
        client: httpx.Client | None = None,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self._client = client or httpx.Client(
            timeout=timeout_seconds,
            trust_env=False,
        )
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def probe_ready(self, bucket: str) -> ObjectStoreAcceptance:
        try:
            response = self._client.get(f"{self.endpoint}/minio/health/ready")
        except httpx.HTTPError as exc:
            raise ServerAcceptanceError("object-store-unavailable", cause=exc) from exc
        if response.status_code != 200:
            raise ServerAcceptanceError("object-store-not-ready")
        return ObjectStoreAcceptance(
            endpoint=self.endpoint,
            bucket=bucket,
            ready=True,
        )

    def store_locked(
        self,
        *,
        bucket: str,
        object_key: str,
        payload: bytes,
        evaluated_at: datetime,
    ) -> LockedAcceptanceObject:
        put = self._request(
            "PUT",
            bucket=bucket,
            object_key=object_key,
            body=payload,
            headers={"content-type": "application/json"},
        )
        if put.status_code not in {200, 201}:
            raise ServerAcceptanceError("locked-object-write-failed")
        version_id = put.headers.get("x-amz-version-id")
        if not version_id:
            raise ServerAcceptanceError("locked-object-version-missing")

        params = (("versionId", version_id),)
        fetched = self._request(
            "GET",
            bucket=bucket,
            object_key=object_key,
            params=params,
        )
        if fetched.status_code != 200 or fetched.content != payload:
            raise ServerAcceptanceError("locked-object-readback-mismatch")
        head = self._request(
            "HEAD",
            bucket=bucket,
            object_key=object_key,
            params=params,
        )
        if head.status_code != 200:
            raise ServerAcceptanceError("locked-object-head-failed")
        lock_mode = head.headers.get("x-amz-object-lock-mode")
        raw_retain_until = head.headers.get("x-amz-object-lock-retain-until-date")
        if lock_mode != "COMPLIANCE" or raw_retain_until is None:
            raise ServerAcceptanceError("locked-object-retention-missing")
        try:
            retain_until = datetime.fromisoformat(
                raw_retain_until.replace("Z", "+00:00")
            )
        except ValueError as exc:
            raise ServerAcceptanceError(
                "locked-object-retention-invalid",
                cause=exc,
            ) from exc
        if retain_until <= evaluated_at:
            raise ServerAcceptanceError("locked-object-retention-expired")

        deletion = self._request(
            "DELETE",
            bucket=bucket,
            object_key=object_key,
            params=params,
        )
        if deletion.status_code not in {200, 202, 204, 403, 409}:
            raise ServerAcceptanceError("locked-object-delete-not-fenced")
        final_read = self._request(
            "GET",
            bucket=bucket,
            object_key=object_key,
            params=params,
        )
        if final_read.status_code != 200 or final_read.content != payload:
            raise ServerAcceptanceError("locked-object-not-durable-after-delete")
        return LockedAcceptanceObject(
            bucket=bucket,
            object_key=object_key,
            version_id=version_id,
            object_sha256=sha256_hex(payload),
            lock_mode="COMPLIANCE",
            retain_until=retain_until,
            delete_response_status=deletion.status_code,
            exact_bytes_verified=True,
            exact_version_delete_blocked=True,
        )

    def _request(
        self,
        method: str,
        *,
        bucket: str,
        object_key: str,
        body: bytes = b"",
        params: tuple[tuple[str, str], ...] = (),
        headers: dict[str, str] | None = None,
        now: datetime | None = None,
    ) -> httpx.Response:
        timestamp = now or datetime.now(UTC)
        date_stamp = timestamp.strftime("%Y%m%d")
        amz_date = timestamp.strftime("%Y%m%dT%H%M%SZ")
        payload_digest = sha256(body).hexdigest()
        canonical_uri = (
            f"/{quote(bucket, safe='-_.~')}/"
            f"{quote(object_key, safe='/-_.~')}"
        )
        canonical_query = "&".join(
            f"{quote(key, safe='-_.~')}={quote(value, safe='-_.~')}"
            for key, value in sorted(params)
        )
        endpoint = urlsplit(self.endpoint)
        request_headers = {
            "host": endpoint.netloc,
            "x-amz-content-sha256": payload_digest,
            "x-amz-date": amz_date,
        }
        if headers:
            request_headers.update(
                {key.lower(): " ".join(value.split()) for key, value in headers.items()}
            )
        signed_header_names = sorted(request_headers)
        canonical_headers = "".join(
            f"{key}:{request_headers[key]}\n" for key in signed_header_names
        )
        signed_headers = ";".join(signed_header_names)
        canonical_request = "\n".join(
            (
                method,
                canonical_uri,
                canonical_query,
                canonical_headers,
                signed_headers,
                payload_digest,
            )
        )
        credential_scope = f"{date_stamp}/{self.region}/s3/aws4_request"
        string_to_sign = "\n".join(
            (
                "AWS4-HMAC-SHA256",
                amz_date,
                credential_scope,
                sha256(canonical_request.encode("utf-8")).hexdigest(),
            )
        )
        signing_key = _aws_signing_key(
            self.secret_key,
            date_stamp=date_stamp,
            region=self.region,
            service="s3",
        )
        signature = hmac.new(
            signing_key,
            string_to_sign.encode("utf-8"),
            sha256,
        ).hexdigest()
        request_headers["authorization"] = (
            "AWS4-HMAC-SHA256 "
            f"Credential={self.access_key}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}"
        )
        query_suffix = f"?{canonical_query}" if canonical_query else ""
        try:
            return self._client.request(
                method,
                f"{self.endpoint}{canonical_uri}{query_suffix}",
                headers=request_headers,
                content=body,
            )
        except httpx.HTTPError as exc:
            raise ServerAcceptanceError("object-store-request-failed", cause=exc) from exc


class ValkeyCasClient:
    """Minimal RESP2 client for the bounded persistent CAS acceptance check."""

    def __init__(self, *, host: str, port: int, timeout_seconds: float) -> None:
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_seconds

    def probe(self, *, release_fingerprint: str, evaluated_at: datetime) -> CasAcceptance:
        nonce = sha256_hex(
            f"{release_fingerprint}:{evaluated_at.isoformat()}"
        )
        key = f"workchord:server-acceptance:{nonce}"
        first_value = f"winner:{nonce}"
        try:
            with socket.create_connection(
                (self.host, self.port),
                timeout=self.timeout_seconds,
            ) as first_connection:
                first_connection.settimeout(self.timeout_seconds)
                first_stream = first_connection.makefile("rwb")
                if _valkey_command(first_stream, "PING") != "PONG":
                    raise ServerAcceptanceError("cas-store-not-ready")
                info = _valkey_command(first_stream, "INFO", "persistence")
                if not isinstance(info, bytes) or b"aof_enabled:1" not in info:
                    raise ServerAcceptanceError("cas-store-aof-disabled")
                first = _valkey_command(
                    first_stream,
                    "SET",
                    key,
                    first_value,
                    "NX",
                    "PX",
                    "60000",
                )
                if first != "OK":
                    raise ServerAcceptanceError("cas-first-write-failed")
                try:
                    fsync = _valkey_command(
                        first_stream,
                        "WAITAOF",
                        "1",
                        "0",
                        str(max(1, int(self.timeout_seconds * 1000))),
                    )
                    if (
                        not isinstance(fsync, list)
                        or len(fsync) != 2
                        or fsync[0] != 1
                    ):
                        raise ServerAcceptanceError("cas-aof-fsync-not-confirmed")
                    with socket.create_connection(
                        (self.host, self.port),
                        timeout=self.timeout_seconds,
                    ) as competing_connection:
                        competing_connection.settimeout(self.timeout_seconds)
                        competing_stream = competing_connection.makefile("rwb")
                        second = _valkey_command(
                            competing_stream,
                            "SET",
                            key,
                            f"loser:{nonce}",
                            "NX",
                            "PX",
                            "60000",
                        )
                        stored = _valkey_command(competing_stream, "GET", key)
                    if second is not None:
                        raise ServerAcceptanceError("cas-conflict-not-rejected")
                    if stored != first_value.encode("utf-8"):
                        raise ServerAcceptanceError("cas-stored-value-mismatch")
                finally:
                    _valkey_command(first_stream, "DEL", key)
                    _valkey_command(
                        first_stream,
                        "WAITAOF",
                        "1",
                        "0",
                        str(max(1, int(self.timeout_seconds * 1000))),
                    )
        except ServerAcceptanceError:
            raise
        except (OSError, ValueError) as exc:
            raise ServerAcceptanceError("cas-store-unavailable", cause=exc) from exc
        return CasAcceptance(
            endpoint=f"{self.host}:{self.port}",
            append_only_enabled=True,
            local_aof_fsync_confirmed=True,
            first_writer_won=True,
            independent_competing_writer=True,
            competing_writer_rejected=True,
            stored_value_verified=True,
        )


def run_server_acceptance(
    config: ServerAcceptanceConfig,
    *,
    evaluated_at: datetime | None = None,
) -> ServerAcceptanceReceipt:
    """Run the bounded self-hosted acceptance predicates and seal the report."""

    now = evaluated_at or datetime.now(UTC)
    if config.deployment_environment != "development":
        raise ServerAcceptanceError("self-hosted-profile-requires-development")
    try:
        build_identity = load_backend_build_identity()
    except (OSError, ValueError) as exc:
        raise ServerAcceptanceError(
            "acceptance-build-identity-invalid",
            cause=exc,
        ) from exc
    source_revision = build_identity.source_revision
    if not _is_hex_revision(source_revision):
        raise ServerAcceptanceError("source-revision-invalid")
    try:
        trusted_signer_public_key = _decode_ed25519_public_key(
            config.trusted_signer_public_key_base64,
            error_message="Trusted signer public key is invalid",
        )
    except ValueError as exc:
        raise ServerAcceptanceError(
            "trusted-signer-public-key-invalid",
            cause=exc,
        ) from exc
    release_fingerprint = sha256_hex(f"git-revision:{source_revision}")

    application = _probe_application(
        config.backend_url,
        gateway_url=config.gateway_url,
        expected_source_revision=source_revision,
        timeout_seconds=config.timeout_seconds,
    )
    if application.backend_artifact_digest != build_identity.artifact_digest:
        raise ServerAcceptanceError("acceptance-backend-artifact-mismatch")
    if (
        application.gateway_artifact_digest
        != build_identity.expected_frontend_artifact_digest
    ):
        raise ServerAcceptanceError("acceptance-frontend-artifact-mismatch")
    from app.autonomy.contracts.postgresql import load_postgresql_contract_bundle

    bundle = load_postgresql_contract_bundle()
    object_store = S3ObjectLockClient(
        endpoint=config.object_store_url,
        access_key=config.object_store_access_key,
        secret_key=config.object_store_secret_key,
        region=config.object_store_region,
        timeout_seconds=config.timeout_seconds,
    )
    signer = OpenBaoTransitClient(
        base_url=config.signer_url,
        token=config.signer_token,
        key_name=config.signer_key,
        timeout_seconds=config.timeout_seconds,
    )
    try:
        object_store_fact = object_store.probe_ready(config.object_store_bucket)
        cas = ValkeyCasClient(
            host=config.valkey_host,
            port=config.valkey_port,
            timeout_seconds=config.timeout_seconds,
        ).probe(release_fingerprint=release_fingerprint, evaluated_at=now)
        signer_fact = signer.probe()
        if not hmac.compare_digest(
            base64.b64decode(signer_fact.public_key_base64, validate=True),
            trusted_signer_public_key,
        ):
            raise ServerAcceptanceError("trusted-signer-public-key-mismatch")

        candidate_values = {
            "evaluated_at": now,
            "source_revision": source_revision,
            "release_fingerprint": release_fingerprint,
            "contract_manifest_digest": bundle.manifest_digest,
            "application": application,
            "signer": signer_fact,
            "object_store": object_store_fact,
            "cas": cas,
        }
        preliminary = ServerAcceptanceCandidate.model_construct(
            **candidate_values,
            report_digest="0" * 64,
        )
        unsigned = preliminary.model_dump(mode="json", exclude={"report_digest"})
        candidate = ServerAcceptanceCandidate(
            **candidate_values,
            report_digest=sha256_hex(unsigned),
        )
        signature = signer.sign_and_verify(
            canonical_json_bytes(candidate),
            signer=signer_fact,
        )
        stored_payload = _signed_report_payload(candidate, signature)
        object_key = (
            f"server-acceptance/{release_fingerprint}/"
            f"{candidate.report_digest}.signed.json"
        )
        locked_object = object_store.store_locked(
            bucket=config.object_store_bucket,
            object_key=object_key,
            payload=stored_payload,
            evaluated_at=now,
        )
        receipt_values = {
            "candidate": candidate,
            "valid_until": min(
                locked_object.retain_until,
                now + timedelta(hours=24),
            ),
            "remote_signature": signature,
            "signature_verified": True,
            "evidence_object": locked_object,
            "receipt_signature_verified": True,
        }
        preliminary_receipt = ServerAcceptanceReceipt.model_construct(
            **receipt_values,
            receipt_signature="vault:v1:cGxhY2Vob2xkZXI=",
            receipt_digest="0" * 64,
        )
        receipt_claims = preliminary_receipt.model_dump(
            mode="json",
            exclude={"receipt_signature", "receipt_digest"},
        )
        receipt_signature = signer.sign_and_verify(
            canonical_json_bytes(receipt_claims),
            signer=signer_fact,
        )
        signed_receipt_values = {
            **receipt_values,
            "receipt_signature": receipt_signature,
        }
        signed_preliminary = ServerAcceptanceReceipt.model_construct(
            **signed_receipt_values,
            receipt_digest="0" * 64,
        )
        unsigned_receipt = signed_preliminary.model_dump(
            mode="json",
            exclude={"receipt_digest"},
        )
        return ServerAcceptanceReceipt(
            **signed_receipt_values,
            receipt_digest=sha256_hex(unsigned_receipt),
        )
    finally:
        signer.close()
        object_store.close()


def build_blocked_result(
    *,
    source_revision: str,
    error: ServerAcceptanceError,
    evaluated_at: datetime | None = None,
) -> BlockedServerAcceptance:
    now = evaluated_at or datetime.now(UTC)
    fingerprint = sha256_hex(f"git-revision:{source_revision}")
    values = {
        "evaluated_at": now,
        "source_revision": source_revision,
        "release_fingerprint": fingerprint,
        "blocker_code": error.code,
        "cause_kind": error.cause_kind,
    }
    preliminary = BlockedServerAcceptance.model_construct(
        **values,
        receipt_digest="0" * 64,
    )
    unsigned = preliminary.model_dump(mode="json", exclude={"receipt_digest"})
    return BlockedServerAcceptance(**values, receipt_digest=sha256_hex(unsigned))


def _probe_application(
    backend_url: str,
    *,
    gateway_url: str,
    expected_source_revision: str,
    timeout_seconds: float,
) -> ApplicationAcceptance:
    try:
        with httpx.Client(timeout=timeout_seconds, trust_env=False) as client:
            response = client.get(f"{backend_url.rstrip('/')}/health/ready")
            response.raise_for_status()
            payload = response.json()
            backend_identity_response = client.get(
                f"{backend_url.rstrip('/')}/.well-known/workchord-build.json"
            )
            backend_identity_response.raise_for_status()
            backend_identity = backend_identity_response.json()
            gateway_health_response = client.get(
                f"{gateway_url.rstrip('/')}/health"
            )
            gateway_health_response.raise_for_status()
            gateway_health = gateway_health_response.json()
            gateway_identity_response = client.get(
                f"{gateway_url.rstrip('/')}/.well-known/workchord-build.json"
            )
            gateway_identity_response.raise_for_status()
            gateway_identity = gateway_identity_response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise ServerAcceptanceError("application-readiness-unavailable", cause=exc) from exc
    if not isinstance(payload, dict) or payload.get("status") != "ready":
        raise ServerAcceptanceError("application-not-ready")
    if (
        not isinstance(gateway_health, dict)
        or gateway_health.get("status") != "ok"
    ):
        raise ServerAcceptanceError("application-gateway-not-ready")
    if (
        not isinstance(backend_identity, dict)
        or not isinstance(gateway_identity, dict)
    ):
        raise ServerAcceptanceError("application-build-identity-invalid")
    try:
        common_identity_fields = (
            "schema_version",
            "component",
            "source_revision",
            "artifact_digest",
        )
        backend_identity_fields = (
            *common_identity_fields,
            "expected_frontend_artifact_digest",
        )
        backend_build_identity = BackendBuildIdentity.model_validate(
            {
                field: backend_identity.get(field)
                for field in backend_identity_fields
            }
        )
        gateway_build_identity = BuildIdentity.model_validate(
            {
                field: gateway_identity.get(field)
                for field in common_identity_fields
            }
        )
    except ValueError as exc:
        raise ServerAcceptanceError(
            "application-build-identity-invalid",
            cause=exc,
        ) from exc
    if (
        backend_build_identity.component != "backend"
        or gateway_build_identity.component != "frontend"
    ):
        raise ServerAcceptanceError("application-build-component-mismatch")
    backend_source_revision = backend_build_identity.source_revision
    gateway_source_revision = gateway_build_identity.source_revision
    backend_contract_manifest_digest = backend_identity.get(
        "contract_manifest_digest"
    )
    if (
        backend_source_revision != expected_source_revision
        or gateway_source_revision != expected_source_revision
    ):
        raise ServerAcceptanceError("application-image-revision-mismatch")
    database = payload.get("database")
    migration_gate = payload.get("migration_gate")
    if not isinstance(database, dict) or not isinstance(migration_gate, dict):
        raise ServerAcceptanceError("application-readiness-response-invalid")
    try:
        database_url = database.get("url")
        database_login_role = (
            urlsplit(database_url).username
            if isinstance(database_url, str)
            else None
        )
        return ApplicationAcceptance(
            backend_url=backend_url.rstrip("/"),
            gateway_url=gateway_url.rstrip("/"),
            status="ready",
            database_backend=database.get("backend"),
            database_login_role=database_login_role,
            database_connected=database.get("connected"),
            schema_current=database.get("schema_current"),
            migration_gate_clear=migration_gate.get("clear"),
            current_revision=database.get("current_revision"),
            expected_revision=database.get("expected_revision"),
            backend_source_revision=backend_source_revision,
            gateway_source_revision=gateway_source_revision,
            backend_artifact_digest=backend_build_identity.artifact_digest,
            gateway_artifact_digest=gateway_build_identity.artifact_digest,
            expected_gateway_artifact_digest=(
                backend_build_identity.expected_frontend_artifact_digest
            ),
            backend_contract_manifest_digest=backend_contract_manifest_digest,
        )
    except ValueError as exc:
        raise ServerAcceptanceError(
            "application-readiness-contract-failed",
            cause=exc,
        ) from exc


def _signed_report_payload(
    candidate: ServerAcceptanceCandidate,
    signature: str,
) -> bytes:
    return canonical_json_bytes(
        {
            "schema_version": "workchord-self-hosted-server-signed-report-v1",
            "candidate": candidate,
            "remote_signature": signature,
            "signature_verified": True,
        }
    )


def _verify_transit_signature(
    signer: TransitSignerAcceptance,
    payload: bytes,
    signature: str,
) -> None:
    parts = signature.split(":", 2)
    if len(parts) != 3 or parts[0] != "vault":
        raise ValueError("Transit signature format is invalid")
    try:
        version = int(parts[1].removeprefix("v"))
        signature_bytes = base64.b64decode(parts[2], validate=True)
        public_key = base64.b64decode(
            signer.public_key_base64,
            validate=True,
        )
    except (Base64Error, ValueError) as exc:
        raise ValueError("Transit signature encoding is invalid") from exc
    if version != signer.key_version:
        raise ValueError("Transit signature key version mismatch")
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(
            signature_bytes,
            payload,
        )
    except (InvalidSignature, ValueError) as exc:
        raise ValueError("Transit signature verification failed") from exc


def verify_receipt_trusted_signer(
    receipt: ServerAcceptanceReceipt,
    trusted_public_key_base64: str,
) -> None:
    """Bind a self-contained receipt to a public key supplied out of band."""

    trusted_public_key = _decode_ed25519_public_key(
        trusted_public_key_base64,
        error_message="Trusted signer public key is invalid",
    )
    receipt_public_key = _decode_ed25519_public_key(
        receipt.candidate.signer.public_key_base64,
        error_message="Receipt signer public key is invalid",
    )
    if not hmac.compare_digest(receipt_public_key, trusted_public_key):
        raise ValueError("Receipt signer does not match the trusted public key")


def verify_receipt_current_build(
    receipt: ServerAcceptanceReceipt,
    build_identity: BackendBuildIdentity,
    *,
    verified_at: datetime | None = None,
) -> None:
    """Require an unexpired receipt for the verifier's exact baked artifacts."""

    now = verified_at or datetime.now(UTC)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Verification clock must be timezone-aware")
    if receipt.candidate.evaluated_at > now + timedelta(minutes=5):
        raise ValueError("Receipt evaluation time is in the future")
    if now > receipt.valid_until:
        raise ValueError("Receipt acceptance horizon has expired")
    if receipt.candidate.source_revision != build_identity.source_revision:
        raise ValueError("Receipt source revision differs from this image")
    application = receipt.candidate.application
    if application.backend_artifact_digest != build_identity.artifact_digest:
        raise ValueError("Receipt backend artifact differs from this image")
    if (
        application.gateway_artifact_digest
        != build_identity.expected_frontend_artifact_digest
    ):
        raise ValueError("Receipt frontend artifact differs from this image")


def _decode_ed25519_public_key(value: str, *, error_message: str) -> bytes:
    try:
        public_key = base64.b64decode(value.strip(), validate=True)
    except (Base64Error, ValueError) as exc:
        raise ValueError(error_message) from exc
    if len(public_key) != 32:
        raise ValueError(error_message)
    return public_key


def _aws_signing_key(
    secret_key: str,
    *,
    date_stamp: str,
    region: str,
    service: str,
) -> bytes:
    date_key = hmac.new(
        f"AWS4{secret_key}".encode("utf-8"),
        date_stamp.encode("utf-8"),
        sha256,
    ).digest()
    region_key = hmac.new(date_key, region.encode("utf-8"), sha256).digest()
    service_key = hmac.new(region_key, service.encode("utf-8"), sha256).digest()
    return hmac.new(service_key, b"aws4_request", sha256).digest()


def _valkey_command(stream: BinaryIO, *parts: str) -> object:
    payload = [f"*{len(parts)}\r\n".encode("ascii")]
    for part in parts:
        encoded = part.encode("utf-8")
        payload.extend(
            (
                f"${len(encoded)}\r\n".encode("ascii"),
                encoded,
                b"\r\n",
            )
        )
    stream.write(b"".join(payload))
    stream.flush()
    return _read_resp(stream)


def _read_resp(stream: BinaryIO) -> object:
    line = stream.readline()
    if not line.endswith(b"\r\n"):
        raise ValueError("Incomplete RESP response")
    prefix = line[:1]
    value = line[1:-2]
    if prefix == b"+":
        return value.decode("utf-8")
    if prefix == b"-":
        raise ValueError("Valkey returned an error")
    if prefix == b":":
        return int(value)
    if prefix == b"$":
        length = int(value)
        if length == -1:
            return None
        payload = stream.read(length)
        if stream.read(2) != b"\r\n":
            raise ValueError("Incomplete RESP bulk response")
        return payload
    if prefix == b"*":
        length = int(value)
        if length == -1:
            return None
        return [_read_resp(stream) for _ in range(length)]
    raise ValueError("Unsupported RESP response")


def _is_hex_revision(value: str) -> bool:
    return len(value) in {40, 64} and all(character in "0123456789abcdef" for character in value)
