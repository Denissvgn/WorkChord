import api from './api';

export interface PlanShareTask {
    id: number;
    title: string;
    priority: number;
    effort_days: number;
    effort_hours: number;
    status: string;
    assignee_name?: string | null;
    start_date?: string | null;
    end_date?: string | null;
    is_optional: boolean;
    is_deferred: boolean;
    tags: string[];
    dependencies: number[];
    children: PlanShareTask[];
}

export interface PlanShareTeamMember {
    name: string;
    position: string;
    availability_percent: number;
}

export interface PlanShareSnapshot {
    iteration: {
        id: number;
        name: string;
        start_date: string;
        end_date: string;
    };
    tasks: PlanShareTask[];
    team_members: PlanShareTeamMember[];
    snapshot_info: {
        created_at: string;
        reason: string;
    };
}

export interface PlanShare {
    id: number;
    public_id: string;
    iteration_id: number;
    iteration_name: string;
    created_by_display: string;
    snapshot_data: PlanShareSnapshot;
    created_at: string;
    revoked_at?: string | null;
}

export const planShareService = {
    getCurrent: async (iterationId: number): Promise<PlanShare | null> => {
        const response = await api.get<PlanShare | null>(
            `/iterations/${iterationId}/plan-share`,
        );
        return response.data;
    },

    create: async (iterationId: number): Promise<PlanShare> => {
        const response = await api.post<PlanShare>(
            `/iterations/${iterationId}/plan-share`,
        );
        return response.data;
    },

    getByPublicId: async (publicId: string): Promise<PlanShare> => {
        const response = await api.get<PlanShare>(
            `/plan-shares/${encodeURIComponent(publicId)}`,
        );
        return response.data;
    },

    revoke: async (shareId: number): Promise<void> => {
        await api.delete(`/plan-shares/${shareId}`);
    },
};
