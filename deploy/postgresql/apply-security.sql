\set ON_ERROR_STOP on

\if :{?owner_role}
\else
  \echo 'owner_role psql variable is required'
  \quit 2
\endif
\if :{?migrator_role}
\else
  \echo 'migrator_role psql variable is required'
  \quit 2
\endif
\if :{?runtime_role}
\else
  \echo 'runtime_role psql variable is required'
  \quit 2
\endif
\if :{?readonly_role}
\else
  \echo 'readonly_role psql variable is required'
  \quit 2
\endif
\if :{?backup_role}
\else
  \echo 'backup_role psql variable is required'
  \quit 2
\endif

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA workchord FROM PUBLIC;

SELECT format('ALTER SCHEMA workchord OWNER TO %I', :'owner_role') \gexec
SELECT format('GRANT %I TO %I', :'owner_role', :'migrator_role') \gexec
SELECT format('GRANT USAGE ON SCHEMA workchord TO %I', :'runtime_role') \gexec
SELECT format('GRANT USAGE ON SCHEMA workchord TO %I', :'readonly_role') \gexec
SELECT format('GRANT USAGE ON SCHEMA workchord TO %I', :'backup_role') \gexec

SELECT format(
  'GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA workchord TO %I',
  :'runtime_role'
) \gexec
SELECT format(
  'GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA workchord TO %I',
  :'runtime_role'
) \gexec
SELECT format(
  'REVOKE INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER '
  'ON TABLE workchord.alembic_version, workchord.database_migration_gates FROM %I',
  :'runtime_role'
) \gexec
SELECT format(
  'GRANT SELECT ON TABLE workchord.alembic_version, '
  'workchord.database_migration_gates TO %I',
  :'runtime_role'
) \gexec
SELECT format('GRANT SELECT ON ALL TABLES IN SCHEMA workchord TO %I', :'readonly_role') \gexec
SELECT format('GRANT SELECT ON ALL TABLES IN SCHEMA workchord TO %I', :'backup_role') \gexec
SELECT format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA workchord TO %I', :'backup_role') \gexec

SELECT format(
  'ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA workchord '
  'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO %I',
  :'owner_role', :'runtime_role'
) \gexec
SELECT format(
  'ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA workchord '
  'GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO %I',
  :'owner_role', :'runtime_role'
) \gexec
SELECT format(
  'ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA workchord '
  'GRANT SELECT ON TABLES TO %I',
  :'owner_role', :'readonly_role'
) \gexec
SELECT format(
  'ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA workchord '
  'GRANT SELECT ON TABLES TO %I',
  :'owner_role', :'backup_role'
) \gexec

SELECT format('REVOKE CREATE ON SCHEMA workchord FROM %I', :'runtime_role') \gexec
SELECT format('REVOKE CREATE ON SCHEMA public FROM %I', :'runtime_role') \gexec
SELECT format('REVOKE %I FROM %I', :'owner_role', :'runtime_role') \gexec

SELECT format(
  'ALTER ROLE %I IN DATABASE %I SET timezone TO ''UTC''',
  role_name, current_database()
) FROM (
  VALUES (:'owner_role'), (:'migrator_role'), (:'runtime_role'),
         (:'readonly_role'), (:'backup_role')
) AS roles(role_name) \gexec
SELECT format(
  'ALTER ROLE %I IN DATABASE %I SET search_path TO workchord, pg_catalog',
  role_name, current_database()
) FROM (
  VALUES (:'owner_role'), (:'migrator_role'), (:'runtime_role'),
         (:'readonly_role'), (:'backup_role')
) AS roles(role_name) \gexec
