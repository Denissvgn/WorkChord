"""Delivery duration samples and queues with explicit observation coverage."""

from datetime import datetime
from pydantic import BaseModel, Field


class DurationSamples(BaseModel):
    unit: str = "elapsed_seconds"
    sample_count: int = 0
    mean: float | None = None
    median: float | None = None
    censored_count: int = 0
    unknown_count: int = 0


class DeliveryQueueItem(BaseModel):
    task_id: int
    title: str
    reason: str
    age_seconds: float | None


class DeliveryMetricsResponse(BaseModel):
    contract_version: int = 1
    window_start: datetime
    window_end: datetime
    scope_basis: str = "scope_at_observation"
    accepted_leaf_tasks: int = 0
    acceptance_events: int = 0
    rejection_events: int = 0
    canceled_leaf_tasks: int = 0
    reopened_events: int = 0
    lead_time: DurationSamples
    cycle_time: DurationSamples
    review_delay: DurationSamples
    coverage: dict[str, int | str] = Field(default_factory=dict)
    review_queue: list[DeliveryQueueItem] = Field(default_factory=list)
    recovery_queue: list[DeliveryQueueItem] = Field(default_factory=list)
    queues_truncated: bool = False
