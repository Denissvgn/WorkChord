import i18n from '../../i18n/i18n';
import type { SavedView } from '../../types/savedView';
import type { Task } from '../../types/task';
import type {
    TriageItem,
    TriageItemStatus,
    TriageTaskDraftResponse
} from '../../types/triage';

export const t = i18n.t.bind(i18n);

export const statusOptions: TriageItemStatus[] = ['new', 'accepted', 'snoozed', 'declined', 'duplicate', 'converted'];

export const statusLabelKeys: Record<TriageItemStatus, string> = {
    new: 'surfaces.triagePage.statuses.new',
    accepted: 'surfaces.triagePage.statuses.accepted',
    declined: 'surfaces.triagePage.statuses.declined',
    duplicate: 'surfaces.triagePage.statuses.duplicate',
    snoozed: 'surfaces.triagePage.statuses.snoozed',
    converted: 'surfaces.triagePage.statuses.converted',
};

export const statusClassName = (status: TriageItemStatus) => {
    switch (status) {
        case 'accepted':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'declined':
            return 'bg-surface-muted text-content-secondary border-border';
        case 'duplicate':
            return 'bg-surface-muted text-content-secondary border-border';
        case 'snoozed':
            return 'bg-surface-muted text-content-secondary border-border';
        case 'converted':
            return 'bg-feedback-purple-muted text-feedback-purple-foreground border-feedback-purple-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
};

export const triageFiltersFromSavedView = (view: SavedView) => {
    const raw = view.filters_json;
    const statuses = Array.isArray(raw.statuses)
        ? raw.statuses.filter((status): status is TriageItemStatus => (
            typeof status === 'string' && statusOptions.includes(status as TriageItemStatus)
        ))
        : [];

    return {
        active: typeof raw.active === 'boolean' ? raw.active : true,
        status: statuses[0] ?? '',
        q: typeof raw.q === 'string' ? raw.q : '',
        source: typeof raw.source === 'string' ? raw.source : '',
    };
};

export const toLocalDateTimeInputValue = (date: Date) => {
    const timezoneOffsetMs = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - timezoneOffsetMs).toISOString().slice(0, 16);
};

export const optionalText = (value: string) => {
    const trimmed = value.trim();
    return trimmed ? trimmed : null;
};

export const parseOptionalNumber = (value: string) => value ? Number(value) : null;

export const formatSuggestionScore = (score: number) => score.toFixed(score >= 10 ? 1 : 2);

export const formatDraftDescription = (draft: TriageTaskDraftResponse) => {
    const sections = [draft.suggested_description.trim()].filter(Boolean);

    if (draft.acceptance_criteria.length > 0) {
        sections.push(`Acceptance Criteria:\n${draft.acceptance_criteria.map(item => `- ${item}`).join('\n')}`);
    }
    if (draft.suggested_checklist.length > 0) {
        sections.push(`Checklist:\n${draft.suggested_checklist.map(item => `- ${item}`).join('\n')}`);
    }
    if (draft.risks.length > 0) {
        sections.push(`Risks:\n${draft.risks.map(item => `- ${item}`).join('\n')}`);
    }

    return sections.join('\n\n');
};

export const isDueSnoozed = (item: TriageItem) => {
    if (item.status !== 'snoozed' || !item.snoozed_until) return false;
    return new Date(item.snoozed_until).getTime() <= Date.now();
};

export const SOURCE_LINK_ERROR_CODE = 'intake_source_link_not_allowed';

/** The named source-link refusal as one sentence (what is wrong plus the next step), or null for any other error. */
export const getSourceLinkError = (error: unknown): string | null => {
    const detail = (error as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail;
    if (!detail || typeof detail !== 'object') return null;
    const { code, message, next_step: nextStep } = detail as { code?: unknown; message?: unknown; next_step?: unknown };
    if (code !== SOURCE_LINK_ERROR_CODE || typeof message !== 'string') return null;
    return typeof nextStep === 'string' && nextStep ? `${message} ${nextStep}` : message;
};

export const getErrorMessage = (error: unknown, fallback: string) => {
    const response = (error as { response?: { data?: { detail?: unknown } } })?.response;
    const detail = response?.data?.detail;

    if (typeof detail === 'string') return detail;
    if (detail && typeof detail === 'object' && typeof (detail as { message?: unknown }).message === 'string') {
        return (detail as { message: string }).message;
    }
    if (Array.isArray(detail)) {
        const messages = detail
            .map(item => {
                if (typeof item === 'string') return item;
                if (item && typeof item === 'object' && 'msg' in item) {
                    return String((item as { msg: unknown }).msg);
                }
                return '';
            })
            .filter(Boolean);
        if (messages.length > 0) return messages.join(', ');
    }
    if (error instanceof Error && error.message) return error.message;
    return fallback;
};

interface TaskListOption {
    id: number;
    title: string;
    depth: number;
}

export const flattenTasks = (tasks: Task[] = [], depth = 0): TaskListOption[] => {
    return tasks.flatMap(task => [
        { id: task.id, title: task.title, depth },
        ...flattenTasks(task.children ?? [], depth + 1),
    ]);
};

export const makeLookup = <T extends { id: number; name: string }>(items: T[]) => {
    return items.reduce<Record<number, string>>((lookup, item) => {
        lookup[item.id] = item.name;
        return lookup;
    }, {});
};

export type TriageLifecycleAction = 'accept' | 'decline' | 'snooze' | 'clarify' | 'duplicate';

// Sources the agent role skills write, shown by name in the source filter.
export const AGENT_SOURCE_LABEL_KEYS: Record<string, string> = {
    'agent-observed-defect': 'surfaces.triagePage.sourceAgentDefect',
    'agent-discovery': 'surfaces.triagePage.sourceAgentDiscovery',
};

export interface DuplicateActionDefaults {
    targetType: 'triage' | 'task';
    targetId: number;
    title: string;
    iterationId?: number | null;
}

