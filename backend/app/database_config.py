"""Driver-neutral database URL, connection, and engine configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Mapping

from sqlalchemy.engine import URL, make_url


POSTGRESQL_DRIVER = "postgresql+psycopg"
SQLITE_ASYNC_DRIVER = "sqlite+aiosqlite"
SQLITE_SYNC_DRIVER = "sqlite"

_POSTGRESQL_CONNECTION_QUERY_KEYS = frozenset(
    {
        "application_name",
        "connect_timeout",
        "options",
        "sslcert",
        "sslkey",
        "sslmode",
        "sslrootcert",
    }
)
_SENSITIVE_QUERY_PARTS = ("key", "password", "secret", "token")
_APPLICATION_NAME_PATTERN = re.compile(r"[A-Za-z0-9_.:-]{1,64}")
_PROCESS_CONNECTION_BUDGETS = {
    "web": 20,
    "delivery_worker": 10,
}


class DatabaseConfigurationError(ValueError):
    """Raised when database settings are unsupported or unsafe."""


@dataclass(frozen=True)
class DatabaseConfiguration:
    """Validated, dialect-specific database configuration."""

    async_url: URL
    sync_url: URL
    backend: str
    redacted_url: str
    process_role: str
    approved_connection_capacity: int
    connect_args: Mapping[str, Any]
    pool_size: int | None
    max_overflow: int | None
    pool_timeout_seconds: float | None
    pool_recycle_seconds: int
    pool_pre_ping: bool

    @property
    def bounded_connection_capacity(self) -> int | None:
        if self.pool_size is None or self.max_overflow is None:
            return None
        return self.pool_size + self.max_overflow

    def async_engine_kwargs(self, *, echo: bool = False) -> dict[str, Any]:
        options: dict[str, Any] = {
            "connect_args": dict(self.connect_args),
            "echo": echo,
            "pool_pre_ping": self.pool_pre_ping,
            "pool_recycle": self.pool_recycle_seconds,
        }
        if self.backend == "postgresql":
            options.update(
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_timeout=self.pool_timeout_seconds,
            )
        return options

    def summary(self) -> dict[str, Any]:
        """Return observable connection policy without credentials."""

        return {
            "backend": self.backend,
            "url": self.redacted_url,
            "process_role": self.process_role,
            "approved_connection_capacity": self.approved_connection_capacity,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "bounded_connection_capacity": self.bounded_connection_capacity,
            "pool_timeout_seconds": self.pool_timeout_seconds,
            "pool_recycle_seconds": self.pool_recycle_seconds,
            "pool_pre_ping": self.pool_pre_ping,
        }


def _settings_value(settings: Any, name: str) -> Any:
    try:
        return getattr(settings, name)
    except AttributeError as exc:  # pragma: no cover - developer integration guard
        raise DatabaseConfigurationError(
            f"Database settings object is missing {name}"
        ) from exc


def _certificate_path(value: str, *, setting_name: str) -> str:
    if not value:
        return ""
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise DatabaseConfigurationError(f"{setting_name} must be an absolute path")
    if not path.is_file():
        raise DatabaseConfigurationError(f"{setting_name} must name a readable file")
    return str(path)


def redact_database_url(value: str | URL) -> str:
    """Render a URL without exposing passwords or secret query values."""

    url = make_url(value) if isinstance(value, str) else value
    redacted_query: dict[str, str | tuple[str, ...]] = {}
    for key, query_value in url.query.items():
        if any(part in key.lower() for part in _SENSITIVE_QUERY_PARTS):
            redacted_query[key] = "***"
        else:
            redacted_query[key] = query_value
    return url.set(query=redacted_query).render_as_string(hide_password=True)


def alembic_safe_url(value: str | URL) -> str:
    """Render a URL for Alembic ConfigParser without percent interpolation."""

    url = make_url(value) if isinstance(value, str) else value
    return url.render_as_string(hide_password=False).replace("%", "%%")


def parse_database_configuration(settings: Any) -> DatabaseConfiguration:
    """Validate settings and build driver-specific runtime/migration URLs."""

    try:
        async_url = make_url(str(_settings_value(settings, "database_url")))
    except Exception as exc:
        raise DatabaseConfigurationError("DATABASE_URL is not a valid SQLAlchemy URL") from exc

    application_name = str(
        _settings_value(settings, "database_application_name")
    ).strip()
    if _APPLICATION_NAME_PATTERN.fullmatch(application_name) is None:
        raise DatabaseConfigurationError(
            "DATABASE_APPLICATION_NAME must contain 1-64 safe identifier characters"
        )

    pool_size = int(_settings_value(settings, "database_pool_size"))
    max_overflow = int(_settings_value(settings, "database_max_overflow"))
    process_role = str(_settings_value(settings, "database_process_role"))
    try:
        approved_connection_capacity = _PROCESS_CONNECTION_BUDGETS[process_role]
    except KeyError as exc:
        raise DatabaseConfigurationError(
            "DATABASE_PROCESS_ROLE must be web or delivery_worker"
        ) from exc
    if pool_size + max_overflow > approved_connection_capacity:
        raise DatabaseConfigurationError(
            "Configured database pool exceeds the approved "
            f"{process_role} process budget of {approved_connection_capacity}"
        )
    pool_timeout = float(
        _settings_value(settings, "database_pool_timeout_seconds")
    )
    pool_recycle = int(
        _settings_value(settings, "database_pool_recycle_seconds")
    )
    pool_pre_ping = bool(_settings_value(settings, "database_pool_pre_ping"))
    connect_timeout = int(
        _settings_value(settings, "database_connect_timeout_seconds")
    )

    backend = async_url.get_backend_name()
    environment = str(_settings_value(settings, "deployment_environment"))
    postgresql_required = bool(
        _settings_value(settings, "database_postgresql_required")
    )

    if backend == "sqlite":
        if async_url.drivername != SQLITE_ASYNC_DRIVER:
            raise DatabaseConfigurationError(
                f"SQLite DATABASE_URL runtime URLs must use {SQLITE_ASYNC_DRIVER}"
            )
        if async_url.query:
            raise DatabaseConfigurationError(
                "SQLite DATABASE_URL query parameters are not supported; use database settings"
            )
        if environment == "production":
            if postgresql_required:
                raise DatabaseConfigurationError(
                    "Production SQLite is disabled by DATABASE_POSTGRESQL_REQUIRED"
                )
            database = async_url.database
            if not database or database == ":memory:":
                raise DatabaseConfigurationError(
                    "Production SQLite requires a persistent database under /app/data"
                )
            database_path = Path(database)
            data_root = Path("/app/data")
            resolved = database_path.resolve()
            if (
                not database_path.is_absolute()
                or resolved == data_root
                or not resolved.is_relative_to(data_root)
            ):
                raise DatabaseConfigurationError(
                    "Production SQLite DATABASE_URL must resolve inside /app/data"
                )
        return DatabaseConfiguration(
            async_url=async_url,
            sync_url=async_url.set(drivername=SQLITE_SYNC_DRIVER),
            backend="sqlite",
            redacted_url=redact_database_url(async_url),
            process_role=process_role,
            approved_connection_capacity=approved_connection_capacity,
            connect_args={"timeout": float(connect_timeout)},
            pool_size=None,
            max_overflow=None,
            pool_timeout_seconds=None,
            pool_recycle_seconds=pool_recycle,
            pool_pre_ping=pool_pre_ping,
        )

    if backend != "postgresql" or async_url.drivername != POSTGRESQL_DRIVER:
        raise DatabaseConfigurationError(
            "DATABASE_URL must use sqlite+aiosqlite or postgresql+psycopg"
        )
    if not async_url.database:
        raise DatabaseConfigurationError("PostgreSQL DATABASE_URL must name a database")
    if environment == "production" and (not async_url.host or not async_url.username):
        raise DatabaseConfigurationError(
            "Production PostgreSQL requires an explicit host and username"
        )

    conflicting_query = _POSTGRESQL_CONNECTION_QUERY_KEYS.intersection(async_url.query)
    if conflicting_query:
        names = ", ".join(sorted(conflicting_query))
        raise DatabaseConfigurationError(
            f"Configure PostgreSQL connection policy with DATABASE_* settings, not URL keys: {names}"
        )

    ssl_mode = str(_settings_value(settings, "database_ssl_mode"))
    ssl_root_cert = _certificate_path(
        str(_settings_value(settings, "database_ssl_root_cert")),
        setting_name="DATABASE_SSL_ROOT_CERT",
    )
    ssl_cert = _certificate_path(
        str(_settings_value(settings, "database_ssl_cert")),
        setting_name="DATABASE_SSL_CERT",
    )
    ssl_key = _certificate_path(
        str(_settings_value(settings, "database_ssl_key")),
        setting_name="DATABASE_SSL_KEY",
    )

    if bool(ssl_cert) != bool(ssl_key):
        raise DatabaseConfigurationError(
            "DATABASE_SSL_CERT and DATABASE_SSL_KEY must be configured together"
        )
    if ssl_mode in {"verify-ca", "verify-full"} and not ssl_root_cert:
        raise DatabaseConfigurationError(
            f"DATABASE_SSL_ROOT_CERT is required for sslmode={ssl_mode}"
        )
    if ssl_mode == "disable" and (ssl_root_cert or ssl_cert or ssl_key):
        raise DatabaseConfigurationError(
            "TLS certificate settings cannot be used with DATABASE_SSL_MODE=disable"
        )
    if environment == "production" and ssl_mode != "verify-full":
        raise DatabaseConfigurationError(
            "Production PostgreSQL requires DATABASE_SSL_MODE=verify-full"
        )

    statement_timeout = int(
        _settings_value(settings, "database_statement_timeout_ms")
    )
    lock_timeout = int(_settings_value(settings, "database_lock_timeout_ms"))
    connect_args: dict[str, Any] = {
        "application_name": application_name,
        "connect_timeout": connect_timeout,
        "options": (
            f"-c statement_timeout={statement_timeout} "
            f"-c lock_timeout={lock_timeout} -c timezone=UTC"
        ),
        "sslmode": ssl_mode,
    }
    if ssl_root_cert:
        connect_args["sslrootcert"] = ssl_root_cert
    if ssl_cert:
        connect_args["sslcert"] = ssl_cert
        connect_args["sslkey"] = ssl_key

    return DatabaseConfiguration(
        async_url=async_url,
        sync_url=async_url,
        backend="postgresql",
        redacted_url=redact_database_url(async_url),
        process_role=process_role,
        approved_connection_capacity=approved_connection_capacity,
        connect_args=connect_args,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout_seconds=pool_timeout,
        pool_recycle_seconds=pool_recycle,
        pool_pre_ping=pool_pre_ping,
    )
