import type { QueryClient } from '@tanstack/react-query';
import { planningInputService } from '../../services/planningInputService';
import { teamService } from '../../services/teamService';
import type { TeamMember, TeamMemberCreate } from '../../types/team';

export const refreshCapacity = (client: QueryClient) => Promise.all([
    ...['team', 'workload', 'capacity', 'gantt', 'planning-navigation-summary'].map(root =>
        client.invalidateQueries({ queryKey: [root] })),
]);

const sameMember = (row: TeamMember, candidate: TeamMemberCreate) => candidate.profile_id
    ? row.profile_id === candidate.profile_id
    : !row.profile_id && row.name === candidate.name && (row.email ?? '') === (candidate.email ?? '');

/** Read revisions separately for each write, since creating a row changes the iteration. */
export const addCapacityRows = async (iterationId: number, candidates: TeamMemberCreate[]) => {
    const existing = [...await teamService.getByIteration(iterationId)];
    for (const candidate of candidates) {
        if (existing.some(row => sameMember(row, candidate))) continue;
        const observed = await planningInputService.readInitial<TeamMember>('member', iterationId, true, {
            profile_id: candidate.profile_id, name: candidate.name, email: candidate.email,
        });
        existing.push(await teamService.create(iterationId, candidate, observed.expected_revisions));
    }
};
