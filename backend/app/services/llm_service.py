"""LLM service for task formalization and schedule explanation."""
from collections import Counter
from dataclasses import dataclass
import json
import logging
import re
from typing import Any, Optional

import httpx

from app.config import get_settings
from app.schemas.llm import (
    FormalizeResponse, SuggestedSubtask,
    ImproveDescriptionResponse,
    ExplainScheduleResponse, ScheduleDecisionExplanation, WorkloadAnalysis,
    GroundedAISuggestionResponse, GroundedFact,
)
from app.schemas.gantt import SchedulingDecision, WorkloadIssue
from app.schemas.triage import TriageClassificationDraft, TriageTaskDraftResponse
from app.services.language_service import (
    AILanguageMode,
    LanguageCode,
    language_instruction,
    localized,
    normalize_ai_language_mode,
    normalize_language,
    resolve_ai_language,
)
from app.utils.url_policy import normalize_provider_api_url


DEFAULT_LLM_API_URLS = {
    "openai": "https://api.openai.com/v1/chat/completions",
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "nvidia": "https://integrate.api.nvidia.com/v1/chat/completions",
}

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LLMCallResult:
    """Normalized OpenAI-compatible chat completion result."""

    content: str
    finish_reason: Optional[str] = None

    @property
    def is_truncated(self) -> bool:
        """Whether the provider stopped because the token limit was reached."""
        return self.finish_reason == "length"


class LLMService:
    """Service for LLM-powered features."""

    def __init__(self, settings_override=None):
        settings = settings_override or get_settings()
        self.provider = getattr(settings, "llm_provider", "openai")
        self.api_key = settings.llm_api_key
        self.api_url = self.resolve_api_url(self.provider, settings.llm_api_url)
        self.model = settings.llm_model
        self.temperature = float(getattr(settings, "llm_temperature", 0.2))
        self.max_output_tokens = int(getattr(settings, "llm_max_output_tokens", 3000))
        self.ui_language: LanguageCode = normalize_language(
            getattr(settings, "app_ui_language", "en")
        )
        self.ai_language_mode: AILanguageMode = normalize_ai_language_mode(
            getattr(settings, "ai_language_mode", "auto")
        )

    def _resolve_language(self, context: Any) -> LanguageCode:
        """Resolve AI prose language for the supplied source context."""
        return resolve_ai_language(
            context=context,
            default_language=self.ui_language,
            mode=self.ai_language_mode,
        ).language

    def _language_instruction(self, language: LanguageCode) -> str:
        """Return consistent provider instructions for localized AI prose."""
        return language_instruction(language)

    def _t(self, language: LanguageCode, en: str, ru: str) -> str:
        """Return a deterministic localized fallback string."""
        return localized(language, en=en, ru=ru)

    @classmethod
    async def from_runtime(cls, db) -> "LLMService":
        """Construct an LLM service from DB-backed runtime settings."""
        from app.services.system_settings_service import RuntimeSettingsService

        settings = await RuntimeSettingsService(db).get_llm_settings()
        return cls(settings_override=settings)

    @classmethod
    def resolve_api_url(cls, provider: str = "openai", api_url: str | None = None) -> str:
        """Resolve the OpenAI-compatible chat completions URL for a provider."""
        if api_url:
            normalized_provider = (provider or "openai").lower()
            normalized_url = api_url.strip().rstrip("/")
            if (
                normalized_provider in DEFAULT_LLM_API_URLS
                and not normalized_url.endswith("/chat/completions")
            ):
                normalized_url = f"{normalized_url}/chat/completions"
            return normalize_provider_api_url(normalized_url)

        normalized_provider = (provider or "openai").lower()
        if normalized_provider == "custom":
            return ""
        if normalized_provider not in DEFAULT_LLM_API_URLS:
            raise ValueError(f"Unsupported LLM provider: {provider}")

        return DEFAULT_LLM_API_URLS[normalized_provider]

    async def formalize_task(
        self,
        title: str,
        description: Optional[str] = None,
        context: Optional[str] = None
    ) -> FormalizeResponse:
        """Formalize a task using LLM."""
        language = self._resolve_language({
            "title": title,
            "description": description,
            "context": context,
        })
        if not self.api_key:
            # Fallback without LLM
            return self._formalize_fallback(title, description, language)

        prompt = f"""Formalize the following task for a development project.

{self._language_instruction(language)}

Title: {title}
Description: {description or 'Not provided'}
Project Context: {context or 'Not provided'}

Provide:
1. A clear, formal task title
2. A detailed task description
3. Estimated effort in days
4. Suggested subtasks with effort estimates

Respond in JSON format:
{{
    "formalized_title": "...",
    "suggested_description": "...",
    "suggested_effort_days": 3,
    "suggested_subtasks": [
        {{"title": "...", "effort_days": 0.5}}
    ]
}}"""

        try:
            response = await self._call_llm(prompt)
            # Parse JSON from response
            import json
            data = json.loads(response)

            return FormalizeResponse(
                original_title=title,
                formalized_title=data.get("formalized_title", title),
                suggested_description=data.get("suggested_description", description or ""),
                language=language,
                suggested_effort_days=data.get("suggested_effort_days"),
                suggested_subtasks=[
                    SuggestedSubtask(title=s["title"], effort_days=s["effort_days"])
                    for s in data.get("suggested_subtasks", [])
                ]
            )
        except Exception:
            logger.warning(
                "Task formalization provider failed; using deterministic fallback",
                exc_info=True,
                extra={"provider": self.provider},
            )
            return self._formalize_fallback(title, description, language)

    def _formalize_fallback(
        self,
        title: str,
        description: Optional[str],
        language: LanguageCode,
    ) -> FormalizeResponse:
        """Fallback formalization without LLM."""
        # Simple heuristic-based formalization
        formal_title = title
        prefixes = ("Реализ", "Разработ", "Создан", "Implement", "Develop")
        if not title.startswith(prefixes):
            formal_title = (
                f"Реализация: {title}"
                if language == "ru"
                else f"Implement: {title}"
            )

        return FormalizeResponse(
            original_title=title,
            formalized_title=formal_title,
            suggested_description=description or self._t(
                language,
                f"Develop and implement {title.lower()}",
                f"Разработать и реализовать {title.lower()}",
            ),
            language=language,
            suggested_effort_days=None,
            suggested_subtasks=[]
        )

    async def improve_description(
        self,
        current_description: str,
        context: Optional[str] = None
    ) -> ImproveDescriptionResponse:
        """Improve task description using LLM."""
        language = self._resolve_language({
            "current_description": current_description,
            "context": context,
        })
        if not self.api_key:
            return ImproveDescriptionResponse(
                improved_description=current_description,
                language=language,
            )

        prompt = f"""Improve the following task description for a development project.
Make it more clear, detailed, and actionable.

{self._language_instruction(language)}

Current Description: {current_description}
Context: {context or 'Not provided'}

Provide an improved description that includes:
- Clear objectives
- Acceptance criteria
- Technical considerations if applicable

Respond with just the improved description text."""

        try:
            improved = await self._call_llm(prompt)
            return ImproveDescriptionResponse(
                improved_description=improved.strip(),
                language=language,
            )
        except Exception:
            logger.warning(
                "Task description improvement provider failed; using original description",
                exc_info=True,
                extra={"provider": self.provider},
            )
            return ImproveDescriptionResponse(
                improved_description=current_description,
                language=language,
            )

    async def suggest_task(
        self,
        context_pack: dict[str, Any],
    ) -> GroundedAISuggestionResponse:
        """Generate a grounded advisory task suggestion from a context pack."""
        language = self._resolve_language(context_pack)
        if not self.api_key:
            return self._task_ai_fallback(
                context_pack,
                warning=self._t(
                    language,
                    "LLM unavailable; deterministic suggestion generated from supplied task context.",
                    "LLM недоступна; детерминированное предложение сформировано из переданного контекста задачи.",
                ),
                language=language,
            )

        prompt = self._task_ai_prompt(context_pack, language)
        try:
            result = await self._call_llm_result(prompt)
            data = self._parse_json_object(result.content)
            return self._normalize_task_ai_response(data, context_pack, result, language)
        except Exception:
            logger.warning(
                "Task AI suggestion provider failed; using deterministic fallback",
                exc_info=True,
                extra={"provider": self.provider},
            )
            return self._task_ai_fallback(
                context_pack,
                warning=self._t(
                    language,
                    "LLM response could not be used; deterministic suggestion generated from supplied task context.",
                    "Ответ LLM не удалось использовать; детерминированное предложение сформировано из переданного контекста задачи.",
                ),
                language=language,
            )

    def _task_ai_prompt(self, context_pack: dict[str, Any], language: LanguageCode) -> str:
        """Build the JSON-only grounded task AI prompt."""
        return f"""Generate advisory task wording from the supplied context.

{self._language_instruction(language)}

Rules:
- Use only the supplied context as grounded facts.
- Do not invent IDs, endpoints, statuses, relationships, metrics, dates, owners, or acceptance criteria as facts.
- Put missing information in open_questions.
- Put optional inferred ideas in ungrounded_suggestions.
- Keep suggested_description concise and grounded; do not include ungrounded ideas in it.
- Return JSON only.

Respond with this exact JSON shape:
{{
  "suggested_title": "Optional improved title",
  "suggested_description": "Grounded task description",
  "acceptance_criteria": ["Grounded acceptance criterion or verification step"],
  "implementation_notes": ["Grounded implementation note"],
  "risks": ["Grounded risk or uncertainty"],
  "open_questions": ["Question for missing information"],
  "grounded_facts": [
    {{"claim": "Claim copied or summarized from context", "source": "task.description"}}
  ],
  "ungrounded_suggestions": ["Optional idea explicitly not present in source context"],
  "warnings": ["Validation or source-limit warning"]
}}

Context:
{json.dumps(context_pack, ensure_ascii=False, default=str)}"""

    def _task_ai_fallback(
        self,
        context_pack: dict[str, Any],
        warning: str,
        language: LanguageCode,
    ) -> GroundedAISuggestionResponse:
        """Build a deterministic grounded task suggestion without provider output."""
        form = context_pack.get("form", {}) if isinstance(context_pack.get("form"), dict) else {}
        title = self._clean_text(form.get("title")) or self._clean_text(context_pack.get("task_title"))
        description = (
            self._clean_text(form.get("description"))
            or self._clean_text(context_pack.get("task_description"))
            or title
            or ""
        )
        facts = self._grounded_facts_from_context(context_pack)
        open_questions: list[str] = []
        if not self._clean_text(form.get("description")) and not self._clean_text(context_pack.get("task_description")):
            open_questions.append(self._t(
                language,
                "What concrete behavior or outcome should this task deliver?",
                "Какое конкретное поведение или результат должна дать эта задача?",
            ))
        if not context_pack.get("project"):
            open_questions.append(self._t(
                language,
                "Should this work be linked to a project or outcome?",
                "Нужно ли связать эту работу с проектом или ожидаемым результатом?",
            ))
        if not form.get("depends_on"):
            open_questions.append(self._t(
                language,
                "Are there dependencies or prerequisites that should be captured?",
                "Есть ли зависимости или предварительные условия, которые нужно зафиксировать?",
            ))

        acceptance = self._dedupe_ordered([
            self._t(
                language,
                "The task description reflects only the supplied title, description, labels, and context.",
                "Описание задачи отражает только переданные название, описание, метки и контекст.",
            ),
            self._t(
                language,
                "The owner can verify the result against the accepted task description.",
                "Владелец может проверить результат по принятому описанию задачи.",
            ),
        ])
        risks = []
        if len(description.strip()) < 80:
            risks.append(self._t(
                language,
                "Current task context is sparse; scope should be confirmed before execution.",
                "Текущий контекст задачи недостаточен; перед выполнением нужно подтвердить объём работ.",
            ))

        return GroundedAISuggestionResponse(
            provider=self.provider,
            model=self.model,
            language=language,
            is_fallback=True,
            finish_reason=None,
            is_truncated=False,
            suggested_title=title,
            suggested_description=description,
            acceptance_criteria=acceptance,
            implementation_notes=[],
            risks=risks,
            open_questions=open_questions,
            grounded_facts=facts,
            ungrounded_suggestions=[],
            warnings=[warning],
        )

    def _normalize_task_ai_response(
        self,
        data: dict[str, Any],
        context_pack: dict[str, Any],
        result: LLMCallResult,
        language: LanguageCode,
    ) -> GroundedAISuggestionResponse:
        """Validate and normalize provider task AI output."""
        form = context_pack.get("form", {}) if isinstance(context_pack.get("form"), dict) else {}
        source_text = self._task_context_source_text(context_pack)
        suggested_description = self._clean_text(data.get("suggested_description")) or (
            self._clean_text(form.get("description")) or self._clean_text(form.get("title")) or ""
        )
        warnings = self._clean_string_list(data.get("warnings"))
        ungrounded_suggestions = self._clean_string_list(data.get("ungrounded_suggestions"))
        suggested_description, demoted = self._demote_unsupported_task_claims(
            suggested_description,
            source_text,
        )
        if demoted:
            ungrounded_suggestions.extend(demoted)
            warnings.append(self._t(
                language,
                "Provider output contained details not found in task context; they were separated as ungrounded suggestions.",
                "Ответ провайдера содержал детали, которых нет в контексте задачи; они отделены как неподтверждённые предложения.",
            ))
        if result.is_truncated:
            warnings.append(self._t(
                language,
                "Provider stopped because the output token limit was reached.",
                "Провайдер остановился из-за ограничения на число выходных токенов.",
            ))

        facts = self._normalize_grounded_facts(data.get("grounded_facts"), context_pack)
        if not facts:
            facts = self._grounded_facts_from_context(context_pack)

        return GroundedAISuggestionResponse(
            provider=self.provider,
            model=self.model,
            language=language,
            is_fallback=False,
            finish_reason=result.finish_reason,
            is_truncated=result.is_truncated,
            suggested_title=self._clean_text(data.get("suggested_title")) or self._clean_text(form.get("title")),
            suggested_description=suggested_description,
            acceptance_criteria=self._clean_string_list(data.get("acceptance_criteria")),
            implementation_notes=self._clean_string_list(data.get("implementation_notes")),
            risks=self._clean_string_list(data.get("risks")),
            open_questions=self._clean_string_list(data.get("open_questions")),
            grounded_facts=facts,
            ungrounded_suggestions=self._dedupe_ordered(ungrounded_suggestions),
            warnings=self._dedupe_ordered(warnings),
        )

    def _grounded_facts_from_context(self, context_pack: dict[str, Any]) -> list[GroundedFact]:
        """Extract small source-labelled facts from the task context pack."""
        facts: list[GroundedFact] = []
        form = context_pack.get("form", {}) if isinstance(context_pack.get("form"), dict) else {}
        for key, source in (
            ("title", "task.title"),
            ("description", "task.description"),
            ("tags", "task.labels"),
            ("source", "task.source"),
            ("source_url", "task.source_url"),
            ("external_key", "task.external_key"),
        ):
            value = form.get(key)
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value if str(item).strip())
            text = self._clean_text(value)
            if text:
                facts.append(GroundedFact(claim=text[:400], source=source))
        project = context_pack.get("project")
        if isinstance(project, dict):
            name = self._clean_text(project.get("name"))
            if name:
                facts.append(GroundedFact(claim=f"Project: {name}", source="project.summary"))
        template = context_pack.get("template")
        if isinstance(template, dict):
            name = self._clean_text(template.get("name"))
            if name:
                facts.append(GroundedFact(claim=f"Template: {name}", source="template.default_description"))
        user_context = self._clean_text(context_pack.get("user_context"))
        if user_context:
            facts.append(GroundedFact(claim=user_context[:400], source="user_context"))
        return facts[:12]

    def _normalize_grounded_facts(
        self,
        value: Any,
        context_pack: dict[str, Any],
    ) -> list[GroundedFact]:
        """Normalize provider fact records and keep only known source labels."""
        known_sources = {
            "task.title",
            "task.description",
            "task.labels",
            "task.source",
            "task.source_url",
            "task.external_key",
            "project.summary",
            "milestone.summary",
            "template.default_description",
            "dependencies",
            "parent_task",
            "child_tasks",
            "request_links",
            "user_context",
        }
        if not isinstance(value, list):
            return []
        facts: list[GroundedFact] = []
        for item in value:
            if not isinstance(item, dict):
                continue
            claim = self._clean_text(item.get("claim"))
            source = self._clean_text(item.get("source"))
            if claim and source and source in known_sources:
                facts.append(GroundedFact(claim=claim[:500], source=source))
        return facts[:20]

    def _task_context_source_text(self, context_pack: dict[str, Any]) -> str:
        """Flatten context text for heuristic unsupported-claim checks."""
        parts: list[str] = []
        def collect(value: Any) -> None:
            if value is None:
                return
            if isinstance(value, dict):
                for nested in value.values():
                    collect(nested)
            elif isinstance(value, list):
                for nested in value:
                    collect(nested)
            else:
                parts.append(str(value))
        collect(context_pack)
        return "\n".join(parts).lower()

    def _demote_unsupported_task_claims(
        self,
        description: str,
        source_text: str,
    ) -> tuple[str, list[str]]:
        """Move common hallucinated implementation details out of the description."""
        if not description:
            return description, []
        unsupported_markers = [
            "uuid",
            "organization",
            "many-to-many",
            "patch /api",
            "swagger",
            "openapi",
            "80%",
            "archived",
            "postgresql enum",
            "lookup-table",
            "unique index",
            "project_user",
        ]
        kept: list[str] = []
        demoted: list[str] = []
        for line in description.splitlines():
            normalized = line.lower()
            marker_hit = next(
                (
                    marker for marker in unsupported_markers
                    if marker in normalized and marker not in source_text
                ),
                None,
            )
            if marker_hit:
                cleaned = line.strip(" -\t")
                if cleaned:
                    demoted.append(cleaned)
                continue
            kept.append(line)
        return "\n".join(kept).strip(), self._dedupe_ordered(demoted)

    async def classify_triage_item(
        self,
        triage_item: dict[str, Any],
        label_groups: list[dict[str, Any]],
        projects: list[dict[str, Any]],
        assignees: list[dict[str, Any]],
        duplicate_candidates: list[dict[str, Any]],
    ) -> TriageClassificationDraft:
        """Classify a triage item into advisory structured suggestions."""
        language = self._resolve_language({
            "triage_item": triage_item,
            "label_groups": label_groups,
            "projects": projects,
            "assignees": assignees,
            "duplicate_candidates": duplicate_candidates,
        })
        if not self.api_key:
            return self._triage_classification_fallback(
                triage_item=triage_item,
                label_groups=label_groups,
                projects=projects,
                assignees=assignees,
                duplicate_candidates=duplicate_candidates,
                rationale=self._t(
                    language,
                    "LLM unavailable; suggestion generated from existing hints and keyword matches.",
                    "LLM недоступна; предложение сформировано из существующих подсказок и совпадений по ключевым словам.",
                ),
                language=language,
            )

        prompt = self._triage_classification_prompt(
            triage_item=triage_item,
            label_groups=label_groups,
            projects=projects,
            assignees=assignees,
            duplicate_candidates=duplicate_candidates,
            language=language,
        )

        try:
            response = await self._call_llm(prompt)
            data = self._parse_json_object(response)
            return TriageClassificationDraft(
                suggested_type_label_slug=data.get("suggested_type_label_slug"),
                suggested_area_label_slug=data.get("suggested_area_label_slug"),
                suggested_priority=data.get("suggested_priority"),
                suggested_label_slugs=data.get("suggested_label_slugs") or [],
                unmatched_label_text=data.get("unmatched_label_text") or [],
                suggested_assignee_id=data.get("suggested_assignee_id"),
                suggested_assignee_hint=data.get("suggested_assignee_hint"),
                suggested_project_id=data.get("suggested_project_id"),
                duplicate_candidates=data.get("duplicate_candidates") or [],
                confidence=data.get("confidence", 0.0),
                rationale=data.get("rationale") or self._t(
                    language,
                    "LLM-generated advisory classification.",
                    "Рекомендательная классификация, созданная LLM.",
                ),
                language=language,
                is_fallback=False,
                raw_response_json={**data, "_language": language},
            )
        except Exception:
            logger.warning(
                "Triage classification provider failed; using deterministic fallback",
                extra={"triage_item_id": triage_item.get("id"), "provider": self.provider},
                exc_info=True,
            )
            return self._triage_classification_fallback(
                triage_item=triage_item,
                label_groups=label_groups,
                projects=projects,
                assignees=assignees,
                duplicate_candidates=duplicate_candidates,
                rationale=self._t(
                    language,
                    "LLM response could not be used; suggestion generated from existing hints and keyword matches.",
                    "Ответ LLM не удалось использовать; предложение сформировано из существующих подсказок и совпадений по ключевым словам.",
                ),
                language=language,
            )

    async def draft_triage_task(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]] = None,
        classification: Optional[dict[str, Any]] = None,
        current_title: Optional[str] = None,
        current_description: Optional[str] = None,
    ) -> TriageTaskDraftResponse:
        """Draft transient task details for converting a triage item."""
        language = self._resolve_language({
            "triage_item": triage_item,
            "template": template,
            "classification": classification,
            "current_title": current_title,
            "current_description": current_description,
        })
        if not self.api_key:
            return self._triage_task_draft_fallback(
                triage_item=triage_item,
                template=template,
                classification=classification,
                current_title=current_title,
                current_description=current_description,
                rationale=self._t(
                    language,
                    "LLM unavailable; draft generated from intake content, selected template, and classification hints.",
                    "LLM недоступна; черновик сформирован из входящего запроса, выбранного шаблона и подсказок классификации.",
                ),
                language=language,
            )

        prompt = self._triage_task_draft_prompt(
            triage_item=triage_item,
            template=template,
            classification=classification,
            current_title=current_title,
            current_description=current_description,
            language=language,
        )

        try:
            response = LLMCallResult(
                content=await self._call_llm(prompt),
                finish_reason=getattr(self, "_last_finish_reason", None),
            )
            data = self._parse_json_object(response.content)
            warnings = self._clean_string_list(data.get("warnings"))
            if response.is_truncated:
                warnings.append(self._t(
                    language,
                    "Provider stopped because the output token limit was reached.",
                    "Провайдер остановился из-за ограничения на число выходных токенов.",
                ))
            return TriageTaskDraftResponse(
                triage_item_id=int(triage_item["id"]),
                suggested_title=(
                    self._clean_text(data.get("suggested_title"))
                    or self._draft_title(triage_item, template, current_title, language)
                ),
                suggested_description=(
                    self._clean_text(data.get("suggested_description"))
                    or self._draft_description(triage_item, template, current_description, language)
                ),
                suggested_checklist=self._clean_string_list(data.get("suggested_checklist")),
                acceptance_criteria=self._clean_string_list(data.get("acceptance_criteria")),
                risks=self._clean_string_list(data.get("risks")),
                template_id=template.get("id") if template else None,
                classification_suggestion_id=classification.get("id") if classification else None,
                is_fallback=False,
                provider=self.provider,
                model=self.model,
                language=language,
                finish_reason=response.finish_reason,
                is_truncated=response.is_truncated,
                grounded_facts=self._triage_draft_grounded_facts(triage_item, template, current_title, current_description),
                implementation_notes=self._clean_string_list(data.get("implementation_notes")),
                open_questions=self._clean_string_list(data.get("open_questions")),
                ungrounded_suggestions=self._clean_string_list(data.get("ungrounded_suggestions")),
                warnings=self._dedupe_ordered(warnings),
                rationale=self._clean_text(data.get("rationale")) or self._t(
                    language,
                    "LLM-generated task draft.",
                    "Черновик задачи, созданный LLM.",
                ),
            )
        except Exception:
            logger.warning(
                "Triage task-draft provider failed; using deterministic fallback",
                extra={"triage_item_id": triage_item.get("id"), "provider": self.provider},
                exc_info=True,
            )
            return self._triage_task_draft_fallback(
                triage_item=triage_item,
                template=template,
                classification=classification,
                current_title=current_title,
                current_description=current_description,
                rationale=self._t(
                    language,
                    "LLM response could not be used; draft generated from intake content, selected template, and classification hints.",
                    "Ответ LLM не удалось использовать; черновик сформирован из входящего запроса, выбранного шаблона и подсказок классификации.",
                ),
                language=language,
            )

    def _triage_task_draft_prompt(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]],
        classification: Optional[dict[str, Any]],
        current_title: Optional[str],
        current_description: Optional[str],
        language: LanguageCode,
    ) -> str:
        """Build the JSON-only triage task drafting prompt."""
        context = {
            "triage_item": triage_item,
            "selected_task_template": template,
            "classification_suggestion": classification,
            "current_convert_form": {
                "title": current_title,
                "description": current_description,
            },
        }
        return f"""Draft task details for converting this triage item into implementation work.

{self._language_instruction(language)}

Use the supplied triage content as the source of truth. If a task template is present,
incorporate its defaults without inventing unrelated scope. If a classification
suggestion is present, use it as advisory context only.

Respond with a single JSON object using this exact shape:
{{
  "suggested_title": "Clear task title",
  "suggested_description": "Concise task description with scope and context",
  "suggested_checklist": ["Implementation step or verification item"],
  "acceptance_criteria": ["Observable condition that must be true"],
  "risks": ["Risk, unknown, or dependency to watch"],
  "rationale": "Short reason for the draft."
}}

Context:
{json.dumps(context, ensure_ascii=False, default=str)}"""

    def _triage_task_draft_fallback(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]],
        classification: Optional[dict[str, Any]],
        current_title: Optional[str],
        current_description: Optional[str],
        rationale: str,
        language: LanguageCode,
    ) -> TriageTaskDraftResponse:
        """Build deterministic task draft suggestions without provider output."""
        suggested_title = self._draft_title(triage_item, template, current_title, language)
        suggested_description = self._draft_description(
            triage_item,
            template,
            current_description,
            language,
        )
        checklist = self._draft_checklist(template, language)
        acceptance_criteria = self._draft_acceptance_criteria(
            triage_item,
            template,
            classification,
            language,
        )
        risks = self._draft_risks(triage_item, classification, language)

        return TriageTaskDraftResponse(
            triage_item_id=int(triage_item["id"]),
            suggested_title=suggested_title,
            suggested_description=suggested_description,
            suggested_checklist=checklist,
            acceptance_criteria=acceptance_criteria,
            risks=risks,
            template_id=template.get("id") if template else None,
            classification_suggestion_id=classification.get("id") if classification else None,
            is_fallback=True,
            provider=self.provider,
            model=self.model,
            language=language,
            grounded_facts=self._triage_draft_grounded_facts(triage_item, template, current_title, current_description),
            open_questions=[
                self._t(
                    language,
                    "Confirm scope and expected outcome before converting if the intake detail is incomplete.",
                    "Подтвердите объём и ожидаемый результат перед конвертацией, если входящих данных недостаточно.",
                )
            ] if not self._clean_text(triage_item.get("description")) else [],
            warnings=[rationale],
            rationale=rationale,
        )

    def _triage_draft_grounded_facts(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]],
        current_title: Optional[str],
        current_description: Optional[str],
    ) -> list[dict[str, str]]:
        """Return source-labelled facts for transient triage task drafts."""
        facts: list[dict[str, str]] = []
        for value, source in (
            (current_title or triage_item.get("title"), "triage.title"),
            (current_description or triage_item.get("description"), "triage.description"),
            (triage_item.get("source"), "triage.source"),
            (triage_item.get("source_url"), "triage.source_url"),
            (triage_item.get("external_key"), "triage.external_key"),
        ):
            text = self._clean_text(value)
            if text:
                facts.append({"claim": text[:400], "source": source})
        if template:
            name = self._clean_text(template.get("name"))
            if name:
                facts.append({"claim": f"Template: {name}", "source": "template.default_description"})
        return facts[:12]

    def _draft_title(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]],
        current_title: Optional[str],
        language: LanguageCode,
    ) -> str:
        """Choose a stable draft title from user input, template, or intake."""
        return (
            self._clean_text(current_title)
            or self._clean_text(template.get("default_title") if template else None)
            or self._clean_text(triage_item.get("title"))
            or self._t(language, "Draft task from intake", "Черновик задачи из входящего запроса")
        )

    def _draft_description(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]],
        current_description: Optional[str],
        language: LanguageCode,
    ) -> str:
        """Build a deterministic task description from available context."""
        base_description = (
            self._clean_text(current_description)
            or self._clean_text(template.get("default_description") if template else None)
            or self._clean_text(triage_item.get("description"))
            or self._clean_text(triage_item.get("title"))
            or self._t(
                language,
                "Convert the intake item into a scoped task.",
                "Преобразовать входящий запрос в задачу с понятным объёмом работ.",
            )
        )
        context_lines: list[str] = []
        source = self._clean_text(triage_item.get("source"))
        external_key = self._clean_text(triage_item.get("external_key"))
        source_url = self._clean_text(triage_item.get("source_url"))
        if source:
            context_lines.append(f"{self._t(language, 'Source', 'Источник')}: {source}")
        if external_key:
            context_lines.append(f"{self._t(language, 'External key', 'Внешний ключ')}: {external_key}")
        if source_url:
            context_lines.append(f"{self._t(language, 'Source URL', 'URL источника')}: {source_url}")

        if not context_lines:
            return base_description
        heading = self._t(language, "Intake context", "Контекст входящего запроса")
        return "\n\n".join([base_description, heading + ":\n" + "\n".join(context_lines)])

    def _draft_checklist(self, template: Optional[dict[str, Any]], language: LanguageCode) -> list[str]:
        """Return template checklist plus baseline conversion checks."""
        template_items = (
            template.get("default_checklist")
            if template and isinstance(template.get("default_checklist"), list)
            else []
        )
        return self._dedupe_ordered([
            *self._clean_string_list(template_items),
            self._t(language, "Confirm scope with the requester or owner", "Подтвердить объём работ с заявителем или владельцем"),
            self._t(language, "Implement the agreed task changes", "Реализовать согласованные изменения по задаче"),
            self._t(language, "Verify acceptance criteria before handoff", "Проверить критерии приёмки перед передачей результата"),
        ])

    def _draft_acceptance_criteria(
        self,
        triage_item: dict[str, Any],
        template: Optional[dict[str, Any]],
        classification: Optional[dict[str, Any]],
        language: LanguageCode,
    ) -> list[str]:
        """Generate stable acceptance criteria from intake/template hints."""
        criteria = [
            self._t(language, "The task scope reflects the original intake request.", "Объём задачи отражает исходный входящий запрос."),
            self._t(language, "The implementation is verified against the requested behavior.", "Реализация проверена относительно запрошенного поведения."),
        ]
        if template and template.get("name"):
            criteria.append(self._t(
                language,
                f"Relevant defaults from the {template['name']} template are addressed.",
                f"Учтены релевантные значения по умолчанию из шаблона {template['name']}.",
            ))
        priority = classification.get("suggested_priority") if classification else triage_item.get("priority_hint")
        if priority is not None:
            criteria.append(self._t(
                language,
                f"Priority {priority} handling expectations are documented before completion.",
                f"Ожидания по обработке приоритета {priority} зафиксированы до завершения.",
            ))
        return self._dedupe_ordered(criteria)

    def _draft_risks(
        self,
        triage_item: dict[str, Any],
        classification: Optional[dict[str, Any]],
        language: LanguageCode,
    ) -> list[str]:
        """Generate stable risk notes from sparse intake data."""
        risks: list[str] = []
        if not self._clean_text(triage_item.get("description")):
            risks.append(self._t(
                language,
                "Original intake has limited detail; scope may need confirmation.",
                "В исходном запросе мало деталей; объём работ может потребовать подтверждения.",
            ))
        unmatched = classification.get("unmatched_label_text") if classification else []
        unmatched_labels = self._clean_string_list(unmatched)
        if unmatched_labels:
            risks.append(self._t(
                language,
                f"Unmatched labels may need taxonomy review: {', '.join(unmatched_labels)}.",
                f"Нераспознанные метки могут потребовать проверки таксономии: {', '.join(unmatched_labels)}.",
            ))
        duplicate_candidates = classification.get("duplicate_candidates") if classification else []
        if duplicate_candidates:
            risks.append(self._t(
                language,
                "Potential duplicate or related work should be reviewed before implementation.",
                "Перед реализацией нужно проверить возможный дубликат или связанную работу.",
            ))
        if not risks:
            risks.append(self._t(
                language,
                "No specific risks were identified from the available intake context.",
                "По доступному контексту входящего запроса конкретные риски не выявлены.",
            ))
        return risks

    def _clean_text(self, value: Any) -> Optional[str]:
        """Return stripped text or None."""
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    def _clean_string_list(self, value: Any) -> list[str]:
        """Normalize provider or template list fields into non-empty strings."""
        if not isinstance(value, list):
            return []
        return self._dedupe_ordered([
            str(item).strip()
            for item in value
            if str(item).strip()
        ])

    def _dedupe_ordered(self, values: list[str]) -> list[str]:
        """Return strings in input order without duplicates."""
        result: list[str] = []
        for value in values:
            if value and value not in result:
                result.append(value)
        return result

    def _triage_classification_prompt(
        self,
        triage_item: dict[str, Any],
        label_groups: list[dict[str, Any]],
        projects: list[dict[str, Any]],
        assignees: list[dict[str, Any]],
        duplicate_candidates: list[dict[str, Any]],
        language: LanguageCode,
    ) -> str:
        """Build the JSON-only triage classification prompt."""
        context = {
            "triage_item": triage_item,
            "active_label_groups": label_groups,
            "candidate_projects": projects,
            "candidate_assignees": assignees,
            "duplicate_candidates": duplicate_candidates,
        }
        return f"""Classify the triage item for a project manager.

{self._language_instruction(language)}

Use only known label slugs and known numeric IDs from the supplied context. If a useful
label, project, or assignee is not present in the context, put free text in
unmatched_label_text or suggested_assignee_hint and leave the ID/slug null.
Duplicate candidates must be selected only from the supplied duplicate_candidates list.

Respond with a single JSON object using this exact shape:
{{
  "suggested_type_label_slug": "feature|bug|chore|incident|research|release|request|null",
  "suggested_area_label_slug": "backend|frontend|scheduling|analytics|integrations|null",
  "suggested_priority": 1,
  "suggested_label_slugs": ["bug", "backend"],
  "unmatched_label_text": [],
  "suggested_assignee_id": null,
  "suggested_assignee_hint": null,
  "suggested_project_id": null,
  "duplicate_candidates": [
    {{"target_type": "task", "target_id": 123, "score": 0.9, "reason": "same source key"}}
  ],
  "confidence": 0.75,
  "rationale": "Short reason for the suggestion."
}}

Context:
{json.dumps(context, ensure_ascii=False, default=str)}"""

    def _parse_json_object(self, value: str) -> dict[str, Any]:
        """Parse provider output that should contain a single JSON object."""
        stripped = value.strip()
        fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, re.DOTALL)
        if fence_match:
            stripped = fence_match.group(1)
        elif not stripped.startswith("{"):
            start = stripped.find("{")
            end = stripped.rfind("}")
            if start >= 0 and end > start:
                stripped = stripped[start:end + 1]
        data = json.loads(stripped)
        if not isinstance(data, dict):
            raise ValueError("LLM response must be a JSON object")
        return data

    def _triage_classification_fallback(
        self,
        triage_item: dict[str, Any],
        label_groups: list[dict[str, Any]],
        projects: list[dict[str, Any]],
        assignees: list[dict[str, Any]],
        duplicate_candidates: list[dict[str, Any]],
        rationale: str,
        language: LanguageCode,
    ) -> TriageClassificationDraft:
        """Build deterministic triage classification without a provider."""
        labels_by_group = {
            group.get("key"): group.get("labels", [])
            for group in label_groups
        }
        label_slugs = {
            label.get("slug")
            for group in label_groups
            for label in group.get("labels", [])
            if label.get("slug")
        }
        existing_labels = [
            str(label).strip()
            for label in triage_item.get("labels", [])
            if str(label).strip()
        ]
        text = self._normalized_triage_text(triage_item)

        type_slug = self._first_existing_group_label(existing_labels, labels_by_group.get("type", []))
        if not type_slug:
            type_slug = self._keyword_label(
                text,
                labels_by_group.get("type", []),
                {
                    "bug": ["bug", "error", "failed", "failure", "broken", "crash", "exception"],
                    "incident": ["incident", "outage", "sev", "urgent production"],
                    "feature": ["feature", "add", "new", "build", "support"],
                    "request": ["request", "customer", "ask", "ticket"],
                    "research": ["research", "investigate", "spike", "explore"],
                    "release": ["release", "ship", "deploy"],
                    "chore": ["cleanup", "maintenance", "chore"],
                },
            )

        area_slug = self._first_existing_group_label(existing_labels, labels_by_group.get("area", []))
        if not area_slug:
            area_slug = self._keyword_label(
                text,
                labels_by_group.get("area", []),
                {
                    "backend": ["api", "backend", "database", "server", "migration"],
                    "frontend": ["ui", "frontend", "screen", "page", "button", "modal"],
                    "scheduling": ["schedule", "gantt", "iteration", "capacity"],
                    "analytics": ["analytics", "dashboard", "metric", "report"],
                    "integrations": ["github", "webhook", "integration", "external"],
                },
            )

        suggested_labels: list[str] = []
        for slug in [*existing_labels, type_slug, area_slug]:
            if slug and slug in label_slugs and slug not in suggested_labels:
                suggested_labels.append(slug)

        unmatched_labels = [
            label for label in existing_labels
            if label not in label_slugs
        ]
        priority = self._fallback_priority(triage_item, text)
        assignee_id, assignee_hint = self._fallback_assignee(triage_item, assignees, text)
        project_id = self._fallback_project(triage_item, projects, text)

        return TriageClassificationDraft(
            suggested_type_label_slug=type_slug,
            suggested_area_label_slug=area_slug,
            suggested_priority=priority,
            suggested_label_slugs=suggested_labels,
            unmatched_label_text=unmatched_labels,
            suggested_assignee_id=assignee_id,
            suggested_assignee_hint=assignee_hint,
            suggested_project_id=project_id,
            duplicate_candidates=duplicate_candidates,
            confidence=0.45 if any([type_slug, area_slug, project_id, assignee_id]) else 0.25,
            rationale=rationale,
            language=language,
            is_fallback=True,
            raw_response_json={"_language": language},
        )

    def _normalized_triage_text(self, triage_item: dict[str, Any]) -> str:
        """Combine triage text fields for fallback keyword matching."""
        parts = [
            triage_item.get("title"),
            triage_item.get("description"),
            triage_item.get("source"),
            triage_item.get("source_url"),
            triage_item.get("external_key"),
            triage_item.get("assignee_hint"),
            " ".join(triage_item.get("labels") or []),
        ]
        return " ".join(str(part).lower() for part in parts if part)

    def _first_existing_group_label(
        self,
        existing_labels: list[str],
        group_labels: list[dict[str, Any]],
    ) -> Optional[str]:
        """Return the first existing label that belongs to a label group."""
        group_slugs = {label.get("slug") for label in group_labels}
        for label in existing_labels:
            if label in group_slugs:
                return label
        return None

    def _keyword_label(
        self,
        text: str,
        group_labels: list[dict[str, Any]],
        keyword_map: dict[str, list[str]],
    ) -> Optional[str]:
        """Infer a label slug from keywords if that slug exists in the group."""
        group_slugs = {label.get("slug") for label in group_labels}
        for slug, keywords in keyword_map.items():
            if slug in group_slugs and any(keyword in text for keyword in keywords):
                return slug
        for label in group_labels:
            slug = label.get("slug")
            name = str(label.get("name") or "").lower()
            if slug and (str(slug).lower() in text or (name and name in text)):
                return slug
        return None

    def _fallback_priority(
        self,
        triage_item: dict[str, Any],
        text: str,
    ) -> Optional[int]:
        """Infer priority from existing hints or severity keywords."""
        priority = triage_item.get("priority_hint")
        if isinstance(priority, int) and 1 <= priority <= 10:
            return priority
        if any(keyword in text for keyword in ["urgent", "critical", "blocker", "blocked", "sev1"]):
            return 1
        if any(keyword in text for keyword in ["high", "important", "customer"]):
            return 2
        return 5

    def _fallback_assignee(
        self,
        triage_item: dict[str, Any],
        assignees: list[dict[str, Any]],
        text: str,
    ) -> tuple[Optional[int], Optional[str]]:
        """Resolve an assignee hint against candidate team members."""
        hint = triage_item.get("assignee_hint")
        if hint:
            normalized_hint = str(hint).strip().lower()
            for assignee in assignees:
                if str(assignee.get("name") or "").strip().lower() == normalized_hint:
                    return assignee.get("id"), str(hint).strip()

        best_assignee: Optional[dict[str, Any]] = None
        best_score = 0
        for assignee in assignees:
            profile = assignee.get("profile") or {}
            if profile.get("automation_enabled") is False:
                continue
            score = 0
            profile_text = " ".join(
                str(value)
                for value in [
                    profile.get("headline"),
                    profile.get("summary"),
                ]
                if value
            ).lower()
            if profile_text and any(token in profile_text for token in text.split() if len(token) >= 3):
                score += 2
            for skill in profile.get("skills") or []:
                skill_terms = [
                    skill.get("skill_key"),
                    skill.get("skill_name"),
                    skill.get("category"),
                    *(skill.get("keywords_json") or []),
                ]
                matched = any(
                    str(term).strip().lower() in text
                    for term in skill_terms
                    if str(term).strip()
                )
                if matched:
                    if skill.get("is_weakness"):
                        score -= 4
                    else:
                        score += int(skill.get("level") or 3) + int(skill.get("interest") or 3)
            if score > best_score:
                best_score = score
                best_assignee = assignee

        if best_assignee is not None:
            return best_assignee.get("id"), str(best_assignee.get("name") or "").strip() or None

        if hint:
            return None, str(hint).strip()
        return None, None

    def _fallback_project(
        self,
        triage_item: dict[str, Any],
        projects: list[dict[str, Any]],
        text: str,
    ) -> Optional[int]:
        """Resolve project hint or project name keyword."""
        project_hint_id = triage_item.get("project_hint_id")
        project_ids = {project.get("id") for project in projects}
        if project_hint_id in project_ids:
            return project_hint_id
        for project in projects:
            name = str(project.get("name") or "").strip().lower()
            if name and name in text:
                return project.get("id")
        return None

    async def explain_schedule(
        self,
        decisions: list[SchedulingDecision],
        workload_issues: list[WorkloadIssue] | None = None,
        detail_level: str = "full"
    ) -> ExplainScheduleResponse:
        """Generate human-readable explanation for scheduling decisions."""
        workload_issues = workload_issues or []
        language = self._resolve_language({
            "decisions": [
                {
                    "task_title": decision.task_title,
                    "decision_type": decision.decision_type,
                    "reason": decision.reason,
                }
                for decision in decisions
            ],
            "workload_issues": [
                {"member_name": issue.member_name, "issue": issue.issue}
                for issue in workload_issues
            ],
        })
        response = self._schedule_explanation_fallback(
            decisions=decisions,
            workload_issues=workload_issues,
            detail_level=detail_level,
            language=language,
        )

        # LLM enhancement is optional. Any provider error preserves the
        # deterministic explanation so callers never need provider availability.
        if self.api_key and detail_level == "full" and len(decisions) <= 10:
            try:
                enhanced_summary = await self._enhance_explanation(decisions, workload_issues, language)
                if enhanced_summary and enhanced_summary.content.strip():
                    response.summary = enhanced_summary.content.strip()
                    response.is_fallback = False
                    response.provider = self.provider
                    response.model = self.model
                    response.finish_reason = enhanced_summary.finish_reason
                    response.is_truncated = enhanced_summary.is_truncated
                    if enhanced_summary.is_truncated:
                        response.warnings.append(
                            self._t(
                                language,
                                "Provider stopped because the output token limit was reached; deterministic schedule details are still included.",
                                "Провайдер остановился из-за ограничения на число выходных токенов; детерминированные детали расписания всё равно включены.",
                            )
                        )
            except Exception:
                # Provider enhancement is optional; deterministic details remain complete.
                logger.warning(
                    "Schedule explanation enhancement failed; using deterministic fallback",
                    extra={"decision_count": len(decisions), "provider": self.provider},
                    exc_info=True,
                )

        return response

    def _schedule_explanation_fallback(
        self,
        decisions: list[SchedulingDecision],
        workload_issues: list[WorkloadIssue],
        detail_level: str,
        language: LanguageCode,
    ) -> ExplainScheduleResponse:
        """Build a deterministic schedule explanation without an LLM provider."""
        scheduled = [d for d in decisions if d.decision_type == "scheduled"]
        delayed = [d for d in decisions if d.decision_type == "delayed"]
        overdue = [d for d in decisions if d.decision_type == "overdue"]
        reordered = [d for d in decisions if d.decision_type == "reordered"]

        decision_counts = Counter(d.decision_type for d in decisions)
        summary_parts: list[str] = []
        if decisions:
            if language == "ru":
                summary_parts.append(f"Проверено решений по расписанию: {len(decisions)}.")
            else:
                decision_label = "decision" if len(decisions) == 1 else "decisions"
                decision_verb = "was" if len(decisions) == 1 else "were"
                summary_parts.append(
                    f"{len(decisions)} scheduling {decision_label} {decision_verb} reviewed."
                )
            summary_parts.extend(
                [
                    f"{count} {label}."
                    for decision_type, label in [
                        ("scheduled", self._t(language, "task(s) scheduled", "задач запланировано")),
                        ("delayed", self._t(language, "task(s) delayed", "задач отложено")),
                        ("reordered", self._t(language, "task(s) reordered", "задач переупорядочено")),
                        ("overdue", self._t(language, "task(s) extend beyond the iteration", "задач выходят за границы итерации")),
                    ]
                    if (count := decision_counts.get(decision_type, 0))
                ]
            )
        else:
            summary_parts.append(self._t(
                language,
                "No scheduling decisions were produced.",
                "Решения по расписанию не сформированы.",
            ))

        if workload_issues:
            if language == "ru":
                summary_parts.append(f"Проблемы нагрузки требуют проверки: {len(workload_issues)}.")
            else:
                issue_label = "issue" if len(workload_issues) == 1 else "issues"
                issue_verb = "needs" if len(workload_issues) == 1 else "need"
                summary_parts.append(
                    f"{len(workload_issues)} workload {issue_label} {issue_verb} review."
                )

        recommendations = self._schedule_recommendations(
            scheduled=scheduled,
            delayed=delayed,
            overdue=overdue,
            reordered=reordered,
            workload_issues=workload_issues,
            language=language,
        )
        if recommendations:
            summary_parts.append(
                self._t(language, "Recommended next steps: ", "Рекомендуемые следующие шаги: ")
                + " ".join(recommendations)
            )

        summary = " ".join(summary_parts)

        explanations = [
            ScheduleDecisionExplanation(
                task_id=d.task_id,
                task_title=d.task_title,
                decision_type=d.decision_type,
                explanation=d.reason,
            )
            for d in decisions
        ]
        if detail_level == "brief":
            explanations = explanations[:3]

        workload_issue_text = [
            self._t(
                language,
                f"Task '{d.task_title}' is outside the iteration: {d.reason}",
                f"Задача '{d.task_title}' выходит за границы итерации: {d.reason}",
            )
            for d in overdue
        ]
        workload_issue_text.extend(
            f"{issue.member_name}: {issue.issue}"
            for issue in workload_issues
        )

        return ExplainScheduleResponse(
            summary=summary,
            decisions=explanations,
            workload_analysis=WorkloadAnalysis(
                balanced=not overdue and not workload_issues,
                issues=workload_issue_text,
            ),
            provider=self.provider,
            model=self.model,
            language=language,
            is_fallback=True,
        )

    def _schedule_recommendations(
        self,
        scheduled: list[SchedulingDecision],
        delayed: list[SchedulingDecision],
        overdue: list[SchedulingDecision],
        reordered: list[SchedulingDecision],
        workload_issues: list[WorkloadIssue],
        language: LanguageCode,
    ) -> list[str]:
        """Derive stable recommendations from scheduler output."""
        recommendations: list[str] = []
        if delayed:
            recommendations.append(self._t(language, "Review delayed tasks and dependency chains.", "Проверьте отложенные задачи и цепочки зависимостей."))
        if reordered:
            recommendations.append(self._t(language, "Confirm reordered work still matches stakeholder priorities.", "Подтвердите, что переупорядоченная работа всё ещё соответствует приоритетам заинтересованных сторон."))
        if overdue:
            recommendations.append(self._t(language, "Reduce scope, adjust estimates, or move overdue tasks.", "Сократите объём, уточните оценки или перенесите просроченные задачи."))
        if workload_issues:
            recommendations.append(self._t(language, "Rebalance assignments before committing the iteration plan.", "Перераспределите назначения перед фиксацией плана итерации."))
        if scheduled and not recommendations:
            recommendations.append(self._t(language, "Use the computed order and monitor progress against iteration dates.", "Используйте рассчитанный порядок и отслеживайте прогресс относительно дат итерации."))
        return recommendations

    async def _enhance_explanation(
        self,
        decisions: list[SchedulingDecision],
        workload_issues: list[WorkloadIssue],
        language: LanguageCode,
    ) -> Optional[LLMCallResult]:
        """Use LLM to enhance schedule explanation."""
        decisions_text = "\n".join([
            f"- {d.task_title}: {d.decision_type} - {d.reason}"
            for d in decisions
        ]) or "- No scheduling decisions were produced."
        workload_text = "\n".join([
            f"- {issue.member_name}: {issue.issue}"
            for issue in workload_issues
        ]) or "- No workload issues were reported."

        prompt = f"""Summarize the following scheduling decisions in 2-3 sentences for a project manager:

{self._language_instruction(language)}

{decisions_text}

Workload issues:
{workload_text}

        Keep it concise and focus on the most important points."""

        try:
            content = await self._call_llm(prompt)
            return LLMCallResult(
                content=content,
                finish_reason=getattr(self, "_last_finish_reason", None),
            )
        except Exception:
            logger.warning(
                "Schedule explanation provider call failed; preserving deterministic response",
                extra={"provider": self.provider},
                exc_info=True,
            )
            return None

    async def _call_llm(self, prompt: str) -> str:
        """Call LLM API."""
        result = await self._call_llm_result(prompt)
        self._last_finish_reason = result.finish_reason
        return result.content

    async def _call_llm_result(self, prompt: str) -> LLMCallResult:
        """Call LLM API and preserve OpenAI-compatible finish metadata."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": self.temperature,
                    "max_tokens": self.max_output_tokens
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            choice = data["choices"][0]
            return LLMCallResult(
                content=choice["message"]["content"],
                finish_reason=choice.get("finish_reason"),
            )
