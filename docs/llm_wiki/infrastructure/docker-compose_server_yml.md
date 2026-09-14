# docker-compose.server.yml

**Path:** `docker-compose.server.yml`

## Services

| Service | Image / Build | Ports | Depends On |
|---------|---------------|-------|------------|
| `postgres` | — |  |  |
| `migration` | — |  | `{'database-bootstrap': {'condition': 'service_completed_successfully'}}` |
| `repair` | — |  | `{'database-security': {'condition': 'service_completed_successfully'}}` |
| `backend` | — |  |  |
| `delivery-worker` | — |  |  |
| `frontend` | — |  |  |
| `database-bootstrap` | `postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296` |  | `{'postgres': {'condition': 'service_healthy'}}` |
| `database-security` | `postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296` |  | `{'migration': {'condition': 'service_completed_successfully'}}` |
| `openbao` | `openbao/openbao:2.6.1@sha256:5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0` |  |  |
| `openbao-bootstrap` | `openbao/openbao:2.6.1@sha256:5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0` |  | `{'openbao': {'condition': 'service_healthy'}}` |
| `minio` | `minio/minio:RELEASE.2025-09-07T16-13-09Z@sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e` |  |  |
| `minio-bootstrap` | `minio/mc:RELEASE.2025-08-13T08-35-41Z@sha256:a7fe349ef4bd8521fb8497f55c6042871b2ae640607cf99d9bede5e9bdf11727` |  | `{'minio': {'condition': 'service_started'}}` |
| `valkey` | `valkey/valkey:8.1.9-alpine@sha256:a038175878d66b9d274fbf8be73c0305e93798b83917647f167e18cef3c71eec` |  |  |
| `autonomy-acceptance` | — |  | `{'backend': {'condition': 'service_healthy'}, 'delivery-worker': {'condition': 'service_started'}, 'openbao-bootstrap': {'condition': 'service_completed_successfully'}, 'minio-bootstrap': {'condition': 'service_completed_successfully'}, 'valkey': {'condition': 'service_healthy'}}` |

### postgres

- **Volumes:** `./deploy/postgresql/init-server-roles.sh:/docker-entrypoint-initdb.d/15-server-roles.sh:ro`
- **Environment:** `{'WORKCHORD_MIGRATOR_PASSWORD': '${WORKCHORD_MIGRATOR_PASSWORD:?Set WORKCHORD_MIGRATOR_PASSWORD}', 'WORKCHORD_RUNTIME_PASSWORD': '${WORKCHORD_RUNTIME_PASSWORD:?Set WORKCHORD_RUNTIME_PASSWORD}', 'WORKCHORD_BACKUP_PASSWORD': '${WORKCHORD_BACKUP_PASSWORD:?Set WORKCHORD_BACKUP_PASSWORD}'}`

### migration

- **Environment:** `{'DATABASE_URL': '${DATABASE_MIGRATION_URL:?Set DATABASE_MIGRATION_URL}', 'DATABASE_SESSION_ROLE': 'workchord_owner'}`
- **Depends on:** `{'database-bootstrap': {'condition': 'service_completed_successfully'}}`

### repair

- **Environment:** `{'DATABASE_URL': '${DATABASE_MIGRATION_URL:?Set DATABASE_MIGRATION_URL}', 'DATABASE_SESSION_ROLE': 'workchord_owner'}`
- **Depends on:** `{'database-security': {'condition': 'service_completed_successfully'}}`

### backend

- **Volumes:** `workchord_server_data:/app/data`
- **Environment:** `{'DATABASE_URL': '${DATABASE_RUNTIME_URL:?Set DATABASE_RUNTIME_URL}', 'DATABASE_SESSION_ROLE': '', 'DEPLOYMENT_ENVIRONMENT': 'development', 'SESSION_COOKIE_SECURE': '${WORKCHORD_SESSION_COOKIE_SECURE:-true}', 'MCP_DNS_REBINDING_PROTECTION': 'true', 'MCP_ALLOWED_HOSTS': '${MCP_ALLOWED_HOSTS:-["localhost:*","127.0.0.1:*","[::1]:*"]}', 'MCP_ALLOWED_ORIGINS': '${MCP_ALLOWED_ORIGINS:-["http://localhost:*","http://127.0.0.1:*"]}', 'MCP_UNSAFE_ALLOW_PUBLIC_BINDING': 'false'}`

### delivery-worker

- **Environment:** `{'DATABASE_URL': '${DATABASE_RUNTIME_URL:?Set DATABASE_RUNTIME_URL}', 'DATABASE_SESSION_ROLE': ''}`

### frontend


### database-bootstrap

- **Image:** `postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296`
- **Volumes:** `./deploy/postgresql/init-server-roles.sh:/opt/workchord/init-server-roles.sh:ro`
- **Environment:** `{'PGHOST': 'postgres', 'PGPORT': '5432', 'PGDATABASE': 'workchord', 'PGUSER': 'postgres', 'PGPASSWORD': '${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}', 'WORKCHORD_MIGRATOR_PASSWORD': '${WORKCHORD_MIGRATOR_PASSWORD:?Set WORKCHORD_MIGRATOR_PASSWORD}', 'WORKCHORD_RUNTIME_PASSWORD': '${WORKCHORD_RUNTIME_PASSWORD:?Set WORKCHORD_RUNTIME_PASSWORD}', 'WORKCHORD_BACKUP_PASSWORD': '${WORKCHORD_BACKUP_PASSWORD:?Set WORKCHORD_BACKUP_PASSWORD}'}`
- **Depends on:** `{'postgres': {'condition': 'service_healthy'}}`
- **Command:** `['/opt/workchord/init-server-roles.sh']`

### database-security

- **Image:** `postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296`
- **Volumes:** `./deploy/postgresql/apply-server-security.sh:/opt/workchord/apply-server-security.sh:ro`, `./deploy/postgresql/apply-security.sql:/opt/workchord/apply-security.sql:ro`
- **Environment:** `{'PGHOST': 'postgres', 'PGPORT': '5432', 'PGDATABASE': 'workchord', 'PGUSER': 'postgres', 'PGPASSWORD': '${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}'}`
- **Depends on:** `{'migration': {'condition': 'service_completed_successfully'}}`
- **Command:** `['/opt/workchord/apply-server-security.sh']`

### openbao

- **Image:** `openbao/openbao:2.6.1@sha256:5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0`
- **Environment:** `{'BAO_ADDR': 'http://127.0.0.1:8200', 'BAO_DEV_LISTEN_ADDRESS': '0.0.0.0:8200', 'BAO_DEV_ROOT_TOKEN_ID': '${OPENBAO_DEV_ROOT_TOKEN:?Set OPENBAO_DEV_ROOT_TOKEN}'}`
- **Command:** `['server', '-dev']`

### openbao-bootstrap

- **Image:** `openbao/openbao:2.6.1@sha256:5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0`
- **Volumes:** `./deploy/autonomy/openbao-bootstrap.sh:/opt/workchord/openbao-bootstrap.sh:ro`, `./deploy/autonomy/openbao-acceptance-policy.hcl:/opt/workchord/openbao-acceptance-policy.hcl:ro`, `workchord_autonomy_runtime:/run/workchord-autonomy`, `${WORKCHORD_ACCEPTANCE_REPORT_DIR:?Set WORKCHORD_ACCEPTANCE_REPORT_DIR}:/var/lib/workchord/acceptance`
- **Environment:** `{'BAO_ADDR': 'http://openbao:8200', 'OPENBAO_DEV_ROOT_TOKEN': '${OPENBAO_DEV_ROOT_TOKEN:?Set OPENBAO_DEV_ROOT_TOKEN}', 'AUTONOMY_SIGNER_KEY': 'workchord-server-acceptance', 'AUTONOMY_SIGNER_TOKEN_FILE': '/run/workchord-autonomy/openbao-token', 'AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE': '/run/workchord-autonomy/openbao-signer-public-key.b64', 'AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_OUTPUT': '/var/lib/workchord/acceptance/trusted-signer-public-key.b64'}`
- **Depends on:** `{'openbao': {'condition': 'service_healthy'}}`

### minio

- **Image:** `minio/minio:RELEASE.2025-09-07T16-13-09Z@sha256:14cea493d9a34af32f524e538b8346cf79f3321eff8e708c1e2960462bd8936e`
- **Volumes:** `workchord_autonomy_minio:/data`
- **Environment:** `{'MINIO_ROOT_USER': '${MINIO_ROOT_USER:?Set MINIO_ROOT_USER}', 'MINIO_ROOT_PASSWORD': '${MINIO_ROOT_PASSWORD:?Set MINIO_ROOT_PASSWORD}'}`
- **Command:** `['server', '/data', '--console-address', ':9001']`

### minio-bootstrap

- **Image:** `minio/mc:RELEASE.2025-08-13T08-35-41Z@sha256:a7fe349ef4bd8521fb8497f55c6042871b2ae640607cf99d9bede5e9bdf11727`
- **Volumes:** `./deploy/autonomy/minio-bootstrap.sh:/opt/workchord/minio-bootstrap.sh:ro`, `./deploy/autonomy/minio-acceptance-policy.json:/opt/workchord/minio-acceptance-policy.json:ro`
- **Environment:** `{'MINIO_ROOT_USER': '${MINIO_ROOT_USER:?Set MINIO_ROOT_USER}', 'MINIO_ROOT_PASSWORD': '${MINIO_ROOT_PASSWORD:?Set MINIO_ROOT_PASSWORD}', 'AUTONOMY_MINIO_ACCESS_KEY': '${AUTONOMY_MINIO_ACCESS_KEY:?Set AUTONOMY_MINIO_ACCESS_KEY}', 'AUTONOMY_MINIO_SECRET_KEY': '${AUTONOMY_MINIO_SECRET_KEY:?Set AUTONOMY_MINIO_SECRET_KEY}', 'AUTONOMY_MINIO_ENDPOINT': 'http://minio:9000', 'AUTONOMY_MINIO_EVIDENCE_BUCKET': 'workchord-server-acceptance', 'AUTONOMY_MINIO_RETENTION': '${AUTONOMY_MINIO_RETENTION:-1d}'}`
- **Depends on:** `{'minio': {'condition': 'service_started'}}`

### valkey

- **Image:** `valkey/valkey:8.1.9-alpine@sha256:a038175878d66b9d274fbf8be73c0305e93798b83917647f167e18cef3c71eec`
- **Volumes:** `workchord_autonomy_valkey:/data`
- **Command:** `['valkey-server', '--appendonly', 'yes', '--appendfsync', 'everysec', '--save', '']`

### autonomy-acceptance

- **Volumes:** `workchord_autonomy_runtime:/run/workchord-autonomy:ro`, `${WORKCHORD_ACCEPTANCE_REPORT_DIR:?Set WORKCHORD_ACCEPTANCE_REPORT_DIR}:/var/lib/workchord/acceptance`
- **Environment:** `{'DEPLOYMENT_ENVIRONMENT': 'development', 'AUTONOMY_BACKEND_URL': 'http://backend:8001', 'AUTONOMY_GATEWAY_URL': 'http://frontend', 'AUTONOMY_SIGNER_URL': 'http://openbao:8200', 'AUTONOMY_SIGNER_TOKEN_FILE': '/run/workchord-autonomy/openbao-token', 'AUTONOMY_SIGNER_KEY': 'workchord-server-acceptance', 'AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE': '/run/workchord-autonomy/openbao-signer-public-key.b64', 'AUTONOMY_MINIO_ENDPOINT': 'http://minio:9000', 'AUTONOMY_MINIO_ACCESS_KEY': '${AUTONOMY_MINIO_ACCESS_KEY:?Set AUTONOMY_MINIO_ACCESS_KEY}', 'AUTONOMY_MINIO_SECRET_KEY': '${AUTONOMY_MINIO_SECRET_KEY:?Set AUTONOMY_MINIO_SECRET_KEY}', 'AUTONOMY_MINIO_EVIDENCE_BUCKET': 'workchord-server-acceptance', 'AUTONOMY_MINIO_REGION': 'us-east-1', 'AUTONOMY_VALKEY_HOST': 'valkey', 'AUTONOMY_VALKEY_PORT': '6379', 'AUTONOMY_ACCEPTANCE_TIMEOUT_SECONDS': '${AUTONOMY_ACCEPTANCE_TIMEOUT_SECONDS:-10}'}`
- **Depends on:** `{'backend': {'condition': 'service_healthy'}, 'delivery-worker': {'condition': 'service_started'}, 'openbao-bootstrap': {'condition': 'service_completed_successfully'}, 'minio-bootstrap': {'condition': 'service_completed_successfully'}, 'valkey': {'condition': 'service_healthy'}}`
- **Command:** `['workchord-server-acceptance', '--output', '/var/lib/workchord/acceptance/pending.json']`

## Networks

- `autonomy`

## Named Volumes

- `workchord_autonomy_minio`
- `workchord_autonomy_runtime`
- `workchord_autonomy_valkey`
- `workchord_server_data`

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
