import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useIdentity } from '../identity/identityContext';
import { iterationService } from '../../services/iterationService';
import { projectService } from '../../services/projectService';
import { planningNavigationSummaryKey } from '../planningMasters/usePlanningNavigationSummary';
import { pickDefaultIteration } from '../scope/workScope';
import type { Iteration } from '../../types/iteration';
import { firstRunSteps, nextFirstRunStep, type FirstRunFacts, type FirstRunStep, type FirstRunStepId } from './firstRunSteps';

export interface FirstRunProgress {
    /** False until every source has answered; the panel stays hidden rather than guess. */
    known: boolean;
    /** False for sessions that cannot set a workspace up, such as a paired read-only reader. */
    applies: boolean;
    steps: FirstRunStep[];
    nextId: FirstRunStepId | null;
    complete: boolean;
    facts: FirstRunFacts;
    /** The project's name when there is exactly one. */
    projectName: string | null;
    plannedIteration: Iteration | null;
}

/**
 * How far the workspace is set up, from the data alone: the chosen profile, the projects, the
 * iterations, and the planning-readiness response of the iteration Plan opens. The later
 * steps read the same response as Plan, so a step and its checkpoint never disagree.
 */
export const useFirstRunProgress = (): FirstRunProgress => {
    const identityContext = useIdentity();
    const identity = identityContext?.identity;
    // feedback-policy: query loading,error,retry,empty - the panel stays hidden until the projects are known.
    const projects = useQuery({ queryKey: ['projects'], queryFn: () => projectService.getAll(), staleTime: 60000 });
    // feedback-policy: query loading,error,retry,empty - the panel stays hidden until the iterations are known.
    const iterations = useQuery({ queryKey: ['iterations'], queryFn: iterationService.getAll, staleTime: 60000 });
    const iterationList = iterations.data;
    // Setup progress follows the workspace's default iteration, even when the visible scope is Backlog.
    const plannedIteration = iterationList ? pickDefaultIteration(iterationList) ?? null : null;
    const iterationId = plannedIteration?.id ?? 0;
    // feedback-policy: query loading,error,retry,empty - the panel stays hidden until readiness is known.
    const readiness = useQuery({
        queryKey: planningNavigationSummaryKey(iterationId),
        queryFn: () => iterationService.getPlanningReadiness(iterationId),
        enabled: iterationId > 0,
        staleTime: 60000,
    });

    const summary = iterationId > 0 ? readiness.data : undefined;
    const facts: FirstRunFacts = useMemo(() => ({
        profileChosen: Boolean(identity?.profile),
        projectCount: projects.data?.length ?? 0,
        iterationCount: iterationList?.length ?? 0,
        capacityRows: summary?.team_member_count ?? 0,
        taskCount: summary?.task_count ?? 0,
        scheduleApplied: summary?.checkpoints?.find(item => item.id === 'schedule')?.state === 'done',
    }), [identity?.profile, iterationList?.length, projects.data?.length, summary]);
    const steps = useMemo(() => firstRunSteps(facts), [facts]);
    const nextId = nextFirstRunStep(steps);

    const known = identity !== undefined
        && projects.data !== undefined
        && iterationList !== undefined
        && (iterationId === 0 || summary !== undefined);
    const applies = identity !== undefined
        && identity.access !== 'observe'
        && identity.principal?.kind !== 'agent';

    const projectName = projects.data?.length === 1 ? projects.data[0].name : null;

    return { known, applies, steps, nextId, complete: nextId === null, facts, projectName, plannedIteration };
};
