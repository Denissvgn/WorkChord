import { useQuery } from '@tanstack/react-query';
import { teamService } from '../../services/teamService';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import type { GanttTask } from '../../types/gantt';
import { agentRowValues, useAgentRowFacts } from './useAgentRowFacts';

export const useTaskAssigneeDisplay = (task: Task | GanttTask, iterationId: number | null) => {
    // feedback-policy: query loading,error,retry,empty - unavailable capacity identity leaves the task's supplied name visible.
    const team = useQuery({ queryKey: ['team', iterationId], queryFn: () => teamService.getByIteration(iterationId!), enabled: iterationId !== null });
    const needsDetail = !('agent_readiness' in task);
    // feedback-policy: query loading,error,retry,empty - Gantt has no dispatch facts; failed reads keep the shared unknown state.
    const detail = useQuery({ queryKey: ['tasks', 'assignee-detail', task.id], queryFn: () => taskService.getById(task.id), enabled: needsDetail, staleTime: 30_000 });
    const facts = useAgentRowFacts([task]);
    const options = team.data?.map(member => ({ id: member.id, name: member.name, kind: member.profile?.profile_kind, profileId: member.profile_id ?? member.profile?.id ?? null }));
    const option = options?.find(member => member.id === task.assignee?.id);
    const values = agentRowValues({ ...detail.data, ...task }, options, facts);
    return { ...values, profileId: option ? option.profileId ?? null : undefined, kind: option?.kind, teamReadFailed: team.isError };
};

