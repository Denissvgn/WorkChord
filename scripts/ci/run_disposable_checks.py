#!/usr/bin/env python3
"""Run database, frontend and browser checks using isolated native processes."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
from uuid import uuid4
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
PLAYWRIGHT_VERSION = "1.59.1"


def runtime_environment():
    """Inherit toolchain settings without inheriting an operator's application secrets."""
    names = {"PATH", "HOME", "LANG", "LC_ALL", "TZ", "TMPDIR", "TEMP", "TMP", "CI",
        "SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "NODE_EXTRA_CA_CERTS",
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy",
        "NPM_CONFIG_CACHE", "PLAYWRIGHT_BROWSERS_PATH", "POSTGRES_ADMIN_URL"}
    env = {key: value for key, value in os.environ.items() if key in names}
    env["NO_PROXY"] = ",".join(filter(None, [env.get("NO_PROXY"), "127.0.0.1,localhost,::1"]))
    return env


def require_free_browser_ports():
    for port in (8001, 8002, 4173):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", port))


def validate_admin_url(value):
    """Keep libpq connection overrides from escaping the loopback fixture boundary."""
    url = urlsplit(value)
    if (url.scheme not in {"postgresql", "postgresql+psycopg"}
            or url.hostname not in {"127.0.0.1", "localhost", "::1"}
            or url.path != "/postgres" or url.query or url.fragment):
        raise ValueError("POSTGRES_ADMIN_URL must be a plain loopback PostgreSQL URL ending in /postgres")
    if url.port is not None and not 1024 <= url.port <= 65535:
        raise ValueError("Use an unprivileged local PostgreSQL port")


def stop_process_group(process):
    """Stop the owned service and its descendants, and always reap the parent."""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=15)
        return True
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=10)
        return False


def source_digest():
    paths = subprocess.check_output(["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=ROOT).split(b"\0")
    digest = hashlib.sha256()
    for raw in sorted(set(paths)):
        if not raw:
            continue
        name = raw.decode()
        path = ROOT / name
        if not path.is_file() or name.startswith("docs/llm_wiki/"):
            continue
        digest.update(raw + b"\0" + path.read_bytes())
    return digest.hexdigest()



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--backend-only", action="store_true")
    parser.add_argument("--full-backend", action="store_true")
    parser.add_argument("--managed-browser", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix="workchord-checks-"))
    if output.exists() and any(output.iterdir()):
        parser.error("Output must be a new or empty directory to preserve previous receipts")
    output.mkdir(parents=True, exist_ok=True)
    receipt = {"revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_sha256": source_digest(), "started_at": datetime.now(timezone.utc).isoformat(),
        "environment": "native-processes", "commands": [], "playwright_version": PLAYWRIGHT_VERSION}
    processes = []
    handles = []
    workspace = tempfile.TemporaryDirectory(prefix="workchord-runtime-")
    scratch = Path(workspace.name)
    env = {**runtime_environment(), "WORKCHORD_AUTH_MODE": "trusted_local", "DEPLOYMENT_ENVIRONMENT": "test",
        "DATABASE_SSL_MODE": "disable", "PYTHONPATH": str(ROOT / "backend"),
        "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPYCACHEPREFIX": str(scratch / "pycache"),
        "DATABASE_URL": f"sqlite+aiosqlite:///{scratch / 'workchord_test_import.db'}"}

    def run(label, command, *, cwd=scratch, check=True, process_env=None):
        print(label, flush=True)
        with (output / f"{label}.log").open("w") as log:
            result = subprocess.run(command, cwd=cwd, env=process_env or env, stdout=log, stderr=subprocess.STDOUT)
        receipt["commands"].append({"label": label, "argv": [str(item) for item in command],
            "exit_code": result.returncode, "log": f"{label}.log"})
        if check and result.returncode:
            raise RuntimeError(f"{label} failed; see {output / (label + '.log')}")
        return result.returncode

    def start(label, command, *, cwd=scratch, process_env=None):
        log = (output / f"{label}.log").open("w")
        handles.append(log)
        process = subprocess.Popen(command, cwd=cwd, env=process_env or env,
            stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        processes.append((label, process))
        receipt["commands"].append({"label": f"start-{label}", "argv": [str(item) for item in command],
            "exit_code": 0, "log": f"{label}.log"})
        return process

    status = "failed"
    try:
        admin = env.get("POSTGRES_ADMIN_URL", "")
        validate_admin_url(admin)
        run("python-version", [sys.executable, "--version"])
        run("contract", [sys.executable, str(ROOT / "scripts/generate_client_contract.py"), "--check"])
        targets = [ROOT / "backend/tests"] if args.full_backend else [ROOT / "backend/tests" / name for name in [
            "test_delivery_scenarios.py", "test_client_contract.py", "test_managed_authority.py",
            "test_identity_lifecycle.py", "test_work_correctness.py", "test_authority_migrations.py"]]
        failures = []
        for label, marker in (("sqlite", "not postgresql"), ("postgresql", "postgresql")):
            if run(label, [sys.executable, "-m", "pytest", "-q", "-o", f"cache_dir={scratch / 'pytest-cache'}",
                "-m", marker, f"--junitxml={output / (label + '.xml')}", *map(str, targets)], check=False):
                failures.append(label)
        if not args.backend_only:
            require_free_browser_ports()
            frontend = scratch / "frontend"
            shutil.copytree(ROOT / "frontend", frontend, ignore=shutil.ignore_patterns(
                "node_modules", "dist", "coverage", "test-results", ".env", ".env.*", "*.tsbuildinfo"))
            run("frontend-install", ["npm", "ci"], cwd=frontend)
            run("node-version", ["node", "--version"])
            for label, command in (("frontend-tests", ["npm", "run", "test:run", "--", "--reporter=default", "--reporter=junit", f"--outputFile={output / 'frontend.xml'}"]),
                                   ("frontend-lint", ["npm", "run", "lint"]), ("frontend-build", ["npm", "run", "build"])):
                if run(label, command, cwd=frontend, check=False):
                    failures.append(label)
            browser_dir = scratch / "browser"
            browser_dir.mkdir()
            run("browser-install", ["npm", "install", "--ignore-scripts", "--no-audit", "--no-fund", f"playwright@{PLAYWRIGHT_VERSION}"], cwd=browser_dir)
            run("browser-runtime", ["npx", "--no-install", "playwright", "install", "chromium"], cwd=browser_dir)
            browser_file = "browser_managed_work.mjs" if args.managed_browser else "browser_write_readback.mjs"
            shutil.copyfile(ROOT / "scripts/ci" / browser_file, browser_dir / browser_file)
            app_env = {**env, "DATABASE_URL": f"sqlite+aiosqlite:///{scratch / 'workchord_test_browser.db'}",
                "VITE_API_URL": "http://127.0.0.1:8001", "BROWSER_BASE_URL": "http://localhost:4173",
                "BROWSER_ARTIFACTS_DIR": str(output), "WORKCHORD_FIXTURE_ISSUER": "http://localhost:8002",
                "WORKCHORD_FIXTURE_NONCE": uuid4().hex}
            if args.managed_browser:
                app_env.update(WORKCHORD_AUTH_MODE="managed", OIDC_ISSUER_URL="http://localhost:8002",
                    OIDC_CLIENT_ID="browser-client", OIDC_CLIENT_SECRET="disposable-browser-secret",
                    OIDC_REDIRECT_URI="http://localhost:4173/api/auth/callback", OIDC_ALLOW_HTTP_LOOPBACK="true",
                    CORS_ORIGINS='["http://localhost:4173"]', SESSION_COOKIE_SECURE="false")
            start("api", [sys.executable, str(ROOT / "scripts/ci/serve_disposable_api.py")], process_env=app_env)
            start("frontend", [str(frontend / "node_modules/.bin/vite"), "--host", "127.0.0.1", "--port", "4173", "--strictPort"], cwd=frontend, process_env=app_env)
            if run("browser", ["node", browser_file], cwd=browser_dir, process_env=app_env, check=False):
                failures.append("browser")
        if failures:
            raise RuntimeError(f"Failed checks: {', '.join(failures)}")
        status = "passed"
    except Exception as exc:
        receipt["error"] = str(exc)
    finally:
        for label, process in reversed(processes):
            stopped = stop_process_group(process)
            receipt["commands"].append({"label": f"stop-{label}", "exit_code": 0 if stopped else 1,
                "process_exit_code": process.returncode})
            if not stopped:
                status = "failed"
                receipt.setdefault("cleanup_errors", []).append(label)
        for handle in handles:
            handle.close()
        workspace.cleanup()
        receipt["source_sha256_after"] = source_digest()
        if receipt["source_sha256_after"] != receipt["source_sha256"]:
            status = "failed"
            receipt["source_error"] = "Source changed during execution; results require a stable-source rerun"
        receipt["finished_at"] = datetime.now(timezone.utc).isoformat()
        receipt["junit"] = {}
        expected = ["sqlite.xml", "postgresql.xml"] + ([] if args.backend_only else ["frontend.xml"])
        for name in expected:
            path = output / name
            try:
                root = ET.parse(path).getroot()
                suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
                counts = {key: sum(int(suite.get(key, 0)) for suite in suites) for key in ("tests", "failures", "errors", "skipped")}
                receipt["junit"][name] = counts
                counts["expected_failures"] = len(root.findall(".//skipped[@type='pytest.xfail']"))
                if counts["tests"] <= counts["skipped"] or counts["failures"] or counts["errors"]:
                    raise ValueError("Expected successful executed results")
            except (OSError, ET.ParseError, ValueError) as exc:
                status = "failed"
                receipt.setdefault("artifact_errors", []).append(f"{name}: {exc}")
        receipt["status"] = status
        receipt["artifacts"] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(output.iterdir()) if path.is_file()}
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"{status}: {output}", flush=True)
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
