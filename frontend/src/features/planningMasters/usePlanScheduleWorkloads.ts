import { useQuery } from '@tanstack/react-query';
import { teamService } from '../../services/teamService';
import type { TeamMember } from '../../types/team';

export const usePlanScheduleWorkloads = (iterationId: number, members: TeamMember[]) => {
    // feedback-policy: query loading,error,retry,empty - the owning checkpoint displays these states.
    return useQuery({
        queryKey: ['plan-schedule-workloads', iterationId, members.map(member => member.id)],
        queryFn: () => Promise.all(members.map(member => teamService.getWorkload(member.id))),
        staleTime: 0,
    });
};
