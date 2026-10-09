import api from './api';

export type PlanningInputKind = 'calendar' | 'project' | 'iteration' | 'profile' | 'member' | 'vacation';
export interface ObservedPlanningInput<T> {
    kind: PlanningInputKind;
    resource_id: number;
    resource: T;
    expected_revisions: Record<number, number>;
    complete: true;
}

export type MemberPlanningIntent = { profile_id?: number | null; name?: string; email?: string | null; text?: string; csv_text?: string };
export type ObservedRevisions = Record<number, number>;
export const revisionHeaders = (revisions: ObservedRevisions) => ({ 'X-Expected-Revisions': JSON.stringify(revisions) });

const validateObservation = <T,>(value: ObservedPlanningInput<T>, kind: PlanningInputKind, id: number) => {
    if (value?.kind !== kind || value.resource_id !== id || value.complete !== true || !value.resource ||
        (value.resource as { id?: unknown }).id !== id || !value.expected_revisions || Array.isArray(value.expected_revisions)) {
        throw new Error('The initial planning context is incomplete. Reload before editing.');
    }
    if (kind === 'iteration' && value.expected_revisions[id] === undefined) throw new Error('The initial iteration context is incomplete.');
    const entries = Object.entries(value.expected_revisions);
    if (entries.length > 500 || entries.some(([key, revision]) => !/^[1-9][0-9]*$/.test(key) ||
        !Number.isSafeInteger(Number(key)) || !Number.isSafeInteger(revision) || revision < 1) ||
        new TextEncoder().encode(JSON.stringify(value.expected_revisions)).length > 16384) {
        throw new Error('The initial planning revision context is invalid or too large.');
    }
    return value;
};

export const planningInputService = {
    readInitial: async <T>(kind: PlanningInputKind, resourceId: number, creatingMember = false, intent?: MemberPlanningIntent) => {
        const result = intent
            ? await api.post<ObservedPlanningInput<T>>(`/tasks/planning-inputs/member/${resourceId}/context`, intent, { params: { creating_member: creatingMember } })
            : await api.get<ObservedPlanningInput<T>>(`/tasks/planning-inputs/${kind}/${resourceId}/context`, { params: { creating_member: creatingMember } });
        return validateObservation(result.data, kind, resourceId);
    },
};
