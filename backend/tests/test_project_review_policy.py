"""Project editors can round-trip the current policy. Changes need an operator."""
import pytest
from sqlalchemy import insert, update

from app.authority import Authority, AuthorityError
from app.models.project import Project
from tests.test_managed_authority import client, managed_store
from tests.test_delivery_scenarios import delivery_store


async def test_editor_round_trips_publisher_policy_and_operator_changes_it(managed_store):
    _, scenario, tokens, _ = managed_store
    path = f"/api/projects/{scenario.projects[0]}"
    headers = {"X-CSRF-Token": "csrf-0", "Origin": "https://test"}
    async with client(tokens[0], **headers) as editor, client(**{"X-Admin-API-Key": "managed-operator-fixture"}) as operator:
        for strict in (False, True):
            configured = await operator.put(path, json={"require_different_review_publisher": strict})
            assert configured.status_code == 200
            assert configured.json()["require_different_review_publisher"] is strict
            for value in ({"require_different_review_publisher": strict}, {"require_different_review_publisher": None}, {}):
                response = await editor.put(path, json={"description": f"Independent review {strict}", **value})
                assert response.status_code == 200
                assert response.json()["require_different_review_publisher"] is strict
            denied = await editor.put(path, json={"require_different_review_publisher": not strict})
            assert denied.status_code == 403
            assert (await editor.get(path)).json()["require_different_review_publisher"] is strict


async def test_project_policy_needs_operator_at_the_managed_write_boundary(managed_store):
    factory, scenario, _, principals = managed_store
    project_id = scenario.projects[0]
    editor = Authority(principals[0], "human", projects={project_id: "manager"})
    async with factory() as db:
        db.info["authority"] = editor
        current = await db.get(Project, project_id)
        assert current.require_different_review_publisher is False
        current.description = "Ordinary project metadata"
        await db.commit()
        current.require_different_review_publisher = True
        with pytest.raises(AuthorityError, match="operator"):
            await db.flush()
        await db.rollback()
        db.add(Project(name="Imported strict project", require_different_review_publisher=True))
        with pytest.raises(AuthorityError, match="operator"):
            await db.flush()
        await db.rollback()
        for statement in (
            update(Project).where(Project.id == project_id).values(require_different_review_publisher=True),
            insert(Project).values(name="Strict project", require_different_review_publisher=True),
        ):
            with pytest.raises(AuthorityError, match="operator"):
                await db.execute(statement)
        assert (await db.get(Project, project_id)).require_different_review_publisher is False
    async with factory() as db:
        db.info["authority"] = Authority(principals[0], "human", workspace_role="owner")
        project = await db.get(Project, project_id)
        project.require_different_review_publisher = True
        await db.commit()
    async with factory() as db:
        db.info["authority"] = editor
        project = await db.get(Project, project_id)
        assert project.require_different_review_publisher is True
        project.require_different_review_publisher = False
        with pytest.raises(AuthorityError, match="operator"):
            await db.flush()
