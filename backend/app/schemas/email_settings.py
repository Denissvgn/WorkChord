"""Email settings schemas."""
from pydantic import BaseModel, EmailStr, Field

from app.schemas.system_settings import RuntimeSettingSource


class EmailSettingsUpdate(BaseModel):
    """Schema for updating email settings."""
    enabled: bool = False
    smtp_host: str = ""
    smtp_port: int = Field(default=587, ge=1, le=65535)
    smtp_user: str = ""
    smtp_password: str | None = None  # None means "keep existing"
    smtp_from_email: str = "notifications@workchord.local"
    smtp_use_tls: bool = True
    clear_smtp_password: bool = False
    reset_fields: list[str] = Field(default_factory=list)


class EmailSettingsResponse(BaseModel):
    """Schema for email settings response (password masked)."""
    enabled: bool
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_from_email: str
    smtp_use_tls: bool
    has_password: bool  # Indicates if password is configured
    field_sources: dict[str, RuntimeSettingSource] = Field(default_factory=dict)


class TestEmailRequest(BaseModel):
    """Schema for test email request."""
    recipient: EmailStr


class TestEmailResponse(BaseModel):
    """Schema for test email response."""
    success: bool
    message: str
