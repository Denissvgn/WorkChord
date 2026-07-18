\set ON_ERROR_STOP on

ALTER DATABASE workchord SET timezone TO 'UTC';
ALTER DATABASE workchord SET search_path TO workchord, pg_catalog;

CREATE SCHEMA IF NOT EXISTS workchord AUTHORIZATION postgres;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA workchord FROM PUBLIC;

ALTER ROLE postgres IN DATABASE workchord SET timezone TO 'UTC';
ALTER ROLE postgres IN DATABASE workchord SET search_path TO workchord, pg_catalog;
