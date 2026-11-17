import { useQuery } from '@tanstack/react-query';
import { teamService } from '../../services/teamService';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import type { GanttTask } from '../../types/gantt';
import { agentRowValues, assigneeKind, useAgentRowFacts } from './useAgentRowFacts';
import { assigneeOptionsFrom } from './useTaskRowEdits';

export const useTaskAssigneeDisplay = (task: Task | GanttTask, iterationId: number | null) => {
    // feedback-policy: query loading,error,retry,empty - unavailable capacity identity leaves the task's supplied name visible.
    const team = useQuery({ queryKey: ['team', iterationId], queryFn: () => teamService.getByIteration(iterationId!), enabled: iterationId !== null });
    const options = team.data ? assigneeOptionsFrom(team.data) : undefined;
    const option = options?.find(member => member.id === task.assignee?.id);
    const kind = assigneeKind(task.assignee, option);
    // Gantt rows carry no dispatch facts and pipeline cards leave the live assignment unset; the
    // task read has it. Only an open task of an agent assignee has a status line that needs it.
    const liveAssignment = (task as Partial<Task>).agent_working;
    const needsDetail = kind === 'agent' && (liveAssignment === undefined || liveAssignment === null)
        && task.status !== 'resolved' && task.status !== 'closed';
    // feedback-policy: query loading,error,retry,empty - a missing dispatch fact keeps the shared unknown state until the read succeeds.
    const detail = useQuery({ queryKey: ['tasks', 'assignee-detail', task.id], queryFn: () => taskService.getById(task.id), enabled: needsDetail, staleTime: 30_000 });
    const facts = useAgentRowFacts([task]);
    const values = agentRowValues({ ...detail.data, ...task, agent_working: liveAssignment ?? detail.data?.agent_working }, options, facts);
    // The assignee's profile id once the team read has found the assignee's row: null for a row
    // without a profile, undefined while the read loads, after it fails, or when the row is missing.
    return { ...values, profileId: option ? option.profileId ?? null : undefined, kind };
};

