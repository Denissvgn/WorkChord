# GitHub Actions: Client and scenario baseline

**Path:** `.github/workflows/client-baseline.yml`
**Type:** `github_actions`

## Triggers

- `workflow_call`
- `workflow_dispatch`

## Jobs

| Job | Display Name | Runs On | Needs | Steps |
|---|---|---|---|---:|
| `delivery` | `Browser (${{ matrix.access }})` | `ubuntu-24.04` | — | 7 |
| `android` | `Android unit results and debug APK` | `ubuntu-24.04` | — | 6 |

### delivery

- Reserve cleanup and artifact time - runs `python3 - <<'PYTHON' import os import time deadline = time.time() + int(os.environ["JOB_BUDGET_MINUTES"]) * 60 - 180 with open(os.environ["GITHUB_ENV"], "a") as output: output.write(f"WORKCHORD_CI_DEADLINE_EPOCH={deadline}\n") PYTHON`
- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 - uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405`
- actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 - uses `actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238`
- Install backend and browser dependencies - runs `python -m venv "$RUNNER_TEMP/workchord-python" "$RUNNER_TEMP/workchord-python/bin/pip" install --require-hashes -r backend/build-requirements.lock "$RUNNER_TEMP/workchord-python/bin/pip" install --require-hashes -r backend/requirements.lock "$RUNNER_TEMP/workchord-python/bin/pip" install --require-hashes -r backend/test-requirements.lock "$RUNNER_TEMP/workchord-python/bin/pip" install --no-build-isolation --no-deps -e ./backend sudo python3 scripts/ci/apt_runtime.py npx --yes playwright@1.59.1 install-deps chromium`
- Run the pinned native runtimes - runs `"$RUNNER_TEMP/workchord-python/bin/python" scripts/ci/run_disposable_checks.py --browser-only --timeout-seconds 600 ${{ matrix.browser_args }} --output /tmp/workchord-client-results`
- client-baseline-${{ matrix.access }}-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`

### android

- Reserve cleanup and artifact time - runs `python3 - <<'PYTHON' import os import time deadline = time.time() + int(os.environ["JOB_BUDGET_MINUTES"]) * 60 - 180 with open(os.environ["GITHUB_ENV"], "a") as output: output.write(f"WORKCHORD_CI_DEADLINE_EPOCH={deadline}\n") PYTHON`
- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 - uses `actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961`
- Install the Android SDK components - runs `if ! test -x "$ANDROID_HOME/cmdline-tools/12.0/bin/sdkmanager"; then curl --fail --location --retry 3 \ https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \ -o "$RUNNER_TEMP/workchord-android-tools.zip" printf '%s  %s\n' d313adb7aedccf6cf0cfca51ec180f0059f5f8f8 "$RUNNER_TEMP/workchord-android-tools.zip" | sha1sum -c - unzip -q "$RUNNER_TEMP/workchord-android-tools.zip" -d "$RUNNER_TEMP/workchord-android-tools" mkdir -p "$ANDROID_HOME/cmdline-tools" mv "$RUNNER_TEMP/workchord-android-tools/cmdline-tools" "$ANDROID_HOME/cmdline-tools/12.0" fi python3 - <<'PY' import os import subprocess from pathlib import Path manager = str(Path(os.environ["ANDROID_HOME"]) / "cmdline-tools/12.0/bin/sdkmanager") subprocess.run([manager, "--licenses"], input="y\n" * 100, text=True, stdout=subprocess.DEVNULL, check=True, timeout=120) subprocess.run([manager, "platforms;android-34", "build-tools;34.0.0"], check=True, timeout=180) PY`
- Build and execute with the pinned native JDK and SDK - runs `python3 scripts/ci/run_android_checks.py --timeout-seconds 1200 --output /tmp/workchord-android-results`
- android-baseline-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`

## Notes

This reusable workflow is called from the main CI workflow and remains manually dispatchable. Its trusted-local and managed browser variants use isolated SQLite-backed API/frontend processes and Playwright; full backend/frontend workloads run in their dedicated jobs. Android retains the pinned native JDK, SDK, wrapper, both result variants and debug APK.

Each job records its work deadline before setup and uses incremental receipts with bounded commands and cleanup. Artifact uploads run after success or failure. The matrix retains independent outcomes instead of cancelling the other browser variant after a failure. Automatic execution does not require a container registry.

Before Playwright installs Chromium system dependencies, shared APT preparation replaces the Ubuntu Azure mirror and applies bounded download timeouts and retries while preserving signed repository checks. The native PostgreSQL action uses the same preparation. Setup failures remain failures of the required aggregate gate.
