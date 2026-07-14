"""Scheduling rules schemas for API."""
from typing import Optional

from pydantic import BaseModel, Field


class SortCriterionSchema(BaseModel):
    """A single sort criterion."""
    field: str = Field(..., description="Field to sort by (e.g., 'priority', 'adjusted_effort')")
    order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'")


class FilterConfigSchema(BaseModel):
    """Filter configuration with conditions."""
    all: list[str] = Field(default_factory=list, description="All conditions must match (AND)")


class SchedulingPassSchema(BaseModel):
    """A scheduling pass with filter and sort rules."""
    id: str = Field(..., min_length=1, description="Unique identifier for this pass")
    description: str = Field(default="", description="Human-readable description")
    enabled: bool = Field(default=True, description="Whether this pass is active")
    filter: FilterConfigSchema = Field(default_factory=FilterConfigSchema)
    sort: list[SortCriterionSchema] = Field(default_factory=list)


class EffortModifierSchema(BaseModel):
    """An effort modifier rule."""
    id: str = Field(..., min_length=1, description="Unique identifier")
    enabled: bool = Field(default=True, description="Whether this modifier is active")
    formula: Optional[str] = Field(default=None, description="Formula expression (e.g., 'effort / coefficient')")
    operation: Optional[str] = Field(default=None, pattern="^(ceil|floor|round)$", description="Math operation")
    fallback: str = Field(default="effort", description="Fallback expression if formula fails")
    min_value: Optional[float] = Field(default=None, ge=0, description="Minimum result value")


class BalanceWorkloadSchema(BaseModel):
    """Workload balancing configuration."""
    enabled: bool = Field(default=False, description="Enable workload balancing")
    max_overload_percent: float = Field(default=10, ge=0, le=100, description="Maximum allowed overload percentage")


class ConstraintsSchema(BaseModel):
    """Scheduling constraints configuration."""
    sequential_per_assignee: bool = Field(default=True, description="Tasks of same assignee don't overlap")
    respect_dependencies: bool = Field(default=True, description="Honor task dependencies")
    min_start_date: bool = Field(default=True, description="Respect task.min_start_date if set")
    max_finish_date: bool = Field(default=True, description="Respect task deadlines")
    prefer_uninterrupted: bool = Field(default=True, description="Prefer slots without vacation interruption")
    balance_workload: Optional[BalanceWorkloadSchema] = Field(default=None, description="Workload balancing settings")


class SchedulingRulesSchema(BaseModel):
    """Complete scheduling rules configuration."""
    schema_version: str = Field(default="1.0", description="Configuration schema version")
    effort_modifiers: list[EffortModifierSchema] = Field(default_factory=list)
    scheduling_passes: list[SchedulingPassSchema] = Field(default_factory=list)
    constraints: ConstraintsSchema = Field(default_factory=ConstraintsSchema)

    class Config:
        from_attributes = True


class SchedulingRulesResponse(BaseModel):
    """Response wrapper for scheduling rules."""
    rules: SchedulingRulesSchema
    source: str = Field(..., description="Source of rules: 'yaml', 'database', or 'defaults'")
