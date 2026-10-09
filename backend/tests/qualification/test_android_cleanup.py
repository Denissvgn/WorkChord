"""Emulator cleanup retains unrelated replacements and drains owned controllers."""

from pathlib import Path
import sys
import threading
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts" / "ci"))
import android_qualification as qualification


def owned_fixture():
    value = qualification.Qualification.__new__(qualification.Qualification)
    value.adb = ["adb", "-s", "emulator-5554"]
    value.data = {"device_serial": "emulator-5554", "owner_nonce": "owned"}
    value.installed = {"changed": "original", "owned": "matching"}
    value.reversed = [8123, 8124]
    value.controller_stop = threading.Event()
    value.controller_thread = None
    value.owner = lambda: None
    value.installed_hash = lambda package, label: "replacement" if package == "changed" else "matching"
    value.adb_read = lambda *args: "(reverse) tcp:8123 tcp:9999\nhost tcp:8124 tcp:8124"
    return value


def test_cleanup_aggregates_failures_and_preserves_replaced_resources(monkeypatch):
    value = owned_fixture()
    calls = []
    monkeypatch.setattr(qualification.subprocess, "run", lambda argv, **kwargs: calls.append(argv))
    with pytest.raises(ValueError, match="Owned cleanup incomplete"):
        value.cleanup()
    assert calls == [value.adb + ["uninstall", "owned"], value.adb + ["reverse", "--remove", "tcp:8124"]]
    assert value.installed == {"changed": "original"}
    assert value.reversed == [8123]


def test_cleanup_stops_controller_before_any_resource_observation(monkeypatch):
    value = owned_fixture()
    events = []
    value.controller_thread = SimpleNamespace(join=lambda timeout: events.append(("joined", value.controller_stop.is_set())), is_alive=lambda: False)
    value.owner = lambda: events.append(("owner", value.controller_thread is None))
    monkeypatch.setattr(qualification.subprocess, "run", lambda *args, **kwargs: None)
    with pytest.raises(ValueError):value.cleanup()
    assert events[0] == ("joined", True)
    assert all(stopped for kind, stopped in events if kind == "owner")


def test_unstopped_controller_holds_cleanup_before_resource_mutation(monkeypatch):
    value = owned_fixture()
    value.controller_thread = SimpleNamespace(join=lambda timeout: None, is_alive=lambda: True)
    value.owner = lambda: pytest.fail("Resource ownership must not be observed before controller drain")
    with pytest.raises(ValueError, match="cleanup is held"):value.cleanup()


def test_cancelled_marker_wait_does_not_observe_or_restore_resources():
    value = owned_fixture()
    value.controller_stop.set()
    value.marker = lambda *args: pytest.fail("Cancelled controller touched the emulator")
    with pytest.raises(ValueError, match="cancelled"):value.await_marker("stage.txt", lambda _: False)


def test_instrumentation_failure_drains_started_controller(tmp_path):
    import hashlib
    value = owned_fixture()
    value.project = tmp_path / "project"
    value.tools = tmp_path / "tools"
    value.run = SimpleNamespace(output=tmp_path / "evidence", data={})
    value.run.output.mkdir()
    for directory in ("release", "androidTest/release"):
        apk = value.project / "app/build/outputs/apk" / directory / "owned.apk"
        apk.parent.mkdir(parents=True)
        apk.write_bytes(b"owned qualification fixture")
    value.certificate_sha256 = "a" * 64
    value.cases = [("FixtureCase", "networkInterruptionLocksCurrentWorkAndRecoversLocalInputs")]
    value.data.update(api_origin="https://localhost:8123", browser_origin="https://localhost:8124",
        fixture_nonce="owned", fixture_parent_id=1)
    value.installed = {}
    value.installed_hash = lambda package, label: hashlib.sha256(b"owned qualification fixture").hexdigest()
    value.controller = lambda method: value.controller_stop.wait(20)
    def command(label, argv, timeout=30):
        if label == "manifest-inspection":
            return "\n".join(f"android:{name}=(type 0x12)0x0" for name in ("allowBackup", "usesCleartextTraffic", "debuggable"))
        if "certificate-inspection" in label:return "certificate SHA-256 digest: " + value.certificate_sha256
        if label == "instrumentation-0":raise RuntimeError("Owned instrumentation timeout")
        return ""
    value.command = command
    with pytest.raises(RuntimeError, match="instrumentation timeout"):
        value.exercise(lambda: None)
    assert value.controller_stop.is_set()
    assert value.controller_thread is None
