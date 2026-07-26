#!/bin/bash
set -Eeuo pipefail

: "${WORKCHORD_MIGRATOR_PASSWORD:?WORKCHORD_MIGRATOR_PASSWORD is required}"
: "${WORKCHORD_RUNTIME_PASSWORD:?WORKCHORD_RUNTIME_PASSWORD is required}"
: "${WORKCHORD_BACKUP_PASSWORD:?WORKCHORD_BACKUP_PASSWORD is required}"
: "${POSTGRES_USER:=${PGUSER:-postgres}}"
: "${POSTGRES_DB:=${PGDATABASE:-workchord}}"

psql \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    -v ON_ERROR_STOP=1 <<'SQL'
\getenv migrator_password WORKCHORD_MIGRATOR_PASSWORD
\getenv runtime_password WORKCHORD_RUNTIME_PASSWORD
\getenv backup_password WORKCHORD_BACKUP_PASSWORD

SELECT 'CREATE ROLE workchord_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'workchord_owner')
\gexec
SELECT 'CREATE ROLE workchord_migrator LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'workchord_migrator')
\gexec
SELECT 'CREATE ROLE workchord_runtime LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'workchord_runtime')
\gexec
SELECT 'CREATE ROLE workchord_readonly NOLOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'workchord_readonly')
\gexec
SELECT 'CREATE ROLE workchord_backup LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE REPLICATION NOBYPASSRLS'
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'workchord_backup')
\gexec

ALTER ROLE workchord_owner NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
ALTER ROLE workchord_migrator LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
ALTER ROLE workchord_runtime LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
ALTER ROLE workchord_readonly NOLOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
ALTER ROLE workchord_backup LOGIN NOINHERIT NOSUPERUSER NOCREATEDB NOCREATEROLE REPLICATION NOBYPASSRLS;

SELECT format(
    'ALTER ROLE workchord_migrator PASSWORD %L',
    :'migrator_password'
)
\gexec
SELECT format(
    'ALTER ROLE workchord_runtime PASSWORD %L',
    :'runtime_password'
)
\gexec
SELECT format(
    'ALTER ROLE workchord_backup PASSWORD %L',
    :'backup_password'
)
\gexec

CREATE SCHEMA IF NOT EXISTS workchord AUTHORIZATION workchord_owner;
ALTER SCHEMA workchord OWNER TO workchord_owner;

-- A server volume may predate the split service roles. Transfer only objects
-- inside WorkChord's application schema so owner-session migrations can
-- continue without granting the migrator superuser privileges.
SELECT format(
    'ALTER %s %I.%I OWNER TO workchord_owner',
    CASE object.relkind
        WHEN 'r' THEN 'TABLE'
        WHEN 'p' THEN 'TABLE'
        WHEN 'S' THEN 'SEQUENCE'
        WHEN 'v' THEN 'VIEW'
        WHEN 'm' THEN 'MATERIALIZED VIEW'
        WHEN 'f' THEN 'FOREIGN TABLE'
    END,
    object.schema_name,
    object.object_name
)
FROM (
    SELECT class.relkind,
           namespace.nspname AS schema_name,
           class.relname AS object_name
    FROM pg_class AS class
    JOIN pg_namespace AS namespace ON namespace.oid = class.relnamespace
    WHERE namespace.nspname = 'workchord'
      AND class.relkind IN ('r', 'p', 'S', 'v', 'm', 'f')
      AND class.relowner <> (SELECT oid FROM pg_roles WHERE rolname = 'workchord_owner')
    ORDER BY
        CASE WHEN class.relkind = 'S' THEN 1 ELSE 0 END,
        class.relname
) AS object
\gexec

SELECT format(
    'ALTER ROUTINE %I.%I(%s) OWNER TO workchord_owner',
    namespace.nspname,
    procedure.proname,
    pg_get_function_identity_arguments(procedure.oid)
)
FROM pg_proc AS procedure
JOIN pg_namespace AS namespace ON namespace.oid = procedure.pronamespace
WHERE namespace.nspname = 'workchord'
  AND procedure.proowner <> (SELECT oid FROM pg_roles WHERE rolname = 'workchord_owner')
ORDER BY procedure.proname, procedure.oid
\gexec

GRANT workchord_owner TO workchord_migrator;
GRANT USAGE ON SCHEMA workchord TO workchord_runtime;

ALTER DEFAULT PRIVILEGES FOR ROLE workchord_owner IN SCHEMA workchord
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO workchord_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE workchord_owner IN SCHEMA workchord
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO workchord_runtime;
SQL
