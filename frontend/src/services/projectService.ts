import api from './api';
import type { Task } from '../types/task';
import type { Iteration } from '../types/iteration';
import type {
    Initiative,
    InitiativeCreate,
    InitiativeUpdate,
    Project,
    ProjectCreate,
    ProjectMilestone,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneDeleteResponse,
    ProjectMilestoneUpdateRequest,
    ProjectPortfolioSummary,
    ProjectSummary,
    ProjectUpdate,
    ProjectUpdateEntry,
    ProjectUpdateEntryCreate,
    RoadmapMilestonePage,
} from '../types/project';

export const projectService = {
    getInitiatives: async () => {
        const response = await api.get<Initiative[]>('/initiatives');
        return response.data;
    },

    getInitiativeById: async (id: number) => {
        const response = await api.get<Initiative>(`/initiatives/${id}`);
        return response.data;
    },

    createInitiative: async (data: InitiativeCreate) => {
        const response = await api.post<Initiative>('/initiatives', data);
        return response.data;
    },

    updateInitiative: async (id: number, data: InitiativeUpdate) => {
        const response = await api.put<Initiative>(`/initiatives/${id}`, data);
        return response.data;
    },

    deleteInitiative: async (id: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/initiatives/${id}`);
        return response.data;
    },

    getAll: async () => {
        const response = await api.get<Project[]>('/projects');
        return response.data;
    },

    getById: async (id: number) => {
        const response = await api.get<Project>(`/projects/${id}`);
        return response.data;
    },

    create: async (data: ProjectCreate) => {
        const response = await api.post<Project>('/projects', data);
        return response.data;
    },

    update: async (id: number, data: ProjectUpdate) => {
        const response = await api.put<Project>(`/projects/${id}`, data);
        return response.data;
    },

    delete: async (id: number, detachTasks = false) => {
        const response = await api.delete<{ success: boolean; message: string }>(
            `/projects/${id}`,
            { params: { detach_tasks: detachTasks } }
        );
        return response.data;
    },

    getTasks: async (id: number) => {
        const response = await api.get<Task[]>(`/projects/${id}/tasks`);
        return response.data;
    },

    getSummary: async (id: number) => {
        const response = await api.get<ProjectSummary>(`/projects/${id}/summary`);
        return response.data;
    },

    getPortfolioSummaries: async () => {
        const response = await api.get<ProjectPortfolioSummary[]>('/projects/portfolio-summaries');
        return response.data;
    },

    getMilestones: async (id: number) => {
        const response = await api.get<ProjectMilestone[]>(`/projects/${id}/milestones`);
        return response.data;
    },

    getRoadmapMilestones: async (afterId: number | null, limit = 500) => {
        const response = await api.get<RoadmapMilestonePage>('/roadmap/milestones', {
            params: {
                after_id: afterId ?? undefined,
                limit,
            },
        });
        return response.data;
    },

    createMilestone: async (id: number, data: ProjectMilestoneCreateRequest) => {
        const response = await api.post<ProjectMilestone>(`/projects/${id}/milestones`, data);
        return response.data;
    },

    updateMilestone: async (projectId: number, milestoneId: number, data: ProjectMilestoneUpdateRequest) => {
        const response = await api.patch<ProjectMilestone>(
            `/projects/${projectId}/milestones/${milestoneId}`,
            data
        );
        return response.data;
    },

    deleteMilestone: async (projectId: number, milestoneId: number) => {
        const response = await api.delete<ProjectMilestoneDeleteResponse>(
            `/projects/${projectId}/milestones/${milestoneId}`
        );
        return response.data;
    },

    getIterations: async (id: number) => {
        const response = await api.get<Iteration[]>(`/projects/${id}/iterations`);
        return response.data;
    },

    getUpdates: async (id: number) => {
        const response = await api.get<ProjectUpdateEntry[]>(`/projects/${id}/updates`);
        return response.data;
    },

    createUpdate: async (id: number, data: ProjectUpdateEntryCreate) => {
        const response = await api.post<ProjectUpdateEntry>(`/projects/${id}/updates`, data);
        return response.data;
    },
};
