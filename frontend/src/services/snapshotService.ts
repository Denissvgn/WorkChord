import api from './api';

export interface IterationSnapshot {
    filename: string;
    created_at: string | null;
    reason: string;
    size_bytes: number;
}

export interface SnapshotRestoreResponse {
    message: string;
    success: boolean;
    source_snapshot: string;
    pre_restore_snapshot: string;
    restored_count: number;
    audit_event_id: number;
}

export const snapshotService = {
    list: async (iterationId: number) => {
        const response = await api.get<IterationSnapshot[]>(`/iterations/${iterationId}/snapshots`);
        return response.data;
    },

    restore: async (iterationId: number, filename: string) => {
        const response = await api.post<SnapshotRestoreResponse>(
            `/iterations/${iterationId}/snapshots/${encodeURIComponent(filename)}/restore`,
            { confirm: true },
        );
        return response.data;
    },
};
