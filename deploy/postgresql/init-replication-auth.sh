#!/usr/bin/env bash
set -euo pipefail

# Development/rehearsal only. The Compose network and loopback host bind are
# the network boundary; SCRAM still authenticates the pg_basebackup user.
printf '%s\n' 'host replication all all scram-sha-256' >> "${PGDATA}/pg_hba.conf"
