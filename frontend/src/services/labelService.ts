import api from './api';
import type {
    Label,
    LabelCreate,
    LabelGroup,
    LabelGroupCreate,
    LabelGroupListParams,
    LabelGroupUpdate,
    LabelListParams,
    LabelUpdate,
} from '../types/label';

const buildLabelGroupQuery = (params?: LabelGroupListParams) => {
    const searchParams = new URLSearchParams();

    if (params?.include_inactive !== undefined) {
        searchParams.set('include_inactive', String(params.include_inactive));
    }

    const query = searchParams.toString();
    return query ? `?${query}` : '';
};

const buildLabelQuery = (params?: LabelListParams) => {
    const searchParams = new URLSearchParams();

    if (params?.group_key) {
        searchParams.set('group_key', params.group_key);
    }
    if (params?.include_inactive !== undefined) {
        searchParams.set('include_inactive', String(params.include_inactive));
    }
    if (params?.q) {
        searchParams.set('q', params.q);
    }

    const query = searchParams.toString();
    return query ? `?${query}` : '';
};

export interface FrontendLabelService {
    getGroups: (params?: LabelGroupListParams) => Promise<LabelGroup[]>;
    getLabels: (params?: LabelListParams) => Promise<Label[]>;
    createGroup: (data: LabelGroupCreate) => Promise<LabelGroup>;
    updateGroup: (groupId: number, data: LabelGroupUpdate) => Promise<LabelGroup>;
    createLabel: (data: LabelCreate) => Promise<Label>;
    updateLabel: (labelId: number, data: LabelUpdate) => Promise<Label>;
}

export const labelService: FrontendLabelService = {
    getGroups: async (params?: LabelGroupListParams) => {
        const response = await api.get<LabelGroup[]>(`/label-groups${buildLabelGroupQuery(params)}`);
        return response.data;
    },

    getLabels: async (params?: LabelListParams) => {
        const response = await api.get<Label[]>(`/labels${buildLabelQuery(params)}`);
        return response.data;
    },

    createGroup: async (data: LabelGroupCreate) => {
        const response = await api.post<LabelGroup>('/label-groups', data);
        return response.data;
    },

    updateGroup: async (groupId: number, data: LabelGroupUpdate) => {
        const response = await api.put<LabelGroup>(`/label-groups/${groupId}`, data);
        return response.data;
    },

    createLabel: async (data: LabelCreate) => {
        const response = await api.post<Label>('/labels', data);
        return response.data;
    },

    updateLabel: async (labelId: number, data: LabelUpdate) => {
        const response = await api.put<Label>(`/labels/${labelId}`, data);
        return response.data;
    },
};
