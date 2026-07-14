import api from './api';
import type {
    AppRuntimeSettings,
    AppRuntimeSettingsUpdate,
    GitHubRuntimeSettings,
    GitHubRuntimeSettingsUpdate,
    LLMRuntimeSettings,
    LLMRuntimeSettingsUpdate,
    SystemSettings,
    WebIntakeRuntimeSettings,
    WebIntakeRuntimeSettingsUpdate,
} from '../types/systemSettings';

export const systemSettingsService = {
    getSettings: async (): Promise<SystemSettings> => {
        const response = await api.get<SystemSettings>('/system-settings');
        return response.data;
    },

    updateApp: async (data: AppRuntimeSettingsUpdate): Promise<AppRuntimeSettings> => {
        const response = await api.put<AppRuntimeSettings>('/system-settings/app', data);
        return response.data;
    },

    updateLLM: async (data: LLMRuntimeSettingsUpdate): Promise<LLMRuntimeSettings> => {
        const response = await api.put<LLMRuntimeSettings>('/system-settings/llm', data);
        return response.data;
    },

    updateGitHub: async (data: GitHubRuntimeSettingsUpdate): Promise<GitHubRuntimeSettings> => {
        const response = await api.put<GitHubRuntimeSettings>('/system-settings/github', data);
        return response.data;
    },

    updateWebIntake: async (data: WebIntakeRuntimeSettingsUpdate): Promise<WebIntakeRuntimeSettings> => {
        const response = await api.put<WebIntakeRuntimeSettings>('/system-settings/web-intake', data);
        return response.data;
    },
};
