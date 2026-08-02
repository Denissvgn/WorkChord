export const PLANNING_RETURN_STEP_PARAM = 'fromPlanStep';

export const PLANNING_STEP_IDS = [
    'iteration',
    'team',
    'work',
    'blockers',
    'schedule',
    'review',
] as const;

export type PlanningStepId = typeof PLANNING_STEP_IDS[number];

export const isPlanningStepId = (value: string | null): value is PlanningStepId => (
    Boolean(value && PLANNING_STEP_IDS.includes(value as PlanningStepId))
);

export const planMasterStepHref = (stepId: PlanningStepId) => (
    `/plan/master?step=${stepId}`
);

export const withPlanMasterReturn = (
    route: string,
    returnStepId: PlanningStepId,
    options: Record<string, string> = {},
) => {
    const [pathname, existingSearch = ''] = route.split('?');
    const search = new URLSearchParams(existingSearch);
    Object.entries(options).forEach(([key, value]) => search.set(key, value));
    search.set(PLANNING_RETURN_STEP_PARAM, returnStepId);
    return `${pathname}?${search.toString()}`;
};
