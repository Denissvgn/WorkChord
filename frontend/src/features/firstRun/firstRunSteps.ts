import type { PlanningStepId } from '../planningMasters/planningReturn';

/** The six setup steps, in the order a new workspace takes them. */
export const FIRST_RUN_STEP_IDS = ['profile', 'project', 'iteration', 'capacity', 'tasks', 'schedule'] as const;

export type FirstRunStepId = typeof FIRST_RUN_STEP_IDS[number];

/** The plan checkpoint each later step opens. The first two steps are done in place on Overview. */
export const FIRST_RUN_PLAN_CHECKPOINT: Readonly<Partial<Record<FirstRunStepId, PlanningStepId>>> = {
    iteration: 'iteration',
    capacity: 'team',
    tasks: 'work',
    schedule: 'schedule',
};

/** Marks a link into Plan as opened from the Get started panel, so Plan offers the way back. */
export const FIRST_RUN_SETUP_PARAM = 'setup';

export const firstRunPlanHref = (checkpoint: PlanningStepId) => (
    `/plan?step=${checkpoint}&${FIRST_RUN_SETUP_PARAM}=1`
);

/**
 * What the workspace holds, read from the server. Nothing here is a stored flag: every step
 * is done exactly while its data exists.
 */
export interface FirstRunFacts {
    /** This session works as a chosen profile. */
    profileChosen: boolean;
    projectCount: number;
    iterationCount: number;
    /** Capacity rows on the iteration in scope. */
    capacityRows: number;
    /** Tasks in the iteration in scope. */
    taskCount: number;
    /** The server reports the iteration's schedule checkpoint as done: the schedule is applied. */
    scheduleApplied: boolean;
}

export interface FirstRunStep {
    id: FirstRunStepId;
    /** 1-based position. */
    number: number;
    done: boolean;
}

const STEP_DONE: Record<FirstRunStepId, (facts: FirstRunFacts) => boolean> = {
    profile: facts => facts.profileChosen,
    project: facts => facts.projectCount > 0,
    iteration: facts => facts.iterationCount > 0,
    capacity: facts => facts.capacityRows > 0,
    tasks: facts => facts.taskCount > 0,
    schedule: facts => facts.scheduleApplied,
};

export const firstRunSteps = (facts: FirstRunFacts): FirstRunStep[] => (
    FIRST_RUN_STEP_IDS.map((id, index) => ({ id, number: index + 1, done: STEP_DONE[id](facts) }))
);

/** The step the panel opens: the first one not done, or null once all six are. */
export const nextFirstRunStep = (steps: readonly FirstRunStep[]): FirstRunStepId | null => (
    steps.find(step => !step.done)?.id ?? null
);
