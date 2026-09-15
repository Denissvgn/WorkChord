#!/usr/bin/env python3
"""Run pinned database, frontend, and browser checks without an existing app stack."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
from uuid import uuid4
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
NODE_IMAGE = "node:22.23.1-alpine3.23@sha256:8516dce0483394d5708d4b2ee6cacb79fb1d617ea4e2787c2120bcca92ce372e"
POSTGRES_IMAGE = "postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296"
BROWSER_IMAGE = "mcr.microsoft.com/playwright:v1.59.1-noble"


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
    run_id = uuid4().hex
    python_image = f"workchord-disposable-checks:{run_id}"
    network = f"workchord-check-{run_id}"
    containers = []
    receipt = {"revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "source_sha256": source_digest(), "started_at": datetime.now(timezone.utc).isoformat(),
               "environment": "disposable-containers", "run_id": run_id, "commands": [],
               "images": {"python": python_image, "node": NODE_IMAGE, "postgres": POSTGRES_IMAGE, "browser": BROWSER_IMAGE}}

    def run(label, command, *, check=True):
        print(label, flush=True)
        started = time.monotonic()
        with (output / f"{label}.log").open("w") as log:
            result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        receipt["commands"].append({"label": label, "argv": command, "exit_code": result.returncode,
                                    "elapsed_seconds": round(time.monotonic() - started, 2), "log": f"{label}.log"})
        if check and result.returncode:
            raise RuntimeError(f"{label} failed; see {output / (label + '.log')}")
        return result.returncode

    def start(label, image, extra, command):
        name = f"{network}-{label}"
        containers.append(name)
        run(f"start-{label}", ["docker", "run", "-d", "--name", name, "--network", network,
                              "--network-alias", label, *extra, image, *command])
        return name

    status = "failed"
    network_created = False
    try:
        run("build-python", ["docker", "build", "-f", "scripts/ci/Dockerfile.checks", "-t", python_image, "."])
        run("create-network", ["docker", "network", "create", network])
        network_created = True
        postgres = start("postgres", POSTGRES_IMAGE,
                         ["-e", "POSTGRES_PASSWORD=workchord-check-only", "-e",
                          "POSTGRES_INITDB_ARGS=--locale-provider=builtin --builtin-locale=PG_UNICODE_FAST"], [])
        for _ in range(60):
            ready = subprocess.run(["docker", "exec", postgres, "pg_isready", "-U", "postgres"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if ready.returncode == 0:
                break
            time.sleep(1)
        else:
            raise RuntimeError("Disposable PostgreSQL did not become ready")
        common = ["docker", "run", "--rm", "--network", network, "-v", f"{ROOT}:/source:ro",
                  "-v", f"{output}:/artifacts", "-e", "PYTHONPATH=/source/backend",
                  "-e", "DATABASE_URL=sqlite+aiosqlite:////tmp/workchord_test_import.db",
                  "-e", "POSTGRES_ADMIN_URL=postgresql+psycopg://postgres:workchord-check-only@postgres:5432/postgres"]
        run("python-version", [*common, python_image, "python", "--version"])
        run("contract", [*common, python_image, "python", "/source/scripts/generate_client_contract.py", "--check"])
        targets = ["/source/backend/tests"] if args.full_backend else [
            "/source/backend/tests/test_delivery_scenarios.py", "/source/backend/tests/test_client_contract.py",
            "/source/backend/tests/test_managed_authority.py", "/source/backend/tests/test_identity_lifecycle.py",
            "/source/backend/tests/test_work_correctness.py", "/source/backend/tests/test_authority_migrations.py"]
        failures = []
        for label, marker in (("sqlite", "not postgresql"), ("postgresql", "postgresql")):
            code = run(label, [*common, python_image, "python", "-m", "pytest", "-q", "-o",
                              "cache_dir=/tmp/pytest-cache", "-m", marker,
                              f"--junitxml=/artifacts/{label}.xml", *targets], check=False)
            if code:
                failures.append(label)
        if not args.backend_only:
            identity_env = (["--network-alias", "oidc", "-e", "WORKCHORD_AUTH_MODE=managed", "-e", "DEPLOYMENT_ENVIRONMENT=test",
                "-e", "OIDC_ISSUER_URL=http://oidc:8002", "-e", "OIDC_CLIENT_ID=browser-client", "-e", "OIDC_CLIENT_SECRET=disposable-browser-secret",
                "-e", "OIDC_REDIRECT_URI=http://localhost:4173/api/auth/callback", "-e", "OIDC_ALLOW_HTTP_LOOPBACK=true",
                "-e", 'CORS_ORIGINS=["http://localhost:4173"]', "-e", "SESSION_COOKIE_SECURE=false"] if args.managed_browser else [])
            api = start("api", python_image, [*identity_env,"-v", f"{ROOT}:/source:ro", "-e", "PYTHONPATH=/source/backend",
                        "-e", f"DATABASE_URL=sqlite+aiosqlite:////tmp/workchord_test_{run_id}.db"],
                        ["python", "/source/scripts/ci/serve_disposable_api.py"])
            frontend = start("frontend", NODE_IMAGE, ["-v", f"{ROOT / 'frontend'}:/source:ro",
                             "-v", f"{output}:/artifacts", "-e", "VITE_API_URL=http://api:8001",
                             "-e", "__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS=frontend"],
                             ["sh", "-c", "mkdir /work && tail -f /dev/null"])
            setup = "cd /source && tar --exclude=node_modules --exclude=dist --exclude=coverage --exclude=test-results --exclude=.env --exclude=.env.local -cf - . | tar -xf - -C /work"
            run("frontend-copy", ["docker", "exec", frontend, "sh", "-c", setup])
            run("frontend-install", ["docker", "exec", "-w", "/work", frontend, "npm", "ci"])
            run("node-version", ["docker", "exec", frontend, "node", "--version"])
            for label, command in (("frontend-tests", ["npm", "run", "test:run", "--", "--reporter=default", "--reporter=junit", "--outputFile=/artifacts/frontend.xml"]),
                                   ("frontend-lint", ["npm", "run", "lint"]), ("frontend-build", ["npm", "run", "build"])):
                if run(label, ["docker", "exec", "-w", "/work", frontend, *command], check=False):
                    failures.append(label)
            run("frontend-serve", ["docker", "exec", "-d", "-w", "/work", frontend,
                                   "./node_modules/.bin/vite", "--host", "0.0.0.0", "--port", "4173", "--strictPort"])
            browser_file = "browser_managed_work.mjs" if args.managed_browser else "browser_write_readback.mjs"
            browser_script = f"mkdir /runner && cd /runner && npm install --no-audit --no-fund playwright@1.59.1 && cp /source/scripts/ci/{browser_file} . && node {browser_file}"
            if run("browser", ["docker", "run", "--rm", "--network", f"container:{frontend}" if args.managed_browser else network, "--ipc=private", "--shm-size=1g",
                               "-v", f"{ROOT}:/source:ro", "-v", f"{output}:/artifacts",
                               "-e", f"BROWSER_BASE_URL={'http://localhost:4173' if args.managed_browser else 'http://frontend:4173'}", BROWSER_IMAGE, "sh", "-c", browser_script], check=False):
                failures.append("browser")
            run("api-log", ["docker", "logs", api], check=False)
        if failures:
            raise RuntimeError(f"Failed checks: {', '.join(failures)}")
        status = "passed"
    except Exception as exc:
        receipt["error"] = str(exc)
    finally:
        cleanup_failed = False
        for name in reversed(containers):
            cleanup_failed |= bool(run(f"cleanup-{name.rsplit('-', 1)[-1]}", ["docker", "rm", "-f", "-v", name], check=False))
        if network_created:
            cleanup_failed |= bool(run("cleanup-network", ["docker", "network", "rm", network], check=False))
        if cleanup_failed:
            status = "failed"
            receipt["cleanup_error"] = "A disposable container or network could not be removed"
        receipt["source_sha256_after"] = source_digest()
        if receipt["source_sha256_after"] != receipt["source_sha256"]:
            status = "failed"
            receipt["source_error"] = "Source changed during execution; results require a stable-source rerun"
        receipt["finished_at"] = datetime.now(timezone.utc).isoformat()
        receipt["junit"] = {}
        for path in output.glob("*.xml"):
            try:
                root = ET.parse(path).getroot()
            except ET.ParseError as exc:
                status = "failed"
                receipt.setdefault("artifact_errors", []).append(f"{path.name}: {exc}")
                continue
            suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
            receipt["junit"][path.name] = {key: sum(int(suite.get(key, 0)) for suite in suites)
                                           for key in ("tests", "failures", "errors", "skipped")}
            receipt["junit"][path.name]["expected_failures"] = len(root.findall(".//skipped[@type='pytest.xfail']"))
            if receipt["junit"][path.name]["tests"] <= receipt["junit"][path.name]["skipped"]:
                status = "failed"
                receipt.setdefault("artifact_errors", []).append(f"{path.name}: no executed results")
        receipt["status"] = status
        receipt["artifacts"] = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in sorted(output.iterdir()) if path.is_file()}
        (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
        print(f"{status}: {output}", flush=True)
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
