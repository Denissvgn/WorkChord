"""Public exports retain exact signed bytes and reject secret or failed evidence."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from app.autonomy.acceptance_artifacts import export_artifacts, verify_exported_artifacts, MAX_PREVIOUS_RECEIPTS
from app.cli.server_acceptance import main
from app.autonomy.server_acceptance import build_blocked_result, ServerAcceptanceError
from tests.autonomy.test_server_acceptance import _receipt, _build_identity, PUBLIC_KEY_BASE64

PREVIOUS = "previous-20261008T120000Z-123.json"


def _reports(tmp_path):
    reports = tmp_path / "reports"
    reports.mkdir()
    payload = _receipt().model_dump_json(indent=2).encode()
    for name in ["latest.json", PREVIOUS]:
        (reports / name).write_bytes(payload)
        pin = "trusted-signer-public-key.b64" if name == "latest.json" else name.removesuffix(".json") + ".trusted-signer-public-key.b64"
        (reports / pin).write_text(PUBLIC_KEY_BASE64 + "\n")
    independent = tmp_path / "owner-public-pin.b64"
    independent.write_text(PUBLIC_KEY_BASE64 + "\n")
    return reports, independent


def test_archive_roundtrip_uses_exact_bytes_and_independent_trust(tmp_path, monkeypatch, capsys):
    reports, trust = _reports(tmp_path)
    output = tmp_path / "public-artifacts"
    assert export_artifacts(reports, output, outcome="success")["complete"] is True
    assert (output / "latest.json").read_bytes() == (reports / "latest.json").read_bytes()
    shutil.make_archive(str(tmp_path / "download"), "zip", output)
    downloaded = tmp_path / "downloaded"
    shutil.unpack_archive(str(tmp_path / "download.zip"), downloaded)
    result = verify_exported_artifacts(downloaded, trust, _build_identity())
    assert result["receipt_count"] == 2
    assert result["latest"]["source_revision"] == _receipt().candidate.source_revision
    monkeypatch.setattr("app.cli.server_acceptance.load_backend_build_identity", _build_identity)
    assert main(["--verify-exported-artifacts", str(downloaded), "--trusted-signer-public-key-file", str(trust)]) == 0
    assert "SELF-HOSTED-SERVER-ARTIFACTS-VERIFIED" in capsys.readouterr().out
    with pytest.raises(ValueError, match="Unsafe"):
        verify_exported_artifacts(downloaded, downloaded / "trusted-signer-public-key.b64", _build_identity())


def test_allowlist_does_not_export_secret_named_files_or_unknown_receipt_fields(tmp_path):
    reports, trust = _reports(tmp_path)
    secret = "Bearer private-session-value-that-must-never-be-exported"
    for name in ["server.env", "private-key.pem", "signer-token", "session.json", "runtime-output.log", "previous-secret.json"]:
        (reports / name).write_text(secret)
    bad = json.loads((reports / "latest.json").read_text())
    bad["token"] = secret
    (reports / "latest.json").write_text(json.dumps(bad))
    output = tmp_path / "export"
    result = export_artifacts(reports, output, outcome="success")
    assert result["complete"] is False and result["rejected_receipts"] == 1
    assert not (output / "latest.json").exists()
    assert secret.encode() not in b"".join(p.read_bytes() for p in output.iterdir())
    assert {p.name for p in output.iterdir()} == {PREVIOUS, PREVIOUS.removesuffix(".json") + ".trusted-signer-public-key.b64", "failure-summary.json", "candidate-checksums.json"}
    with pytest.raises(ValueError, match="Failure evidence"):
        verify_exported_artifacts(output, trust, _build_identity())


@pytest.mark.parametrize("fault", ["missing-pin", "wrong-pin", "symlink", "fifo", "oversized", "malformed", "deep-json", "changed-signature"])
def test_invalid_receipt_or_public_pin_is_failure_evidence_only(tmp_path, fault):
    reports, trust = _reports(tmp_path)
    latest = reports / "latest.json"
    pin = reports / "trusted-signer-public-key.b64"
    if fault == "missing-pin":
        pin.unlink()
    elif fault == "wrong-pin":
        pin.write_text("private-key-not-public-base64")
    elif fault == "symlink":
        latest.unlink()
        latest.symlink_to(trust)
    elif fault == "fifo":
        latest.unlink()
        os.mkfifo(latest)
    elif fault == "oversized":
        latest.write_bytes(b"x" * 1_048_577)
    elif fault == "malformed":
        latest.write_text("[]")
    elif fault == "deep-json":
        latest.write_text('[' * 2000 + '0' + ']' * 2000)
    else:
        value = json.loads(latest.read_text())
        value["candidate"]["source_revision"] = "e" * 40
        latest.write_text(json.dumps(value))
    output = tmp_path / "export"
    result = export_artifacts(reports, output, outcome="success")
    assert result["complete"] is False
    assert result["rejected_receipts"] == 1
    assert not (output / "latest.json").exists()


def test_controlled_failure_keeps_valid_history_but_never_claims_acceptance(tmp_path):
    reports, trust = _reports(tmp_path)
    output = tmp_path / "failed-export"
    result = export_artifacts(reports, output, outcome="failure")
    assert result["run_outcome"] == "failure" and result["complete"] is False
    assert (output / "latest.json").read_bytes() == (reports / "latest.json").read_bytes()
    with pytest.raises(ValueError, match="Failure evidence"):
        verify_exported_artifacts(output, trust, _build_identity())
    empty = tmp_path / "empty-export"
    assert export_artifacts(tmp_path / "absent", empty, outcome="success")["complete"] is False
    assert not (empty / "latest.json").exists()


@pytest.mark.parametrize("fault", ["bytes", "candidate-index", "independent-pin", "missing-receipt", "extra-file"])
def test_downloaded_archive_tampering_cannot_verify(tmp_path, fault):
    reports, trust = _reports(tmp_path)
    output = tmp_path / "export"
    export_artifacts(reports, output, outcome="success")
    if fault == "bytes":
        with (output / "latest.json").open("ab") as stream:
            stream.write(b" ")
    elif fault == "candidate-index":
        index = json.loads((output / "candidate-checksums.json").read_text())
        index["receipts"][0]["candidate"]["source_revision"] = "e" * 40
        (output / "candidate-checksums.json").write_text(json.dumps(index))
    elif fault == "independent-pin":
        trust.write_text("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    elif fault == "missing-receipt":
        (output / PREVIOUS).unlink()
    else:
        (output / "server.env").write_text("SECRET=do-not-read")
    with pytest.raises((ValueError, OSError)):
        verify_exported_artifacts(output, trust, _build_identity())


def test_retained_history_is_bounded_and_pins_are_associated(tmp_path):
    reports, _ = _reports(tmp_path)
    for index in range(20):
        name = f"previous-20261008T120000Z-{1000 + index}.json"
        (reports / name).write_bytes((reports / "latest.json").read_bytes())
        (reports / (name.removesuffix(".json") + ".trusted-signer-public-key.b64")).write_text(PUBLIC_KEY_BASE64)
    output = tmp_path / "export"
    summary = export_artifacts(reports, output, outcome="success")
    manifest = json.loads((output / "candidate-checksums.json").read_text())
    assert summary["history_truncated"] is True
    assert len(manifest["receipts"]) == MAX_PREVIOUS_RECEIPTS + 1
    assert len(list(output.iterdir())) == 2 * (MAX_PREVIOUS_RECEIPTS + 1) + 2


def test_duplicate_json_keys_cannot_smuggle_unvalidated_bytes(tmp_path):
    reports, _ = _reports(tmp_path)
    original = (reports / "latest.json").read_text()
    hidden = '"candidate":{"token":"Bearer private-session-material-never-export"},'
    (reports / "latest.json").write_text('{' + hidden + original[1:])
    output = tmp_path / "export"
    result = export_artifacts(reports, output, outcome="success")
    assert result["complete"] is False and result["rejected_receipts"] == 1
    assert not (output / "latest.json").exists()
    assert b"private-session-material" not in b"".join(p.read_bytes() for p in output.iterdir())


def test_dependency_failure_exports_only_sanitized_summary(tmp_path):
    root = Path(__file__).resolve().parents[3]
    output = tmp_path / "export"
    result = subprocess.run([sys.executable, "-S", str(root / "scripts/server/export_acceptance_artifacts.py"),
        "--reports", str(tmp_path / "missing"), "--output", str(output), "--outcome", "success"], capture_output=True)
    assert result.returncode == 2
    assert {p.name for p in output.iterdir()} == {"failure-summary.json", "candidate-checksums.json"}
    summary = json.loads((output / "failure-summary.json").read_text())
    assert summary["complete"] is False and summary["status"] == "export-validator-unavailable"


def test_blocked_history_keeps_export_and_verifier_failure_semantics_consistent(tmp_path):
    reports, trust = _reports(tmp_path)
    blocked = build_blocked_result(source_revision=_receipt().candidate.source_revision,
        error=ServerAcceptanceError("controlled-failure"))
    name = "previous-20261008T110000Z-122.json"
    (reports / name).write_text(blocked.model_dump_json())
    output = tmp_path / "export"
    assert export_artifacts(reports, output, outcome="success")["complete"] is False
    assert (output / name).read_bytes() == (reports / name).read_bytes()
    with pytest.raises(ValueError, match="Failure evidence"):
        verify_exported_artifacts(output, trust, _build_identity())
