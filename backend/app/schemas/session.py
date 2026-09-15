from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserSession(BaseModel):
    """Privacy-safe browser session response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    public_id: str
    display_name: str
    principal_id: int | None = None
    authenticated: bool = False
    created_at: datetime
    last_seen_at: datetime
