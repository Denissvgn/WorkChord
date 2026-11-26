# docker-compose.server.yml

**Path:** `docker-compose.server.yml`

## Services

| Service | Image / Build | Ports | Depends On |
|---------|---------------|-------|------------|
| `postgres` | — |  |  |
| `migration` | build: `.` |  | `{'database-bootstrap': {'condition': 'service_completed_successfully'}}` |
| `repair` | build: `.` |  | `{'database-security': {'condition': 'service_completed_successfully'}}` |
| `backend` | build: `.` |  |  |
| `delivery-worker` | build: `.` |  |  |
| `frontend` | build: `.` |  |  |
| `database-bootstrap` | `postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296` |  | `{'postgres': {'condition': 'service_healthy'}}` |
| `database-security` | `postgres:18.4-bookworm@sha256:1961f96e6029a02c3812d7cb329a3b03a3ac2bb067058dec17b0f5596aca9296` |  | `{'migration': {'condition': 'service_completed_successfully'}}` |
| `openbao` | `openbao/openbao:2.6.1@sha256:5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0` |  |  |
| `openbao-bootstrap` | `openbao/openbao:2.6.1@sha256:5b2486ab0fb90bbc788cc345b0a08616dfb375873ee8be5df3a2fd4d378a67e0` |  | `{'openbao': {'condition': 'service_healthy'}}` |
| `evidence-store` | `versity/versitygw:v1.11.0@sha256:8319a530d08d537426e2f855bae5280709795dc73a3f0c347973ef915d6343c5` |  |  |
| `evidence-store-accounts` | `versity/versitygw:v1.11.0@sha256:8319a530d08d537426e2f855bae5280709795dc73a3f0c347973ef915d6343c5` |  | `{'evidence-store': {'condition': 'service_healthy'}}` |
| `evidence-store-bootstrap` | `amazon/aws-cli:2.42.3@sha256:271de464e935f765aa2afb6ec69881e9f4a9afd3e978214a2b5f5ddcbbc161b5` |  | `{'evidence-store-accounts': {'condition': 'service_completed_successfully'}}` |
| `valkey` | `valkey/valkey:8.1.9-alpine@sha256:a038175878d66b9d274fbf8be73c0305e93798b83917647f167e18cef3c71eec` |  |  |
| `autonomy-acceptance` | build: `.` |  | `{'backend': {'condition': 'service_healthy'}, 'delivery-worker': {'condition': 'service_started'}, 'openbao-bootstrap': {'condition': 'service_completed_successfully'}, 'evidence-store-bootstrap': {'condition': 'service_completed_successfully'}, 'valkey': {'condition': 'service_healthy'}}` |

### postgres

- **Volumes:** `./deploy/postgresql/init-server-roles.sh:/docker-entrypoint-initdb.d/15-server-roles.sh:ro`
- **Environment:** `{'WORKCHORD_MIGRATOR_PASSWORD': '${WORKCHORD_MIGRATOR_PASSWORD:?Set WORKCHORD_MIGRATOR_PASSWORD}', 'WORKCHORD_RUNTIME_PASSWORD': '${WORKCHORD_RUNTIME_PASSWORD:?Set WORKCHORD_RUNTIME_PASSWORD}', 'WORKCHORD_BACKUP_PASSWORD': '${WORKCHORD_BACKUP_PASSWORD:?Set WORKCHORD_BACKUP_PASSWORD}'}`

### migration

- **Build context:** `.`
- **Image:** `${WORKCHORD_IMAGE_PREFIX:-workchord}-backend:${WORKCHORD_SOURCE_REVISION:?Set WORKCHORD_SOURCE_REVISION}`
- **Environment:** `{'DATABASE_URL': '${DATABASE_MIGRATION_URL:?Set DATABASE_MIGRATION_URL}', 'DATABASE_SESSION_ROLE': 'workchord_owner'}`
- **Depends on:** `{'database-bootstrap': {'condition': 'service_completed_successfully'}}`

### repair

- **Build context:** `.`
- **Image:** `${WORKCHORD_IMAGE_PREFIX:-workchord}-backend:${WORKCHORD_SOURCE_REVISION:?Set WORKCHORD_SOURCE_REVISION}`
- **Environment:** `{'DATABASE_URL': '${DATABASE_MIGRATION_URL:?Set DATABASE_MIGRATION_URL}', 'DATABASE_SESSION_ROLE': 'workchord_owner'}`
- **Depends on:** `{'database-security': {'condition': 'service_completed_successfully'}}`

### backend

- **Build context:** `.`
- **Image:** `${WORKCHORD_IMAGE_PREFIX:-workchord}-backend:${WORKCHORD_SOURCE_REVISION:?Set WORKCHORD_SOURCE_REVISION}`
- **Volumes:** `workchord_server_data:/app/data`
- **Environment:** `{'DATABASE_URL': '${DATABASE_RUNTIME_URL:?Set DATABASE_RUNTIME_URL}', 'DATABASE_SESSION_ROLE': '', 'DEPLOYMENT_ENVIRONMENT': 'development', 'SESSION_COOKIE_SECURE': '${WORKCHORD_SESSION_COOKIE_SECURE:-true}', 'MCP_DNS_REBINDING_PROTECTION': 'true', 'MCP_ALLOWED_HOSTS': '${MCP_ALLOWED_HOSTS:-["localhost:*","127.0.0.1:*","[::1]:*"]}', 'MCP_ALLOWED_ORIGINS': '${MCP_ALLOWED_ORIGINS:-["http://localhost:*","http://127.0.0.1:*"]}', 'MCP_UNSAFE_ALLOW_PUBLIC_BINDING': 'false', 'READINESS_DETAIL_TOKEN': '${WORKCHORD_READINESS_DETAIL_TOKEN:?Set WORKCHORD_READINESS_DETAIL_TOKEN}'}`

### delivery-worker

- **Build context:** `.`
- **Image:** `${WORKCHORD_IMAGE_PREFIX:-workchord}-backend:${WORKCHORD_SOURCE_REVISION:?Set WORKCHORD_SOURCE_REVISION}`
- **Environment:** `{'DATABASE_URL': '${DATABASE_RUNTIME_URL:?Set DATABASE_RUNTIME_URL}', 'DATABASE_SESSION_ROLE': ''}`

### frontend

- **Build context:** `.`
- **Image:** `${WORKCHORD_IMAGE_PREFIX:-workchord}-frontend:${WORKCHORD_SOURCE_REVISION:?Set WORKCHORD_SOURCE_REVISION}`

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

### evidence-store

- **Image:** `versity/versitygw:v1.11.0@sha256:8319a530d08d537426e2f855bae5280709795dc73a3f0c347973ef915d6343c5`
- **Volumes:** `workchord_autonomy_evidence:/data`
- **Environment:** `{'ROOT_ACCESS_KEY': '${EVIDENCE_STORE_ROOT_ACCESS_KEY:?Set EVIDENCE_STORE_ROOT_ACCESS_KEY}', 'ROOT_SECRET_KEY': '${EVIDENCE_STORE_ROOT_SECRET_KEY:?Set EVIDENCE_STORE_ROOT_SECRET_KEY}'}`
- **Command:** `['mkdir -p /data/buckets /data/versions /data/iam && exec versitygw --port :7070 --health /health --iam-dir /data/iam --quiet posix --versioning-dir /data/versions --fsync /data/buckets']`

### evidence-store-accounts

- **Image:** `versity/versitygw:v1.11.0@sha256:8319a530d08d537426e2f855bae5280709795dc73a3f0c347973ef915d6343c5`
- **Volumes:** `./deploy/autonomy/evidence-store-accounts.sh:/opt/workchord/evidence-store-accounts.sh:ro`
- **Environment:** `{'EVIDENCE_STORE_ROOT_ACCESS_KEY': '${EVIDENCE_STORE_ROOT_ACCESS_KEY:?Set EVIDENCE_STORE_ROOT_ACCESS_KEY}', 'EVIDENCE_STORE_ROOT_SECRET_KEY': '${EVIDENCE_STORE_ROOT_SECRET_KEY:?Set EVIDENCE_STORE_ROOT_SECRET_KEY}', 'AUTONOMY_EVIDENCE_ACCESS_KEY': '${AUTONOMY_EVIDENCE_ACCESS_KEY:?Set AUTONOMY_EVIDENCE_ACCESS_KEY}', 'AUTONOMY_EVIDENCE_SECRET_KEY': '${AUTONOMY_EVIDENCE_SECRET_KEY:?Set AUTONOMY_EVIDENCE_SECRET_KEY}', 'AUTONOMY_EVIDENCE_ENDPOINT': 'http://evidence-store:7070'}`
- **Depends on:** `{'evidence-store': {'condition': 'service_healthy'}}`

### evidence-store-bootstrap

- **Image:** `amazon/aws-cli:2.42.3@sha256:271de464e935f765aa2afb6ec69881e9f4a9afd3e978214a2b5f5ddcbbc161b5`
- **Volumes:** `./deploy/autonomy/evidence-store-bootstrap.sh:/opt/workchord/evidence-store-bootstrap.sh:ro`, `./deploy/autonomy/evidence-store-acceptance-policy.json:/opt/workchord/evidence-store-acceptance-policy.json:ro`
- **Environment:** `{'EVIDENCE_STORE_ROOT_ACCESS_KEY': '${EVIDENCE_STORE_ROOT_ACCESS_KEY:?Set EVIDENCE_STORE_ROOT_ACCESS_KEY}', 'EVIDENCE_STORE_ROOT_SECRET_KEY': '${EVIDENCE_STORE_ROOT_SECRET_KEY:?Set EVIDENCE_STORE_ROOT_SECRET_KEY}', 'AUTONOMY_EVIDENCE_ACCESS_KEY': '${AUTONOMY_EVIDENCE_ACCESS_KEY:?Set AUTONOMY_EVIDENCE_ACCESS_KEY}', 'AUTONOMY_EVIDENCE_ENDPOINT': 'http://evidence-store:7070', 'AUTONOMY_EVIDENCE_BUCKET': 'workchord-server-acceptance', 'AUTONOMY_EVIDENCE_REGION': 'us-east-1', 'AUTONOMY_EVIDENCE_RETENTION_DAYS': '${AUTONOMY_EVIDENCE_RETENTION_DAYS:-1}', 'AWS_CONFIG_FILE': '/dev/null', 'AWS_SHARED_CREDENTIALS_FILE': '/dev/null', 'AWS_EC2_METADATA_DISABLED': 'true', 'AWS_PAGER': ''}`
- **Depends on:** `{'evidence-store-accounts': {'condition': 'service_completed_successfully'}}`

### valkey

- **Image:** `valkey/valkey:8.1.9-alpine@sha256:a038175878d66b9d274fbf8be73c0305e93798b83917647f167e18cef3c71eec`
- **Volumes:** `workchord_autonomy_valkey:/data`
- **Command:** `['valkey-server', '--appendonly', 'yes', '--appendfsync', 'everysec', '--save', '']`

### autonomy-acceptance

- **Build context:** `.`
- **Image:** `${WORKCHORD_IMAGE_PREFIX:-workchord}-backend:${WORKCHORD_SOURCE_REVISION:?Set WORKCHORD_SOURCE_REVISION}`
- **Volumes:** `workchord_autonomy_runtime:/run/workchord-autonomy:ro`, `${WORKCHORD_ACCEPTANCE_REPORT_DIR:?Set WORKCHORD_ACCEPTANCE_REPORT_DIR}:/var/lib/workchord/acceptance`
- **Environment:** `{'DEPLOYMENT_ENVIRONMENT': 'development', 'AUTONOMY_BACKEND_URL': 'http://backend:8001', 'AUTONOMY_READINESS_DETAIL_TOKEN': '${WORKCHORD_READINESS_DETAIL_TOKEN:?Set WORKCHORD_READINESS_DETAIL_TOKEN}', 'AUTONOMY_GATEWAY_URL': 'http://frontend', 'AUTONOMY_SIGNER_URL': 'http://openbao:8200', 'AUTONOMY_SIGNER_TOKEN_FILE': '/run/workchord-autonomy/openbao-token', 'AUTONOMY_SIGNER_KEY': 'workchord-server-acceptance', 'AUTONOMY_TRUSTED_SIGNER_PUBLIC_KEY_FILE': '/run/workchord-autonomy/openbao-signer-public-key.b64', 'AUTONOMY_EVIDENCE_ENDPOINT': 'http://evidence-store:7070', 'AUTONOMY_EVIDENCE_ACCESS_KEY': '${AUTONOMY_EVIDENCE_ACCESS_KEY:?Set AUTONOMY_EVIDENCE_ACCESS_KEY}', 'AUTONOMY_EVIDENCE_SECRET_KEY': '${AUTONOMY_EVIDENCE_SECRET_KEY:?Set AUTONOMY_EVIDENCE_SECRET_KEY}', 'AUTONOMY_EVIDENCE_BUCKET': 'workchord-server-acceptance', 'AUTONOMY_EVIDENCE_REGION': 'us-east-1', 'AUTONOMY_VALKEY_HOST': 'valkey', 'AUTONOMY_VALKEY_PORT': '6379', 'AUTONOMY_ACCEPTANCE_TIMEOUT_SECONDS': '${AUTONOMY_ACCEPTANCE_TIMEOUT_SECONDS:-10}'}`
- **Depends on:** `{'backend': {'condition': 'service_healthy'}, 'delivery-worker': {'condition': 'service_started'}, 'openbao-bootstrap': {'condition': 'service_completed_successfully'}, 'evidence-store-bootstrap': {'condition': 'service_completed_successfully'}, 'valkey': {'condition': 'service_healthy'}}`
- **Command:** `['workchord-server-acceptance', '--output', '/var/lib/workchord/acceptance/pending.json']`

## Networks

- `autonomy`

## Named Volumes

- `workchord_autonomy_evidence`
- `workchord_autonomy_runtime`
- `workchord_autonomy_valkey`
- `workchord_server_data`

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
