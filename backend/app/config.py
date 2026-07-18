from functools import lru_cache
from ipaddress import ip_network
import re
from typing import Any, Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.database_config import parse_database_configuration


class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "sqlite+aiosqlite:///./workchord.db"
    deployment_environment: Literal["development", "test", "production"] = "development"
    database_postgresql_required: bool = False
    database_process_role: Literal[
        "web", "delivery_worker", "migration", "repair"
    ] = "web"
    database_pool_size: int = 15
    database_max_overflow: int = 5
    database_pool_timeout_seconds: float = 30.0
    database_pool_recycle_seconds: int = 1800
    database_pool_pre_ping: bool = True
    database_connect_timeout_seconds: int = 10
    database_statement_timeout_ms: int = 30_000
    database_lock_timeout_ms: int = 5_000
    database_application_name: str = "workchord"
    database_session_role: str = ""
    database_ssl_mode: Literal[
        "disable", "allow", "prefer", "require", "verify-ca", "verify-full"
    ] = "prefer"
    database_ssl_root_cert: str = ""
    database_ssl_cert: str = ""
    database_ssl_key: str = ""
    database_readiness_timeout_seconds: float = 2.0
    database_slow_query_threshold_ms: int = 500

    # API
    api_prefix: str = "/api"
    debug: bool = False

    # LLM (optional)
    llm_provider: Literal["openai", "openrouter", "nvidia", "custom"] = "openai"
    llm_api_key: str = ""
    llm_api_url: str = ""
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.2
    llm_max_output_tokens: int = 3000

    # Common language behavior
    app_ui_language: Literal["en", "ru"] = "en"
    ai_language_mode: Literal["auto", "en", "ru"] = "auto"

    # GitHub integration (optional)
    github_api_url: str = "https://api.github.com"
    github_token: str = ""
    github_request_timeout_seconds: float = 10.0
    github_webhook_secret: str = ""
    github_webhook_create_triage_for_unmatched: bool = False

    # Controlled web intake (optional)
    web_intake_token: str = ""
    web_intake_rate_limit_per_minute: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Email notifications (optional)
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "notifications@workchord.local"
    smtp_use_tls: bool = True  # Set to False for local testing without TLS
    notifications_enabled: bool = False

    # Durable outbound delivery worker
    outbound_delivery_worker_enabled: bool = False
    outbound_delivery_poll_seconds: float = 1.0
    outbound_delivery_batch_size: int = 50

    # Security
    settings_encryption_key: str = ""
    agent_bootstrap_api_key: str = ""
    agent_skill_bundles_public: bool = False
    agent_skill_bundle_trusted_checksums_sha256: str = ""
    agent_skill_bundle_max_artifacts: int = 256
    agent_skill_bundle_max_artifact_bytes: int = 64 * 1024 * 1024
    agent_skill_bundle_max_total_bytes: int = 512 * 1024 * 1024
    agent_skill_bundle_max_metadata_bytes: int = 2 * 1024 * 1024
    agent_skill_bundle_max_file_bytes: int = 2 * 1024 * 1024
    mcp_dns_rebinding_protection: bool = True
    mcp_allowed_hosts: list[str] = [
        "localhost:*",
        "127.0.0.1:*",
        "[::1]:*",
        "testserver",
    ]
    mcp_allowed_origins: list[str] = [
        "http://localhost:*",
        "http://127.0.0.1:*",
        "http://testserver",
    ]
    mcp_http_host: str = "127.0.0.1"
    mcp_unsafe_allow_public_binding: bool = False
    workchord_admin_api_key: str = ""
    allow_private_egress_urls: bool = False
    trusted_proxy_ips: list[str] = []
    session_cookie_name: str = "workchord_session"
    session_cookie_secure: bool = True
    session_max_age_seconds: int = 30 * 24 * 60 * 60
    session_touch_interval_seconds: int = 300
    agent_last_seen_interval_seconds: int = 300

    # Deployment-owned write fence. This is restart-bound configuration rather
    # than mutable process memory or a row in the database being migrated.
    maintenance_mode: Literal[
        "off", "read-only-maintenance", "validation-only"
    ] = "off"
    maintenance_revision: str = "development"
    maintenance_replica_id: str = "local"
    maintenance_retry_after_seconds: int = 60
    maintenance_validation_allowlist: list[str] = [
        "/health",
        "/health/live",
        "/health/ready",
        "/metrics",
    ]

    @field_validator("debug", mode="before")
    @classmethod
    def normalize_debug_flag(cls, value: Any) -> Any:
        if isinstance(value, str) and value.strip().lower() in {"release", "prod", "production"}:
            return False
        return value

    @field_validator("cors_origins")
    @classmethod
    def require_explicit_cors_origins(cls, value: list[str]) -> list[str]:
        """Credentialed browser sessions require an explicit origin allowlist."""
        if "*" in value:
            raise ValueError("CORS_ORIGINS must not contain wildcard origins")
        return value

    @field_validator("agent_skill_bundle_trusted_checksums_sha256", mode="before")
    @classmethod
    def normalize_skill_bundle_trust_pin(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("agent_skill_bundle_trusted_checksums_sha256")
    @classmethod
    def validate_skill_bundle_trust_pin(cls, value: str) -> str:
        if value and re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise ValueError(
                "AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256 must be a 64-character SHA-256"
            )
        return value

    @field_validator("mcp_allowed_hosts")
    @classmethod
    def validate_mcp_allowed_hosts(cls, value: list[str]) -> list[str]:
        if not value or any(
            not host
            or host == "*"
            or "://" in host
            or "/" in host
            or any(character.isspace() for character in host)
            for host in value
        ):
            raise ValueError("MCP_ALLOWED_HOSTS must contain explicit Host values")
        return value

    @field_validator("mcp_allowed_origins")
    @classmethod
    def validate_mcp_allowed_origins(cls, value: list[str]) -> list[str]:
        if any(
            origin == "*"
            or not origin.startswith(("http://", "https://"))
            or origin.rstrip("/") != origin
            for origin in value
        ):
            raise ValueError("MCP_ALLOWED_ORIGINS must contain explicit HTTP origins")
        return value

    @field_validator("trusted_proxy_ips")
    @classmethod
    def validate_trusted_proxy_ips(cls, value: list[str]) -> list[str]:
        """Accept only explicit IP addresses or CIDR networks for proxy trust."""
        normalized: list[str] = []
        for entry in value:
            try:
                normalized.append(str(ip_network(entry.strip(), strict=False)))
            except (AttributeError, ValueError) as exc:
                raise ValueError(
                    "TRUSTED_PROXY_IPS must contain valid IP addresses or CIDR networks"
                ) from exc
        return normalized

    @model_validator(mode="after")
    def validate_release_security_boundaries(self) -> "Settings":
        if (
            self.agent_skill_bundles_public
            and not self.agent_skill_bundle_trusted_checksums_sha256
        ):
            raise ValueError(
                "Public agent skill bundles require "
                "AGENT_SKILL_BUNDLE_TRUSTED_CHECKSUMS_SHA256"
            )

        bundle_limits = (
            self.agent_skill_bundle_max_artifacts,
            self.agent_skill_bundle_max_artifact_bytes,
            self.agent_skill_bundle_max_total_bytes,
            self.agent_skill_bundle_max_metadata_bytes,
            self.agent_skill_bundle_max_file_bytes,
        )
        if any(limit <= 0 for limit in bundle_limits):
            raise ValueError("Agent skill bundle limits must be positive")
        if (
            self.agent_skill_bundle_max_total_bytes
            < self.agent_skill_bundle_max_artifact_bytes
        ):
            raise ValueError(
                "AGENT_SKILL_BUNDLE_MAX_TOTAL_BYTES must be at least the per-artifact limit"
            )

        if not self.mcp_dns_rebinding_protection and (
            self.deployment_environment != "development"
            or not self.mcp_unsafe_allow_public_binding
        ):
            raise ValueError(
                "Disabling MCP DNS-rebinding protection requires the conspicuous "
                "MCP_UNSAFE_ALLOW_PUBLIC_BINDING override in development only"
            )

        if (
            self.deployment_environment == "production"
            and self.database_process_role == "web"
            and self.outbound_delivery_worker_enabled
        ):
            raise ValueError(
                "Production web replicas must disable the embedded delivery worker"
            )
        if (
            self.deployment_environment == "production"
            and self.maintenance_mode != "off"
            and self.maintenance_revision == "development"
        ):
            raise ValueError(
                "Production maintenance mode requires an explicit MAINTENANCE_REVISION"
            )

        parse_database_configuration(self)
        return self

    @field_validator("database_pool_size")
    @classmethod
    def validate_database_pool_size(cls, value: int) -> int:
        if not 1 <= value <= 50:
            raise ValueError("DATABASE_POOL_SIZE must be between 1 and 50")
        return value

    @field_validator("database_max_overflow")
    @classmethod
    def validate_database_max_overflow(cls, value: int) -> int:
        if not 0 <= value <= 50:
            raise ValueError("DATABASE_MAX_OVERFLOW must be between 0 and 50")
        return value

    @field_validator("database_pool_timeout_seconds")
    @classmethod
    def validate_database_pool_timeout(cls, value: float) -> float:
        if not 0.1 <= value <= 120:
            raise ValueError(
                "DATABASE_POOL_TIMEOUT_SECONDS must be between 0.1 and 120"
            )
        return value

    @field_validator("database_pool_recycle_seconds")
    @classmethod
    def validate_database_pool_recycle(cls, value: int) -> int:
        if value != 0 and not 60 <= value <= 86_400:
            raise ValueError(
                "DATABASE_POOL_RECYCLE_SECONDS must be 0 or between 60 and 86400"
            )
        return value

    @field_validator("database_connect_timeout_seconds")
    @classmethod
    def validate_database_connect_timeout(cls, value: int) -> int:
        if not 1 <= value <= 60:
            raise ValueError(
                "DATABASE_CONNECT_TIMEOUT_SECONDS must be between 1 and 60"
            )
        return value

    @field_validator("database_statement_timeout_ms")
    @classmethod
    def validate_database_statement_timeout(cls, value: int) -> int:
        if not 100 <= value <= 300_000:
            raise ValueError(
                "DATABASE_STATEMENT_TIMEOUT_MS must be between 100 and 300000"
            )
        return value

    @field_validator("database_lock_timeout_ms")
    @classmethod
    def validate_database_lock_timeout(cls, value: int) -> int:
        if not 100 <= value <= 60_000:
            raise ValueError(
                "DATABASE_LOCK_TIMEOUT_MS must be between 100 and 60000"
            )
        return value

    @model_validator(mode="after")
    def validate_database_pool_capacity(self) -> "Settings":
        approved_capacity = {
            "web": 20,
            "delivery_worker": 10,
            "migration": 2,
            "repair": 2,
        }[self.database_process_role]
        if self.database_pool_size + self.database_max_overflow > approved_capacity:
            raise ValueError(
                "DATABASE_POOL_SIZE plus DATABASE_MAX_OVERFLOW exceeds the approved "
                f"{self.database_process_role} process budget of {approved_capacity}"
            )
        return self

    @field_validator("session_cookie_name")
    @classmethod
    def validate_session_cookie_name(cls, value: str) -> str:
        """Reject cookie names that could create malformed response headers."""
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", value):
            raise ValueError("SESSION_COOKIE_NAME contains unsupported characters")
        return value

    @field_validator("session_max_age_seconds")
    @classmethod
    def validate_session_lifetime(cls, value: int) -> int:
        """Session lifetime must be positive and no longer than one year."""
        if not 1 <= value <= 365 * 24 * 60 * 60:
            raise ValueError("SESSION_MAX_AGE_SECONDS must be between 1 second and 1 year")
        return value

    @field_validator("session_touch_interval_seconds")
    @classmethod
    def validate_session_touch_interval(cls, value: int) -> int:
        if not 1 <= value <= 24 * 60 * 60:
            raise ValueError(
                "SESSION_TOUCH_INTERVAL_SECONDS must be between 1 second and 1 day"
            )
        return value

    @field_validator("agent_last_seen_interval_seconds")
    @classmethod
    def validate_agent_last_seen_interval(cls, value: int) -> int:
        if not 1 <= value <= 24 * 60 * 60:
            raise ValueError(
                "AGENT_LAST_SEEN_INTERVAL_SECONDS must be between 1 second and 1 day"
            )
        return value

    @field_validator("database_readiness_timeout_seconds")
    @classmethod
    def validate_database_readiness_timeout(cls, value: float) -> float:
        if not 0.1 <= value <= 15:
            raise ValueError(
                "DATABASE_READINESS_TIMEOUT_SECONDS must be between 0.1 and 15"
            )
        return value

    @field_validator("database_slow_query_threshold_ms")
    @classmethod
    def validate_slow_query_threshold(cls, value: int) -> int:
        if not 10 <= value <= 60_000:
            raise ValueError(
                "DATABASE_SLOW_QUERY_THRESHOLD_MS must be between 10 and 60000"
            )
        return value

    @field_validator("maintenance_revision", "maintenance_replica_id")
    @classmethod
    def validate_maintenance_identity(cls, value: str) -> str:
        normalized = value.strip()
        if not re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", normalized):
            raise ValueError(
                "Maintenance revision and replica identity must be safe identifiers"
            )
        return normalized

    @field_validator("maintenance_retry_after_seconds")
    @classmethod
    def validate_maintenance_retry_after(cls, value: int) -> int:
        if not 1 <= value <= 3600:
            raise ValueError(
                "MAINTENANCE_RETRY_AFTER_SECONDS must be between 1 and 3600"
            )
        return value

    @field_validator("maintenance_validation_allowlist")
    @classmethod
    def validate_maintenance_allowlist(cls, value: list[str]) -> list[str]:
        required = {"/health/live", "/health/ready"}
        normalized: list[str] = []
        for path in value:
            candidate = path.strip()
            if (
                not candidate.startswith("/")
                or "?" in candidate
                or "#" in candidate
                or any(character.isspace() for character in candidate)
                or ("*" in candidate and not candidate.endswith("/*"))
            ):
                raise ValueError(
                    "MAINTENANCE_VALIDATION_ALLOWLIST must contain exact paths or /prefix/*"
                )
            normalized.append(candidate.rstrip("/") or "/")
        if not required.issubset(normalized):
            raise ValueError(
                "MAINTENANCE_VALIDATION_ALLOWLIST must include /health/live and /health/ready"
            )
        return list(dict.fromkeys(normalized))

    @field_validator("outbound_delivery_poll_seconds")
    @classmethod
    def validate_delivery_poll_seconds(cls, value: float) -> float:
        if not 0.05 <= value <= 300:
            raise ValueError("OUTBOUND_DELIVERY_POLL_SECONDS must be between 0.05 and 300")
        return value

    @field_validator("outbound_delivery_batch_size")
    @classmethod
    def validate_delivery_batch_size(cls, value: int) -> int:
        if not 1 <= value <= 1000:
            raise ValueError("OUTBOUND_DELIVERY_BATCH_SIZE must be between 1 and 1000")
        return value


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
