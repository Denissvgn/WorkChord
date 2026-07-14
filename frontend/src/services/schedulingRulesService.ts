import api from './api';
import type { SchedulingRules, SchedulingRulesResponse } from '../types/schedulingRules';

export const schedulingRulesService = {
    /**
     * Get current scheduling rules configuration.
     */
    getRules: async (): Promise<SchedulingRulesResponse> => {
        const response = await api.get<SchedulingRulesResponse>('/scheduling-rules');
        return response.data;
    },

    /**
     * Update scheduling rules configuration.
     */
    updateRules: async (rules: SchedulingRules): Promise<SchedulingRulesResponse> => {
        const response = await api.put<SchedulingRulesResponse>('/scheduling-rules', rules);
        return response.data;
    },

    /**
     * Reset scheduling rules to default values.
     */
    resetRules: async (): Promise<SchedulingRulesResponse> => {
        const response = await api.post<SchedulingRulesResponse>('/scheduling-rules/reset');
        return response.data;
    },
};
