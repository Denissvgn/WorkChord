"""The shared workflow vocabulary is rendered identically into every role skill."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from scripts import build_agent_skills


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPOSITORY_ROOT / "agent-skills"


def _copy_vocabulary(tmp_path: Path, mutate=None) -> Path:
    vocabulary = json.loads(
        (REPOSITORY_ROOT / build_agent_skills.WORKFLOW_VOCABULARY_SOURCE).read_text(
            encoding="utf-8"
        )
    )
    if mutate is not None:
        mutate(vocabulary)
    target = tmp_path / build_agent_skills.WORKFLOW_VOCABULARY_SOURCE
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(vocabulary, ensure_ascii=False), encoding="utf-8")
    return tmp_path


def test_every_role_carries_the_current_generated_vocabulary() -> None:
    expected = build_agent_skills.render_workflow_vocabulary_markdown(
        build_agent_skills.load_workflow_vocabulary(REPOSITORY_ROOT)
    )
    for role_name in build_agent_skills.ROLE_METADATA:
        reference = SKILLS_ROOT / role_name / build_agent_skills.WORKFLOW_VOCABULARY_REFERENCE
        text = reference.read_text(encoding="utf-8")
        assert expected in text, role_name
        skill = (SKILLS_ROOT / role_name / "SKILL.md").read_text(encoding="utf-8")
        assert build_agent_skills.WORKFLOW_VOCABULARY_REFERENCE in skill, role_name


def test_vocabulary_names_every_agent_role_once() -> None:
    vocabulary = build_agent_skills.load_workflow_vocabulary(REPOSITORY_ROOT)
    code_roles = [role["code_role"] for role in vocabulary["roles"]]
    assert sorted(code_roles) == ["pm", "verifier", "worker"]
    names = {role["code_role"]: role["name"]["en"] for role in vocabulary["roles"]}
    assert names == {"pm": "PM", "worker": "Worker", "verifier": "Reviewer"}


def test_pipeline_response_has_exactly_the_vocabulary_stages_in_order() -> None:
    from app.schemas.agent import AgentPipelineResponse

    vocabulary = build_agent_skills.load_workflow_vocabulary(REPOSITORY_ROOT)
    stage_ids = [stage["id"] for stage in vocabulary["pipeline_stages"]]
    assert list(AgentPipelineResponse.model_fields) == stage_ids
    assert all(field.is_required() for field in AgentPipelineResponse.model_fields.values())
    for stage in vocabulary["pipeline_stages"]:
        assert "pick" not in stage["description"]["en"].lower()


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda v: v.update(schema_version="other/v1"), "Unsupported workflow vocabulary schema"),
        (lambda v: v["roles"][0]["name"].pop("ru"), "needs exactly"),
        (lambda v: v["actions"].append(dict(v["actions"][0])), "Duplicate workflow vocabulary id"),
        (lambda v: v["terms"][0].update(means="a | b"), "must not contain"),
        (lambda v: v["queues"][0].update(extra="x"), "unknown fields"),
        (lambda v: v.update(stages=[]), "must contain exactly"),
    ],
)
def test_invalid_vocabulary_is_rejected(tmp_path: Path, mutate, message: str) -> None:
    root = _copy_vocabulary(tmp_path, mutate)
    with pytest.raises(build_agent_skills.SkillPackError, match=message):
        build_agent_skills.load_workflow_vocabulary(root)


def test_stale_generated_vocabulary_is_rejected(tmp_path: Path) -> None:
    root = _copy_vocabulary(
        tmp_path, lambda v: v["roles"][2]["name"].update(en="Verifier")
    )
    skills = tmp_path / "agent-skills"
    shutil.copytree(SKILLS_ROOT, skills)
    for relative in build_agent_skills.ASSIGNED_WORK_CONTRACT_DOCUMENTS:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPOSITORY_ROOT / relative, target)
    with pytest.raises(build_agent_skills.SkillPackError, match="Shared workflow vocabulary drift"):
        build_agent_skills.validate_generated_skill_sources(root, skills)
