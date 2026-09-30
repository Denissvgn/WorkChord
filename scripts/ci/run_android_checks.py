#!/usr/bin/env python3
"""Build Android with native JDK 17, SDK 34 and the checksum-pinned Gradle wrapper."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
import subprocess
import tempfile
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
    workspace = tempfile.TemporaryDirectory(prefix="workchord-android-runtime-")
    project = Path(workspace.name) / "project"
    receipt = {"revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "source_sha256": source_digest(), "started_at": datetime.now(timezone.utc).isoformat(),
               "environment": "native-processes", "commands": [],
               "integration_coverage": False}

    def run(label, command):
        print(label, flush=True)
        with (output / f"{label}.log").open("w") as log:
            result = subprocess.run(command, cwd=project, stdout=log, stderr=subprocess.STDOUT)
        receipt["commands"].append({"label": label, "argv": command, "exit_code": result.returncode})
        return result.returncode

    success = False
    try:
        shutil.copytree(ROOT / "android-companion", project,
            ignore=shutil.ignore_patterns("build", ".gradle", ".idea", ".kotlin", "local.properties"))
        java = Path(os.environ["JAVA_HOME"]) / "bin/java" if os.environ.get("JAVA_HOME") else Path("java")
        version = subprocess.check_output([str(java), "-version"], stderr=subprocess.STDOUT, text=True)
        (output / "java-version.log").write_text(version)
        if not re.search(r'version "17[.\"]', version):
            raise RuntimeError("JDK 17 is required")
        sdk = Path(os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or "")
        if not (sdk / "platforms/android-34/android.jar").is_file() or not (sdk / "build-tools/34.0.0").is_dir():
            raise RuntimeError("Install Android SDK platform 34 and build-tools 34.0.0")
        wrapper = project / "gradle/wrapper/gradle-wrapper.jar"
        if hashlib.sha256(wrapper.read_bytes()).hexdigest() != "cb0da6751c2b753a16ac168bb354870ebb1e162e9083f116729cec9c781156b8":
            raise RuntimeError("Gradle wrapper checksum mismatch")
        result = run("gradle", [str(project / "gradlew"), "--no-daemon", "--max-workers=2",
            "--project-cache-dir", str(Path(workspace.name) / "gradle-project-cache"), "testDebugUnitTest", "testReleaseUnitTest", "assembleDebug"])
        for label, relative in (("unit-results", "app/build/test-results/testDebugUnitTest"),
                                ("release-unit-results", "app/build/test-results/testReleaseUnitTest"),
                                ("unit-report", "app/build/reports/tests/testDebugUnitTest"),
                                ("release-unit-report", "app/build/reports/tests/testReleaseUnitTest"),
                                ("apk", "app/build/outputs/apk/debug")):
            if (project / relative).is_dir():
                shutil.copytree(project / relative, output / label)
        suites = []
        receipt["junit_variants"] = {}
        for directory in ("unit-results", "release-unit-results"):
            files = list((output / directory).glob("TEST-*.xml"))
            if not files:
                raise RuntimeError(f"Missing executed Android results: {directory}")
            variant = [ET.parse(path).getroot() for path in files]
            counts = {key: sum(int(suite.get(key, 0)) for suite in variant)
                      for key in ("tests", "failures", "errors", "skipped")}
            receipt["junit_variants"][directory] = counts
            if counts["tests"] <= counts["skipped"] or counts["failures"] or counts["errors"]:
                raise RuntimeError(f"Android variant requires successful executed results: {directory}")
            suites.extend(variant)
        counts = {key: sum(int(suite.get(key, 0)) for suite in suites)
                  for key in ("tests", "failures", "errors", "skipped")}
        receipt["junit"] = counts
        receipt["toolchain"] = {"jdk": version.strip(), "gradle": "8.7", "agp": "8.5.2", "compile_sdk": 34, "build_tools": "34.0.0"}
        apks = list((output / "apk").glob("*.apk"))
        success = result == 0 and counts["tests"] > counts["skipped"] and not counts["failures"] and not counts["errors"] and len(apks) == 1 and apks[0].stat().st_size > 0
        if not success:
            raise RuntimeError("Android requires successful executed unit results and a nonempty debug APK")
    except Exception as exc:
        receipt["error"] = str(exc)
    finally:
        workspace.cleanup()
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
