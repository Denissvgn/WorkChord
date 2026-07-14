import api from './api';

export const exportService = {
    exportIteration: async (iterationId: number) => {
        // For download, we might handle blob directly
        const response = await api.get(`/iterations/${iterationId}/export`, {
            responseType: 'blob'
        });
        return response.data;
    },

    importIteration: async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/iterations/import', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    importIntoIteration: async (iterationId: number, file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post(`/iterations/${iterationId}/import`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    }
};
