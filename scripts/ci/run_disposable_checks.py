#!/usr/bin/env python3
"""Run database, frontend and browser checks using isolated native processes."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
from uuid import uuid4
from urllib.parse import urlsplit

from ci_runtime import RunReceipt, junit_counts, positive_seconds, stop_process_group


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


def require_free_browser_ports(ports=(8001, 8002, 4173)):
    for port in ports:
        with socket.socket() as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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


def source_digest(check_cancel=None):
    paths = subprocess.check_output(["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=ROOT, timeout=15).split(b"\0")
    digest = hashlib.sha256()
    for raw in sorted(set(paths)):
        if not raw:
            continue
        name = raw.decode()
        if check_cancel:
            check_cancel()
        if name.startswith("docs/llm_wiki/"):
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        digest.update(raw + b"\0" + path.read_bytes())
    return digest.hexdigest()



def bind_source(run, digest=source_digest):
    run.check_budget()
    run.data['revision'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, timeout=15).strip()
    run.data['source_sha256'] = digest()
    run.checkpoint()
    def validate_source():
        run.data['source_sha256_after'] = digest()
        if run.data['source_sha256_after'] != run.data['source_sha256']:
            raise ValueError('Source changed during execution; rerun with a stable source')
    run.validators.append(validate_source)


def validate_results(run, selected, managed):
    run.data['junit'] = {}
    errors = []
    for scope in selected:
        if scope == 'browser':
            name = 'managed-browser.json' if managed else 'browser.json'
            try:
                report = json.loads((run.output / name).read_text())
                if report.get('status') != 'passed':
                    raise ValueError('Browser assertions did not pass')
                if managed and (not isinstance(report.get('steps'), list) or not report['steps']
                                or report.get('pageErrors') != []):
                    raise ValueError('Managed browser requires completed assertions without page errors')
                if not managed and (report.get('reloadVerified') is not True
                                    or report.get('writeStatus') != 201 or report.get('independentReadStatus') != 200):
                    raise ValueError('Browser write/read/reload verification is missing')
                run.data['browser_report'] = name
            except (OSError, ValueError) as exc:
                errors.append(f'{name}: {exc}')
        else:
            name = scope + '.xml'
            try:
                run.data['junit'][name] = junit_counts(run.output / name)
            except Exception as exc:
                errors.append(f'{name}: {exc}')
    if errors:
        run.data.setdefault('artifact_errors', []).extend(errors)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--scope', choices=['sqlite', 'postgresql', 'frontend', 'browser'])
    mode.add_argument('--browser-only', action='store_true')
    mode.add_argument('--backend-only', action='store_true')
    parser.add_argument('--full-backend', action='store_true')
    parser.add_argument('--managed-browser', action='store_true')
    parser.add_argument('--planning-browser', action='store_true')
    parser.add_argument('--performance-browser', action='store_true')
    parser.add_argument('--workflow-browser', action='store_true')
    parser.add_argument('--time-entries', action='store_true')
    parser.add_argument('--timeout-seconds', type=positive_seconds, default=1800,
                        help='Work budget; leave time outside this for cleanup and uploads')
    args = parser.parse_args()
    if args.scope:
        selected = [args.scope]
    elif args.browser_only:
        selected = ['browser']
    else:
        selected = ['sqlite', 'postgresql'] + ([] if args.backend_only else ['frontend', 'browser'])
    if args.performance_browser and (not args.managed_browser or args.planning_browser):
        parser.error('--performance-browser requires managed access and its own fixture')
    if args.workflow_browser and (not args.managed_browser or not args.time_entries or args.planning_browser or args.performance_browser):
        parser.error('--workflow-browser requires managed access, enabled time entries and its own fixture')
    if args.planning_browser and not args.managed_browser:
        parser.error('--planning-browser requires --managed-browser')
    if args.managed_browser and 'browser' not in selected:
        parser.error('--managed-browser requires browser checks')
    if args.full_backend and not set(selected).intersection({'sqlite', 'postgresql'}):
        parser.error('--full-backend requires backend checks')
    return args, selected


def main():
    args, selected = parse_args()
    output = args.output or Path(tempfile.mkdtemp(prefix='workchord-checks-'))
    try:
        run = RunReceipt(output, checks=selected, timeout_seconds=args.timeout_seconds)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    with run:
        bind_source(run, source_digest)
        run.data['playwright_version'] = PLAYWRIGHT_VERSION
        run.data['access'] = 'managed' if args.managed_browser else 'trusted-local'
        workspace = tempfile.TemporaryDirectory(prefix='workchord-runtime-')
        run.cleanups.append(workspace.cleanup)
        run.validators.append(lambda: validate_results(run, selected, args.managed_browser))
        scratch = Path(workspace.name)
        env = {**runtime_environment(), 'WORKCHORD_AUTH_MODE': 'trusted_local', 'DEPLOYMENT_ENVIRONMENT': 'test',
               'DATABASE_SSL_MODE': 'disable', 'PYTHONPATH': str(ROOT / 'backend'),
               'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONPYCACHEPREFIX': str(scratch / 'pycache'),
               'DATABASE_URL': f"sqlite+aiosqlite:///{scratch / 'workchord_test_import.db'}"}
        if 'postgresql' in selected:
            validate_admin_url(env.get('POSTGRES_ADMIN_URL', ''))
            env['WORKCHORD_SCHEMA_DIFF_ARTIFACT'] = str(run.output / 'schema-diff.json')
        run.run('python-version', [sys.executable, '--version'], cwd=scratch, env=env, timeout=30)
        if args.scope is None and not args.browser_only:
            run.run('contract', [sys.executable, str(ROOT / 'scripts/generate_client_contract.py'), '--check'], cwd=scratch, env=env, timeout=120)
        if set(selected).intersection({'sqlite', 'postgresql'}):
            targets = [ROOT / 'backend/tests'] if args.full_backend or args.scope else [ROOT / 'backend/tests' / name for name in [
                'test_delivery_scenarios.py', 'test_client_contract.py', 'test_managed_authority.py',
                'test_identity_lifecycle.py', 'test_work_correctness.py', 'test_authority_migrations.py']]
            for scope, marker in (('sqlite', 'not postgresql'), ('postgresql', 'postgresql')):
                if scope in selected:
                    run.run(scope, [sys.executable, '-m', 'pytest', '-q', '--durations=25', '-o',
                        f"cache_dir={scratch / 'pytest-cache'}", '-m', marker,
                        f"--junitxml={run.output / (scope + '.xml')}", *map(str, targets)],
                        cwd=scratch, env=env, timeout=1200 if scope == 'sqlite' else 900, check=False)
            if args.scope == 'postgresql':
                def require_schema_diff():
                    difference = json.loads((run.output / 'schema-diff.json').read_text())
                    if any(difference[key] for key in ('missing_from_sqlite', 'missing_from_postgresql', 'structural_differences')):
                        raise ValueError('Database schemas differ structurally')
                run.validators.append(require_schema_diff)
        if set(selected).intersection({'frontend', 'browser'}):
            frontend = scratch / 'frontend'
            shutil.copytree(ROOT / 'frontend', frontend, ignore=shutil.ignore_patterns(
                'node_modules', 'dist', 'coverage', 'test-results', '.env', '.env.*', '*.tsbuildinfo', '.DS_Store'))
            run.run('frontend-install', ['npm', 'ci'], cwd=frontend, env=env, timeout=300)
            run.run('node-version', ['node', '--version'], cwd=frontend, env=env, timeout=30)
            if 'frontend' in selected:
                for label, command in (
                    ('frontend-tests', ['npm', 'run', 'test:run', '--', '--maxWorkers=2', '--reporter=default', '--reporter=junit', f"--outputFile={run.output / 'frontend.xml'}"]),
                    ('frontend-lint', ['npm', 'run', 'lint']), ('frontend-build', ['npm', 'run', 'build'])):
                    run.run(label, command, cwd=frontend, env=env, timeout=300, check=False)
            if 'browser' in selected:
                require_free_browser_ports()
                browser_dir = scratch / 'browser'
                browser_dir.mkdir()
                run.run('browser-install', ['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund', f'playwright@{PLAYWRIGHT_VERSION}'], cwd=browser_dir, env=env, timeout=180)
                run.run('browser-runtime', ['npx', '--no-install', 'playwright', 'install', 'chromium'], cwd=browser_dir, env=env, timeout=180)
                browser_file = 'browser_performance.mjs' if args.performance_browser else 'browser_planning_inputs.mjs' if args.planning_browser else 'browser_managed_work.mjs' if args.managed_browser else 'browser_write_readback.mjs'
                shutil.copyfile(ROOT / 'scripts/ci' / browser_file, browser_dir / browser_file)
                if args.managed_browser:
                    shutil.copyfile(ROOT / 'scripts/ci/browser_worker.mjs', browser_dir / 'browser_worker.mjs')
                app_env = {**env, 'DATABASE_URL': f"sqlite+aiosqlite:///{scratch / 'workchord_test_browser.db'}",
                    'VITE_API_URL': 'http://127.0.0.1:8001', 'BROWSER_BASE_URL': 'http://localhost:4173',
                    'BROWSER_ARTIFACTS_DIR': str(run.output), 'WORKCHORD_FIXTURE_ISSUER': 'http://localhost:8002',
                    'WORKCHORD_FIXTURE_NONCE': uuid4().hex, 'WORKCHORD_BROWSER_PYTHON': sys.executable, 'WORKCHORD_BROWSER_SOURCE_ROOT': str(ROOT)}
                if args.performance_browser:
                    app_env.update(STRICT_MUTATION_VERSIONS='true', WORKCHORD_FIXTURE_PERFORMANCE='true',
                        WORKCHORD_BENCHMARK_AGENT_KEY='delivery-scenario-worker-key')
                if args.workflow_browser:
                    app_env.update(STRICT_MUTATION_VERSIONS='true', WORKCHORD_FIXTURE_WORKFLOWS='true')
                if args.planning_browser:
                    app_env.update(STRICT_MUTATION_VERSIONS='true', WORKCHORD_FIXTURE_PLANNING='true')
                app_env['TIME_ENTRIES_ENABLED'] = 'true' if args.time_entries else 'false'
                if args.managed_browser:
                    app_env.update(WORKCHORD_AUTH_MODE='managed', OIDC_ISSUER_URL='http://localhost:8002',
                        OIDC_CLIENT_ID='browser-client', OIDC_CLIENT_SECRET='disposable-browser-secret',
                        OIDC_REDIRECT_URI='http://localhost:4173/api/auth/callback', OIDC_ALLOW_HTTP_LOOPBACK='true',
                        CORS_ORIGINS='["http://localhost:4173"]', SESSION_COOKIE_SECURE='false')
                run.start('api', [sys.executable, str(ROOT / 'scripts/ci/serve_disposable_api.py')], cwd=scratch, env=app_env)
                run.start('frontend', [str(frontend / 'node_modules/.bin/vite'), '--host', '127.0.0.1', '--port', '4173', '--strictPort'], cwd=frontend, env=app_env)
                run.run('browser', ['node', browser_file], cwd=browser_dir, env=app_env, timeout=450)
    return run.exit_code


if __name__ == '__main__':
    raise SystemExit(main())
