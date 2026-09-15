#!/usr/bin/env python3
"""Build Android with JDK 17, SDK 34 and the checksum-pinned Gradle wrapper in Docker."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from uuid import uuid4
import xml.etree.ElementTree as ET

from run_disposable_checks import ROOT, source_digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix="workchord-android-"))
    if output.exists() and any(output.iterdir()):
        parser.error("Output must be a new or empty directory")
    output.mkdir(parents=True, exist_ok=True)
    container = f"workchord-android-{uuid4().hex}"
    image = f"workchord-android-checks:{uuid4().hex}"
    receipt = {"revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "source_sha256": source_digest(), "started_at": datetime.now(timezone.utc).isoformat(),
               "environment": "disposable-linux-amd64-container", "commands": [],
               "integration_coverage": False, "image": image}

    def run(label, command):
        print(label, flush=True)
        with (output / f"{label}.log").open("w") as log:
            result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        receipt["commands"].append({"label": label, "argv": command, "exit_code": result.returncode})
        return result.returncode

    created = False
    success = False
    try:
        if run("build-image", ["docker", "build", "--platform", "linux/amd64", "-f", "scripts/ci/Dockerfile.android",
                               "-t", image, "android-companion"]):
            raise RuntimeError("Android image build failed")
        if run("create", ["docker", "create", "--platform", "linux/amd64", "--name", container, image]):
            raise RuntimeError("Android container creation failed")
        created = True
        result = run("gradle", ["docker", "start", "-a", container])
        for label, path in (("unit-results", "/workspace/app/build/test-results/testDebugUnitTest"),
                            ("unit-report", "/workspace/app/build/reports/tests/testDebugUnitTest"),
                            ("apk", "/workspace/app/build/outputs/apk/debug")):
            run(f"copy-{label}", ["docker", "cp", f"{container}:{path}", str(output / label)])
        suites = [ET.parse(path).getroot() for path in (output / "unit-results").glob("TEST-*.xml")]
        counts = {key: sum(int(suite.get(key, 0)) for suite in suites)
                  for key in ("tests", "failures", "errors", "skipped")}
        receipt["junit"] = counts
        receipt["toolchain"] = {"jdk": "17.0.16+8", "gradle": "8.7", "agp": "8.5.2", "compile_sdk": 34, "build_tools": "34.0.0"}
        apks = list((output / "apk").glob("*.apk"))
        success = result == 0 and counts["tests"] > counts["skipped"] and not counts["failures"] and not counts["errors"] and len(apks) == 1 and apks[0].stat().st_size > 0
        if not success:
            raise RuntimeError("Android requires successful executed unit results and a nonempty debug APK")
    except Exception as exc:
        receipt["error"] = str(exc)
    finally:
        if created:
            if run("cleanup", ["docker", "rm", "-f", "-v", container]):
                success = False
                receipt["cleanup_error"] = "The disposable Android container could not be removed"
        receipt["source_sha256_after"] = source_digest()
        if receipt["source_sha256_after"] != receipt["source_sha256"]:
            success = False
            receipt["source_error"] = "Source changed during execution; results require a stable-source rerun"
        receipt["status"] = "passed" if success else "failed"
        receipt["finished_at"] = datetime.now(timezone.utc).isoformat()
        receipt["artifacts"] = {str(path.relative_to(output)): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in sorted(output.rglob("*")) if path.is_file()}
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"{receipt['status']}: {output}", flush=True)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
