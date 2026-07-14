import api from './api';
import type { AgentPipeline, AgentRun, TaskTimelineResponse } from '../types/agent';

export const agentService = {
    async getPipeline(): Promise<AgentPipeline> {
        const response = await api.get<AgentPipeline>('/agent/pipeline');
        return response.data;
    },

    async getRunDetail(runId: number): Promise<AgentRun> {
        const response = await api.get<AgentRun>(`/agent/runs/${runId}`);
        return response.data;
    },

    async getTaskTimeline(taskId: number): Promise<TaskTimelineResponse> {
        const response = await api.get<TaskTimelineResponse>(`/tasks/${taskId}/timeline`);
        return response.data;
    }
};
