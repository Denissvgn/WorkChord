import { revisionHeaders, type ObservedRevisions } from './planningInputService';
import api from './api';
import type {
    MemberCapacity,
    MemberWorkload,
    TeamMember,
    TeamMemberCreate,
    TeamMemberOption,
    TeamMemberProfile,
    TeamMemberProfileCreate,
    TeamMemberProfileSkill,
    TeamMemberProfileSkillCreate,
    TeamMemberProfileSkillUpdate,
    TeamMemberProfileUpdate,
    Vacation,
    VacationCreate,
    VacationImportResponse,
} from '../types/team';

export const teamService = {
    getAll: async () => {
        const response = await api.get<TeamMemberOption[]>('/team-members');
        return response.data;
    },

    getByIteration: async (iterationId: number) => {
        const response = await api.get<TeamMember[]>(`/iterations/${iterationId}/team`);
        return response.data;
    },

    getUniqueEmployees: async () => {
        const response = await api.get<{ name: string; position: string }[]>('/employees/unique');
        return response.data;
    },

    getProfiles: async () => {
        const response = await api.get<TeamMemberProfile[]>('/team-member-profiles');
        return response.data;
    },

    getProfile: async (profileId: number) => {
        const response = await api.get<TeamMemberProfile>(`/team-member-profiles/${profileId}`);
        return response.data;
    },

    createProfile: async (data: TeamMemberProfileCreate) => {
        const response = await api.post<TeamMemberProfile>('/team-member-profiles', data);
        return response.data;
    },

    updateProfile: async (profileId: number, data: TeamMemberProfileUpdate, revisions: ObservedRevisions) => {
        const response = await api.put<TeamMemberProfile>(`/team-member-profiles/${profileId}`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    deleteProfile: async (profileId: number, revisions: ObservedRevisions) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/team-member-profiles/${profileId}`, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    createProfileSkill: async (profileId: number, data: TeamMemberProfileSkillCreate, revisions: ObservedRevisions) => {
        const response = await api.post<TeamMemberProfileSkill>(`/team-member-profiles/${profileId}/skills`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    updateProfileSkill: async (profileId: number, skillId: number, data: TeamMemberProfileSkillUpdate, revisions: ObservedRevisions) => {
        const response = await api.put<TeamMemberProfileSkill>(`/team-member-profiles/${profileId}/skills/${skillId}`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    deleteProfileSkill: async (profileId: number, skillId: number, revisions: ObservedRevisions) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/team-member-profiles/${profileId}/skills/${skillId}`, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    create: async (iterationId: number, data: TeamMemberCreate, revisions: ObservedRevisions) => {
        const response = await api.post<TeamMember>(`/iterations/${iterationId}/team`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    update: async (memberId: number, data: Partial<TeamMemberCreate>, revisions: ObservedRevisions) => {
        const response = await api.put<TeamMember>(`/team-members/${memberId}`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    delete: async (memberId: number, revisions: ObservedRevisions) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/team-members/${memberId}`, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    getWorkload: async (memberId: number) => {
        const response = await api.get<MemberWorkload>(`/team-members/${memberId}/workload`);
        return response.data;
    },

    getCapacity: async (memberId: number) => {
        const response = await api.get<MemberCapacity>(`/team-members/${memberId}/capacity`);
        return response.data;
    },

    addVacation: async (memberId: number, data: VacationCreate, revisions: ObservedRevisions) => {
        const response = await api.post<Vacation>(`/team-members/${memberId}/vacations`, data, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    deleteVacation: async (vacationId: number, revisions: ObservedRevisions) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/vacations/${vacationId}`, { headers: revisionHeaders(revisions) });
        return response.data;
    },

    importVacationsCsv: async (iterationId: number, csvText: string, revisions: ObservedRevisions) => {
        const response = await api.post<VacationImportResponse>(
            `/iterations/${iterationId}/team/vacations/import`,
            { csv_text: csvText }, { headers: revisionHeaders(revisions) }
        );
        return response.data;
    },

    importFromText: async (iterationId: number, text: string, expectedRevisions: ObservedRevisions) => {
        const response = await api.post<{ imported_count: number; members: TeamMember[] }>(
            `/iterations/${iterationId}/team/import`,
            { text, expected_revisions: expectedRevisions }
        );
        return response.data;
    }
};
