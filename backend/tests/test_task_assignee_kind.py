"""Task responses say whether the assignee is a person or an agent, to every reader of the task."""

import pytest

from app.models.task import Task
from app.models.team_member import TeamMember
from tests.test_delivery_scenarios import delivery_store  # noqa: F401 - fixture used by managed_store
from tests.test_managed_authority import client, managed_store  # noqa: F401 - fixture
from tests.test_team_member_agent_connected import READERS, _assert_names_no_agent, _seed_agent_members


async def _assign_planned_task_to_the_connected_agent(factory, scenario):
    async with factory() as db:
        member = (await db.execute(
            TeamMember.__table__.select().where(TeamMember.name == "Connected agent"))).first()
        task = await db.get(Task, scenario.tasks["planned"])
        task.assignee_id = member.id
        await db.commit()


def _assignees(payload):
    rows = payload["items"] if isinstance(payload, dict) and "items" in payload else payload
    return {row["id"]: row["assignee"] for row in rows}


@pytest.mark.parametrize("reader", list(READERS))
async def test_every_reader_sees_the_assignee_kind_on_task_responses(managed_store, reader):
    factory, scenario, tokens, people = managed_store
    await _seed_agent_members(factory, scenario, people, workspace_member=reader != "project-only member")
    await _assign_planned_task_to_the_connected_agent(factory, scenario)
    planned, active, parent = scenario.tasks["planned"], scenario.tasks["active"], scenario.tasks["parent"]
    async with READERS[reader](tokens, scenario) as caller:
        listed = await caller.get(f"/api/iterations/{scenario.iterations[0]}/tasks")
        single = await caller.get(f"/api/tasks/{planned}")
        gantt = await caller.get(f"/api/iterations/{scenario.iterations[0]}/gantt")
    for response in (listed, single, gantt):
        assert response.status_code == 200, response.text
        _assert_names_no_agent(response.text)
        assert "connected-agent@example.test" not in response.text
    rows = _assignees(listed.json())
    assert rows[planned] == {"id": rows[planned]["id"], "name": "Connected agent", "kind": "agent"}
    assert rows[active]["kind"] == "human"
    assert rows[parent] is None
    assert single.json()["assignee"]["kind"] == "agent"
    gantt_rows = {row["id"]: row["assignee"] for row in gantt.json()["tasks"]}
    assert (gantt_rows[planned]["kind"], gantt_rows[active]["kind"]) == ("agent", "human")
