"""Shared additive delivery metrics; legacy completed fields mean implemented work."""

from pydantic import BaseModel


class WorkMetricSummary(BaseModel):
    metric_contract_version: int = 2
    required_tasks: int = 0
    optional_tasks: int = 0
    deferred_tasks: int = 0
    structural_tasks: int = 0
    implemented_tasks: int = 0
    accepted_tasks: int = 0
    required_implemented_tasks: int = 0
    required_accepted_tasks: int = 0
    late_start_tasks: int = 0
    iteration_overflow_tasks: int = 0
    project_target_overflow_tasks: int = 0
    acceptance_unknown_tasks: int = 0
    unknown_estimate_tasks: int = 0
    accepted_percent: float = 0.0


class TaskMetricSignals(BaseModel):
    effective_is_deferred: bool = False
    effective_is_optional: bool = False
    metric_contract_version: int = 2
    is_late_start: bool = False
    is_iteration_overflow: bool = False
    is_project_target_overflow: bool = False
    is_implemented: bool = False
    is_accepted: bool = False
    acceptance_unknown: bool = False
