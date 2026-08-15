import type { AgentTeamSetupStep, AgentTeamStepState } from '../../types/agent';

export const AGENT_TEAM_STEP_IDS = [
    'authority',
    'master',
    'controller',
    'workers',
    'bindings',
    'verifier',
    'review',
] as const;

export type AgentTeamStepId = typeof AGENT_TEAM_STEP_IDS[number];

export interface AgentTeamStepDefinition {
    id: AgentTeamStepId;
    titleKey: string;
    descriptionKey: string;
}

export const AGENT_TEAM_STEP_DEFINITIONS: AgentTeamStepDefinition[] =
    AGENT_TEAM_STEP_IDS.map(id => ({
        id,
        titleKey: `agentTeamSetup.steps.${id}.title`,
        descriptionKey: `agentTeamSetup.steps.${id}.description`,
    }));

export const stepsById = (
    steps: AgentTeamSetupStep[] | undefined,
): Record<AgentTeamStepId, AgentTeamSetupStep | undefined> => {
    const result = Object.fromEntries(
        AGENT_TEAM_STEP_IDS.map(id => [id, undefined]),
    ) as Record<AgentTeamStepId, AgentTeamSetupStep | undefined>;
    for (const step of steps ?? []) result[step.id] = step;
    return result;
};

export const stepProgress = (
    steps: AgentTeamSetupStep[] | undefined,
): { done: number; total: number } | null => {
    if (!steps) return null;
    const total = AGENT_TEAM_STEP_IDS.length;
    const done = steps.filter(step => step.state === 'done').length;
    return { done, total };
};

export const stateTone = (
    state: AgentTeamStepState | undefined,
): 'done' | 'warn' | 'blocked' | 'todo' => state ?? 'todo';
