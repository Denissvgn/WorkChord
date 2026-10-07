import { useQuery } from '@tanstack/react-query';
import { useIdentity } from '../identity/identityContext';
import { timeEntryService } from '../../services/timeEntryService';

export const useTimeEntries = () => {
    const identity = useIdentity()?.identity;
    // feedback-policy: query loading,error,retry,empty - capability failures hide private controls; consumers render retry.
    const capability = useQuery({ queryKey: ['time-entry-capabilities', identity?.principal?.id],
        enabled: identity?.principal?.kind === 'human', staleTime: 0,
        queryFn: ({ signal }) => timeEntryService.capabilities(signal) });
    return { identity, capability, enabled: identity?.principal?.kind === 'human' && !capability.isError
        && capability.data?.schema_version === 1 && capability.data.enabled === true };
};
