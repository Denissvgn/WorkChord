import { useQuery } from '@tanstack/react-query';
import { teamService } from '../../services/teamService';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import type { GanttTask } from '../../types/gantt';
import { agentRowValues, useAgentRowFacts } from './useAgentRowFacts';
import { assigneeOptionsFrom } from './useTaskRowEdits';

export const useTaskAssigneeDisplay = (task: Task | GanttTask, iterationId: number | null) => {
    // feedback-policy: query loading,error,retry,empty - unavailable capacity identity leaves the task's supplied name visible.
    const team = useQuery({ queryKey: ['team', iterationId], queryFn: () => teamService.getByIteration(iterationId!), enabled: iterationId !== null });
    const options = team.data ? assigneeOptionsFrom(team.data) : undefined;
    const option = options?.find(member => member.id === task.assignee?.id);
    // Gantt rows carry no dispatch facts; only an agent assignee has a status line that needs them.
    const needsDetail = !('agent_readiness' in task) && option?.kind === 'agent';
    // feedback-policy: query loading,error,retry,empty - Gantt has no dispatch facts; failed reads keep the shared unknown state.
    const detail = useQuery({ queryKey: ['tasks', 'assignee-detail', task.id], queryFn: () => taskService.getById(task.id), enabled: needsDetail, staleTime: 30_000 });
    const facts = useAgentRowFacts([task]);
    const values = agentRowValues({ ...detail.data, ...task }, options, facts);
    // The assignee's profile id once the team read has found the assignee's row: null for a row
    // without a profile, undefined while the read loads, after it fails, or when the row is missing.
    return { ...values, profileId: option ? option.profileId ?? null : undefined, kind: option?.kind };
};

