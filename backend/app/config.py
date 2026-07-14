from functools import lru_cache
from ipaddress import ip_network
from pathlib import Path
import re
from typing import Any, Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


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
    outbound_delivery_worker_enabled: bool = True
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

        if self.deployment_environment == "production":
            url = make_url(self.database_url)
            if url.get_backend_name() == "sqlite":
                database = url.database
                if not database or database == ":memory:":
                    raise ValueError(
                        "Production SQLite requires a persistent database under /app/data"
                    )
                database_path = Path(database)
                data_root = Path("/app/data")
                if (
                    not database_path.is_absolute()
                    or database_path.resolve() == data_root
                    or not database_path.resolve().is_relative_to(data_root)
                ):
                    raise ValueError(
                        "Production SQLite DATABASE_URL must resolve inside "
                        f"{data_root}"
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
