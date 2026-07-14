"""Schemas for runtime system settings."""
from typing import Literal

from pydantic import BaseModel, Field


RuntimeSettingSource = Literal["runtime", "environment", "default"]
LLMProvider = Literal["openai", "openrouter", "nvidia", "custom"]
LanguageCode = Literal["en", "ru"]
AILanguageMode = Literal["auto", "en", "ru"]


class RuntimeSettingField(BaseModel):
    """One resolved runtime setting field."""

    source: RuntimeSettingSource


class RuntimeSecretField(RuntimeSettingField):
    """Resolved secret metadata without exposing the secret."""

    has_value: bool


class LLMRuntimeSettingsResponse(BaseModel):
    """Resolved LLM runtime settings."""

    provider: LLMProvider
    api_url: str
    model: str
    temperature: float
    max_output_tokens: int
    has_api_key: bool
    field_sources: dict[str, RuntimeSettingSource] = Field(default_factory=dict)


class LLMRuntimeSettingsUpdate(BaseModel):
    """Update request for LLM runtime settings."""

    provider: LLMProvider | None = None
    api_url: str | None = None
    model: str | None = None
    temperature: float | None = Field(default=None, ge=0, le=2)
    max_output_tokens: int | None = Field(default=None, ge=256, le=12000)
    api_key: str | None = None
    clear_api_key: bool = False
    reset_fields: list[str] = Field(default_factory=list)


class GitHubRuntimeSettingsResponse(BaseModel):
    """Resolved GitHub runtime settings."""

    api_url: str
    request_timeout_seconds: float
    webhook_create_triage_for_unmatched: bool
    has_token: bool
    has_webhook_secret: bool
    field_sources: dict[str, RuntimeSettingSource] = Field(default_factory=dict)


class GitHubRuntimeSettingsUpdate(BaseModel):
    """Update request for GitHub runtime settings."""

    api_url: str | None = None
    token: str | None = None
    clear_token: bool = False
    request_timeout_seconds: float | None = Field(default=None, gt=0, le=120)
    webhook_secret: str | None = None
    clear_webhook_secret: bool = False
    webhook_create_triage_for_unmatched: bool | None = None
    reset_fields: list[str] = Field(default_factory=list)


class WebIntakeRuntimeSettingsResponse(BaseModel):
    """Resolved controlled web-intake runtime settings."""

    rate_limit_per_minute: int
    has_token: bool
    field_sources: dict[str, RuntimeSettingSource] = Field(default_factory=dict)


class WebIntakeRuntimeSettingsUpdate(BaseModel):
    """Update request for controlled web-intake runtime settings."""

    token: str | None = None
    clear_token: bool = False
    rate_limit_per_minute: int | None = Field(default=None, ge=1, le=10000)
    reset_fields: list[str] = Field(default_factory=list)


class AppRuntimeSettingsResponse(BaseModel):
    """Resolved app-wide language behavior."""

    ui_language: LanguageCode
    ai_language_mode: AILanguageMode
    field_sources: dict[str, RuntimeSettingSource] = Field(default_factory=dict)


class AppRuntimeSettingsUpdate(BaseModel):
    """Update request for app-wide runtime settings."""

    ui_language: LanguageCode | None = None
    ai_language_mode: AILanguageMode | None = None
    reset_fields: list[str] = Field(default_factory=list)


class RestartRequiredSetting(BaseModel):
    """Read-only setting that remains environment/startup bound."""

    key: str
    description: str


class SystemSettingsResponse(BaseModel):
    """Runtime configuration summary."""

    app: AppRuntimeSettingsResponse
    llm: LLMRuntimeSettingsResponse
    github: GitHubRuntimeSettingsResponse
    web_intake: WebIntakeRuntimeSettingsResponse
    restart_required: list[RestartRequiredSetting]
