"""Bounded public receipt exports and independent offline archive verification."""

from __future__ import annotations

import base64
import json
import os
import re
import stat
import tempfile
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit

from app.autonomy.server_acceptance import (
    BlockedServerAcceptance, ServerAcceptanceReceipt,
    verify_receipt_current_build, verify_receipt_trusted_signer,
)

MAX_RECEIPT_BYTES = 1_048_576
MAX_PREVIOUS_RECEIPTS = 8
RECEIPT_NAME = re.compile(r"latest\.json|previous-[0-9]{8}T[0-9]{6}Z-[0-9]+\.json")
PUBLIC_PIN_NAME = re.compile(r"trusted-signer-public-key\.b64|previous-[0-9]{8}T[0-9]{6}Z-[0-9]+\.trusted-signer-public-key\.b64")


def _read(path: Path, limit: int) -> bytes:
    """Read only a bounded regular file without following a file symlink."""
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise ValueError("Artifact is not a regular file")
        payload = stream.read(limit + 1)
    if len(payload) > limit:
        raise ValueError("Artifact exceeds size limit")
    return payload


def _public_urls(value):
    if isinstance(value, dict):
        for nested in value.values():
            _public_urls(nested)
    elif isinstance(value, list):
        for nested in value:
            _public_urls(nested)
    elif isinstance(value, str) and "://" in value:
        url = urlsplit(value)
        if url.username is not None or url.password is not None or url.query or url.fragment:
            raise ValueError("Artifact URL contains non-public material")


def _receipt(payload: bytes):
    value = _json(payload)
    if not isinstance(value, dict):
        raise ValueError("Receipt must be an object")
    _public_urls(value)
    model = ServerAcceptanceReceipt if value.get("decision") == "SELF-HOSTED-SERVER-ACCEPTED" else BlockedServerAcceptance
    return model.model_validate(value)


def _json(payload: bytes):
    def unique(pairs):
        value = {}
        for key, nested in pairs:
            if key in value:
                raise ValueError("Duplicate artifact JSON key")
            value[key] = nested
        return value
    return json.loads(payload, object_pairs_hook=unique)


def _pin_name(name: str) -> str:
    return "trusted-signer-public-key.b64" if name == "latest.json" else name.removesuffix(".json") + ".trusted-signer-public-key.b64"


def _identity(receipt) -> dict:
    value = {"decision": receipt.decision, "receipt_digest": receipt.receipt_digest}
    if isinstance(receipt, ServerAcceptanceReceipt):
        candidate = receipt.candidate
        value["candidate"] = {
            "source_revision": candidate.source_revision,
            "release_fingerprint": candidate.release_fingerprint,
            "contract_manifest_digest": candidate.contract_manifest_digest,
            "backend_artifact_digest": candidate.application.backend_artifact_digest,
            "gateway_artifact_digest": candidate.application.gateway_artifact_digest,
        }
    else:
        value["candidate"] = {"source_revision": receipt.source_revision, "release_fingerprint": receipt.release_fingerprint}
    return value


def _pin(payload: bytes, receipt: ServerAcceptanceReceipt) -> None:
    text = payload.decode("ascii").strip()
    raw = base64.b64decode(text, validate=True)
    if len(raw) != 32 or base64.b64encode(raw).decode("ascii") != text:
        raise ValueError("Not a canonical Ed25519 public key")
    # This association check is not an independent trust decision.
    verify_receipt_trusted_signer(receipt, text)


def export_artifacts(source: Path, output: Path, *, outcome: str) -> dict:
    """Stage validated exact bytes; failures export a generic summary, never an accepted decision."""
    if outcome not in {"success", "failure"}:
        raise ValueError("Unknown acceptance outcome")
    if source.is_symlink() or output.exists() or output.is_symlink():
        raise ValueError("Unsafe artifact directory")
    files = {}
    receipts = []
    rejected = 0
    previous = sorted((p.name for p in source.iterdir() if RECEIPT_NAME.fullmatch(p.name) and p.name != "latest.json"), reverse=True) if source.is_dir() else []
    names = ["latest.json", *previous[:MAX_PREVIOUS_RECEIPTS]]
    for name in names:
        path = source / name
        if not path.exists() and not path.is_symlink():
            continue
        try:
            payload = _read(path, MAX_RECEIPT_BYTES)
            receipt = _receipt(payload)
            pin_name = None
            pin_payload = None
            if isinstance(receipt, ServerAcceptanceReceipt):
                pin_name = _pin_name(name)
                pin_payload = _read(source / pin_name, 128)
                _pin(pin_payload, receipt)
            files[name] = payload
            if pin_name is not None:
                files[pin_name] = pin_payload
            receipts.append({"file": name, "public_pin": pin_name, **_identity(receipt)})
        except (OSError, ValueError, RecursionError):
            rejected += 1
    accepted = {row["file"] for row in receipts if row["decision"] == "SELF-HOSTED-SERVER-ACCEPTED"}
    complete = (outcome == "success" and rejected == 0 and len(accepted) == len(receipts)
                and "latest.json" in accepted and any(name != "latest.json" for name in accepted))
    summary = {
        "schema_version": 1, "run_outcome": outcome, "complete": complete,
        "status": "public-artifacts-retained" if complete else "acceptance-failed-or-incomplete",
        "rejected_receipts": rejected, "history_truncated": len(previous) > MAX_PREVIOUS_RECEIPTS,
        "accepted_as_production_evidence": False,
    }
    files["failure-summary.json"] = (json.dumps(summary, sort_keys=True, indent=2) + "\n").encode()
    index = {
        "schema_version": 1, "receipts": receipts,
        "files": [{"file": name, "bytes": len(payload), "sha256": sha256(payload).hexdigest()} for name, payload in sorted(files.items())],
    }
    files["candidate-checksums.json"] = (json.dumps(index, sort_keys=True, indent=2) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".public-artifacts-", dir=output.parent) as temporary:
        staging = Path(temporary) / "export"
        staging.mkdir()
        for name, payload in files.items():
            (staging / name).write_bytes(payload)
        staging.rename(output)
    return summary


def verify_exported_artifacts(directory: Path, trusted_public_key: Path, build) -> dict:
    """Verify exact archive membership, hashes and signatures using a separately supplied trust pin."""
    if directory.is_symlink() or trusted_public_key.resolve().is_relative_to(directory.resolve()):
        raise ValueError("Unsafe artifact directory")
    index = _json(_read(directory / "candidate-checksums.json", MAX_RECEIPT_BYTES))
    if set(index) != {"schema_version", "receipts", "files"} or index["schema_version"] != 1:
        raise ValueError("Unknown artifact index")
    if len(index["files"]) > 2 * (MAX_PREVIOUS_RECEIPTS + 1) + 1 or len(index["receipts"]) > MAX_PREVIOUS_RECEIPTS + 1:
        raise ValueError("Artifact index exceeds history limit")
    expected = {"candidate-checksums.json"}
    payloads = {}
    for row in index["files"]:
        if set(row) != {"file", "bytes", "sha256"}:
            raise ValueError("Invalid checksum entry")
        name = row["file"]
        if name in expected or not (name == "failure-summary.json" or RECEIPT_NAME.fullmatch(name) or PUBLIC_PIN_NAME.fullmatch(name)):
            raise ValueError("Artifact outside public allowlist")
        payload = _read(directory / name, MAX_RECEIPT_BYTES if name.endswith(".json") else 128)
        if len(payload) != row["bytes"] or sha256(payload).hexdigest() != row["sha256"]:
            raise ValueError("Artifact checksum mismatch")
        expected.add(name)
        payloads[name] = payload
    if {p.name for p in directory.iterdir()} != expected:
        raise ValueError("Unexpected or missing archive member")
    summary = _json(payloads["failure-summary.json"])
    if not isinstance(summary, dict) or summary.get("complete") is not True or summary.get("run_outcome") != "success":
        raise ValueError("Failure evidence cannot count as acceptance")
    trust = _read(trusted_public_key, 128).decode("ascii")
    receipt_names = set()
    used_pins = set()
    for row in index["receipts"]:
        name = row["file"]
        if name in receipt_names or name not in payloads or not RECEIPT_NAME.fullmatch(name):
            raise ValueError("Invalid receipt index")
        receipt = _receipt(payloads[name])
        if not isinstance(receipt, ServerAcceptanceReceipt):
            raise ValueError("Blocked receipt cannot count as acceptance")
        pin_name = _pin_name(name)
        if row != {"file": name, "public_pin": pin_name, **_identity(receipt)}:
            raise ValueError("Candidate index mismatch")
        _pin(payloads[pin_name], receipt)
        verify_receipt_trusted_signer(receipt, trust)
        if name == "latest.json":
            verify_receipt_current_build(receipt, build)
        receipt_names.add(name)
        used_pins.add(pin_name)
    if "latest.json" not in receipt_names or len(receipt_names) < 2:
        raise ValueError("Required acceptance receipts missing")
    if set(payloads) != receipt_names | used_pins | {"failure-summary.json"}:
        raise ValueError("Unassociated archive member")
    return {"decision": "SELF-HOSTED-SERVER-ARTIFACTS-VERIFIED", "receipt_count": len(receipt_names),
            "latest": next(row for row in index["receipts"] if row["file"] == "latest.json")["candidate"],
            "accepted_as_production_evidence": False}
