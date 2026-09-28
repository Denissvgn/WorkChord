# GitHub Actions: Client and scenario baseline

**Path:** `.github/workflows/client-baseline.yml`
**Type:** `github_actions`

## Triggers

- `pull_request`
- `push`
- `workflow_dispatch`

## Jobs

| Job | Display Name | Runs On | Needs | Steps |
|---|---|---|---|---:|
| `delivery` | `Native database and browser (${{ matrix.access }})` | `ubuntu-24.04` | — | 8 |
| `android` | `Android unit results and debug APK` | `ubuntu-24.04` | — | 5 |

### delivery

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 - uses `actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405`
- actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 - uses `actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238`
- Set up native PostgreSQL - uses `./.github/actions/native-postgres`
- Install backend and browser dependencies - runs `python -m venv "$RUNNER_TEMP/workchord-python" "$RUNNER_TEMP/workchord-python/bin/pip" install --require-hashes -r backend/build-requirements.lock "$RUNNER_TEMP/workchord-python/bin/pip" install --require-hashes -r backend/requirements.lock "$RUNNER_TEMP/workchord-python/bin/pip" install --require-hashes -r backend/test-requirements.lock "$RUNNER_TEMP/workchord-python/bin/pip" install --no-build-isolation --no-deps -e ./backend npx --yes playwright@1.59.1 install-deps chromium`
- Run the pinned native runtimes - runs `"$RUNNER_TEMP/workchord-python/bin/python" scripts/ci/run_disposable_checks.py --full-backend ${{ matrix.browser_args }} --output /tmp/workchord-client-results`
- client-baseline-${{ matrix.access }}-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`
- Stop the job-owned PostgreSQL cluster - runs `>-`

### android

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 - uses `actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961`
- Install the Android SDK components - runs `if ! test -x "$ANDROID_HOME/cmdline-tools/12.0/bin/sdkmanager"; then curl --fail --location --retry 3 \ https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip \ -o "$RUNNER_TEMP/workchord-android-tools.zip" printf '%s  %s\n' d313adb7aedccf6cf0cfca51ec180f0059f5f8f8 "$RUNNER_TEMP/workchord-android-tools.zip" | sha1sum -c - unzip -q "$RUNNER_TEMP/workchord-android-tools.zip" -d "$RUNNER_TEMP/workchord-android-tools" mkdir -p "$ANDROID_HOME/cmdline-tools" mv "$RUNNER_TEMP/workchord-android-tools/cmdline-tools" "$ANDROID_HOME/cmdline-tools/12.0" fi python3 - <<'PY' import os import subprocess from pathlib import Path manager = str(Path(os.environ["ANDROID_HOME"]) / "cmdline-tools/12.0/bin/sdkmanager") subprocess.run([manager, "--licenses"], input="y\n" * 100, text=True, stdout=subprocess.DEVNULL, check=True) subprocess.run([manager, "platforms;android-34", "build-tools;34.0.0"], check=True) PY`
- Build and execute with the pinned native JDK and SDK - runs `python3 scripts/ci/run_android_checks.py --output /tmp/workchord-android-results`
- android-baseline-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`

## Notes

The trusted-local and managed lanes use native Python, Node, PostgreSQL and Playwright processes with isolated state and retained receipts. Android uses a pinned native JDK, SDK components and the verified Gradle wrapper, retaining both build-variant results and a debug APK. Automatic jobs do not require container registries. Workflow definition alone does not establish that a hosted execution completed.
