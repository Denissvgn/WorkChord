"""A late start moves each planned dependent once, however many paths reach it."""

from collections import Counter
from datetime import date, timedelta
import json

import httpx
from sqlalchemy import select

from app.main import app
from app.models.agent import TaskEvent
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.services.task_service import TaskService
from tests.test_delivery_scenarios import delivery_store  # noqa: F401

# The source was planned well before any working day the clock can report, so
# starting it now always moves its forecast later by a positive delay.
PLANNED_START = date(2026, 1, 2)
LATER_START = date(2026, 2, 2)
LAYERS = 4
WIDTH = 3


async def _seed_lattice(factory, scenario):
    """Create a source and LAYERS x WIDTH tasks, each depending on the whole layer before it.

    The last layer is reached by WIDTH ** (LAYERS - 1) distinct paths per task.
    """
    async with factory() as db:
        tasks = TaskService(db)

        async def create(title: str, depends_on: list[int], start: date) -> Task:
            task = await tasks.create(scenario.iterations[0], TaskCreate(
                title=title, project_id=scenario.projects[0], effort_hours=8, depends_on=depends_on,
            ))
            task.start_date = task.end_date = start
            return task

        source = await create("Source", [], PLANNED_START)
        previous = [source.id]
        layers: list[list[int]] = []
        for layer in range(LAYERS):
            created = [
                await create(f"Layer {layer} task {index}", previous, LATER_START + timedelta(days=layer))
                for index in range(WIDTH)
            ]
            previous = [task.id for task in created]
            layers.append(previous)
        await db.commit()
        return source.id, source.version, layers


async def test_late_start_moves_every_reachable_planned_task_exactly_once(delivery_store):
    factory, scenario, _ = delivery_store
    source_id, version, layers = await _seed_lattice(factory, scenario)
    dependents = [task_id for layer in layers for task_id in layer]

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put(
            f"/api/tasks/{source_id}/status", json={"status": "active", "expected_version": version}
        )
        assert response.status_code == 200, response.text
        history = await client.get(f"/api/tasks/{source_id}/status-history")
        assert history.status_code == 200, history.text

    async with factory() as db:
        source = await db.get(Task, source_id)
        delay = source.end_date - PLANNED_START
        assert delay > timedelta(0)
        for layer_index, layer in enumerate(layers):
            expected = LATER_START + timedelta(days=layer_index) + delay
            for task_id in layer:
                task = await db.get(Task, task_id)
                assert (task.start_date, task.end_date) == (expected, expected), task.title
        cascaded = Counter(
            (await db.scalars(select(TaskEvent.task_id).where(
                TaskEvent.event_type == "dates_cascaded", TaskEvent.task_id.in_(dependents)
            ))).all()
        )
        assert cascaded == Counter({task_id: 1 for task_id in dependents})

    entry = next(item for item in history.json() if item["to_status"] == "active")
    assert sorted(entry["affected_task_ids"]) == sorted(dependents)


async def test_each_dependent_names_the_predecessor_it_was_reached_through(delivery_store):
    factory, scenario, _ = delivery_store
    source_id, version, layers = await _seed_lattice(factory, scenario)

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put(
            f"/api/tasks/{source_id}/status", json={"status": "active", "expected_version": version}
        )
        assert response.status_code == 200, response.text

    async with factory() as db:
        for layer_index, layer in enumerate(layers):
            allowed = {source_id} if layer_index == 0 else set(layers[layer_index - 1])
            for task_id in layer:
                event = (await db.scalars(select(TaskEvent).where(
                    TaskEvent.event_type == "dates_cascaded", TaskEvent.task_id == task_id
                ))).one()
                assert json.loads(event.payload)["source_task_id"] in allowed
