"""Language resolution helpers for UI and AI output."""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass
from datetime import date
from html import escape
from typing import Any, Literal

LanguageCode = Literal["en", "ru"]
AILanguageMode = Literal["auto", "en", "ru"]

LANGUAGE_NAMES: dict[LanguageCode, str] = {
    "en": "English",
    "ru": "Russian",
}

_CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
_LATIN_RE = re.compile(r"[A-Za-z]")
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LanguageResolution:
    """Resolved language selection and the reason it was chosen."""

    language: LanguageCode
    mode: AILanguageMode
    source: Literal["forced", "detected", "fallback"]


def normalize_language(value: Any, default: LanguageCode = "en") -> LanguageCode:
    """Return a supported UI/output language."""
    normalized = str(value or "").strip().lower()
    if normalized in {"en", "ru"}:
        return normalized  # type: ignore[return-value]
    return default


def normalize_ai_language_mode(value: Any, default: AILanguageMode = "auto") -> AILanguageMode:
    """Return a supported AI language mode."""
    normalized = str(value or "").strip().lower()
    if normalized in {"auto", "en", "ru"}:
        return normalized  # type: ignore[return-value]
    return default


def flatten_language_context(value: Any) -> str:
    """Flatten nested context data into text for language detection."""
    parts: list[str] = []

    def collect(candidate: Any) -> None:
        if candidate is None:
            return
        if isinstance(candidate, dict):
            for nested in candidate.values():
                collect(nested)
        elif isinstance(candidate, (list, tuple, set)):
            for nested in candidate:
                collect(nested)
        else:
            text = str(candidate).strip()
            if text:
                parts.append(text)

    collect(value)
    return "\n".join(parts)


def detect_language_from_text(text: str) -> LanguageCode | None:
    """Detect English/Russian from dominant script in source context."""
    if not text.strip():
        return None
    cyrillic = len(_CYRILLIC_RE.findall(text))
    latin = len(_LATIN_RE.findall(text))
    meaningful = cyrillic + latin
    if meaningful < 8:
        return None
    if cyrillic >= 8 and cyrillic >= latin * 0.35:
        return "ru"
    if latin >= 8 and latin > cyrillic:
        return "en"
    return None


def resolve_ai_language(
    context: Any,
    default_language: LanguageCode = "en",
    mode: AILanguageMode = "auto",
) -> LanguageResolution:
    """Resolve the AI output language from mode, context, and fallback language."""
    default_language = normalize_language(default_language)
    mode = normalize_ai_language_mode(mode)
    if mode == "en" or mode == "ru":
        language: LanguageCode = mode
        return LanguageResolution(language=language, mode=mode, source="forced")

    detected = detect_language_from_text(flatten_language_context(context))
    if detected:
        return LanguageResolution(language=detected, mode=mode, source="detected")
    return LanguageResolution(language=default_language, mode=mode, source="fallback")


def language_instruction(language: LanguageCode) -> str:
    """Return a prompt instruction that localizes prose while preserving technical tokens."""
    language = normalize_language(language)
    return (
        f"Write all human-readable prose in {LANGUAGE_NAMES[language]}. "
        "Keep JSON keys in English. Do not translate code identifiers, API paths, "
        "database table names, enum values, label slugs, statuses, IDs, URLs, or quoted source text."
    )


def localized(language: LanguageCode, en: str, ru: str) -> str:
    """Return a localized string for deterministic fallback text."""
    return ru if normalize_language(language) == "ru" else en


_RESOURCE_LABELS: dict[str, tuple[str, str, str]] = {
    "calendar": ("Calendar", "Календарь", "не найден"),
    "classification_suggestion": ("Classification suggestion", "Предложение классификации", "не найдено"),
    "dependency": ("Dependency", "Зависимость", "не найдена"),
    "dependency_task": ("Dependency task", "Задача-зависимость", "не найдена"),
    "external_link": ("External link", "Внешняя ссылка", "не найдена"),
    "github_status_automation_rule": ("GitHub status automation rule", "Правило GitHub status automation", "не найдено"),
    "initiative": ("Initiative", "Инициатива", "не найдена"),
    "iteration": ("Iteration", "Итерация", "не найдена"),
    "label": ("Label", "Метка", "не найдена"),
    "label_group": ("Label group", "Группа меток", "не найдена"),
    "milestone": ("Milestone", "Веха", "не найдена"),
    "outbound_webhook_delivery": ("Outbound webhook delivery", "Доставка outbound webhook", "не найдена"),
    "outbound_webhook_target": ("Outbound webhook target", "Цель outbound webhook", "не найдена"),
    "parent_task": ("Parent task", "Родительская задача", "не найдена"),
    "project": ("Project", "Проект", "не найден"),
    "release": ("Release", "Релиз", "не найден"),
    "request_source": ("Request source", "Источник запроса", "не найден"),
    "request_source_link": ("Request source link", "Связь источника запроса", "не найдена"),
    "run": ("Run", "Запуск", "не найден"),
    "saved_view": ("Saved view", "Сохраненное представление", "не найдено"),
    "task": ("Task", "Задача", "не найдена"),
    "team_member": ("Team member", "Участник команды", "не найден"),
    "team_member_profile": ("Team member profile", "Профиль участника команды", "не найден"),
    "team_member_profile_skill": ("Team member profile skill", "Навык профиля участника команды", "не найден"),
    "template": ("Template", "Шаблон", "не найден"),
    "triage_item": ("Triage item", "Элемент Triage", "не найден"),
    "vacation": ("Vacation", "Отпуск", "не найден"),
}

_DELETED_LABELS: dict[str, tuple[str, str, str]] = {
    "github_status_automation_rule": ("GitHub status automation rule", "Правило GitHub status automation", "удалено"),
    "initiative": ("Initiative", "Инициатива", "удалена"),
    "outbound_webhook_target": ("Outbound webhook target", "Цель outbound webhook", "удалена"),
    "project": ("Project", "Проект", "удален"),
    "project_milestone": ("Project milestone", "Веха проекта", "удалена"),
    "saved_view": ("Saved view", "Сохраненное представление", "удалено"),
}

_EXACT_BACKEND_MESSAGES: dict[str, str] = {
    "A triage item cannot be a duplicate of itself.": "Элемент Triage не может быть дубликатом самого себя.",
    "Automation already processed for this delivery": "Автоматизация уже обработана для этой доставки",
    "Cannot duplicate an invalid saved view": "Нельзя дублировать недействительное сохраненное представление",
    "Cannot retry delivery because its target was deleted": "Нельзя повторить доставку, потому что ее цель была удалена",
    "Could not add dependency. Check that both tasks exist and are different.": "Не удалось добавить зависимость. Проверьте, что обе задачи существуют и различаются.",
    "Could not merge tasks. Ensure all tasks exist, belong to this iteration, and have no children.": "Не удалось объединить задачи. Убедитесь, что все задачи существуют, относятся к этой итерации и не имеют дочерних задач.",
    "GitHub response was not a JSON object": "Ответ GitHub не является JSON-объектом",
    "GitHub payload is missing pull_request": "В payload GitHub отсутствует pull_request",
    "GitHub pull request payload is missing number": "В payload GitHub pull request отсутствует number",
    "GitHub pull request payload is missing repository": "В payload GitHub pull request отсутствует repository",
    "GitHub pull request payload is missing repository full_name": "В payload GitHub pull request отсутствует repository full_name",
    "GitHub webhook payload must be a JSON object": "Payload GitHub webhook должен быть JSON-объектом",
    "GitHub webhook payload must be valid JSON": "Payload GitHub webhook должен быть валидным JSON",
    "GitHub webhook secret is not configured": "Секрет GitHub webhook не настроен",
    "Header names must be non-empty": "Имена заголовков не должны быть пустыми",
    "Invalid GitHub webhook signature": "Недействительная подпись GitHub webhook",
    "Missing X-Agent-API-Key header": "Отсутствует заголовок X-Agent-API-Key",
    "Missing X-GitHub-Event header": "Отсутствует заголовок X-GitHub-Event",
    "Missing GitHub webhook signature": "Отсутствует подпись GitHub webhook",
    "Missing iteration data in export file": "В файле экспорта отсутствуют данные итерации",
    "Only the creating session can delete this saved view": "Только создавшая сессия может удалить это сохраненное представление",
    "Only the creating session can update this saved view": "Только создавшая сессия может изменить это сохраненное представление",
    "Personal saved views require created_by_session_id": "Для личных сохраненных представлений требуется created_by_session_id",
    "Project has linked tasks. Use detach_tasks=true to delete and detach tasks.": "У проекта есть связанные задачи. Используйте detach_tasks=true, чтобы удалить проект и отвязать задачи.",
    "Classification suggestion belongs to another triage item": "Предложение классификации относится к другому элементу Triage",
    "Existing task project must match the scoped iteration project.": "Проект существующей задачи должен совпадать с проектом scoped iteration.",
    "Moved subtask project must match parent task project.": "Проект перемещаемой подзадачи должен совпадать с проектом родительской задачи.",
    "Moved task project must match the target iteration project.": "Проект перемещаемой задачи должен совпадать с проектом целевой итерации.",
    "Parent task must belong to the same iteration.": "Родительская задача должна относиться к той же итерации.",
    "Parent task must belong to the target iteration.": "Родительская задача должна относиться к целевой итерации.",
    "Parent task project must match the scoped iteration project.": "Проект родительской задачи должен совпадать с проектом scoped iteration.",
    "Subtask project must match parent task project.": "Проект подзадачи должен совпадать с проектом родительской задачи.",
    "System saved views are read-only": "Системные сохраненные представления доступны только для чтения",
    "Task cannot be moved under itself or its descendants.": "Задачу нельзя переместить внутрь самой себя или ее дочерних задач.",
    "Task dependencies must belong to the same iteration.": "Зависимости задачи должны относиться к той же итерации.",
    "Task dependencies must belong to the selected iteration": "Зависимости задачи должны относиться к выбранной итерации",
    "Task has no children to unmerge": "У задачи нет дочерних задач для разъединения",
    "Task is already at target status": "Задача уже находится в целевом статусе",
    "Task milestone requires a project.": "Веха задачи требует project.",
    "Task milestone must belong to the scoped iteration project.": "Веха задачи должна относиться к проекту scoped iteration.",
    "Task milestone must belong to the target iteration project.": "Веха задачи должна относиться к проекту целевой итерации.",
    "Task milestone must belong to the task project.": "Веха задачи должна относиться к проекту задачи.",
    "Task move would leave dependencies crossing iterations.": "Перемещение задачи оставит зависимости между разными итерациями.",
    "Task project must match the scoped iteration project.": "Проект задачи должен совпадать с проектом scoped iteration.",
    "Task status does not match rule from_status": "Статус задачи не совпадает с from_status правила",
    "Tasks in a scoped iteration must match the iteration project.": "Задачи в scoped iteration должны совпадать с проектом итерации.",
    "Template must be an active task template": "Шаблон должен быть активным шаблоном задачи",
    "Triage conversion into an unscoped iteration requires an explicit project_id or null project_id.": "Конвертация Triage в unscoped iteration требует явный project_id или null project_id.",
    "Triage item has already been converted": "Элемент Triage уже был конвертирован",
    "Use the task status transition endpoint to change status.": "Используйте endpoint перехода статуса задачи для изменения status.",
    "entity_type is required": "entity_type обязателен",
    "event_type must use dot notation": "event_type должен использовать dot notation",
    "label slug already exists": "slug метки уже существует",
    "label group key already exists": "key группы меток уже существует",
    "labels must be a list": "labels должен быть списком",
    "labels must contain at least one non-empty label": "labels должен содержать хотя бы одну непустую метку",
    "priority must be between 1 and 10": "priority должен быть от 1 до 10",
    "set_flags requires is_optional or is_deferred": "set_flags требует is_optional или is_deferred",
    "snoozed_until must be in the future": "snoozed_until должен быть в будущем",
    "status is required": "status обязателен",
    "task_ids must not contain duplicates": "task_ids не должен содержать дубликаты",
    "view_type must be one of tasks, projects, or triage": "view_type должен быть одним из tasks, projects или triage",
}


def entity_not_found_message(entity: str, entity_id: Any, language: LanguageCode = "en") -> str:
    """Return the existing `<entity> with id <id> not found` shape localized."""
    en_label, ru_label, ru_suffix = _RESOURCE_LABELS.get(entity, (entity, entity, "не найдено"))
    return localized(
        language,
        f"{en_label} with id {entity_id} not found",
        f"{ru_label} с id {entity_id} {ru_suffix}",
    )


def scoped_entity_not_found_message(
    entity: str,
    entity_id: Any,
    scope: str,
    scope_id: Any,
    language: LanguageCode = "en",
) -> str:
    """Return a localized `not found for <scope>` detail while preserving IDs."""
    en_label, ru_label, ru_suffix = _RESOURCE_LABELS.get(entity, (entity, entity, "не найдено"))
    scope_en, scope_ru, _ = _RESOURCE_LABELS.get(scope, (scope, scope, ""))
    return localized(
        language,
        f"{en_label} with id {entity_id} not found for {scope_en.lower()} {scope_id}",
        f"{ru_label} с id {entity_id} {ru_suffix} для {scope_ru.lower()} {scope_id}",
    )


def entity_deleted_message(entity: str, entity_id: Any, language: LanguageCode = "en") -> str:
    """Return a localized deletion success message without changing response shape."""
    en_label, ru_label, ru_suffix = _DELETED_LABELS.get(entity, (entity, entity, "удален"))
    return localized(
        language,
        f"{en_label} {entity_id} deleted",
        f"{ru_label} {entity_id} {ru_suffix}",
    )


def backend_error_message(message: str, language: LanguageCode = "en") -> str:
    """Localize common backend-generated detail strings while preserving tokens and IDs."""
    if normalize_language(language) != "ru":
        return message

    if message in _EXACT_BACKEND_MESSAGES:
        return _EXACT_BACKEND_MESSAGES[message]

    lowered = message.lower()
    if lowered in _EXACT_BACKEND_MESSAGES:
        return _EXACT_BACKEND_MESSAGES[lowered]

    match = re.fullmatch(r"(.+) with id ([^ ]+) not found", message)
    if match:
        label, entity_id = match.groups()
        entity = label.strip().lower().replace(" ", "_")
        return entity_not_found_message(entity, entity_id, language)

    match = re.fullmatch(r"(.+) with id ([^ ]+) not found for (.+) ([^ ]+)", message)
    if match:
        label, entity_id, scope_label, scope_id = match.groups()
        entity = label.strip().lower().replace(" ", "_")
        scope = scope_label.strip().lower().replace(" ", "_")
        return scoped_entity_not_found_message(entity, entity_id, scope, scope_id, language)

    match = re.fullmatch(r"(.+) ([^ ]+) deleted", message)
    if match:
        label, entity_id = match.groups()
        entity = label.strip().lower().replace(" ", "_")
        return entity_deleted_message(entity, entity_id, language)

    match = re.fullmatch(r"Unsupported webhook event domain: (.+)", message)
    if match:
        return f"Неподдерживаемый домен webhook event: {match.group(1)}"

    match = re.fullmatch(r"Unsupported webhook event: (.+)", message)
    if match:
        return f"Неподдерживаемый webhook event: {match.group(1)}"

    match = re.fullmatch(r"Unsupported delivery status: (.+)", message)
    if match:
        return f"Неподдерживаемый статус доставки: {match.group(1)}"

    match = re.fullmatch(r"Unsupported bulk action: (.+)", message)
    if match:
        return f"Неподдерживаемое bulk action: {match.group(1)}"

    match = re.fullmatch(r"Header (.+) is managed by the webhook service", message)
    if match:
        return f"Заголовок {match.group(1)} управляется сервисом webhook"

    match = re.fullmatch(r"Duplicate task IDs are not allowed: (.+)", message)
    if match:
        return f"Дублирующиеся task IDs не разрешены: {match.group(1)}"

    match = re.fullmatch(r"Task IDs not found: (.+)", message)
    if match:
        return f"Task IDs не найдены: {match.group(1)}"

    match = re.fullmatch(r"Task IDs must belong to project ([^:]+): (.+)", message)
    if match:
        return f"Task IDs должны относиться к проекту {match.group(1)}: {match.group(2)}"

    match = re.fullmatch(r"Task dependency not found: (.+)", message)
    if match:
        return f"Зависимость задачи не найдена: {match.group(1)}"

    match = re.fullmatch(r"Dependency not found: Task (.+) -> Task (.+)", message)
    if match:
        return f"Зависимость не найдена: Task {match.group(1)} -> Task {match.group(2)}"

    match = re.fullmatch(r"status must be one of (.+)", message)
    if match:
        return f"status должен быть одним из {match.group(1)}"

    match = re.fullmatch(r"statuses must contain only (.+)", message)
    if match:
        return f"statuses должен содержать только {match.group(1)}"

    match = re.fullmatch(r"Team member with id ([^ ]+) is linked to profile ([^,]+), not (.+)", message)
    if match:
        return f"Участник команды с id {match.group(1)} связан с профилем {match.group(2)}, а не {match.group(3)}"

    match = re.fullmatch(r"Use triage action endpoints to update: (.+)", message)
    if match:
        return f"Используйте endpoints действий Triage для изменения: {match.group(1)}"

    match = re.fullmatch(r"(.+) must be a JSON object", message)
    if match:
        return f"{match.group(1)} должен быть JSON-объектом"

    match = re.fullmatch(r"(.+) must be an integer or null", message)
    if match:
        return f"{match.group(1)} должен быть целым числом или null"

    match = re.fullmatch(r"(.+) must be an integer", message)
    if match:
        return f"{match.group(1)} должен быть целым числом"

    match = re.fullmatch(r"(.+) must be at least (.+)", message)
    if match:
        return f"{match.group(1)} должен быть не меньше {match.group(2)}"

    match = re.fullmatch(r"(.+) must be at most (.+)", message)
    if match:
        return f"{match.group(1)} должен быть не больше {match.group(2)}"

    match = re.fullmatch(r"(.+) must be a boolean or null", message)
    if match:
        return f"{match.group(1)} должен быть boolean или null"

    match = re.fullmatch(r"(.+) must be a boolean", message)
    if match:
        return f"{match.group(1)} должен быть boolean"

    match = re.fullmatch(r"(.+) must be a string", message)
    if match:
        return f"{match.group(1)} должен быть строкой"

    match = re.fullmatch(r"(.+) must be one of (.+), or empty", message)
    if match:
        return f"{match.group(1)} должен быть одним из {match.group(2)} или пустым"

    match = re.fullmatch(r"(.+) must be one of (.+)", message)
    if match:
        return f"{match.group(1)} должен быть одним из {match.group(2)}"

    match = re.fullmatch(r"(.+) must be a YYYY-MM-DD string or empty", message)
    if match:
        return f"{match.group(1)} должен быть строкой YYYY-MM-DD или пустым"

    match = re.fullmatch(r"(.+) must be a list of strings", message)
    if match:
        return f"{match.group(1)} должен быть списком строк"

    match = re.fullmatch(r"(.+) is required", message)
    if match:
        return f"{match.group(1)} обязателен"

    return message


async def resolve_runtime_ui_language(db: Any = None, default: LanguageCode | None = None) -> LanguageCode:
    """Resolve the runtime UI language from DB-backed settings, then environment/default."""
    fallback = normalize_language(default)
    if db is not None:
        try:
            from app.services.system_settings_service import RuntimeSettingsService

            settings = await RuntimeSettingsService(db).get_app_settings()
            return normalize_language(getattr(settings, "app_ui_language", None), default=fallback)
        except Exception:
            # Runtime settings are optional; environment/default language remains safe.
            logger.warning(
                "Unable to resolve DB-backed runtime UI language; using fallback",
                exc_info=True,
            )
    try:
        from app.config import get_settings

        return normalize_language(getattr(get_settings(), "app_ui_language", None), default=fallback)
    except Exception:
        # Configuration access is a process boundary; the explicit fallback is safe.
        logger.warning(
            "Unable to resolve environment-backed UI language; using fallback",
            exc_info=True,
        )
        return fallback


_TASK_STATUS_LABELS: dict[LanguageCode, dict[str, str]] = {
    "en": {
        "planned": "Planned",
        "active": "Active",
        "resolved": "Resolved",
        "closed": "Closed",
    },
    "ru": {
        "planned": "Запланировано",
        "active": "Активно",
        "resolved": "Решено",
        "closed": "Закрыто",
    },
}


def task_status_label(status: str, language: LanguageCode = "en") -> str:
    """Return a user-facing label for a task status while preserving unknown enum values."""
    language = normalize_language(language)
    return _TASK_STATUS_LABELS[language].get(str(status), str(status))


def invalid_status_transition_message(old_status: str, new_status: str, language: LanguageCode = "en") -> str:
    """Return the existing status-transition validation detail shape in the UI language."""
    return localized(
        language,
        f"Invalid status transition from '{old_status}' to '{new_status}'",
        f"Недопустимый переход статуса с '{old_status}' на '{new_status}'",
    )


def task_requires_schedule_message(language: LanguageCode = "en") -> str:
    """Return the transition error shown when a planned task lacks scheduled dates."""
    return localized(
        language,
        "Task cannot be transitioned until execution dates are scheduled. Run Auto-Schedule.",
        "Задача не может быть переведена пока не спланированы сроки исполнения. Выполните Auto-Schedule.",
    )


def incomplete_dependency_message(
    dependency_title: str,
    dependency_status: str,
    language: LanguageCode = "en",
) -> str:
    """Return the transition error shown when a dependency blocks activation."""
    return localized(
        language,
        (
            "Cannot change status: dependency "
            f"'{dependency_title}' is not complete (current status: {dependency_status})"
        ),
        (
            "Невозможно сменить статус: зависимость "
            f"'{dependency_title}' не завершена (текущий статус: {dependency_status})"
        ),
    )


def automatic_child_status_reason(language: LanguageCode = "en") -> str:
    """Return the audit reason for automatic parent status updates."""
    return localized(
        language,
        "Automatic transition based on child task statuses",
        "Автоматический переход по статусам дочерних задач",
    )


def notification_status_change_subject(
    task_id: int,
    old_status: str,
    new_status: str,
    language: LanguageCode = "en",
) -> str:
    """Return a localized status-change email subject."""
    old_label = task_status_label(old_status, language)
    new_label = task_status_label(new_status, language)
    return localized(
        language,
        f"[PM] Task #{task_id}: {old_label} → {new_label}",
        f"[PM] Задача #{task_id}: {old_label} → {new_label}",
    )


def notification_status_change_body_html(
    task_title: str,
    task_id: int,
    old_status: str,
    new_status: str,
    cascade_updates: list[dict],
    reason: str | None,
    language: LanguageCode = "en",
) -> str:
    """Return a localized status-change email body."""
    old_label = task_status_label(old_status, language)
    new_label = task_status_label(new_status, language)
    title = escape(task_title)
    escaped_reason = escape(reason) if reason else ""
    if normalize_language(language) == "ru":
        heading = "Изменение статуса задачи"
        task_label = "Задача"
        status_label = "Статус"
        reason_label = "Причина"
        cascade_heading = "⚠️ Каскадное обновление зависимых задач:"
        headers = ("Задача", "Старые даты", "Новые даты")
    else:
        heading = "Task status changed"
        task_label = "Task"
        status_label = "Status"
        reason_label = "Reason"
        cascade_heading = "⚠️ Dependent tasks were updated:"
        headers = ("Task", "Old dates", "New dates")

    body_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>{heading}</h2>
            <p><strong>{task_label}:</strong> {title} (#{task_id})</p>
            <p><strong>{status_label}:</strong> {old_label} → <strong>{new_label}</strong></p>
            {f"<p><strong>{reason_label}:</strong> {escaped_reason}</p>" if escaped_reason else ""}
        """

    if cascade_updates:
        body_html += f"""
            <h3>{cascade_heading}</h3>
            <table border="1" cellpadding="5" style="border-collapse: collapse;">
                <tr>
                    <th>{headers[0]}</th>
                    <th>{headers[1]}</th>
                    <th>{headers[2]}</th>
                </tr>
            """
        for update in cascade_updates:
            body_html += f"""
                <tr>
                    <td>{escape(str(update.get('task_title', 'N/A')))}</td>
                    <td>{escape(str(update.get('old_start_date', '-')))} → {escape(str(update.get('old_end_date', '-')))}</td>
                    <td>{escape(str(update.get('new_start_date', '-')))} → {escape(str(update.get('new_end_date', '-')))}</td>
                </tr>
                """
        body_html += "</table>"

    body_html += """
        </body>
        </html>
        """
    return body_html


def notification_overdue_subject(task_id: int, days_overdue: int, language: LanguageCode = "en") -> str:
    """Return a localized overdue-start email subject."""
    return localized(
        language,
        f"[PM] ⚠️ Task #{task_id} did not start on time ({days_overdue} day(s))",
        f"[PM] ⚠️ Задача #{task_id} не начата вовремя ({days_overdue} дн.)",
    )


def notification_overdue_body_html(
    task_title: str,
    task_id: int,
    planned_start: date,
    days_overdue: int,
    language: LanguageCode = "en",
) -> str:
    """Return a localized overdue-start email body."""
    title = escape(task_title)
    if normalize_language(language) == "ru":
        heading = "⚠️ Задержка старта задачи"
        task_label = "Задача"
        planned_label = "Запланированный старт"
        overdue_label = "Задержка"
        guidance = "Пожалуйста, переведите задачу в статус <strong>Активно</strong> или скорректируйте план."
        day_text = f"{days_overdue} дней"
    else:
        heading = "⚠️ Task start is delayed"
        task_label = "Task"
        planned_label = "Planned start"
        overdue_label = "Delay"
        guidance = "Please move the task to <strong>Active</strong> or adjust the plan."
        day_text = f"{days_overdue} day(s)"

    return f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #7c3aed;">{heading}</h2>
            <p><strong>{task_label}:</strong> {title} (#{task_id})</p>
            <p><strong>{planned_label}:</strong> {planned_start}</p>
            <p><strong>{overdue_label}:</strong> {day_text}</p>
            <p style="color: #7c3aed;">{guidance}</p>
        </body>
        </html>
        """
