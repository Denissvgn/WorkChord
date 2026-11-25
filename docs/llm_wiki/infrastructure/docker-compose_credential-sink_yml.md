# docker-compose.credential-sink.yml

**Path:** `docker-compose.credential-sink.yml`

## Services

| Service | Image / Build | Ports | Depends On |
|---------|---------------|-------|------------|
| `backend` | — |  |  |

### backend

- **Volumes:** `{'type': 'bind', 'source': '${WORKCHORD_CREDENTIAL_SINK_HOST_DIR:?Set WORKCHORD_CREDENTIAL_SINK_HOST_DIR}', 'target': '/run/workchord/credential-sink'}`
- **Environment:** `{'AGENT_TEAM_CREDENTIAL_SINK_DIR': '/run/workchord/credential-sink'}`

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
