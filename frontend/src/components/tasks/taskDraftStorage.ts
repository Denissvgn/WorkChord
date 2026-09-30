import type { TaskEditorValues } from './taskEditorContract';

export const readTaskDraft = (key: string | null, defaults: TaskEditorValues): TaskEditorValues | null => {
    if (!key) return null;
    try {
        const raw = sessionStorage.getItem(key);
        if (!raw) return null;
        const record = JSON.parse(raw);
        if (typeof record.savedAt !== 'number' || Date.now() - record.savedAt > 86400000
            || !record.values || typeof record.values.title !== 'string'
            || typeof record.values.priority !== 'number' || record.values.effort_days !== null && typeof record.values.effort_days !== 'number') return null;
        const values = { ...defaults };
        for (const field of Object.keys(defaults) as (keyof TaskEditorValues)[]) {
            if (!(field in record.values)) continue;
            const value = record.values[field];
            const initial = defaults[field];
            const nullable = ['brief', 'effort_days', 'owner_profile_id', 'description', 'assignee_id', 'project_id', 'milestone_id', 'parent_id', 'expected_version', 'min_start_date', 'max_end_date', 'effort_hours'].includes(field);
            if (field === 'brief' && value !== null) {
                const fields = ['goal', 'context', 'scope', 'exclusions', 'verification', 'artifact_expectations'];
                if (value?.schema_version === 1 && fields.every(key => typeof value[key] === 'string')
                    && Array.isArray(value.acceptance_criteria) && value.acceptance_criteria.length <= 100
                    && value.acceptance_criteria.every((item: { id?: unknown; text?: unknown; revision?: unknown; verification?: unknown }) => typeof item.id === 'string' && typeof item.text === 'string' && typeof item.verification === 'string' && Number.isInteger(item.revision))) values.brief = value;
                continue;
            }
            const compatible = Array.isArray(initial)
                ? Array.isArray(value) && value.every(item => field === 'depends_on' ? Number.isInteger(item) : typeof item === 'string')
                : value === null ? nullable : typeof value === typeof initial || initial === null && ['string', 'number'].includes(typeof value);
            if (compatible) {
                Object.assign(values, { [field]: value });
            }
        }
        return values;
    } catch { return null; }
};

export const writeTaskDraft = (key: string | null, values: TaskEditorValues) => {
    if (!key) return;
    try { sessionStorage.setItem(key, JSON.stringify({ savedAt: Date.now(), values })); } catch { /* The in-page draft remains available. */ }
};

export const removeTaskDraft = (key: string | null, includeProgress = false) => {
    if (!key) return;
    try { sessionStorage.removeItem(key); if (includeProgress) { sessionStorage.removeItem(`${key}:progress`); sessionStorage.removeItem(`${key}:discussion`); } } catch { /* Storage may be disabled. */ }
};
