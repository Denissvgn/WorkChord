import { create } from 'zustand';
import type { SampleManifest } from './sampleProject';

const STORAGE_KEY = 'workchord-sample-project';
const validId = (value: unknown) => typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
const read = (): SampleManifest | null => {
    try {
        const value = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? 'null') as SampleManifest | null;
        if (!value || typeof value.owner !== 'string' || typeof value.complete !== 'boolean' || !Array.isArray(value.records)
            || value.records.some(item => !['project', 'milestone', 'iteration', 'profile', 'member', 'task'].includes(item.kind)
                || !Number.isSafeInteger(item.id) || item.id < 1 || typeof item.name !== 'string')) return null;
        if (value.previousScope && (!(value.previousScope.project === 'all' || validId(value.previousScope.project))
            || !(value.previousScope.iteration === 'backlog' || validId(value.previousScope.iteration)))) delete value.previousScope;
        return value;
    } catch { return null; }
};
interface SampleState {
    manifest: SampleManifest | null;
    busy: boolean;
    save: (manifest: SampleManifest) => void;
    setBusy: (busy: boolean) => void;
}

/** This is a deletion receipt, never a source of onboarding completion or plan readiness. */
export const useSampleProject = create<SampleState>(set => ({
    manifest: read(), busy: false,
    save: manifest => {
        // Retain the in-memory receipt even if browser storage becomes unavailable mid-load.
        set({ manifest: { ...manifest, records: [...manifest.records] } });
        localStorage.setItem(STORAGE_KEY, JSON.stringify(manifest));
    },
    setBusy: busy => set({ busy }),
}));
