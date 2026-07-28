import { useQuery } from '@tanstack/react-query';
import { agentService } from '../../services/agentService';
import { stepProgress, stepsById } from './masters';

export const useAgentTeamReadiness = (topologyKey?: string) => {
    // feedback-policy: query loading,error,retry,empty - the master renders each state and exposes manual refresh.
    const query = useQuery({
        queryKey: ['agent-team-setup', topologyKey ?? 'current'],
        queryFn: () => agentService.getAgentTeamStatus(topologyKey),
        retry: false,
        staleTime: 15_000,
    });

    return {
        ...query,
        status: query.data,
        steps: stepsById(query.data?.steps),
        progress: stepProgress(query.data?.steps),
    };
};
