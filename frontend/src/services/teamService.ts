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

    updateProfile: async (profileId: number, data: TeamMemberProfileUpdate) => {
        const response = await api.put<TeamMemberProfile>(`/team-member-profiles/${profileId}`, data);
        return response.data;
    },

    deleteProfile: async (profileId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/team-member-profiles/${profileId}`);
        return response.data;
    },

    createProfileSkill: async (profileId: number, data: TeamMemberProfileSkillCreate) => {
        const response = await api.post<TeamMemberProfileSkill>(`/team-member-profiles/${profileId}/skills`, data);
        return response.data;
    },

    updateProfileSkill: async (profileId: number, skillId: number, data: TeamMemberProfileSkillUpdate) => {
        const response = await api.put<TeamMemberProfileSkill>(`/team-member-profiles/${profileId}/skills/${skillId}`, data);
        return response.data;
    },

    deleteProfileSkill: async (profileId: number, skillId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/team-member-profiles/${profileId}/skills/${skillId}`);
        return response.data;
    },

    create: async (iterationId: number, data: TeamMemberCreate) => {
        const response = await api.post<TeamMember>(`/iterations/${iterationId}/team`, data);
        return response.data;
    },

    update: async (memberId: number, data: Partial<TeamMemberCreate>) => {
        const response = await api.put<TeamMember>(`/team-members/${memberId}`, data);
        return response.data;
    },

    delete: async (memberId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/team-members/${memberId}`);
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

    addVacation: async (memberId: number, data: VacationCreate) => {
        const response = await api.post<Vacation>(`/team-members/${memberId}/vacations`, data);
        return response.data;
    },

    deleteVacation: async (vacationId: number) => {
        const response = await api.delete<{ success: boolean; message: string }>(`/vacations/${vacationId}`);
        return response.data;
    },

    importVacationsCsv: async (iterationId: number, csvText: string) => {
        const response = await api.post<VacationImportResponse>(
            `/iterations/${iterationId}/team/vacations/import`,
            { csv_text: csvText }
        );
        return response.data;
    },

    importFromText: async (iterationId: number, text: string) => {
        const response = await api.post<{ imported_count: number; members: TeamMember[] }>(
            `/iterations/${iterationId}/team/import`,
            { text }
        );
        return response.data;
    }
};
