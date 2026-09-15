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
| `delivery` | `Disposable database and browser (${{ matrix.access }})` | `ubuntu-latest` | — | 3 |
| `android` | `Android unit results and debug APK` | `ubuntu-latest` | — | 3 |

### delivery

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- Run the pinned runtimes - runs `python3 scripts/ci/run_disposable_checks.py --full-backend ${{ matrix.browser_args }} --output /tmp/workchord-client-results`
- client-baseline-${{ matrix.access }}-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`

### android

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- Build and execute with the pinned JDK and SDK - runs `python3 scripts/ci/run_android_checks.py --output /tmp/workchord-android-results`
- android-baseline-${{ github.sha }} - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`

## Notes

The two jobs invoke the same isolated runners used locally and retain revision-bound receipts, logs and build artifacts even on failure. Repository credentials, SDK-local configuration and production signing material are not inputs. Defining the workflow does not establish that a hosted run has completed.
