"""A worker may declare the harness session that ran it; the shape is checked, the value is not verified."""

import pytest
from pydantic import ValidationError

from app.schemas.agent import AgentRunCreate, AgentWorkBegin, ModelAwareAgentWorkBegin


def begins(metadata):
    return [
        lambda: AgentWorkBegin(assignment_id=1, queue_revision=1, metadata=metadata),
        lambda: ModelAwareAgentWorkBegin(assignment_id=1, queue_revision=1, model_binding_id=1,
                                         model_binding_revision=1, resolved_model_id="model-a", metadata=metadata),
        lambda: AgentRunCreate(task_id=1, metadata=metadata),
    ]


@pytest.mark.parametrize("session_id", ["7f3c2a10-5b6e-4d1a-9c2f-0e8b1a2c3d4e", "thread_01J9ZK"])
def test_a_declared_harness_session_is_kept_with_the_run_metadata(session_id):
    metadata = {"harness": {"kind": "claude-code", "session_id": session_id}, "note": "safe"}
    for build in begins(metadata):
        assert build().metadata == metadata


def test_metadata_without_a_harness_is_unchanged():
    for build in begins({"anything": {"nested": True}}):
        assert build().metadata == {"anything": {"nested": True}}


@pytest.mark.parametrize("harness", [
    "claude-code:7f3c",
    {"kind": "claude-code"},
    {"kind": "claude-code", "session_id": "7f3c", "path": "/home/me/.claude"},
    {"kind": "Claude Code", "session_id": "7f3c"},
    {"kind": "claude-code", "session_id": ""},
    {"kind": "claude-code", "session_id": "/home/me/.claude/projects/x/7f3c.jsonl"},
    {"kind": "claude-code", "session_id": "C:\\\\Users\\\\me\\\\session"},
    {"kind": "claude-code", "session_id": "x" * 256},
    {"kind": "claude-code", "session_id": "pmag_" + "a" * 40},
])
def test_a_malformed_or_secret_harness_is_refused(harness):
    for build in begins({"harness": harness}):
        with pytest.raises(ValidationError):
            build()
