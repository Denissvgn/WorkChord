"""Safety-fenced lifecycle management for disposable test databases."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import os
from pathlib import Path
import re
import tempfile
from typing import Iterator
from uuid import uuid4

from sqlalchemy.engine import URL, make_url


TEST_DATABASE_PREFIX = "workchord_test_"
TEST_DATABASE_PATTERN = re.compile(r"^workchord_test_[0-9a-f]{32}$")
TEST_RUNTIME_ROLE_PREFIX = "workchord_test_runtime_"
TEST_RUNTIME_ROLE_PATTERN = re.compile(
    r"^workchord_test_runtime_[0-9a-f]{32}$"
)
DEFAULT_POSTGRES_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", "postgres"})
ADMIN_DATABASES = frozenset({"postgres", "template1"})


class UnsafeDatabaseTarget(RuntimeError):
    """Raised before a fixture could touch a non-test database target."""


def _deployment_environment(explicit: str | None) -> str:
    return explicit or os.environ.get("DEPLOYMENT_ENVIRONMENT", "")


def assert_safe_test_database_url(
    database_url: str | URL,
    *,
    deployment_environment: str | None = None,
    allowed_postgres_hosts: frozenset[str] = DEFAULT_POSTGRES_HOSTS,
    allowed_sqlite_root: Path | None = None,
) -> URL:
    """Return a parsed URL only when it is unambiguously test-owned.

    PostgreSQL targets need a UUID-suffixed name on a local allowlisted host.
    SQLite targets must be in the operating-system temporary directory and use
    the same test prefix. An in-memory SQLite database is also safe.
    """

    if _deployment_environment(deployment_environment) != "test":
        raise UnsafeDatabaseTarget(
            "Destructive database fixtures require DEPLOYMENT_ENVIRONMENT=test"
        )

    url = make_url(database_url)
    backend = url.get_backend_name()
    database = url.database

    if backend == "postgresql":
        if url.host not in allowed_postgres_hosts:
            raise UnsafeDatabaseTarget(
                f"PostgreSQL test host {url.host!r} is not explicitly allowlisted"
            )
        if not database or TEST_DATABASE_PATTERN.fullmatch(database) is None:
            raise UnsafeDatabaseTarget(
                "PostgreSQL test databases must use workchord_test_<32 lowercase hex>"
            )
        return url

    if backend == "sqlite":
        if database in {None, "", ":memory:"}:
            return url
        database_path = Path(database).resolve()
        safe_root = (allowed_sqlite_root or Path(tempfile.gettempdir())).resolve()
        if not database_path.is_relative_to(safe_root):
            raise UnsafeDatabaseTarget(
                f"SQLite test database must resolve below {safe_root}"
            )
        if not database_path.name.startswith(TEST_DATABASE_PREFIX):
            raise UnsafeDatabaseTarget(
                f"SQLite test database filename must start with {TEST_DATABASE_PREFIX}"
            )
        return url

    raise UnsafeDatabaseTarget(f"Unsupported test database dialect: {backend}")


def _render(url: URL) -> str:
    return url.render_as_string(hide_password=False)


def _psycopg_render(url: URL) -> str:
    """Render a SQLAlchemy Psycopg URL as a libpq/Psycopg connection URL."""

    return url.set(drivername="postgresql").render_as_string(hide_password=False)


@dataclass(frozen=True)
class PostgresTestDatabase:
    """One uniquely named PostgreSQL database owned by a fixture."""

    name: str
    url: str
    encoding: str
    locale_provider: str
    locale: str
    collation_version: str
    timezone: str
    search_path: str
    migration_role: str
    runtime_role: str
    role_timezone: str
    role_search_path: str
    runtime_can_create_public: bool
    runtime_can_create_application_schema: bool
    default_table_privileges: tuple[str, ...]
    default_sequence_privileges: tuple[str, ...]


class PostgresTestDatabaseManager:
    """Create and drop isolated PostgreSQL databases through a local admin URL."""

    def __init__(
        self,
        admin_url: str,
        *,
        deployment_environment: str | None = None,
        allowed_hosts: frozenset[str] = DEFAULT_POSTGRES_HOSTS,
    ) -> None:
        self._deployment_environment = _deployment_environment(deployment_environment)
        if self._deployment_environment != "test":
            raise UnsafeDatabaseTarget(
                "PostgreSQL administration requires DEPLOYMENT_ENVIRONMENT=test"
            )
        self._admin_url = make_url(admin_url)
        if self._admin_url.get_backend_name() != "postgresql":
            raise UnsafeDatabaseTarget("POSTGRES_ADMIN_URL must be PostgreSQL")
        if self._admin_url.drivername not in {"postgresql+psycopg", "postgresql"}:
            raise UnsafeDatabaseTarget("POSTGRES_ADMIN_URL must use Psycopg 3")
        if self._admin_url.host not in allowed_hosts:
            raise UnsafeDatabaseTarget(
                f"PostgreSQL admin host {self._admin_url.host!r} is not allowlisted"
            )
        if self._admin_url.database not in ADMIN_DATABASES:
            raise UnsafeDatabaseTarget(
                "POSTGRES_ADMIN_URL must resolve to postgres or template1"
            )
        self._allowed_hosts = allowed_hosts
        self._created: set[str] = set()
        self._runtime_roles: dict[str, str] = {}

    def _target_url(self, name: str) -> URL:
        target = self._admin_url.set(drivername="postgresql+psycopg", database=name)
        return assert_safe_test_database_url(
            target,
            deployment_environment=self._deployment_environment,
            allowed_postgres_hosts=self._allowed_hosts,
        )

    def create(self) -> PostgresTestDatabase:
        """Create one empty contract-shaped database and return its facts."""

        import psycopg
        from psycopg import sql

        name = f"{TEST_DATABASE_PREFIX}{uuid4().hex}"
        runtime_role = f"{TEST_RUNTIME_ROLE_PREFIX}{uuid4().hex}"
        target_url = self._target_url(name)
        if TEST_RUNTIME_ROLE_PATTERN.fullmatch(runtime_role) is None:  # pragma: no cover
            raise UnsafeDatabaseTarget("Generated PostgreSQL test role is unsafe")
        self._runtime_roles[name] = runtime_role

        with psycopg.connect(
            _psycopg_render(self._admin_url), autocommit=True
        ) as connection:
            connection.execute(
                sql.SQL(
                    "CREATE DATABASE {} TEMPLATE template0 ENCODING 'UTF8' "
                    "LOCALE_PROVIDER builtin BUILTIN_LOCALE 'PG_UNICODE_FAST'"
                ).format(sql.Identifier(name))
            )

        try:
            with psycopg.connect(
                _psycopg_render(self._admin_url), autocommit=True
            ) as connection:
                connection.execute(
                    sql.SQL("CREATE ROLE {} NOLOGIN").format(
                        sql.Identifier(runtime_role)
                    )
                )
                connection.execute(
                    sql.SQL(
                        "ALTER ROLE {} IN DATABASE {} SET timezone TO 'UTC'"
                    ).format(
                        sql.Identifier(runtime_role),
                        sql.Identifier(name),
                    )
                )
                connection.execute(
                    sql.SQL(
                        "ALTER ROLE {} IN DATABASE {} SET search_path TO "
                        "workchord, pg_catalog"
                    ).format(
                        sql.Identifier(runtime_role),
                        sql.Identifier(name),
                    )
                )

            with psycopg.connect(
                _psycopg_render(target_url), autocommit=True
            ) as connection:
                migration_role = connection.execute(
                    "SELECT current_user"
                ).fetchone()[0]
                connection.execute("CREATE SCHEMA workchord")
                connection.execute("REVOKE CREATE ON SCHEMA public FROM PUBLIC")
                connection.execute(
                    sql.SQL("GRANT USAGE ON SCHEMA workchord TO {}").format(
                        sql.Identifier(runtime_role)
                    )
                )
                connection.execute(
                    sql.SQL(
                        "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA workchord "
                        "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {}"
                    ).format(
                        sql.Identifier(migration_role),
                        sql.Identifier(runtime_role),
                    )
                )
                connection.execute(
                    sql.SQL(
                        "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA workchord "
                        "GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO {}"
                    ).format(
                        sql.Identifier(migration_role),
                        sql.Identifier(runtime_role),
                    )
                )
                connection.execute(
                    sql.SQL("ALTER DATABASE {} SET timezone TO 'UTC'").format(
                        sql.Identifier(name)
                    )
                )
                connection.execute(
                    sql.SQL(
                        "ALTER DATABASE {} SET search_path TO workchord, pg_catalog"
                    ).format(sql.Identifier(name))
                )

            with psycopg.connect(
                _psycopg_render(target_url), autocommit=True
            ) as connection:
                row = connection.execute(
                    """
                    SELECT
                        pg_encoding_to_char(encoding),
                        datlocprovider,
                        datlocale,
                        datcollversion
                    FROM pg_database
                    WHERE datname = current_database()
                    """
                ).fetchone()
                timezone = connection.execute("SHOW timezone").fetchone()[0]
                search_path = connection.execute("SHOW search_path").fetchone()[0]
                role_settings = dict(
                    setting.split("=", 1)
                    for (setting,) in connection.execute(
                        """
                        SELECT unnest(settings.setconfig)
                        FROM pg_db_role_setting AS settings
                        JOIN pg_roles AS role ON role.oid = settings.setrole
                        JOIN pg_database AS database
                          ON database.oid = settings.setdatabase
                        WHERE role.rolname = %s AND database.datname = %s
                        """,
                        (runtime_role, name),
                    )
                )
                schema_privileges = connection.execute(
                    """
                    SELECT
                        has_schema_privilege(%s, 'public', 'CREATE'),
                        has_schema_privilege(%s, 'workchord', 'CREATE')
                    """,
                    (runtime_role, runtime_role),
                ).fetchone()
                default_privilege_rows = connection.execute(
                    """
                    SELECT defaults.defaclobjtype, expanded.privilege_type
                    FROM pg_default_acl AS defaults
                    JOIN pg_namespace AS namespace
                      ON namespace.oid = defaults.defaclnamespace
                    JOIN pg_roles AS owner ON owner.oid = defaults.defaclrole
                    CROSS JOIN LATERAL aclexplode(defaults.defaclacl) AS expanded
                    JOIN pg_roles AS grantee ON grantee.oid = expanded.grantee
                    WHERE namespace.nspname = 'workchord'
                      AND owner.rolname = %s
                      AND grantee.rolname = %s
                    ORDER BY defaults.defaclobjtype, expanded.privilege_type
                    """,
                    (migration_role, runtime_role),
                ).fetchall()

            if row != ("UTF8", "b", "PG_UNICODE_FAST", "1"):
                raise UnsafeDatabaseTarget(
                    f"PostgreSQL test database does not match the contract: {row!r}"
                )
            if timezone not in {"UTC", "Etc/UTC"}:
                raise UnsafeDatabaseTarget(
                    f"PostgreSQL test database timezone is not UTC: {timezone!r}"
                )
            if search_path.replace(" ", "") != "workchord,pg_catalog":
                raise UnsafeDatabaseTarget(
                    f"PostgreSQL test search_path is not contract-shaped: {search_path!r}"
                )
            normalized_role_settings = {
                key.lower(): value for key, value in role_settings.items()
            }
            role_timezone = normalized_role_settings.get("timezone", "")
            role_search_path = normalized_role_settings.get("search_path", "")
            if role_timezone not in {"UTC", "Etc/UTC"}:
                raise UnsafeDatabaseTarget(
                    "PostgreSQL test runtime role timezone is not UTC: "
                    f"{role_timezone!r}"
                )
            if role_search_path.replace(" ", "") != "workchord,pg_catalog":
                raise UnsafeDatabaseTarget(
                    "PostgreSQL test runtime role search_path is not contract-shaped: "
                    f"{role_search_path!r}"
                )
            if any(schema_privileges):
                raise UnsafeDatabaseTarget(
                    "PostgreSQL test runtime role can create in an application search path"
                )

            default_privileges: dict[str, list[str]] = {"r": [], "S": []}
            for object_type, privilege in default_privilege_rows:
                default_privileges.setdefault(object_type, []).append(privilege)
            default_table_privileges = tuple(default_privileges["r"])
            default_sequence_privileges = tuple(default_privileges["S"])
            if default_table_privileges != ("DELETE", "INSERT", "SELECT", "UPDATE"):
                raise UnsafeDatabaseTarget(
                    "PostgreSQL test table default privileges are not contract-shaped: "
                    f"{default_table_privileges!r}"
                )
            if default_sequence_privileges != ("SELECT", "UPDATE", "USAGE"):
                raise UnsafeDatabaseTarget(
                    "PostgreSQL test sequence default privileges are not contract-shaped: "
                    f"{default_sequence_privileges!r}"
                )
        except BaseException:
            self._drop_name(name)
            raise

        self._created.add(name)
        return PostgresTestDatabase(
            name=name,
            url=_render(target_url),
            encoding=row[0],
            locale_provider="builtin",
            locale=row[2],
            collation_version=row[3],
            timezone=timezone,
            search_path=search_path,
            migration_role=migration_role,
            runtime_role=runtime_role,
            role_timezone=role_timezone,
            role_search_path=role_search_path,
            runtime_can_create_public=bool(schema_privileges[0]),
            runtime_can_create_application_schema=bool(schema_privileges[1]),
            default_table_privileges=default_table_privileges,
            default_sequence_privileges=default_sequence_privileges,
        )

    def _drop_name(self, name: str) -> None:
        import psycopg
        from psycopg import sql

        self._target_url(name)
        runtime_role = self._runtime_roles.get(name)
        if runtime_role is not None and TEST_RUNTIME_ROLE_PATTERN.fullmatch(runtime_role) is None:
            raise UnsafeDatabaseTarget(
                f"PostgreSQL test role {runtime_role!r} is not safety-fenced"
            )
        with psycopg.connect(
            _psycopg_render(self._admin_url), autocommit=True
        ) as connection:
            connection.execute(
                sql.SQL("DROP DATABASE IF EXISTS {} WITH (FORCE)").format(
                    sql.Identifier(name)
                )
            )
            if runtime_role is not None:
                connection.execute(
                    sql.SQL("DROP ROLE IF EXISTS {}").format(
                        sql.Identifier(runtime_role)
                    )
                )
        self._created.discard(name)
        self._runtime_roles.pop(name, None)

    def drop(self, database: PostgresTestDatabase) -> None:
        """Drop one database previously returned by this manager."""

        if database.name not in self._created:
            raise UnsafeDatabaseTarget(
                f"Database {database.name!r} is not owned by this test manager"
            )
        self._drop_name(database.name)

    def cleanup(self) -> None:
        """Best-effort deterministic cleanup for every database still owned."""

        failures: list[BaseException] = []
        for name in sorted(self._created):
            try:
                self._drop_name(name)
            except BaseException as exc:  # pragma: no cover - requires server loss
                failures.append(exc)
        if failures:
            raise RuntimeError(
                f"Failed to clean {len(failures)} PostgreSQL test database(s)"
            ) from failures[0]

    @contextmanager
    def database(self) -> Iterator[PostgresTestDatabase]:
        """Create and always drop one database around a test block."""

        database = self.create()
        try:
            yield database
        finally:
            if database.name in self._created:
                self.drop(database)
