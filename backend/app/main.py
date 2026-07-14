import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import async_session_maker, init_db
from app.routers import agent, agent_catalog, agent_planning, agent_skill_bundles, calendars, iterations, team, tasks, projects, gantt, github, intake, llm, export, snapshots, session, scheduling_rules, email_settings, triage, templates, labels, saved_views, request_sources, outbound_webhooks, system_settings
from app.mcp_server import mcp, mount_mcp_http
from app.services.github_status_automation_service import GitHubStatusAutomationService
from app.services.label_service import LabelService
from app.services.outbound_webhook_service import outbound_delivery_worker_loop
from app.services.saved_view_service import SavedViewService
from app.services.system_settings_service import RuntimeSettingsService
from app.services.template_service import TemplateService

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    async with mcp.session_manager.run():
        # Startup
        await init_db()
        async with async_session_maker() as db:
            await TemplateService(db).seed_default_templates()
            await LabelService(db).seed_default_labels()
            await SavedViewService(db).seed_default_views()
            await GitHubStatusAutomationService(db).seed_default_rules()
            await RuntimeSettingsService(db).migrate_legacy_email_settings()
        delivery_stop = asyncio.Event()
        delivery_worker = None
        if settings.outbound_delivery_worker_enabled:
            delivery_worker = asyncio.create_task(
                outbound_delivery_worker_loop(
                    delivery_stop,
                    poll_seconds=settings.outbound_delivery_poll_seconds,
                    batch_size=settings.outbound_delivery_batch_size,
                ),
                name="outbound-delivery-worker",
            )
        try:
            yield
        finally:
            delivery_stop.set()
            if delivery_worker is not None:
                await delivery_worker


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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    """Health check endpoint."""
    return {"status": "ok"}
