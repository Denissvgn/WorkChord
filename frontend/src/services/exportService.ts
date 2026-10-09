import { revisionHeaders, type ObservedRevisions } from './planningInputService';
import api from './api';

export const exportService = {
    previewImport: async (file: File, iterationId?: number, signal?: AbortSignal) => {
        const data = new FormData(); data.append('file', file);
        return (await api.post<{ complete: true; expected_revisions: ObservedRevisions; file_sha256: string }>(
            iterationId ? `/iterations/${iterationId}/import-context` : '/iterations/import-context', data, { signal })).data;
    },
    exportIteration: async (iterationId: number) => {
        // For download, we might handle blob directly
        const response = await api.get(`/iterations/${iterationId}/export`, {
            responseType: 'blob'
        });
        return response.data;
    },

    importIteration: async (file: File, revisions: ObservedRevisions) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/iterations/import', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                ...revisionHeaders(revisions),
            },
        });
        return response.data;
    },

    importIntoIteration: async (iterationId: number, file: File, revisions: ObservedRevisions) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post(`/iterations/${iterationId}/import`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                ...revisionHeaders(revisions),
            },
        });
        return response.data;
    }
};
