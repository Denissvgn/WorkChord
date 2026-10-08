import api from './api';

export type PlanningInputKind = 'calendar' | 'project' | 'iteration' | 'profile' | 'member' | 'vacation';
export interface ObservedPlanningInput<T> {
    kind: PlanningInputKind;
    resource_id: number;
    resource: T;
    expected_revisions: Record<number, number>;
    complete: true;
}

export const planningInputService = {
    readInitial: async <T>(kind: PlanningInputKind, resourceId: number, creatingMember = false) => {
        const result = await api.get<ObservedPlanningInput<T>>(`/tasks/planning-inputs/${kind}/${resourceId}/context`, {
            params: { creating_member: creatingMember },
        });
        return result.data;
    },
};
