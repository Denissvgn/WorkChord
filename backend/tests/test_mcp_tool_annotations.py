"""Every MCP tool tells clients whether it reads, writes, or removes.

A client running with nobody to approve calls refuses a tool it has to assume
is destructive, so a tool that declares nothing is unusable there.
"""

from __future__ import annotations

import re

import pytest

from app.mcp_server import mcp

READ_NAME = re.compile(r"^(?:(?:agent|workspace|system)_(?:get|list|search|preview|draft)_|recommendations_for_)")
REMOVAL_TOOLS = {
    "agent_delete_project_milestone",
    "workspace_delete_external_link",
    "workspace_unlink_request_source",
}


def needs_approval(annotations) -> bool:
    """The rule unattended clients apply: an unset hint counts as the unsafe value."""
    if annotations is None:
        return True
    if annotations.destructiveHint is True:
        return True
    if annotations.readOnlyHint is True:
        return False
    return annotations.destructiveHint is not False or annotations.openWorldHint is not False


@pytest.fixture
async def tools():
    return {tool.name: tool for tool in await mcp.list_tools()}


async def test_every_tool_declares_how_it_behaves(tools) -> None:
    undeclared = sorted(
        name
        for name, tool in tools.items()
        if tool.annotations is None
        or tool.annotations.readOnlyHint is None
        or tool.annotations.openWorldHint is not False
        or (tool.annotations.readOnlyHint is False and tool.annotations.destructiveHint is None)
    )

    assert undeclared == []


async def test_read_tools_are_declared_read_only_and_nothing_else_is(tools) -> None:
    declared_read_only = {name for name, tool in tools.items() if tool.annotations.readOnlyHint}

    assert declared_read_only == {name for name in tools if READ_NAME.match(name)}


async def test_only_tools_that_remove_a_record_are_declared_destructive(tools) -> None:
    declared_destructive = {name for name, tool in tools.items() if tool.annotations.destructiveHint}

    assert declared_destructive == REMOVAL_TOOLS


async def test_an_unattended_client_can_run_everything_except_removals(tools) -> None:
    refused = {name for name, tool in tools.items() if needs_approval(tool.annotations)}

    assert refused == REMOVAL_TOOLS
    for name in ("agent_get_capabilities", "agent_get_my_work", "agent_begin_my_work", "agent_submit_my_work"):
        assert name not in refused


async def test_annotations_reach_the_wire_format(tools) -> None:
    wire = tools["agent_begin_my_work"].model_dump(mode="json", by_alias=True, exclude_none=True)

    assert wire["annotations"] == {"readOnlyHint": False, "destructiveHint": False, "openWorldHint": False}
