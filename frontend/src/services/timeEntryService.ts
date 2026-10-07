import api from './api';

export interface TimeValues { work_date: string; timezone: string; minutes: number; note: string }
export interface TimeEntry extends TimeValues {
    id: number; project_id: number; task_id: number | null; task_title: string | null; principal_id: number;
    version: number; voided: boolean; created_at: string; updated_at: string;
}
export interface TimePage { items: TimeEntry[]; has_more: boolean; next_after_id: number | null; upper_id: number }
export interface TimeRevision extends TimeValues { version: number; principal_id: number; reason: string; voided: boolean; created_at: string }
export interface TimeReport {
    project_id: number; scope: 'mine' | 'project'; start: string; end: string; upper_id: number;
    has_more: boolean; next_after_id: number | null; can_view_project_totals: boolean;
    items: { task_id: number; task_title: string | null; recorded_minutes: number | null; entry_count: number;
        estimate_hours: number | null; estimate_state: 'known' | 'unknown' | 'unavailable' }[];
    totals: { task_count: number; tasks_with_records: number; recorded_minutes: number | null;
        project_work_minutes: number | null; known_estimate_hours: number | null; tasks_with_estimates: number };
}
export interface TimeFilters { project_id: number; task_id?: number; start?: string; end?: string; scope?: 'mine' | 'project' }

export const timeAccessDenied = (error: unknown) => [401, 403, 404].includes((error as { response?: { status?: number } })?.response?.status ?? 0);
const boundedPage = <T extends { items: unknown[]; has_more: boolean; next_after_id: number | null; upper_id: number }>(page: T, after: number, upper?: number): T => {
    if (!Array.isArray(page.items) || page.items.length > 100 || typeof page.has_more !== 'boolean' || !Number.isSafeInteger(page.upper_id) || page.upper_id < 0
        || upper !== undefined && upper !== page.upper_id
        || page.has_more && (!Number.isSafeInteger(page.next_after_id) || page.next_after_id! <= after || page.next_after_id! > page.upper_id)
        || !page.has_more && page.next_after_id !== null) throw new Error('Invalid bounded time page; reload the current scope.');
    return page;
};

export const timeEntryService = {
    capabilities: async (signal?: AbortSignal) => (await api.get<{ schema_version: number; enabled: boolean }>('/time-entries/capabilities', { signal })).data,
    list: async (filters: TimeFilters, after_id = 0, upper_id?: number, signal?: AbortSignal) => {
        const page = boundedPage((await api.get<TimePage>('/time-entries', { params: { ...filters, after_id, upper_id, include_voided: true }, signal })).data, after_id, upper_id);
        if (page.items.some(row => !Number.isSafeInteger(row.id) || row.id <= after_id || row.id > page.upper_id
            || row.project_id !== filters.project_id || !Number.isSafeInteger(row.version) || row.version < 1
            || filters.task_id !== undefined && row.task_id !== filters.task_id)
            || page.items.some((row, index) => index > 0 && row.id <= page.items[index - 1].id)
            || page.has_more && page.next_after_id !== page.items.at(-1)?.id) throw new Error('Invalid or mismatched time-entry scope.');
        return page;
    },
    create: async (project_id: number, task_id: number | null, request_id: string, values: TimeValues) =>
        (await api.post<TimeEntry>('/time-entries', { ...values, project_id, task_id, request_id })).data,
    correct: async (entry: Pick<TimeEntry, 'id' | 'version'>, values: TimeValues, reason: string) =>
        (await api.put<TimeEntry>(`/time-entries/${entry.id}`, { ...values, reason, expected_version: entry.version })).data,
    void: async (entry: Pick<TimeEntry, 'id' | 'version'>, reason: string) =>
        (await api.post<TimeEntry>(`/time-entries/${entry.id}/void`, { reason, expected_version: entry.version })).data,
    get: async (id: number) => (await api.get<TimeEntry>(`/time-entries/${id}`)).data,
    history: async (id: number, after_version = 0, signal?: AbortSignal) => {
        const page = (await api.get<{ items: TimeRevision[]; has_more: boolean; next_after_version: number | null }>(`/time-entries/${id}/history`, { params: { after_version }, signal })).data;
        if (!Array.isArray(page.items) || page.items.length > 100 || typeof page.has_more !== 'boolean'
            || page.items.some((row, index) => !Number.isSafeInteger(row.version) || row.version <= (index ? page.items[index - 1].version : after_version))
            || page.has_more && page.next_after_version !== page.items.at(-1)?.version
            || !page.has_more && page.next_after_version !== null) throw new Error('Invalid correction-history page.');
        return page;
    },
    report: async (filters: TimeFilters & { start: string; end: string }, after_id = 0, upper_id?: number, signal?: AbortSignal) => {
        const page = boundedPage((await api.get<TimeReport>('/time-entries/report', { params: { ...filters, after_id, upper_id }, signal })).data, after_id, upper_id);
        if (page.project_id !== filters.project_id || page.start !== filters.start || page.end !== filters.end || page.scope !== (filters.scope ?? 'mine')
            || page.items.some((row, index) => !Number.isSafeInteger(row.task_id) || row.task_id <= (index ? page.items[index - 1].task_id : after_id) || row.task_id > page.upper_id)
            || page.has_more && page.next_after_id !== page.items.at(-1)?.task_id) throw new Error('Invalid or mismatched time-report scope.');
        return page;
    },
    export: async (filters: TimeFilters & { start: string; end: string }, kind: 'entries' | 'totals') =>
        (await api.get<Blob>('/time-entries/export', { params: { ...filters, kind }, responseType: 'blob' })).data,
};
