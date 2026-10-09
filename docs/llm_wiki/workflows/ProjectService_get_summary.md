# ProjectService_get_summary

**Entry point:** `project_service.ProjectService.get_summary`
**Modules involved:** [project_service](../modules/project_service.md), [request_source_service](../modules/request_source_service.md), [schemas_project](../modules/schemas_project.md), [services_work_metrics](../modules/services_work_metrics.md), [time](../modules/time.md)

> Calculate project task summary metrics.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `services_work_metrics.working_today`
3. `services_work_metrics.working_today`
4. `request_source_service.RequestSourceService`
5. `schemas_project.ProjectSummary`

## Touches

- [project_service](../modules/project_service.md)
- [request_source_service](../modules/request_source_service.md)
- [schemas_project](../modules/schemas_project.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `project_service.ProjectService.get_summary`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
