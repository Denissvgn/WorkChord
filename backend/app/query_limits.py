"""Explicit response cardinality bounds for synchronous API surfaces."""

from __future__ import annotations


MAX_ITERATION_TREE_TASKS = 2_500
MAX_PROJECT_TREE_TASKS = 2_500
MAX_BOUNDED_LIST_ITEMS = 500
MAX_ITERATION_LIST_ITEMS = MAX_BOUNDED_LIST_ITEMS
MAX_PROJECT_LIST_ITEMS = MAX_BOUNDED_LIST_ITEMS
MAX_SYNC_EXPORT_TASKS = 5_000


class CollectionLimitExceededError(RuntimeError):
    """A synchronous endpoint would exceed its documented response bound."""

    def __init__(self, resource: str, maximum: int):
        self.resource = resource
        self.maximum = maximum
        super().__init__(
            f"{resource} exceeds the synchronous response limit of {maximum}; "
            "use a summary or bounded export workflow"
        )

    def detail(self) -> dict[str, object]:
        return {
            "code": "collection_limit_exceeded",
            "message": str(self),
            "resource": self.resource,
            "maximum": self.maximum,
        }
