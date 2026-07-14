import api from './api';
import type {
    EmailSettings,
    EmailSettingsUpdate,
    TestEmailResponse
} from '../types/emailSettings';

export const emailSettingsService = {
    /**
     * Get current email settings
     */
    getSettings: async (): Promise<EmailSettings> => {
        const response = await api.get<EmailSettings>('/email-settings');
        return response.data;
    },

    /**
     * Update email settings
     */
    updateSettings: async (data: EmailSettingsUpdate): Promise<EmailSettings> => {
        const response = await api.put<EmailSettings>('/email-settings', data);
        return response.data;
    },

    /**
     * Send test email to verify connection
     */
    testConnection: async (recipient: string): Promise<TestEmailResponse> => {
        const response = await api.post<TestEmailResponse>('/email-settings/test', {
            recipient
        });
        return response.data;
    }
};
