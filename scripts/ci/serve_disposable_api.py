#!/usr/bin/env python3
"""Start the real HTTP application only against a safety-fenced temporary database."""

import asyncio
import os

import uvicorn
from fastapi import Request

from tests.support.database import assert_safe_test_database_url


def main():
    url = assert_safe_test_database_url(os.environ["DATABASE_URL"])
    if url.get_backend_name() != "sqlite":
        raise SystemExit("The browser harness requires its own temporary SQLite database")
    from app.services.upgrade_service import run_alembic_upgrade
    run_alembic_upgrade(backup=False, run_repairs=True)
    from app.database import async_session_maker, close_database
    from tests.support.delivery import seed_delivery_scenario
    dataset_counts = None

    async def seed():
        nonlocal dataset_counts
        async with async_session_maker() as db:
            scenario = await seed_delivery_scenario(db)
            if os.environ.get('WORKCHORD_FIXTURE_PERFORMANCE') == 'true':
                from datetime import date
                from app.models.iteration import Iteration
                from app.models.task import Task
                db.add(Iteration(id=3, name='Bounded HTTP sample', calendar_id=1, project_id=1,
                    start_date=date(2026, 1, 1), end_date=date(2026, 1, 20)))
                await db.flush()
                db.add_all([Task(title=f'HTTP large {i}', project_id=1, iteration_id=1, owner_profile_id=scenario.profile) for i in range(2501)])
                db.add_all([Task(title=f'HTTP bounded {i}', project_id=1, iteration_id=3, owner_profile_id=scenario.profile,
                    status=('planned', 'active', 'resolved')[i % 3]) for i in range(500)])
                await db.commit()
                from sqlalchemy import select, func
                dataset_counts = {'actual_task_count': await db.scalar(select(func.count()).select_from(Task)),
                    'large_iteration_tasks': 2501, 'bounded_iteration_tasks': 500, 'initial_seed_tasks': 8}
                if dataset_counts['actual_task_count'] != 3009:
                    raise RuntimeError('HTTP fixture differs from declared workload')
            if os.environ.get("WORKCHORD_AUTH_MODE") == "managed":
                from app.models.task import Task
                for name in ("planned", "active", "resolved", "closed_urgent", "closed_low", "nested", "other_project"):
                    task = await db.get(Task, scenario.tasks[name])
                    task.owner_profile_id = scenario.profile
                    task.ownership_provenance = "explicit"
                from app.models.identity import Principal, IdentitySubject, ProjectMembership, PrincipalProfileLink
                for index, name in enumerate(["alice", "bob", "charlie"]):
                    principal = Principal(kind="human", display_name=name.title())
                    db.add(principal)
                    await db.flush()
                    db.add(IdentitySubject(principal_id=principal.id, issuer=os.environ.get("WORKCHORD_FIXTURE_ISSUER", "http://oidc:8002"), subject=name))
                    db.add(ProjectMembership(principal_id=principal.id, project_id=scenario.projects[index if index < 2 else 0], role="manager" if index < 2 else "reviewer"))
                    if index == 0:
                        db.add(PrincipalProfileLink(principal_id=principal.id, profile_id=scenario.profile, linked_by_principal_id=principal.id))
                if os.environ.get('WORKCHORD_FIXTURE_PLANNING') == 'true':
                    from app.models.identity import WorkspaceMembership
                    operator = Principal(kind='human', display_name='Dora')
                    db.add(operator); await db.flush()
                    db.add(IdentitySubject(principal_id=operator.id, issuer=os.environ.get('WORKCHORD_FIXTURE_ISSUER', 'http://oidc:8002'), subject='dora'))
                    db.add(WorkspaceMembership(principal_id=operator.id, role='owner'))
                await db.commit()
        await close_database()

    asyncio.run(seed())
    from app.main import app
    nonce = os.environ.get("WORKCHORD_FIXTURE_NONCE")
    if nonce:
        from fastapi import HTTPException
        from fastapi.responses import JSONResponse
        import time
        faults = {}

        @app.get('/api/tasks/{task_id}/_fixture/dataset')
        async def dataset(request: Request, task_id: int):
            if request.headers.get('X-Fixture-Key') != nonce or dataset_counts is None or task_id != 1:
                raise HTTPException(404)
            return dataset_counts

        @app.post("/api/tasks/{task_id}/_fixture/read-fault")
        async def read_fault(request: Request, task_id: int):
            if request.headers.get("X-Fixture-Key") != nonce:
                raise HTTPException(403)
            body = await request.json()
            if not isinstance(body, dict):
                raise HTTPException(422)
            status = body.get("status")
            if body.get("task_id") != task_id:
                raise HTTPException(422)
            if type(task_id) is not int or not 0 < task_id <= 2147483647 or status not in {0, 403, 404, 503}:
                raise HTTPException(422)
            faults.clear()
            faults[task_id] = (status, time.monotonic() + 30)
            return {"configured": True}

        @app.middleware("http")
        async def identify_fixture(request, call_next):
            segments = request.url.path.split("/")
            task_id = int(segments[3]) if len(segments) >= 4 and segments[1:3] == ["api", "tasks"] and segments[3].isdigit() else None
            status, expires = faults.get(task_id, (0, 0))
            if request.method == "GET" and status and time.monotonic() < expires:
                response = JSONResponse({"detail": "Disposable injected read failure"}, status_code=status)
            else:
                response = await call_next(request)
            response.headers["X-WorkChord-Fixture"] = nonce
            return response
    if os.environ.get("WORKCHORD_AUTH_MODE") == "managed":
        import subprocess
        import sys
        from pathlib import Path
        provider = subprocess.Popen([sys.executable, str(Path(__file__).with_name("serve_disposable_oidc.py"))])
        try:
            uvicorn.run(app, host=os.environ.get("WORKCHORD_FIXTURE_BIND", "127.0.0.1"), port=8001, access_log=False)
        finally:
            provider.terminate()
            provider.wait(timeout=10)
    else:
        uvicorn.run(app, host=os.environ.get("WORKCHORD_FIXTURE_BIND", "127.0.0.1"), port=8001)


if __name__ == "__main__":
    main()
