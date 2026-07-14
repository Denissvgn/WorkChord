import api from './api';
import type {
    ExplainScheduleDetailLevel,
    ExplainScheduleRequest,
    ExplainScheduleResponse,
    GanttResponse,
    ScheduleResult,
} from '../types/gantt';

export const ganttService = {
    getChart: async (iterationId: number) => {
        const response = await api.get<GanttResponse>(`/iterations/${iterationId}/gantt`);
        return response.data;
    },

    schedule: async (iterationId: number) => {
        const response = await api.post<ScheduleResult>(`/iterations/${iterationId}/schedule`);
        return response.data;
    },

    explainSchedule: async (
        iterationId: number,
        detailLevel: ExplainScheduleDetailLevel = 'full'
    ) => {
        if (detailLevel === 'full') {
            const response = await api.post<ExplainScheduleResponse>(
                `/iterations/${iterationId}/explain-schedule`
            );
            return response.data;
        }

        const body: ExplainScheduleRequest = { detail_level: detailLevel };
        const response = await api.post<ExplainScheduleResponse>(
            `/iterations/${iterationId}/explain-schedule`,
            body
        );
        return response.data;
    }
};
