import { Check } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { AGENT_TEAM_STEP_DEFINITIONS, stateTone } from '../../features/agentTeamSetup/masters';
import type { AgentTeamStepId } from '../../features/agentTeamSetup/masters';
import type { useAgentTeamReadiness } from '../../features/agentTeamSetup/useAgentTeamReadiness';
type AgentTeamStepScope = 'authority' | 'topology' | 'runtime';
const stepScope = (stepId: string): AgentTeamStepScope => {
    if (stepId === 'authority') return 'authority';
    if (stepId === 'review') return 'runtime';
    return 'topology';
};

const AGENT_TEAM_STEP_SCOPES: AgentTeamStepScope[] = [
    'authority',
    'topology',
    'runtime',
];

export const AgentTeamStepList = ({
    currentStepId,
    idPrefix,
    steps,
}: {
    currentStepId: AgentTeamStepId | null;
    idPrefix: string;
    steps: ReturnType<typeof useAgentTeamReadiness>['steps'];
}) => {
    const { t } = useTranslation();

    return (
        <ol className="agent-team-step-groups">
            {AGENT_TEAM_STEP_SCOPES.map(scope => {
                const definitions = AGENT_TEAM_STEP_DEFINITIONS.filter(
                    definition => stepScope(definition.id) === scope,
                );
                const labelId = `${idPrefix}-${scope}-label`;
                return (
                    <li key={scope} className="agent-team-step-group">
                        <h3 id={labelId} className="agent-team-step-scope">
                            {t(`agentTeamSetup.statusScopes.${scope}.title`)}
                        </h3>
                        <ol
                            className="step-rail agent-team-setup-steps"
                            aria-labelledby={labelId}
                        >
                            {definitions.map(definition => {
                                const index = AGENT_TEAM_STEP_DEFINITIONS.findIndex(
                                    candidate => candidate.id === definition.id,
                                );
                                const step = steps[definition.id];
                                const tone = stateTone(step?.state);
                                return (
                                    <li
                                        key={definition.id}
                                        className={`step-item ${tone}`}
                                        aria-current={
                                            currentStepId === definition.id
                                                ? 'step'
                                                : undefined
                                        }
                                    >
                                        <span className="step-num">
                                            {tone === 'done'
                                                ? <Check size={11} aria-hidden="true" />
                                                : index + 1}
                                        </span>
                                        <span>
                                            <span className="step-title">
                                                {t(definition.titleKey)}
                                            </span>
                                            <span className="step-sub">
                                                {step && step.state !== 'done'
                                                    ? t(`agentTeamSetup.steps.${definition.id}.action`)
                                                    : t(definition.descriptionKey)}
                                            </span>
                                        </span>
                                        <span className={`pill sm ${tone}`}>
                                            {t(`agentTeamSetup.stepStates.${tone}`)}
                                        </span>
                                    </li>
                                );
                            })}
                        </ol>
                    </li>
                );
            })}
        </ol>
    );
};
