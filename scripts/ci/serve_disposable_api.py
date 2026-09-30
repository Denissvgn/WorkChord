#!/usr/bin/env python3
"""Start the real HTTP application only against a safety-fenced temporary database."""

import asyncio
import os

import uvicorn

from tests.support.database import assert_safe_test_database_url


def main():
    url = assert_safe_test_database_url(os.environ["DATABASE_URL"])
    if url.get_backend_name() != "sqlite":
        raise SystemExit("The browser harness requires its own temporary SQLite database")
    from app.services.upgrade_service import run_alembic_upgrade
    run_alembic_upgrade(backup=False, run_repairs=True)
    from app.database import async_session_maker, close_database
    from tests.support.delivery import seed_delivery_scenario

    async def seed():
        async with async_session_maker() as db:
            scenario = await seed_delivery_scenario(db)
            if os.environ.get("WORKCHORD_AUTH_MODE") == "managed":
                from app.models.identity import Principal, IdentitySubject, ProjectMembership, PrincipalProfileLink
                for index, name in enumerate(["alice", "bob", "charlie"]):
                    principal = Principal(kind="human", display_name=name.title())
                    db.add(principal)
                    await db.flush()
                    db.add(IdentitySubject(principal_id=principal.id, issuer=os.environ.get("WORKCHORD_FIXTURE_ISSUER", "http://oidc:8002"), subject=name))
                    db.add(ProjectMembership(principal_id=principal.id, project_id=scenario.projects[index if index < 2 else 0], role="manager" if index < 2 else "reviewer"))
                    if index == 0:
                        db.add(PrincipalProfileLink(principal_id=principal.id, profile_id=scenario.profile, linked_by_principal_id=principal.id))
                await db.commit()
        await close_database()

    asyncio.run(seed())
    from app.main import app
    nonce = os.environ.get("WORKCHORD_FIXTURE_NONCE")
    if nonce:
        @app.middleware("http")
        async def identify_fixture(request, call_next):
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
