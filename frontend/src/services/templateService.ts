import api from './api';
import type {
    TemplateListParams,
    WorkTemplate,
    WorkTemplateCreate,
    WorkTemplateUpdate,
} from '../types/template';

const buildTemplateListQuery = (params?: TemplateListParams) => {
    const searchParams = new URLSearchParams();

    if (params?.template_type) {
        searchParams.set('template_type', params.template_type);
    }
    if (params?.include_inactive !== undefined) {
        searchParams.set('include_inactive', String(params.include_inactive));
    }

    const query = searchParams.toString();
    return query ? `?${query}` : '';
};

export interface FrontendTemplateService {
    getAll: (params?: TemplateListParams) => Promise<WorkTemplate[]>;
    getById: (templateId: number) => Promise<WorkTemplate>;
    create: (data: WorkTemplateCreate) => Promise<WorkTemplate>;
    update: (templateId: number, data: WorkTemplateUpdate) => Promise<WorkTemplate>;
}

export const templateService: FrontendTemplateService = {
    getAll: async (params?: TemplateListParams) => {
        const response = await api.get<WorkTemplate[]>(`/templates${buildTemplateListQuery(params)}`);
        return response.data;
    },

    getById: async (templateId: number) => {
        const response = await api.get<WorkTemplate>(`/templates/${templateId}`);
        return response.data;
    },

    create: async (data: WorkTemplateCreate) => {
        const response = await api.post<WorkTemplate>('/templates', data);
        return response.data;
    },

    update: async (templateId: number, data: WorkTemplateUpdate) => {
        const response = await api.put<WorkTemplate>(`/templates/${templateId}`, data);
        return response.data;
    },
};
