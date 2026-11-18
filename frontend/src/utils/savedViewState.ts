import { defaultFilters } from './taskFilterDefaults';
import type { SavedView } from '../types/savedView';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';

/** The filters a saved view stores. */
export const savedViewFilters = (filters: TaskFilters): Record<string, unknown> => ({ ...filters });

export const filterSignature = (raw: Record<string, unknown> | TaskFilters) => JSON.stringify(
    Object.entries(defaultFilters).map(([key, fallback]) => {
        const value = raw[key as keyof typeof raw];
        if (Array.isArray(fallback)) return [key, Array.isArray(value) ? [...new Set(value.filter(item => typeof item === 'string'))].sort() : []];
        if (typeof fallback === 'string') return [key, typeof value === 'string' ? value : fallback];
        return [key, value ?? fallback];
    }),
);

const sameCondition = (left: unknown, right: unknown) => JSON.stringify(left ?? null) === JSON.stringify(right ?? null);

/**
 * Whether the shown filters or sort differ from the saved view (or from no filters when none is chosen).
 * `systemFilters` are conditions applied for the person, such as a hand-over from Plan: while a
 * condition still holds its handed-over value it does not count as a change.
 */
export const savedViewModified = (
    view: SavedView | null | undefined,
    filters: TaskFilters,
    sortKey: string,
    systemFilters: Partial<TaskFilters> = {},
) => {
    const baseline = (view?.filters_json ?? defaultFilters) as Record<string, unknown>;
    const compared: Record<string, unknown> = { ...filters };
    (Object.keys(systemFilters) as (keyof TaskFilters)[]).forEach(key => {
        if (sameCondition(filters[key], systemFilters[key])) compared[key] = baseline[key];
    });
    return filterSignature(compared) !== filterSignature(baseline)
        || sortKey !== (view?.sort_json.sortKey ?? 'priority');
};
