"""Outbound webhook API schemas."""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.url_policy import URLPolicyError, normalize_external_http_url


def _normalize_url(value: str) -> str:
    """Require public outbound webhook URLs to use HTTP or HTTPS."""
    try:
        return normalize_external_http_url(value, resolve=False)
    except URLPolicyError as exc:
        raise ValueError(str(exc)) from exc


def _normalize_events(value: list[str]) -> list[str]:
    """Normalize non-empty subscription tokens without duplicates."""
    seen: set[str] = set()
    normalized: list[str] = []
    for item in value:
        token = str(item).strip()
        if not token:
            continue
        if token not in seen:
            normalized.append(token)
            seen.add(token)
    return normalized


def _normalize_headers(value: dict[str, Any]) -> dict[str, str]:
    """Restrict custom headers to string key/value pairs."""
    normalized: dict[str, str] = {}
    for key, header_value in (value or {}).items():
        key_text = str(key).strip()
        if not key_text:
            raise ValueError("header names must be non-empty")
        if not isinstance(header_value, str):
            raise ValueError("header values must be strings")
        normalized[key_text] = header_value
    return normalized


def _normalize_secret(value: Optional[str]) -> Optional[str]:
    """Normalize optional signing secrets."""
    if value is None:
        return None
    secret = value.strip()
    return secret or None


class OutboundWebhookDeliveryStatus(str, Enum):
    """Delivery states exposed by the outbound webhook API."""

    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"


class OutboundWebhookTargetBase(BaseModel):
    """Shared target configuration fields."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    url: str = Field(..., min_length=1, max_length=1000)
    enabled: bool = True
    subscribed_events_json: list[str] = Field(default_factory=list)
    secret: Optional[str] = Field(default=None, max_length=500)
    headers_json: dict[str, str] = Field(default_factory=dict)

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        return _normalize_url(value)

    @field_validator("subscribed_events_json")
    @classmethod
    def validate_events(cls, value: list[str]) -> list[str]:
        return _normalize_events(value)

    @field_validator("headers_json")
    @classmethod
    def validate_headers(cls, value: dict[str, Any]) -> dict[str, str]:
        return _normalize_headers(value)

    @field_validator("secret")
    @classmethod
    def validate_secret(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_secret(value)


class OutboundWebhookTargetCreate(OutboundWebhookTargetBase):
    """Create an outbound webhook target."""


class OutboundWebhookTargetUpdate(BaseModel):
    """Partial update for an outbound webhook target."""

    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    url: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    enabled: Optional[bool] = None
    subscribed_events_json: Optional[list[str]] = None
    secret: Optional[str] = Field(default=None, max_length=500)
    headers_json: Optional[dict[str, str]] = None

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_url(value) if value is not None else None

    @field_validator("subscribed_events_json")
    @classmethod
    def validate_events(cls, value: Optional[list[str]]) -> Optional[list[str]]:
        return _normalize_events(value) if value is not None else None

    @field_validator("headers_json")
    @classmethod
    def validate_headers(cls, value: Optional[dict[str, Any]]) -> Optional[dict[str, str]]:
        return _normalize_headers(value) if value is not None else None

    @field_validator("secret")
    @classmethod
    def validate_secret(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_secret(value)


class OutboundWebhookTargetResponse(BaseModel):
    """Outbound webhook target response without exposing the secret."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    url: str
    enabled: bool
    subscribed_events_json: list[str]
    has_secret: bool = False
    headers_json: dict[str, str]
    created_at: datetime
    updated_at: datetime


class OutboundWebhookEventResponse(BaseModel):
    """Normalized outbound webhook event response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: str
    event_type: str
    entity_type: str
    entity_id: Optional[int] = None
    payload_json: dict[str, Any]
    occurred_at: datetime


class OutboundWebhookDeliveryResponse(BaseModel):
    """Delivery attempt response with embedded event details."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    target_id: Optional[int] = None
    event_id: int
    target_name: str
    target_url: str
    channel: str = "webhook"
    status: str
    attempt_count: int
    max_attempts: int = 5
    last_http_status: Optional[int] = None
    last_error: Optional[str] = None
    last_response_body: Optional[str] = None
    last_attempt_at: Optional[datetime] = None
    next_retry_at: Optional[datetime] = None
    terminal_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    event: OutboundWebhookEventResponse


class OutboundWebhookRetryResponse(BaseModel):
    """Response returned by retry and test delivery endpoints."""

    delivery: OutboundWebhookDeliveryResponse
