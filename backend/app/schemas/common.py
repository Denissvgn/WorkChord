"""Common schemas and error handling."""
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Detail of validation error."""
    field: str
    message: str


class ErrorResponse(BaseModel):
    """Standard error response."""
    code: str
    message: str
    details: list[ErrorDetail] = []


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str
    success: bool = True
