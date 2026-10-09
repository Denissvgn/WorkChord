# ProjectService__portfolio_summaries

**Entry point:** `project_service.ProjectService._portfolio_summaries`
**Modules involved:** [project_service](../modules/project_service.md), [schemas_project](../modules/schemas_project.md), [services_work_metrics](../modules/services_work_metrics.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `services_work_metrics.aggregate_metrics`
3. `schemas_project.ProjectPortfolioSummary`

## Touches

- [project_service](../modules/project_service.md)
- [schemas_project](../modules/schemas_project.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `project_service.ProjectService._portfolio_summaries`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
