export interface Vacation {
    id: number;
    start_date: string;
    end_date: string;
}

export interface VacationCreate {
    start_date: string;
    end_date: string;
}

export interface VacationImportError {
    row: number;
    message: string;
}

export interface VacationImportResponse {
    imported_count: number;
    skipped_count: number;
    errors: VacationImportError[];
    vacations: Vacation[];
}

export interface TeamMemberProfileSkill {
    id: number;
    profile_id: number;
    skill_key: string;
    skill_name: string;
    category?: string | null;
    level: number;
    interest: number;
    is_weakness: boolean;
    keywords_json: string[];
    notes?: string | null;
    created_at: string;
    updated_at: string;
}

export interface TeamMemberProfileSkillCreate {
    skill_key: string;
    skill_name: string;
    category?: string | null;
    level: number;
    interest: number;
    is_weakness: boolean;
    keywords_json?: string[];
    notes?: string | null;
}

export type TeamMemberProfileSkillUpdate = Partial<TeamMemberProfileSkillCreate>;

export interface TeamMemberProfile {
    id: number;
    display_name: string;
    email?: string | null;
    headline?: string | null;
    summary?: string | null;
    notes?: string | null;
    automation_enabled: boolean;
    skills: TeamMemberProfileSkill[];
    created_at: string;
    updated_at: string;
}

export interface TeamMemberProfileCompact {
    id: number;
    display_name: string;
    email?: string | null;
    headline?: string | null;
    automation_enabled: boolean;
    skills: TeamMemberProfileSkill[];
}

export interface TeamMemberProfileCreate {
    display_name: string;
    email?: string | null;
    headline?: string | null;
    summary?: string | null;
    notes?: string | null;
    automation_enabled: boolean;
}

export type TeamMemberProfileUpdate = Partial<TeamMemberProfileCreate>;

export interface TeamMember {
    id: number;
    iteration_id: number;
    profile_id?: number | null;
    name: string;
    position: string;
    email?: string;
    availability_percent: number;
    professionalism_coefficient: number;
    operational_utilization: number;
    profile?: TeamMemberProfileCompact | null;
    vacations: Vacation[];
}

export interface TeamMemberOption {
    id: number;
    iteration_id?: number | null;
    iteration_name?: string | null;
    name: string;
    position: string;
    email?: string | null;
}

export interface TeamMemberCreate {
    name: string;
    position: string;
    email?: string;
    profile_id?: number | null;
    availability_percent: number;
    professionalism_coefficient: number;
    operational_utilization: number;
}

export interface MemberWorkload {
    team_member_id: number;
    name: string;
    capacity_days: number;
    allocated_days: number;
    free_days: number;
    workload_status: 'green' | 'yellow' | 'red';
    workload_percent: number;
}

/** Detailed capacity breakdown from GET /team-members/{id}/capacity. */
export interface MemberCapacity {
    team_member_id: number;
    working_days: number;
    vacation_days: number;
    available_days: number;
    effective_days: number;
    adjusted_days: number;
    hours: number;
}

export interface AssigneeRecommendation {
    team_member_id: number;
    name: string;
    position: string;
    profile_id?: number | null;
    score: number;
    confidence: number;
    matched_skills: string[];
    weakness_matches: string[];
    workload_warnings: string[];
    rationale: string;
}
