"""Worker-reported usage, immutable pricing snapshots and explicit coverage."""

from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

Quantity = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=6, allow_inf_nan=False)]
Money = Annotated[Decimal, Field(ge=0, max_digits=24, decimal_places=12, allow_inf_nan=False)]


class UsagePricingBasis(BaseModel):
    model_config = ConfigDict(extra="forbid")
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    unit: str = Field(min_length=1, max_length=64, pattern=r"^[a-z][a-z0-9_]*$")
    price_amount: Money
    price_quantity: Decimal = Field(gt=0, max_digits=18, decimal_places=6, allow_inf_nan=False)
    version: str = Field(min_length=1, max_length=128)
    source: str = Field(min_length=1, max_length=500)
    quoted_at: AwareDatetime


class ExecutionUsageWrite(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_id: str = Field(min_length=1, max_length=128, pattern=r"^[a-zA-Z0-9_.:-]+$")
    expected_previous_digest: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    source: str = Field(min_length=1, max_length=200)
    provenance: Literal["provider_reported", "runtime_metered", "manual_reported", "simulated"]
    reporting_mode: Literal["attempt_total"]
    interval_start: AwareDatetime
    interval_end: AwareDatetime
    coverage: Literal["complete", "partial", "unavailable"]
    quantities: dict[str, Quantity | None] = Field(default_factory=dict, max_length=30)
    reported_cost: Money | None = None
    currency: str | None = Field(default=None, pattern=r"^[A-Z]{3}$")
    pricing_basis: UsagePricingBasis | None = None
    reported_human_effort_minutes: Quantity | None = None

    @model_validator(mode="after")
    def validate_report(self):
        if self.interval_end < self.interval_start:
            raise ValueError("Usage interval end must not precede its start")
        if any(not key or len(key) > 64 or not key.replace("_", "").isalnum() or not key.isascii() for key in self.quantities):
            raise ValueError("Usage unit names must be bounded ASCII identifiers")
        if self.reported_cost is not None and self.currency is None:
            raise ValueError("A reported cost requires its currency")
        measured = (self.reported_cost is not None or self.reported_human_effort_minutes is not None
                    or any(value is not None for value in self.quantities.values()))
        if self.coverage == "complete" and not measured:
            raise ValueError("Complete coverage requires an explicitly reported quantity, cost or human effort")
        if self.coverage == "unavailable" and measured:
            raise ValueError("Unavailable usage must not contain measured values")
        if self.pricing_basis is not None and self.pricing_basis.unit not in self.quantities:
            raise ValueError("Pricing basis must name a reported unit")
        if self.reported_human_effort_minutes is not None and self.provenance not in {"manual_reported", "simulated"}:
            raise ValueError("Human effort requires an explicit manual-report source")
        return self


class ExecutionUsageResponse(BaseModel):
    id: int
    original_run_id: int
    original_task_id: int
    sequence: int
    digest: str
    previous_digest: str | None
    report: ExecutionUsageWrite
    reported_at: datetime
    scope_basis: str = "scope_at_first_report"
    independently_reconciled: Literal[False] = False


class ExecutionUsageSummary(BaseModel):
    window_start: datetime
    window_end: datetime
    window_basis: str = "run_start_or_report_receipt"
    expected_runs: int
    reported_runs: int
    unreported_runs: int
    partial_reports: int
    unavailable_reports: int
    simulated_reports: int
    provider_reported_cost: dict[str, Decimal | None]
    estimated_cost: dict[str, Decimal | None]
    known_cost_reports: dict[str, int]
    unknown_cost_reports: int
    accepted_task_identities: int
    reports_linked_to_accepted_tasks: int
    reported_human_effort_minutes: Decimal | None
    human_effort_reports: int
    linked_delivery: dict = Field(default_factory=dict)
    reported_units: dict[str, Decimal | None] = Field(default_factory=dict)
    unit_report_counts: dict[str, int] = Field(default_factory=dict)
    simulated_reported_cost: dict[str, Decimal] = Field(default_factory=dict)
    simulated_estimated_cost: dict[str, Decimal] = Field(default_factory=dict)
    simulated_units: dict[str, Decimal | None] = Field(default_factory=dict)
    measured_report_count: int = 0
    advisory_budget: dict | None = None
    scope_basis: str = "scope_at_first_report"
    independently_reconciled: Literal[False] = False
