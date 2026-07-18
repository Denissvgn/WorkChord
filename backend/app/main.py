from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import TimeoutError as SQLAlchemyTimeoutError

from app.config import get_settings
from app.database import close_database, init_db
from app.database_runtime import DatabaseConflictError, DatabaseUnavailableError
from app.maintenance import (
    MaintenanceModeError,
    RuntimeBoundaryMiddleware,
    maintenance_state,
)
from app.observability import collect_metrics, readiness_snapshot
from app.query_limits import CollectionLimitExceededError
from app.runtime_telemetry import metrics
from app.routers import agent, agent_catalog, agent_planning, agent_skill_bundles, calendars, iterations, team, tasks, projects, gantt, github, intake, llm, export, snapshots, session, scheduling_rules, email_settings, triage, templates, labels, saved_views, request_sources, outbound_webhooks, system_settings
from app.mcp_server import mcp, mount_mcp_http

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    try:
        async with mcp.session_manager.run():
            # Web startup is entirely assert-only. Dedicated migration/repair
            # commands own DDL and default creation; dedicated workers own
            # durable outbound delivery.
            if settings.database_process_role != "web":
                raise RuntimeError("app.main may run only with DATABASE_PROCESS_ROLE=web")
            await init_db()
            yield
    finally:
        await close_database()


app = FastAPI(
    title="WorkChord API",
    description="API для планирования работ команды разработки",
    version="1.6.2",
    lifespan=lifespan,
)


@app.exception_handler(RequestValidationError)
async def redact_request_validation_input(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return useful validation locations without echoing credentials or fences."""
    errors = [
        {
            "type": error.get("type", "value_error"),
            "loc": list(error.get("loc", ())),
            "msg": error.get("msg", "Request validation failed"),
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": errors},
    )


@app.exception_handler(MaintenanceModeError)
async def maintenance_mode_error(
    request: Request, exc: MaintenanceModeError
) -> JSONResponse:
    """Keep hidden-write fences typed even when raised by a dependency."""
    del request
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": exc.detail()},
        headers={
            "Retry-After": str(exc.detail()["retry_after_seconds"]),
            "Cache-Control": "no-store",
        },
    )


@app.exception_handler(CollectionLimitExceededError)
async def collection_limit_error(
    request: Request, exc: CollectionLimitExceededError
) -> JSONResponse:
    """Refuse oversized synchronous graphs without silent truncation."""
    del request
    return JSONResponse(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        content={"detail": exc.detail()},
        headers={"Cache-Control": "no-store"},
    )


@app.exception_handler(DatabaseConflictError)
async def database_conflict_error(
    request: Request, exc: DatabaseConflictError
) -> JSONResponse:
    """Expose exhausted replay-safe conflicts without leaking DB details."""
    del request
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": {
                "code": "database_transaction_conflict",
                "message": str(exc),
            }
        },
        headers={"Cache-Control": "no-store"},
    )


@app.exception_handler(DatabaseUnavailableError)
async def database_unavailable_error(
    request: Request, exc: DatabaseUnavailableError
) -> JSONResponse:
    """Expose exhausted transient availability failures as retryable 503s."""
    del request
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": {
                "code": "database_unavailable",
                "message": str(exc),
            }
        },
        headers={"Cache-Control": "no-store", "Retry-After": "1"},
    )


@app.exception_handler(SQLAlchemyTimeoutError)
async def database_pool_timeout_error(
    request: Request, exc: SQLAlchemyTimeoutError
) -> JSONResponse:
    """Turn pool saturation into an observable retryable failure."""
    del request, exc
    metrics.increment("workchord_database_pool_timeouts_total")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": {
                "code": "database_pool_timeout",
                "message": "Database connection capacity is temporarily exhausted",
            }
        },
        headers={"Cache-Control": "no-store", "Retry-After": "1"},
    )


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RuntimeBoundaryMiddleware)

# Routers
app.include_router(calendars.router, prefix=settings.api_prefix, tags=["Calendars"])
app.include_router(iterations.router, prefix=settings.api_prefix, tags=["Iterations"])
app.include_router(team.router, prefix=settings.api_prefix, tags=["Team"])
app.include_router(tasks.router, prefix=settings.api_prefix, tags=["Tasks"])
app.include_router(projects.router, prefix=settings.api_prefix, tags=["Projects"])
app.include_router(gantt.router, prefix=settings.api_prefix, tags=["Gantt"])
app.include_router(github.router, prefix=settings.api_prefix, tags=["GitHub"])
app.include_router(intake.router, prefix=settings.api_prefix, tags=["Intake"])
app.include_router(llm.router, prefix=settings.api_prefix, tags=["LLM"])
app.include_router(export.router, prefix=settings.api_prefix, tags=["Export"])
app.include_router(snapshots.router, prefix=settings.api_prefix, tags=["Snapshots"])
app.include_router(session.router, prefix=settings.api_prefix, tags=["Session"])
app.include_router(scheduling_rules.router, prefix=settings.api_prefix, tags=["Scheduling Rules"])
app.include_router(email_settings.router, prefix=settings.api_prefix, tags=["Email Settings"])
app.include_router(agent.router, prefix=settings.api_prefix, tags=["Agent"])
app.include_router(agent_catalog.router, prefix=settings.api_prefix, tags=["Agent Catalog"])
app.include_router(agent_planning.router, prefix=settings.api_prefix, tags=["Agent Planning"])
app.include_router(
    agent_skill_bundles.router,
    prefix=settings.api_prefix,
    tags=["Agent Skill Bundles"],
)
app.include_router(
    agent_skill_bundles.well_known_router,
    tags=["Agent Skill Bundles"],
)
app.include_router(triage.router, prefix=settings.api_prefix, tags=["Triage"])
app.include_router(templates.router, prefix=settings.api_prefix, tags=["Templates"])
app.include_router(labels.router, prefix=settings.api_prefix, tags=["Labels"])
app.include_router(saved_views.router, prefix=settings.api_prefix, tags=["Saved Views"])
app.include_router(request_sources.router, prefix=settings.api_prefix, tags=["Request Sources"])
app.include_router(outbound_webhooks.router, prefix=settings.api_prefix, tags=["Outbound Webhooks"])
app.include_router(system_settings.router, prefix=settings.api_prefix, tags=["System Settings"])
mount_mcp_http(app, f"{settings.api_prefix}/mcp")


@app.get("/health")
async def health_check():
    """Backward-compatible process liveness endpoint."""
    return {"status": "ok", "maintenance": maintenance_state()}


@app.get("/health/live")
async def liveness_check():
    """Report only whether this process can service HTTP."""
    return {"status": "ok", "maintenance": maintenance_state()}


@app.get("/health/ready")
async def readiness_check():
    """Fail when the database is unavailable or not at packaged Alembic head."""
    ready, payload = await readiness_snapshot()
    return JSONResponse(status_code=200 if ready else 503, content=payload)


@app.get("/metrics", response_class=PlainTextResponse)
async def metrics_endpoint():
    """Export process/database qualification inputs without SQL or secrets."""
    await collect_metrics()
    return PlainTextResponse(
        metrics.render_prometheus(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
