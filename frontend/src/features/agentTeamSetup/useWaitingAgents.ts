import { useQuery } from '@tanstack/react-query';
import { agentService } from '../../services/agentService';
import { waitingMembers } from './connectAgent';

/**
 * The team status and topology the Connect steps read, under the same query keys, so a drawer and the
 * Connect page share one set of reads. Nothing is read without the admin key.
 */
export const useWaitingAgents = (enabled: boolean) => {
    // feedback-policy: query loading,error,retry,empty - the drawer renders no steps until the status is read.
    const status = useQuery({
        queryKey: ['agent-team-setup', 'current'],
        queryFn: () => agentService.getAgentTeamStatus(),
        enabled,
        retry: false,
    });
    // feedback-policy: query loading,error,retry,empty - the topology is read only when the team can be changed, as in Connect.
    const points = useQuery({
        queryKey: ['agent-team-setup', 'starting-points'],
        queryFn: () => agentService.getAgentTeamStartingPoints(),
        enabled: enabled && status.data?.can_mutate === true,
        retry: false,
    });
    const manifest = points.data?.current ?? null;
    const waiting = status.data && manifest ? waitingMembers(manifest, status.data) : [];
    return { status, manifest, waiting };
};
