"""Response of a plan-import dry run."""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ImportChangeRows(BaseModel):
    """Rows the import creates, changes and removes.

    A row the import creates is named by a stable reference such as ``new-task-1``;
    existing rows keep their ids.
    """

    created: list[dict[str, Any]] = Field(default_factory=list)
    changed: list[dict[str, Any]] = Field(default_factory=list)
    removed: list[dict[str, Any]] = Field(default_factory=list)


class ImportDependencyRows(BaseModel):
    created: list[dict[str, Any]] = Field(default_factory=list)
    removed: list[dict[str, Any]] = Field(default_factory=list)


class ImportProfileRows(BaseModel):
    created: list[dict[str, Any]] = Field(default_factory=list)


class ImportChanges(BaseModel):
    iteration: Optional[dict[str, Any]] = None
    tasks: ImportChangeRows
    dependencies: ImportDependencyRows
    links: ImportChangeRows
    dates: list[dict[str, Any]]
    team_members: ImportChangeRows
    profiles: ImportProfileRows


class ImportDryRunResponse(BaseModel):
    """The exact change set of one import file; nothing was written."""

    target_iteration_id: Optional[int]
    file_sha256: str
    expected_revisions: dict[str, int]
    changes: ImportChanges
    summary: dict[str, int]
    review_digest: str
    written: Literal[False]
