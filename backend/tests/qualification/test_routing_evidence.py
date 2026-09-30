"""Keep CI evidence inventories aligned with the checked-in implementation."""

from pathlib import Path
import subprocess
import sys

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.ci import check_model_aware_routing_closeout as evidence


@pytest.mark.contract
def test_routing_inventory_passes_the_tracked_ci_contract():
    receipt = evidence.validate_closeout(evidence.DEFAULT_INVENTORY, require_tracked=True)

    assert receipt["task_count"] == len(evidence.EXPECTED_TASK_IDS)
    assert receipt["release_gate_count"] == len(evidence.EXPECTED_GATE_IDS)
    assert receipt["evidence_file_count"] > 0
    assert all(not value["accepted"] for value in receipt["external_validation"].values())


@pytest.mark.contract
def test_missing_evidence_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(evidence, "REPOSITORY_ROOT", tmp_path)

    with pytest.raises(evidence.CloseoutContractError, match="does not exist"):
        evidence._evidence_path("removed-schema.py")


@pytest.mark.contract
def test_untracked_evidence_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(evidence, "REPOSITORY_ROOT", tmp_path)
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    (tmp_path / "schema.py").write_text("# Untracked fixture\n")

    with pytest.raises(evidence.CloseoutContractError, match="Git index"):
        evidence._require_tracked({"schema.py"})

    subprocess.run(["git", "add", "--", "schema.py"], cwd=tmp_path, check=True)
    evidence._require_tracked({"schema.py"})
