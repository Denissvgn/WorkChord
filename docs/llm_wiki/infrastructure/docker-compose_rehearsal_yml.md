# docker-compose.rehearsal.yml

**Path:** `docker-compose.rehearsal.yml`

## Services

| Service | Image / Build | Ports | Depends On |
|---------|---------------|-------|------------|
| `backend` | — |  |  |
| `delivery-worker` | — |  |  |
| `frontend` | — | `8080:80` |  |

### backend

- **Environment:** `{'MAINTENANCE_REPLICA_ID': 'auto'}`

### delivery-worker

- **Environment:** `{'MAINTENANCE_REPLICA_ID': 'auto'}`

### frontend

- **Ports:** `8080:80`

## Notes

_Add reviewed operational context here; generated sections are replaced from source observations._
