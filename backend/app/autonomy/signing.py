"""Detached remote-signing envelopes and pinned public-key verification."""

from __future__ import annotations

import base64
import binascii
import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa
from pydantic import Field, field_validator

from app.autonomy.canonical import StrictContractModel, sha256_hex


SHA256_PATTERN = r"^[0-9a-f]{64}$"
KEY_REF_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:/-]{2,511}$"


class DetachedSignatureEnvelope(StrictContractModel):
    """Provider-neutral signature metadata without an embedded trust key."""

    schema_version: Literal["workchord-remote-signature-v1"] = (
        "workchord-remote-signature-v1"
    )
    key_ref: str = Field(pattern=KEY_REF_PATTERN, max_length=512)
    key_version: str = Field(min_length=1, max_length=255)
    issuer: str = Field(min_length=1, max_length=255)
    subject: str = Field(min_length=1, max_length=512)
    algorithm: Literal["ed25519", "ecdsa-p256-sha256", "rsa-pss-sha256"]
    payload_sha256: str = Field(pattern=SHA256_PATTERN)
    signature_base64: str = Field(min_length=4, max_length=16_384)

    @field_validator("signature_base64")
    @classmethod
    def valid_base64(cls, value: str) -> str:
        try:
            base64.b64decode(value, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("signature_base64 must be canonical base64") from exc
        return value


class PublicTrustAnchor(StrictContractModel):
    """A public key returned by a separately trusted resolver."""

    key_ref: str = Field(pattern=KEY_REF_PATTERN, max_length=512)
    key_version: str = Field(min_length=1, max_length=255)
    issuer: str = Field(min_length=1, max_length=255)
    allowed_subjects: tuple[str, ...] = Field(min_length=1, max_length=256)
    algorithm: Literal["ed25519", "ecdsa-p256-sha256", "rsa-pss-sha256"]
    public_key_pem: str = Field(min_length=64, max_length=16_384)
    source_receipt_digest: str = Field(pattern=SHA256_PATTERN)

    @field_validator("public_key_pem")
    @classmethod
    def public_key_only(cls, value: str) -> str:
        if "PRIVATE KEY" in value:
            raise ValueError("A trust anchor must never contain a private key")
        if "BEGIN PUBLIC KEY" not in value:
            raise ValueError("public_key_pem must contain a PEM public key")
        return value


@runtime_checkable
class PublicTrustResolver(Protocol):
    """Resolve a current public key from an external trust source."""

    def resolve(self, *, key_ref: str, key_version: str) -> PublicTrustAnchor: ...


@runtime_checkable
class RemoteSigner(Protocol):
    """Sign a digest through a non-exportable external key service."""

    def sign_digest(
        self,
        *,
        payload_sha256: str,
        key_ref: str,
        subject: str,
    ) -> DetachedSignatureEnvelope: ...


class SignatureVerificationError(ValueError):
    """Raised when a detached remote signature fails closed."""


def verify_detached_signature(
    payload: bytes,
    envelope: DetachedSignatureEnvelope,
    resolver: PublicTrustResolver,
) -> PublicTrustAnchor:
    """Verify digest, trust metadata, key type, and detached signature."""

    payload_digest = sha256_hex(payload)
    if payload_digest != envelope.payload_sha256:
        raise SignatureVerificationError("Signed payload digest mismatch")
    try:
        anchor = resolver.resolve(
            key_ref=envelope.key_ref,
            key_version=envelope.key_version,
        )
    except Exception as exc:
        raise SignatureVerificationError("Public trust source is unavailable") from exc
    if anchor.key_ref != envelope.key_ref or anchor.key_version != envelope.key_version:
        raise SignatureVerificationError("Trust resolver returned the wrong key")
    if anchor.issuer != envelope.issuer:
        raise SignatureVerificationError("Signature issuer is not trusted")
    if envelope.subject not in anchor.allowed_subjects:
        raise SignatureVerificationError("Signature subject is not trusted")
    if anchor.algorithm != envelope.algorithm:
        raise SignatureVerificationError("Signature algorithm does not match trust anchor")
    try:
        signature = base64.b64decode(envelope.signature_base64, validate=True)
        public_key = serialization.load_pem_public_key(anchor.public_key_pem.encode())
        digest_bytes = bytes.fromhex(payload_digest)
        if envelope.algorithm == "ed25519":
            if not isinstance(public_key, ed25519.Ed25519PublicKey):
                raise SignatureVerificationError("Trust key is not Ed25519")
            public_key.verify(signature, digest_bytes)
        elif envelope.algorithm == "ecdsa-p256-sha256":
            if not isinstance(public_key, ec.EllipticCurvePublicKey) or not isinstance(
                public_key.curve, ec.SECP256R1
            ):
                raise SignatureVerificationError("Trust key is not P-256")
            public_key.verify(signature, digest_bytes, ec.ECDSA(hashes.SHA256()))
        else:
            if not isinstance(public_key, rsa.RSAPublicKey):
                raise SignatureVerificationError("Trust key is not RSA")
            public_key.verify(
                signature,
                digest_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
    except InvalidSignature as exc:
        raise SignatureVerificationError("Detached signature is invalid") from exc
    except (ValueError, TypeError, binascii.Error) as exc:
        if isinstance(exc, SignatureVerificationError):
            raise
        raise SignatureVerificationError("Detached signature envelope is invalid") from exc
    return anchor


@dataclass(frozen=True)
class CallableTrustResolver:
    """Small adapter for provider SDK integrations and deterministic tests."""

    callback: Callable[[str, str], PublicTrustAnchor]

    def resolve(self, *, key_ref: str, key_version: str) -> PublicTrustAnchor:
        return self.callback(key_ref, key_version)


def validate_sha256(value: str, *, field_name: str = "digest") -> str:
    """Validate a lowercase SHA-256 string at non-Pydantic boundaries."""

    if re.fullmatch(SHA256_PATTERN, value) is None:
        raise ValueError(f"{field_name} must be a lowercase SHA-256 digest")
    return value
