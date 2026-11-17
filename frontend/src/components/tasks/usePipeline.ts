import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { agentService } from '../../services/agentService';
import type { AgentPipeline } from '../../types/agent';
import { useAdminAccess, useKeylessReader } from '../../hooks/useAdminAccess';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { getApiErrorStatus } from '../../utils/apiError';
import { protectedQueryRetry } from '../../utils/protectedQueries';

const EMPTY_PIPELINE: AgentPipeline = {
    needs_definition: [], ready_to_assign: [], assigned_waiting: [], start_ready: [],
    executing: [], verification_required: [], recovery_required: [],
};

export function usePipeline(enabled: boolean) {
    const { hasAdminKey } = useAdminAccess();
    const { hasAgentKey } = useAgentAccess();
    const reader = useKeylessReader();
    const canRead = hasAdminKey || hasAgentKey || reader.workViews;
    // feedback-policy: query loading,error,retry,empty - PipelineView owns the states.
    const query = useQuery({
        queryKey: ['agent-pipeline'], queryFn: agentService.getPipeline,
        enabled: enabled && canRead, retry: protectedQueryRetry,
        refetchInterval: enabled && canRead ? 5000 : false,
    });
    const status = getApiErrorStatus(query.error);
    const usableData = !canRead || (query.isError && (status === 401 || status === 403)) ? undefined : query.data;
    const pipeline = usableData ?? EMPTY_PIPELINE;
    const agents = useMemo(() => [...new Set(Object.values(pipeline).flat().flatMap(task => [
        task.claimed_by?.display_name, task.assignee?.name,
    ]).filter((name): name is string => Boolean(name)))].sort(), [pipeline]);
    return { ...query, pipeline, usableData, canRead, agents };
}
