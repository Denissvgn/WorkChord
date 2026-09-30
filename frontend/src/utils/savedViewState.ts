import { defaultFilters } from './taskFilterDefaults';
import type { SavedView } from '../types/savedView';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';

export const filterSignature = (raw: Record<string, unknown> | TaskFilters) => JSON.stringify(
    Object.entries(defaultFilters).map(([key, fallback]) => {
        const value = raw[key as keyof typeof raw];
        if (Array.isArray(fallback)) return [key, Array.isArray(value) ? [...new Set(value.filter(item => typeof item === 'string'))].sort() : []];
        if (typeof fallback === 'string') return [key, typeof value === 'string' ? value : fallback];
        return [key, value ?? fallback];
    }),
);

export const savedViewModified = (view: SavedView | null | undefined, filters: TaskFilters, sortKey: string) => (
    filterSignature(filters) !== filterSignature(view?.filters_json ?? defaultFilters)
    || sortKey !== (view?.sort_json.sortKey ?? 'priority')
);
