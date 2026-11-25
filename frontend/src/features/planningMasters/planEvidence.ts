import type { TFunction } from 'i18next';
import type { IterationPlanningReadinessSummary } from '../../types/iteration';
import { formatDate } from '../../utils/formatDate';
import { derivePlanningRecovery } from './masters';
import type { PlanReadiness } from './masters';
import { planStepHref, withPlanReturn } from './planningReturn';
import type { PlanningStepId } from './planningReturn';
import { PLANNING_ITERATION_PARAM, planningIssueTasksHref } from './planningTaskIssues';
import type { PlanningTaskIssue } from './planningTaskIssues';

type EvidenceItem = {
    label: string;
    value: string;
    /** An actionable exception: shown in the exception colour. */
    exception?: boolean;
    href?: string;
    actionLabel?: string;
};

type OwnerLink = { href: string; label: string };

const OWNER_LABEL_KEYS: Readonly<Record<string, string>> = {
    '/iterations': 'plan.page.open.iterations',
    '/team': 'plan.page.open.team',
    '/tasks': 'plan.page.open.tasks',
    '/gantt': 'plan.page.open.gantt',
};

/** Takes every count the server's planning-readiness response carries, so evidence and states agree. */
export const readinessWithServerCounts = (
    readiness: PlanReadiness,
    summary: IterationPlanningReadinessSummary | undefined,
): PlanReadiness => (summary ? {
    ...readiness,
    teamMemberCount: summary.team_member_count,
    teamAgentCount: summary.team_agent_count ?? readiness.teamAgentCount,
    teamCapacity: summary.team_capacity_hours,
    teamMembersNoCap: summary.team_members_no_capacity,
    taskCount: summary.task_count,
    tasksWithoutAssignee: summary.tasks_without_assignee,
    tasksWithoutEffort: summary.tasks_without_effort,
    tasksAgentWithoutCapacity: summary.tasks_agent_without_capacity ?? readiness.tasksAgentWithoutCapacity,
    hasGanttSchedule: summary.has_schedule,
    riskCount: summary.risk_count,
} : readiness);

/** The rows of facts a checkpoint shows today, each optionally linking to the records behind it. */
export const checkpointEvidence = (
    stepId: PlanningStepId,
    readiness: PlanReadiness,
    t: TFunction,
    language: string,
    iterationId: number,
): EvidenceItem[] => {
    // Without an iteration these numbers are not known; never print them as 0.
    const known = readiness.hasCurrentIteration;
    const count = (value: number) => (known ? String(value) : t('plan.master.unknown'));
    const issueRow = (issue: PlanningTaskIssue, label: string, value: number, actionKey: string): EvidenceItem => ({
        label,
        value: count(value),
        exception: known && value > 0,
        ...(known && value > 0 ? {
            href: planningIssueTasksHref({ issue, iterationId, returnStepId: stepId }),
            actionLabel: t(actionKey, { count: value }),
        } : {}),
    });
    const unassigned = issueRow('unassigned', t('plan.master.unassigned'), readiness.tasksWithoutAssignee, 'plan.master.openUnassignedTasks');
    const missingEffort = issueRow('missing-effort', t('plan.master.missingEffort'), readiness.tasksWithoutEffort, 'plan.master.openMissingEffortTasks');
    const tasksInIteration: EvidenceItem = { label: t('plan.page.tasksInIteration'), value: count(readiness.taskCount) };

    if (stepId === 'iteration') {
        return [
            {
                label: t('plan.page.iteration'),
                value: readiness.currentIterationName || t('plan.master.notAvailable'),
            },
            {
                label: t('plan.page.dates'),
                value: known
                    ? `${formatDate(readiness.currentIterationStart, language)} – ${formatDate(readiness.currentIterationEnd, language)}`
                    : t('plan.master.notAvailable'),
            },
            {
                label: t('plan.master.workingDays'),
                value: known
                    ? t('plan.master.daysCount', { count: readiness.currentIterationDays })
                    : t('plan.master.notAvailable'),
            },
        ];
    }
    if (stepId === 'team') {
        return [
            { label: t('plan.master.people'), value: count(readiness.teamMemberCount - (readiness.teamAgentCount ?? 0)) },
            ...((readiness.teamAgentCount ?? 0) > 0
                ? [{ label: t('plan.master.agents'), value: count(readiness.teamAgentCount ?? 0) }]
                : []),
            {
                label: t('plan.master.totalCapacity'),
                value: known ? t('units.hoursCompact', { count: readiness.teamCapacity }) : t('plan.master.unknown'),
            },
            {
                label: t('plan.master.missingAllocation'),
                value: count(readiness.teamMembersNoCap),
                exception: known && readiness.teamMembersNoCap > 0,
            },
        ];
    }
    if (stepId === 'work') return [tasksInIteration];
    if (stepId === 'blockers') {
        const agentRows: EvidenceItem[] = (readiness.tasksAgentWithoutCapacity ?? 0) > 0 ? [{
            label: t('plan.master.agentWorkingNoCapacity'),
            value: count(readiness.tasksAgentWithoutCapacity ?? 0),
            exception: true,
            href: planStepHref('team'),
            actionLabel: t('plan.master.addCapacityRows'),
        }] : [];
        return [unassigned, missingEffort, ...agentRows, tasksInIteration];
    }
    const savedSchedule: EvidenceItem = {
        label: t('plan.master.savedSchedule'),
        value: readiness.hasGanttSchedule ? t('plan.master.available') : t('plan.master.notAvailable'),
    };
    const taskExceptions = [unassigned, missingEffort].filter(item => item.exception);
    if (stepId === 'schedule') return [...taskExceptions, savedSchedule, tasksInIteration];
    // Review carries the at-risk signals: overdue, delayed, outside date limits, or over capacity.
    return [
        ...taskExceptions,
        savedSchedule,
        {
            label: t('plan.page.atRisk'),
            value: count(readiness.riskCount),
            exception: known && readiness.riskCount > 0,
            ...(known && readiness.riskCount > 0 ? {
                href: withPlanReturn('/gantt', stepId),
                actionLabel: t('plan.page.openAtRisk', { count: readiness.riskCount }),
            } : {}),
        },
        tasksInIteration,
    ];
};

/** The existing link to the page that owns the change a checkpoint needs. */
export const checkpointOwnerLink = (
    stepId: PlanningStepId,
    readiness: PlanReadiness,
    t: TFunction,
    iterationId: number,
): OwnerLink => {
    const recovery = derivePlanningRecovery(stepId, readiness);
    if (recovery.planningIssue) {
        return {
            href: planningIssueTasksHref({ issue: recovery.planningIssue, iterationId, returnStepId: stepId }),
            label: recovery.kind === 'repair-assignee'
                ? t('plan.master.assignTasks', { count: recovery.count })
                : t('plan.master.estimateTasks', { count: recovery.count }),
        };
    }
    return {
        href: withPlanReturn(recovery.route, stepId, {
            ...recovery.query,
            ...(recovery.route === '/tasks' && iterationId > 0
                ? { [PLANNING_ITERATION_PARAM]: String(iterationId) }
                : {}),
        }),
        label: t(OWNER_LABEL_KEYS[recovery.route] ?? 'plan.page.open.tasks'),
    };
};
