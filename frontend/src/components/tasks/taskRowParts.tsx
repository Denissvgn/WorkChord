import clsx from 'clsx';
import { Bot, User } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { AGENT_DISPATCH_LABEL_KEY } from '../../features/agentDispatch';
import type { AgentDispatchState } from '../../features/agentDispatch';
import type { TaskStateChip } from './taskStateChip';

/** The fields a task row and a board card both show, so the two views name the same things the same way. */

const chipClassName: Record<TaskStateChip['kind'], string> = {
    blocked: 'bg-feedback-danger-muted text-feedback-danger-foreground',
    needsDefinition: 'bg-feedback-warning-muted text-feedback-warning-foreground',
    waits: 'bg-surface-subtle text-content-secondary',
    ready: 'bg-action-muted text-action',
    inReview: 'bg-surface-subtle text-content-secondary',
};

const chipLabelKey = {
    blocked: 'taskList.blocked',
    needsDefinition: 'taskList.needsDefinition',
    ready: 'taskList.readyToStart',
    inReview: 'taskList.inReview',
} as const;

/** The one state chip of a task; `className` adds visibility rules such as hiding it on narrow rows. */
export const TaskStateChipBadge = ({ chip, className }: { chip: TaskStateChip; className?: string }) => {
    const { t } = useTranslation();
    return (
        <span className={clsx('shrink-0 whitespace-nowrap rounded-full px-2 py-0.5 text-xs', chipClassName[chip.kind], className)}>
            {chip.kind === 'waits' ? t('taskList.dependsOnCount', { count: chip.count }) : t(chipLabelKey[chip.kind])}
        </span>
    );
};

/** A person or an agent, told apart by icon. */
export const AssigneeKindIcon = ({ kind, className }: { kind?: 'human' | 'agent' | 'hybrid'; className?: string }) => {
    const Icon = kind === 'agent' ? Bot : User;
    return <Icon aria-hidden="true" className={clsx('shrink-0', className)} />;
};

/** The agent status line under an agent's name. */
export const AgentDispatchLine = ({ dispatch, className }: { dispatch: AgentDispatchState; className?: string }) => {
    const { t } = useTranslation();
    return (
        <span data-agent-dispatch={dispatch} title={t(AGENT_DISPATCH_LABEL_KEY[dispatch])} className={className}>
            {/* "Agent status unknown" already names what it is about. */}
            {dispatch !== 'unknown' && <span className="sr-only">{t('taskList.agentStatus')}: </span>}{t(AGENT_DISPATCH_LABEL_KEY[dispatch])}
        </span>
    );
};

/** Days of effort; `null` shows an unknown estimate as a dash that a screen reader names. */
export const EffortValue = ({ effort, className }: { effort: number | null; className?: string }) => {
    const { t } = useTranslation();
    if (effort === null) {
        return (
            <span className={clsx('text-xs text-content-tertiary', className)} title={t('domain.unknownEstimate')}>
                <span aria-hidden="true">—</span>
                <span className="sr-only">{t('domain.unknownEstimate')}</span>
            </span>
        );
    }
    return <span className={clsx('text-xs tabular-nums text-content-secondary', className)}>{t('units.daysCompact', { count: effort })}</span>;
};
