"""DB-backed runtime system settings resolution."""
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Literal, Optional
import json
import logging

from cryptography.fernet import Fernet
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.system_settings import SystemSetting
from app.schemas.system_settings import (
    AppRuntimeSettingsResponse,
    GitHubRuntimeSettingsResponse,
    LLMRuntimeSettingsResponse,
    RestartRequiredSetting,
    SystemSettingsResponse,
    WebIntakeRuntimeSettingsResponse,
)
from app.utils.url_policy import (
    URLPolicyError,
    normalize_provider_api_url,
    validate_public_host,
)

logger = logging.getLogger(__name__)

RuntimeSettingSource = Literal["runtime", "environment", "default"]

LEGACY_EMAIL_SETTINGS_FILE = Path("email_settings.json")


class RuntimeSettingsError(ValueError):
    """Raised when a runtime settings update is invalid."""


class RuntimeSettingsEncryptionError(RuntimeSettingsError):
    """Raised when a secret cannot be encrypted or decrypted."""


@dataclass(frozen=True)
class SettingDefinition:
    """Catalog definition for one writable runtime setting."""

    key: str
    category: str
    field: str
    env_attr: str
    default: Any
    is_secret: bool = False
    value_type: type = str


SETTING_DEFINITIONS: dict[str, SettingDefinition] = {
    "app.ui_language": SettingDefinition("app.ui_language", "app", "ui_language", "app_ui_language", "en", value_type=str),
    "app.ai_language_mode": SettingDefinition("app.ai_language_mode", "app", "ai_language_mode", "ai_language_mode", "auto", value_type=str),
    "llm.provider": SettingDefinition("llm.provider", "llm", "provider", "llm_provider", "openai", value_type=str),
    "llm.api_url": SettingDefinition("llm.api_url", "llm", "api_url", "llm_api_url", "", value_type=str),
    "llm.model": SettingDefinition("llm.model", "llm", "model", "llm_model", "gpt-4", value_type=str),
    "llm.temperature": SettingDefinition("llm.temperature", "llm", "temperature", "llm_temperature", 0.2, value_type=float),
    "llm.max_output_tokens": SettingDefinition("llm.max_output_tokens", "llm", "max_output_tokens", "llm_max_output_tokens", 3000, value_type=int),
    "llm.api_key": SettingDefinition("llm.api_key", "llm", "api_key", "llm_api_key", "", is_secret=True, value_type=str),
    "github.api_url": SettingDefinition("github.api_url", "github", "api_url", "github_api_url", "https://api.github.com", value_type=str),
    "github.token": SettingDefinition("github.token", "github", "token", "github_token", "", is_secret=True, value_type=str),
    "github.request_timeout_seconds": SettingDefinition("github.request_timeout_seconds", "github", "request_timeout_seconds", "github_request_timeout_seconds", 10.0, value_type=float),
    "github.webhook_secret": SettingDefinition("github.webhook_secret", "github", "webhook_secret", "github_webhook_secret", "", is_secret=True, value_type=str),
    "github.webhook_create_triage_for_unmatched": SettingDefinition("github.webhook_create_triage_for_unmatched", "github", "webhook_create_triage_for_unmatched", "github_webhook_create_triage_for_unmatched", False, value_type=bool),
    "web_intake.token": SettingDefinition("web_intake.token", "web_intake", "token", "web_intake_token", "", is_secret=True, value_type=str),
    "web_intake.rate_limit_per_minute": SettingDefinition("web_intake.rate_limit_per_minute", "web_intake", "rate_limit_per_minute", "web_intake_rate_limit_per_minute", 30, value_type=int),
    "email.enabled": SettingDefinition("email.enabled", "email", "enabled", "notifications_enabled", False, value_type=bool),
    "email.smtp_host": SettingDefinition("email.smtp_host", "email", "smtp_host", "smtp_host", "", value_type=str),
    "email.smtp_port": SettingDefinition("email.smtp_port", "email", "smtp_port", "smtp_port", 587, value_type=int),
    "email.smtp_user": SettingDefinition("email.smtp_user", "email", "smtp_user", "smtp_user", "", value_type=str),
    "email.smtp_password": SettingDefinition("email.smtp_password", "email", "smtp_password", "smtp_password", "", is_secret=True, value_type=str),
    "email.smtp_from_email": SettingDefinition("email.smtp_from_email", "email", "smtp_from_email", "smtp_from_email", "notifications@workchord.local", value_type=str),
    "email.smtp_use_tls": SettingDefinition("email.smtp_use_tls", "email", "smtp_use_tls", "smtp_use_tls", True, value_type=bool),
}

FIELD_TO_KEY: dict[str, dict[str, str]] = {}
for definition in SETTING_DEFINITIONS.values():
    FIELD_TO_KEY.setdefault(definition.category, {})[definition.field] = definition.key

RESTART_REQUIRED_SETTINGS = [
    RestartRequiredSetting(key="DATABASE_URL", description="Database engine and connection are initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_POSTGRESQL_REQUIRED", description="Production database fallback policy is enforced before startup."),
    RestartRequiredSetting(key="DATABASE_PROCESS_ROLE", description="The approved per-process connection budget is selected at startup."),
    RestartRequiredSetting(key="DATABASE_POOL_SIZE", description="Database pool capacity is allocated at process startup."),
    RestartRequiredSetting(key="DATABASE_MAX_OVERFLOW", description="Database overflow capacity is allocated at process startup."),
    RestartRequiredSetting(key="DATABASE_POOL_TIMEOUT_SECONDS", description="Pool checkout policy is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_POOL_RECYCLE_SECONDS", description="Pooled connection lifetime is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_POOL_PRE_PING", description="Pooled connection validation is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_CONNECT_TIMEOUT_SECONDS", description="Database connection policy is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_STATEMENT_TIMEOUT_MS", description="PostgreSQL statement policy is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_LOCK_TIMEOUT_MS", description="PostgreSQL lock policy is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_APPLICATION_NAME", description="Database connection identity is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_SSL_MODE", description="Database TLS policy is initialized at process startup."),
    RestartRequiredSetting(key="DATABASE_SSL_ROOT_CERT", description="Database trust roots are loaded at process startup."),
    RestartRequiredSetting(key="DATABASE_SSL_CERT", description="Database client identity is loaded at process startup."),
    RestartRequiredSetting(key="DATABASE_SSL_KEY", description="Database client identity is loaded at process startup."),
    RestartRequiredSetting(key="API_PREFIX", description="FastAPI router prefixes are bound at application startup."),
    RestartRequiredSetting(key="DEBUG", description="Database logging and process debug behavior are startup-bound."),
    RestartRequiredSetting(key="CORS_ORIGINS", description="CORS middleware is installed with startup configuration."),
    RestartRequiredSetting(key="SETTINGS_ENCRYPTION_KEY", description="Root key used to decrypt runtime secrets."),
    RestartRequiredSetting(key="AGENT_BOOTSTRAP_API_KEY", description="Bootstrap agent authentication remains environment-only."),
    RestartRequiredSetting(key="WORKCHORD_ADMIN_API_KEY", description="Admin control-plane authentication remains environment-only."),
    RestartRequiredSetting(key="TRUSTED_PROXY_IPS", description="Proxy trust decisions are initialized from environment configuration."),
    RestartRequiredSetting(key="VITE_API_URL", description="Frontend dev proxy setting is read by Vite at build/dev-server start."),
]


class RuntimeSettingsService:
    """Read, update, and resolve catalogued runtime system settings."""

    def __init__(self, db: AsyncSession, settings_override=None):
        self.db = db
        self.env_settings = settings_override or get_settings()

    def _fernet(self) -> Fernet:
        key = getattr(self.env_settings, "settings_encryption_key", "") or ""
        if not key:
            raise RuntimeSettingsEncryptionError("SETTINGS_ENCRYPTION_KEY is required to save runtime secrets")
        try:
            return Fernet(key)
        except Exception as exc:
            raise RuntimeSettingsEncryptionError("SETTINGS_ENCRYPTION_KEY is invalid") from exc

    def _encrypt_secret(self, value: str) -> str:
        return self._fernet().encrypt(value.encode("utf-8")).decode("utf-8")

    def _decrypt_secret(self, value: str) -> str:
        try:
            return self._fernet().decrypt(value.encode("utf-8")).decode("utf-8")
        except RuntimeSettingsEncryptionError:
            raise
        except Exception as exc:
            raise RuntimeSettingsEncryptionError("Runtime secret could not be decrypted") from exc

    async def _row(self, key: str) -> Optional[SystemSetting]:
        result = await self.db.execute(select(SystemSetting).where(SystemSetting.key == key))
        return result.scalar_one_or_none()

    async def _category_rows(self, category: str) -> list[SystemSetting]:
        result = await self.db.execute(
            select(SystemSetting).where(SystemSetting.category == category)
        )
        return list(result.scalars().all())

    def _definition(self, key: str) -> SettingDefinition:
        definition = SETTING_DEFINITIONS.get(key)
        if not definition:
            raise RuntimeSettingsError(f"Unsupported runtime setting: {key}")
        return definition

    def _field_key(self, category: str, field: str) -> str:
        key = FIELD_TO_KEY.get(category, {}).get(field)
        if not key:
            raise RuntimeSettingsError(f"Unsupported {category} runtime setting field: {field}")
        return key

    def _coerce(self, definition: SettingDefinition, value: Any) -> Any:
        if definition.value_type is bool:
            if not isinstance(value, bool):
                raise RuntimeSettingsError(f"{definition.field} must be a boolean")
            return value
        if definition.value_type is int:
            if isinstance(value, bool):
                raise RuntimeSettingsError(f"{definition.field} must be an integer")
            coerced = int(value)
            if definition.key == "llm.max_output_tokens" and not 256 <= coerced <= 12000:
                raise RuntimeSettingsError("max_output_tokens must be between 256 and 12000")
            if definition.key == "web_intake.rate_limit_per_minute" and coerced < 1:
                raise RuntimeSettingsError("rate_limit_per_minute must be at least 1")
            if definition.key == "email.smtp_port" and not 1 <= coerced <= 65535:
                raise RuntimeSettingsError("smtp_port must be between 1 and 65535")
            return coerced
        if definition.value_type is float:
            if isinstance(value, bool):
                raise RuntimeSettingsError(f"{definition.field} must be a number")
            coerced = float(value)
            if definition.key == "llm.temperature" and not 0 <= coerced <= 2:
                raise RuntimeSettingsError("temperature must be between 0 and 2")
            if definition.key == "github.request_timeout_seconds" and not 0 < coerced <= 120:
                raise RuntimeSettingsError("request_timeout_seconds must be between 0 and 120")
            return coerced

        coerced = str(value).strip() if value is not None else ""
        if definition.key == "llm.provider" and coerced not in {"openai", "openrouter", "nvidia", "custom"}:
            raise RuntimeSettingsError("provider must be openai, openrouter, nvidia, or custom")
        if definition.key == "app.ui_language" and coerced not in {"en", "ru"}:
            raise RuntimeSettingsError("ui_language must be en or ru")
        if definition.key == "app.ai_language_mode" and coerced not in {"auto", "en", "ru"}:
            raise RuntimeSettingsError("ai_language_mode must be auto, en, or ru")
        if definition.key in {"llm.model", "github.api_url", "email.smtp_from_email"} and not coerced:
            raise RuntimeSettingsError(f"{definition.field} cannot be blank")
        if definition.key == "llm.api_url" and coerced:
            try:
                return normalize_provider_api_url(coerced)
            except URLPolicyError as exc:
                raise RuntimeSettingsError(str(exc)) from exc
        if definition.key == "github.api_url":
            try:
                return normalize_provider_api_url(coerced)
            except URLPolicyError as exc:
                raise RuntimeSettingsError(str(exc)) from exc
        return coerced

    def _allow_private_egress(self) -> bool:
        return bool(getattr(self.env_settings, "allow_private_egress_urls", False))

    def _validate_smtp_host_for_egress(self, host: str) -> str:
        if not host:
            return ""
        try:
            return validate_public_host(
                host,
                allow_private=self._allow_private_egress(),
                resolve=False,
            )
        except URLPolicyError as exc:
            raise RuntimeSettingsError(str(exc)) from exc

    async def set_value(self, key: str, value: Any) -> SystemSetting:
        definition = self._definition(key)
        if definition.is_secret:
            raise RuntimeSettingsError(f"{key} is a secret setting")
        coerced = self._coerce(definition, value)
        row = await self._row(key)
        if not row:
            row = SystemSetting(
                key=definition.key,
                category=definition.category,
                is_secret=False,
            )
            self.db.add(row)
        row.value_json = coerced
        row.secret_ciphertext = None
        row.is_secret = False
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def set_secret(self, key: str, value: str) -> SystemSetting:
        definition = self._definition(key)
        if not definition.is_secret:
            raise RuntimeSettingsError(f"{key} is not a secret setting")
        coerced = self._coerce(definition, value)
        if not coerced:
            raise RuntimeSettingsError(f"{definition.field} cannot be blank")
        row = await self._row(key)
        if not row:
            row = SystemSetting(
                key=definition.key,
                category=definition.category,
                is_secret=True,
            )
            self.db.add(row)
        row.value_json = None
        row.secret_ciphertext = self._encrypt_secret(coerced)
        row.is_secret = True
        await self.db.commit()
        await self.db.refresh(row)
        return row

    async def clear_key(self, key: str) -> None:
        self._definition(key)
        await self.db.execute(delete(SystemSetting).where(SystemSetting.key == key))
        await self.db.commit()

    async def clear_fields(self, category: str, fields: list[str]) -> None:
        for field in fields:
            await self.clear_key(self._field_key(category, field))

    def _env_value(self, definition: SettingDefinition) -> tuple[Any, RuntimeSettingSource]:
        value = getattr(self.env_settings, definition.env_attr, definition.default)
        source: RuntimeSettingSource = "environment" if value != definition.default else "default"
        return value, source

    async def resolve(self, key: str) -> tuple[Any, RuntimeSettingSource]:
        definition = self._definition(key)
        row = await self._row(key)
        if row:
            if definition.is_secret:
                if row.secret_ciphertext:
                    return self._decrypt_secret(row.secret_ciphertext), "runtime"
            else:
                return self._coerce(definition, row.value_json), "runtime"

        value, source = self._env_value(definition)
        return self._coerce(definition, value), source

    async def has_secret(self, key: str) -> tuple[bool, RuntimeSettingSource]:
        definition = self._definition(key)
        if not definition.is_secret:
            raise RuntimeSettingsError(f"{key} is not a secret setting")
        row = await self._row(key)
        if row and row.secret_ciphertext:
            return True, "runtime"
        value, source = self._env_value(definition)
        return bool(value), source

    async def _field_sources(self, category: str) -> dict[str, RuntimeSettingSource]:
        sources: dict[str, RuntimeSettingSource] = {}
        for field, key in FIELD_TO_KEY[category].items():
            if SETTING_DEFINITIONS[key].is_secret:
                _, source = await self.has_secret(key)
            else:
                _, source = await self.resolve(key)
            sources[field] = source
        return sources

    async def get_llm_settings(self):
        provider, _ = await self.resolve("llm.provider")
        api_key, _ = await self.resolve("llm.api_key")
        api_url, _ = await self.resolve("llm.api_url")
        model, _ = await self.resolve("llm.model")
        temperature, _ = await self.resolve("llm.temperature")
        max_output_tokens, _ = await self.resolve("llm.max_output_tokens")
        ui_language, _ = await self.resolve("app.ui_language")
        ai_language_mode, _ = await self.resolve("app.ai_language_mode")
        return SimpleNamespace(
            llm_provider=provider,
            llm_api_key=api_key,
            llm_api_url=api_url,
            llm_model=model,
            llm_temperature=temperature,
            llm_max_output_tokens=max_output_tokens,
            app_ui_language=ui_language,
            ai_language_mode=ai_language_mode,
        )

    async def get_app_settings(self):
        ui_language, _ = await self.resolve("app.ui_language")
        ai_language_mode, _ = await self.resolve("app.ai_language_mode")
        return SimpleNamespace(
            app_ui_language=ui_language,
            ai_language_mode=ai_language_mode,
        )

    async def get_github_settings(self):
        api_url, _ = await self.resolve("github.api_url")
        token, _ = await self.resolve("github.token")
        timeout, _ = await self.resolve("github.request_timeout_seconds")
        webhook_secret, _ = await self.resolve("github.webhook_secret")
        create_triage, _ = await self.resolve("github.webhook_create_triage_for_unmatched")
        return SimpleNamespace(
            github_api_url=api_url,
            github_token=token,
            github_request_timeout_seconds=timeout,
            github_webhook_secret=webhook_secret,
            github_webhook_create_triage_for_unmatched=create_triage,
        )

    async def get_web_intake_settings(self):
        token, _ = await self.resolve("web_intake.token")
        rate_limit, _ = await self.resolve("web_intake.rate_limit_per_minute")
        return SimpleNamespace(
            web_intake_token=token,
            web_intake_rate_limit_per_minute=rate_limit,
        )

    async def get_email_settings(self, *, include_secret: bool = True):
        enabled, _ = await self.resolve("email.enabled")
        host, _ = await self.resolve("email.smtp_host")
        port, _ = await self.resolve("email.smtp_port")
        user, _ = await self.resolve("email.smtp_user")
        password = ""
        if include_secret:
            password, _ = await self.resolve("email.smtp_password")
        from_email, _ = await self.resolve("email.smtp_from_email")
        use_tls, _ = await self.resolve("email.smtp_use_tls")
        return SimpleNamespace(
            enabled=enabled,
            smtp_host=host,
            smtp_port=port,
            smtp_user=user,
            smtp_password=password,
            smtp_from_email=from_email,
            smtp_use_tls=use_tls,
        )

    async def llm_response(self) -> LLMRuntimeSettingsResponse:
        provider, _ = await self.resolve("llm.provider")
        api_url, _ = await self.resolve("llm.api_url")
        model, _ = await self.resolve("llm.model")
        temperature, _ = await self.resolve("llm.temperature")
        max_output_tokens, _ = await self.resolve("llm.max_output_tokens")
        has_api_key, _ = await self.has_secret("llm.api_key")
        return LLMRuntimeSettingsResponse(
            provider=provider,
            api_url=api_url,
            model=model,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            has_api_key=has_api_key,
            field_sources=await self._field_sources("llm"),
        )

    async def github_response(self) -> GitHubRuntimeSettingsResponse:
        api_url, _ = await self.resolve("github.api_url")
        timeout, _ = await self.resolve("github.request_timeout_seconds")
        create_triage, _ = await self.resolve("github.webhook_create_triage_for_unmatched")
        has_token, _ = await self.has_secret("github.token")
        has_webhook_secret, _ = await self.has_secret("github.webhook_secret")
        return GitHubRuntimeSettingsResponse(
            api_url=api_url,
            request_timeout_seconds=timeout,
            webhook_create_triage_for_unmatched=create_triage,
            has_token=has_token,
            has_webhook_secret=has_webhook_secret,
            field_sources=await self._field_sources("github"),
        )

    async def web_intake_response(self) -> WebIntakeRuntimeSettingsResponse:
        rate_limit, _ = await self.resolve("web_intake.rate_limit_per_minute")
        has_token, _ = await self.has_secret("web_intake.token")
        return WebIntakeRuntimeSettingsResponse(
            rate_limit_per_minute=rate_limit,
            has_token=has_token,
            field_sources=await self._field_sources("web_intake"),
        )

    async def app_response(self) -> AppRuntimeSettingsResponse:
        ui_language, _ = await self.resolve("app.ui_language")
        ai_language_mode, _ = await self.resolve("app.ai_language_mode")
        return AppRuntimeSettingsResponse(
            ui_language=ui_language,
            ai_language_mode=ai_language_mode,
            field_sources=await self._field_sources("app"),
        )

    async def system_response(self) -> SystemSettingsResponse:
        return SystemSettingsResponse(
            app=await self.app_response(),
            llm=await self.llm_response(),
            github=await self.github_response(),
            web_intake=await self.web_intake_response(),
            restart_required=RESTART_REQUIRED_SETTINGS,
        )

    async def _reject_endpoint_change_without_secret_rotation(
        self,
        *,
        api_url_key: str,
        secret_key: str,
        new_api_url: str,
        new_secret: Optional[str],
        clear_secret: bool,
    ) -> None:
        """Require credential rotation when an API endpoint host changes."""
        current_api_url, _ = await self.resolve(api_url_key)
        if not current_api_url:
            return
        from urllib.parse import urlparse

        current_host = urlparse(current_api_url).hostname
        new_host = urlparse(new_api_url).hostname
        if current_host == new_host:
            return
        has_secret, _ = await self.has_secret(secret_key)
        if has_secret and not new_secret and not clear_secret:
            raise RuntimeSettingsError(
                "Changing an API URL with an existing secret requires rotating or clearing the secret in the same request."
            )

    async def update_llm(self, data) -> LLMRuntimeSettingsResponse:
        await self.clear_fields("llm", data.reset_fields)
        if data.provider is not None:
            await self.set_value("llm.provider", data.provider)
        if data.api_url is not None:
            await self._reject_endpoint_change_without_secret_rotation(
                api_url_key="llm.api_url",
                secret_key="llm.api_key",
                new_api_url=data.api_url,
                new_secret=data.api_key,
                clear_secret=data.clear_api_key,
            )
            await self.set_value("llm.api_url", data.api_url)
        if data.model is not None:
            await self.set_value("llm.model", data.model)
        if data.temperature is not None:
            await self.set_value("llm.temperature", data.temperature)
        if data.max_output_tokens is not None:
            await self.set_value("llm.max_output_tokens", data.max_output_tokens)
        if data.clear_api_key:
            await self.clear_key("llm.api_key")
        elif data.api_key:
            await self.set_secret("llm.api_key", data.api_key)
        return await self.llm_response()

    async def update_app(self, data) -> AppRuntimeSettingsResponse:
        await self.clear_fields("app", data.reset_fields)
        if data.ui_language is not None:
            await self.set_value("app.ui_language", data.ui_language)
        if data.ai_language_mode is not None:
            await self.set_value("app.ai_language_mode", data.ai_language_mode)
        return await self.app_response()

    async def update_github(self, data) -> GitHubRuntimeSettingsResponse:
        await self.clear_fields("github", data.reset_fields)
        if data.api_url is not None:
            await self._reject_endpoint_change_without_secret_rotation(
                api_url_key="github.api_url",
                secret_key="github.token",
                new_api_url=data.api_url,
                new_secret=data.token,
                clear_secret=data.clear_token,
            )
            await self.set_value("github.api_url", data.api_url)
        if data.request_timeout_seconds is not None:
            await self.set_value("github.request_timeout_seconds", data.request_timeout_seconds)
        if data.webhook_create_triage_for_unmatched is not None:
            await self.set_value(
                "github.webhook_create_triage_for_unmatched",
                data.webhook_create_triage_for_unmatched,
            )
        if data.clear_token:
            await self.clear_key("github.token")
        elif data.token:
            await self.set_secret("github.token", data.token)
        if data.clear_webhook_secret:
            await self.clear_key("github.webhook_secret")
        elif data.webhook_secret:
            await self.set_secret("github.webhook_secret", data.webhook_secret)
        return await self.github_response()

    async def update_web_intake(self, data) -> WebIntakeRuntimeSettingsResponse:
        await self.clear_fields("web_intake", data.reset_fields)
        if data.rate_limit_per_minute is not None:
            await self.set_value("web_intake.rate_limit_per_minute", data.rate_limit_per_minute)
        if data.clear_token:
            await self.clear_key("web_intake.token")
        elif data.token:
            await self.set_secret("web_intake.token", data.token)
        return await self.web_intake_response()

    async def update_email(self, data):
        if getattr(data, "reset_fields", None):
            await self.clear_fields("email", data.reset_fields)
        smtp_host = self._validate_smtp_host_for_egress(data.smtp_host)
        await self.set_value("email.enabled", data.enabled)
        await self.set_value("email.smtp_host", smtp_host)
        await self.set_value("email.smtp_port", data.smtp_port)
        await self.set_value("email.smtp_user", data.smtp_user)
        await self.set_value("email.smtp_from_email", data.smtp_from_email)
        await self.set_value("email.smtp_use_tls", data.smtp_use_tls)
        if getattr(data, "clear_smtp_password", False):
            await self.clear_key("email.smtp_password")
        elif data.smtp_password:
            await self.set_secret("email.smtp_password", data.smtp_password)
        return await self.get_email_settings(include_secret=False)

    async def migrate_legacy_email_settings(self) -> None:
        """Import legacy JSON email settings once if DB email settings are empty."""
        rows = await self._category_rows("email")
        if rows or not LEGACY_EMAIL_SETTINGS_FILE.exists():
            return

        try:
            data = json.loads(LEGACY_EMAIL_SETTINGS_FILE.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return
        except Exception:
            logger.warning(
                "Failed to read legacy email settings",
                exc_info=True,
                extra={"path": str(LEGACY_EMAIL_SETTINGS_FILE)},
            )
            return

        logger.info("Importing legacy email_settings.json into system_settings")
        for field in (
            "enabled",
            "smtp_host",
            "smtp_port",
            "smtp_user",
            "smtp_from_email",
            "smtp_use_tls",
        ):
            key = self._field_key("email", field)
            if field in data:
                await self.set_value(key, data[field])

        password = data.get("smtp_password")
        if password:
            password_value = str(password)
            try:
                password_value = self._decrypt_secret(password_value)
            except RuntimeSettingsEncryptionError:
                # Legacy files may contain plain text, encrypted text with a
                # different key, or encrypted text when the key is now absent.
                # Saving below will still enforce the current runtime key.
                logger.warning(
                    "Legacy email password could not be decrypted; trying documented plaintext migration",
                    exc_info=True,
                    extra={"path": str(LEGACY_EMAIL_SETTINGS_FILE)},
                )
            try:
                await self.set_secret("email.smtp_password", password_value)
            except RuntimeSettingsEncryptionError as exc:
                logger.warning("Skipped legacy email password import: %s", exc)
