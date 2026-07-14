import api from './api';
import type {
    GitHubStatusAutomationRule,
    GitHubStatusAutomationRuleCreate,
    GitHubStatusAutomationRuleUpdate,
} from '../types/github';

export const githubService = {
    getStatusAutomationRules: async () => {
        const response = await api.get<GitHubStatusAutomationRule[]>('/github/status-automation-rules');
        return response.data;
    },

    createStatusAutomationRule: async (data: GitHubStatusAutomationRuleCreate) => {
        const response = await api.post<GitHubStatusAutomationRule>('/github/status-automation-rules', data);
        return response.data;
    },

    updateStatusAutomationRule: async (ruleId: number, data: GitHubStatusAutomationRuleUpdate) => {
        const response = await api.put<GitHubStatusAutomationRule>(`/github/status-automation-rules/${ruleId}`, data);
        return response.data;
    },

    deleteStatusAutomationRule: async (ruleId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(
            `/github/status-automation-rules/${ruleId}`
        );
        return response.data;
    },
};
