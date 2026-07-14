import api from './api';
import type {
    SavedView,
    SavedViewCreate,
    SavedViewDashboardCard,
    SavedViewDuplicate,
    SavedViewListParams,
    SavedViewUpdate,
} from '../types/savedView';

const buildSavedViewListQuery = (params: SavedViewListParams) => {
    const searchParams = new URLSearchParams();
    searchParams.set('view_type', params.view_type);
    return `?${searchParams.toString()}`;
};

export interface FrontendSavedViewService {
    getAll: (params: SavedViewListParams) => Promise<SavedView[]>;
    getById: (savedViewId: number) => Promise<SavedView>;
    getDashboardCards: (iterationId: number) => Promise<SavedViewDashboardCard[]>;
    create: (data: SavedViewCreate) => Promise<SavedView>;
    update: (savedViewId: number, data: SavedViewUpdate) => Promise<SavedView>;
    delete: (savedViewId: number) => Promise<void>;
    duplicate: (savedViewId: number, data?: SavedViewDuplicate) => Promise<SavedView>;
}

export const savedViewService: FrontendSavedViewService = {
    getAll: async (params: SavedViewListParams) => {
        const response = await api.get<SavedView[]>(`/saved-views${buildSavedViewListQuery(params)}`);
        return response.data;
    },

    getById: async (savedViewId: number) => {
        const response = await api.get<SavedView>(`/saved-views/${savedViewId}`);
        return response.data;
    },

    getDashboardCards: async (iterationId: number) => {
        const response = await api.get<SavedViewDashboardCard[]>(
            `/saved-views/dashboard-cards?iteration_id=${iterationId}`
        );
        return response.data;
    },

    create: async (data: SavedViewCreate) => {
        const response = await api.post<SavedView>('/saved-views', data);
        return response.data;
    },

    update: async (savedViewId: number, data: SavedViewUpdate) => {
        const response = await api.put<SavedView>(`/saved-views/${savedViewId}`, data);
        return response.data;
    },

    delete: async (savedViewId: number) => {
        await api.delete(`/saved-views/${savedViewId}`);
    },

    duplicate: async (savedViewId: number, data: SavedViewDuplicate = {}) => {
        const response = await api.post<SavedView>(`/saved-views/${savedViewId}/duplicate`, data);
        return response.data;
    },
};
