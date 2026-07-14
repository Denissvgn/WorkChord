import api from './api';
import type {
    ExplainScheduleDetailLevel,
    ExplainScheduleRequest,
    ExplainScheduleResponse,
    GanttResponse,
    SchedulePreviewResponse,
    ScheduleResult,
} from '../types/gantt';
import type { TaskBatchUpdateItem } from '../types/task';

export const ganttService = {
    getChart: async (iterationId: number) => {
        const response = await api.get<GanttResponse>(`/iterations/${iterationId}/gantt`);
        return response.data;
    },

    schedule: async (iterationId: number) => {
        const response = await api.post<ScheduleResult>(`/iterations/${iterationId}/schedule`);
        return response.data;
    },

    /**
     * Dry-run sandbox edits through the real backend scheduler.
     * Nothing is persisted; the response mirrors what applying the same
     * changes via batch-update (which auto-reschedules) would produce.
     */
    previewSchedule: async (iterationId: number, changes: TaskBatchUpdateItem[]) => {
        const response = await api.post<SchedulePreviewResponse>(
            `/iterations/${iterationId}/schedule/preview`,
            { changes }
        );
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
