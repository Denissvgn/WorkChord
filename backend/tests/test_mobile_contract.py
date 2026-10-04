"""Android's golden examples are derived from current canonical backend schemas."""

from pathlib import Path
import runpy
import sys


ROOT = Path(__file__).resolve().parents[2]


def test_mobile_examples_are_current_and_deterministic():
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        exporter = runpy.run_path(str(ROOT / "scripts/generate_mobile_contract_fixtures.py"))
        first = exporter["serialized_examples"]()
        assert first == exporter["serialized_examples"]()
        assert first == (ROOT / "android-companion/app/src/test/resources/mobile-contract-v1.json").read_text()
    finally:
        sys.path.pop(0)
