"""A work-metric count and the list it opens are chosen by the same predicate."""

from app.services.work_metrics import METRIC_MATCHES, aggregate_metrics
from tests.test_delivery_scenarios import delivery_store
from tests.test_managed_authority import client

COUNT_KEYS = {"total": "total_tasks", "implemented": "implemented_tasks", "accepted": "accepted_tasks", "blocked": "blocked_tasks",
              "overdue": "overdue_tasks", "late_start": "late_start_tasks", "iteration_overflow": "iteration_overflow_tasks",
              "acceptance_unknown": "acceptance_unknown_tasks", "unknown_estimate": "unknown_estimate_tasks"}


def expected(counts, metric):
    return counts["status_counts"][metric] if metric in counts["status_counts"] else counts[COUNT_KEYS[metric]]


async def test_every_metric_list_has_as_many_tasks_as_its_count(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        for scope in ({"project_id": scenario.projects[0]}, {"iteration_id": scenario.iterations[0]}):
            counts = await aggregate_metrics(db, **scope)
            assert counts["total_tasks"] > 0
            for metric in METRIC_MATCHES:
                matches = await aggregate_metrics(db, **scope, matching=metric, limit=500)
                assert len(matches["items"]) == expected(counts, metric), (scope, metric)
                assert matches["has_more"] is False


async def test_metric_matches_route_scopes_and_rejects_unknown_metrics(delivery_store):
    _, scenario, _ = delivery_store
    async with client() as browser:
        listed = await browser.get("/api/tasks/metric-matches", params={"metric": "total", "project_id": scenario.projects[0]})
        assert listed.status_code == 200, listed.text
        assert {"id", "title", "status", "project_name", "iteration_name"} <= set(listed.json()["items"][0])
        assert (await browser.get("/api/tasks/metric-matches", params={"metric": "everything", "project_id": scenario.projects[0]})).status_code == 422
        assert (await browser.get("/api/tasks/metric-matches", params={"metric": "total"})).status_code == 422
