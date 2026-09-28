# GitHub Actions: Deployment acceptance

**Path:** `.github/workflows/deployment-acceptance.yml`
**Type:** `github_actions`

## Triggers

- `workflow_dispatch`

## Jobs

| Job | Display Name | Runs On | Needs | Steps |
|---|---|---|---|---:|
| `server-acceptance` | `Self-hosted server acceptance` | `ubuntu-24.04` | — | 4 |

### server-acceptance

- actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd - uses `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`
- Build and accept the self-hosted stack - runs `./scripts/server/accept_self_hosted.sh ./scripts/server/accept_self_hosted.sh`
- Validate the bounded receipt - runs `test -s .runtime/autonomy/reports/latest.json test -s .runtime/autonomy/reports/trusted-signer-public-key.b64 test "$(find .runtime/autonomy/reports \ -maxdepth 1 -name 'previous-*.json' | wc -l)" -ge 1 grep -q '"decision": "SELF-HOSTED-SERVER-ACCEPTED"' \ .runtime/autonomy/reports/latest.json grep -q '"accepted_as_production_evidence": false' \ .runtime/autonomy/reports/latest.json`
- Stop the acceptance stack - runs `if test -f .runtime/autonomy/server.env; then docker compose \ --project-name workchord-server \ --env-file .runtime/autonomy/server.env \ -f docker-compose.yml \ -f docker-compose.server.yml \ --profile autonomy \ down fi`

## Notes

This workflow runs only through workflow_dispatch. It retains the actual Compose deployment, two-run durable-state check, bounded signed-receipt verification and teardown. Container registry access remains a prerequisite for this explicitly requested deployment operation; it is not an automatic PR/main gate.
