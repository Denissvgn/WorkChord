# GitHub Actions: Deployment acceptance

**Path:** `.github/workflows/deployment-acceptance.yml`
**Type:** `github_actions`

## Triggers

- `workflow_dispatch`

## Jobs

| Job | Display Name | Runs On | Needs | Steps |
|---|---|---|---|---:|
| `server-acceptance` | `Self-hosted server acceptance` | `ubuntu-24.04` | — | 8 |

### server-acceptance

- `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1` - uses `actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1`
- `actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0` - uses `actions/setup-python@6d4fd22b20465ccc0f7354476588e8df7c9ca0e0`
- `Prepare public receipt validators` - runs `python -m venv .runtime/acceptance-export-venv .runtime/acceptance-export-venv/bin/pip install --require-hashes -r backend/requirements.lock`
- `Build and accept the self-hosted stack` - runs `./scripts/server/accept_self_hosted.sh ./scripts/server/accept_self_hosted.sh`
- `Validate the bounded receipt` - runs `test -s .runtime/autonomy/reports/latest.json test -s .runtime/autonomy/reports/trusted-signer-public-key.b64 test "$(find .runtime/autonomy/reports \ -maxdepth 1 -name 'previous-*.json' \| wc -l)" -ge 1 grep -q '"decision": "SELF-HOSTED-SERVER-ACCEPTED"' \ .runtime/autonomy/reports/latest.json grep -q '"accepted_as_production_evidence": false' \ .runtime/autonomy/reports/latest.json`
- `Export bounded public evidence` - runs `exporter=python3 if test -x .runtime/acceptance-export-venv/bin/python; then exporter=.runtime/acceptance-export-venv/bin/python fi "$exporter" scripts/server/export_acceptance_artifacts.py \ --reports .runtime/autonomy/reports \ --output .runtime/autonomy/reports/public-artifacts \ --outcome "$ACCEPTANCE_OUTCOME"`
- `Retain public acceptance evidence` - uses `actions/upload-artifact@bbbca2ddaa5d8feaa63e36b76fdaad77386f024f`
- `Stop the acceptance stack` - runs `if test -f .runtime/autonomy/server.env; then docker compose \ --project-name workchord-server \ --env-file .runtime/autonomy/server.env \ -f docker-compose.yml \ -f docker-compose.server.yml \ --profile autonomy \ down fi`

## Notes

This workflow runs only through workflow_dispatch. It retains the actual Compose deployment, two-run durable-state check, bounded signed-receipt verification and teardown. Container registry access remains a prerequisite for this explicitly requested deployment operation; it is not an automatic PR/main gate.

The workflow always stages validated public artifacts and uploads only staged JSON/public-pin files before teardown, with 14-day retention and a pinned upload action. Failed acceptance or missing required receipts leave the run unsuccessful and retain sanitized failure evidence. A generated workflow observation does not establish that hosted retention has actually executed.
