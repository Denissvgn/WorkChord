"""Exception handlers and error middleware."""
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.schemas.common import ErrorResponse, ErrorDetail


class WorkChordException(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, code: str = "error"):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundException(WorkChordException):
    """Resource not found exception."""
    def __init__(self, resource: str, id: int):
        super().__init__(
            message=f"{resource} with id {id} not found",
            code="not_found"
        )


class ValidationException(WorkChordException):
    """Validation error exception."""
    def __init__(self, message: str, details: Optional[list[ErrorDetail]] = None):
        super().__init__(message=message, code="validation_error")
        self.details = details or []


class CircularDependencyException(WorkChordException):
    """Circular dependency detected."""
    def __init__(self, task_ids: list[int]):
        super().__init__(
            message=f"Circular dependency detected in tasks: {task_ids}",
            code="circular_dependency"
        )


def setup_exception_handlers(app: FastAPI):
    """Setup custom exception handlers for the application."""

    @app.exception_handler(WorkChordException)
    async def handle_workchord_exception(
        request: Request, exc: WorkChordException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
                details=getattr(exc, 'details', [])
            ).model_dump()
        )

    @app.exception_handler(NotFoundException)
    async def handle_not_found_exception(
        request: Request, exc: NotFoundException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                code=exc.code,
                message=exc.message
            ).model_dump()
        )

    @app.exception_handler(ValidationError)
    async def handle_validation_error(
        request: Request, exc: ValidationError
    ) -> JSONResponse:
        details = [
            ErrorDetail(
                field=".".join(str(loc) for loc in err["loc"]),
                message=err["msg"]
            )
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=ErrorResponse(
                code="validation_error",
                message="Request validation failed",
                details=details
            ).model_dump()
        )

    @app.exception_handler(IntegrityError)
    async def handle_integrity_error(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                code="integrity_error",
                message="Database constraint violation"
            ).model_dump()
        )
