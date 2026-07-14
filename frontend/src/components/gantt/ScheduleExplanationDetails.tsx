import i18n from '../../i18n/i18n';
import { useState } from 'react';
import { addDays, format, parseISO } from 'date-fns';
import { AlertTriangle, ChevronDown, ChevronRight, ExternalLink } from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../common/Button';
import type { GanttTask, ScheduleDecisionExplanation } from '../../types/gantt';
import { formatDate } from '../../utils/formatDate';

const t = i18n.t.bind(i18n);

interface ScheduleExplanationDetailsProps {
    decisions: ScheduleDecisionExplanation[];
    taskLookup: Map<number, GanttTask>;
    memberVacations: Record<number, string[]>;
    workloadBalanced: boolean;
    workloadIssues: string[];
    onOpenTask: (task: GanttTask) => void;
}

const DECISION_BADGE_CLASSES: Record<string, string> = {
    scheduled: 'bg-feedback-success-muted text-feedback-success-foreground ring-feedback-success-border',
    delayed: 'bg-feedback-warning-muted text-feedback-warning-foreground ring-feedback-warning-border',
    reordered: 'bg-feedback-info-muted text-feedback-info-foreground ring-feedback-info-border',
    overdue: 'bg-feedback-danger-muted text-feedback-danger-foreground ring-feedback-danger-border',
};

const getTaskStart = (task?: GanttTask) => task?.schedule_result?.scheduled_start || task?.start_date || null;

const getTaskEnd = (task?: GanttTask) => task?.schedule_result?.scheduled_end || task?.end_date || null;

const formatRange = (start?: string | null, end?: string | null) => {
    if (!start && !end) return t('surfaces.scheduleExplanation.unscheduled');
    if (start && end && start !== end) return `${formatDate(start)} → ${formatDate(end)}`;
    return formatDate(start || end);
};

const getAffectedTaskIds = (decision: ScheduleDecisionExplanation) => {
    const maybeAffected = (decision as ScheduleDecisionExplanation & { affected_tasks?: unknown }).affected_tasks;
    if (!Array.isArray(maybeAffected)) return [];
    return maybeAffected.filter((id): id is number => typeof id === 'number');
};

const dateKeyAfter = (dateKey: string) => format(addDays(parseISO(dateKey), 1), 'yyyy-MM-dd');

const groupDateRanges = (dateKeys: string[]) => {
    const sortedDates = Array.from(new Set(dateKeys)).sort();
    if (sortedDates.length === 0) return [];

    const ranges: Array<{ start: string; end: string }> = [];
    let rangeStart = sortedDates[0];
    let rangeEnd = sortedDates[0];

    sortedDates.slice(1).forEach(dateKey => {
        if (dateKey === dateKeyAfter(rangeEnd)) {
            rangeEnd = dateKey;
            return;
        }
        ranges.push({ start: rangeStart, end: rangeEnd });
        rangeStart = dateKey;
        rangeEnd = dateKey;
    });

    ranges.push({ start: rangeStart, end: rangeEnd });
    return ranges;
};

const overlapsTaskRange = (dateKey: string, start?: string | null, end?: string | null) => {
    if (!start || !end) return false;
    return dateKey >= start && dateKey <= end;
};

const resolveTaskLabel = (taskId: number, taskLookup: Map<number, GanttTask>) => {
    const task = taskLookup.get(taskId);
    return task ? `${task.title} (#${task.id})` : t('surfaces.scheduleExplanation.taskNumber', { id: taskId });
};

export const ScheduleExplanationDetails = ({
    decisions,
    taskLookup,
    memberVacations,
    workloadBalanced,
    workloadIssues,
    onOpenTask,
}: ScheduleExplanationDetailsProps) => {
    const [expandedDecisionIds, setExpandedDecisionIds] = useState<Set<number>>(new Set());

    if (decisions.length === 0) return null;

    const toggleDecision = (taskId: number) => {
        setExpandedDecisionIds(prev => {
            const next = new Set(prev);
            if (next.has(taskId)) next.delete(taskId);
            else next.add(taskId);
            return next;
        });
    };

    return (
        <div className="border-t border-feedback-purple-border pt-3">
            <div className="mb-2 flex items-center justify-between gap-3">
                <h4 className="font-medium text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.taskLevelDecisions')}</h4>
                <span className="text-xs text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.decisionCount', { count: decisions.length })}</span>
            </div>

            <div className="divide-y divide-feedback-purple-border overflow-hidden border-y border-feedback-purple-border">
                {decisions.map(decision => {
                    const task = taskLookup.get(decision.task_id);
                    const isExpanded = expandedDecisionIds.has(decision.task_id);
                    const taskStart = getTaskStart(task);
                    const taskEnd = getTaskEnd(task);
                    const affectedTaskIds = getAffectedTaskIds(decision);
                    const dependencies = task?.dependencies || [];
                    const taskVacationDates = task?.assignee?.id
                        ? (memberVacations[task.assignee.id] || []).filter(dateKey => overlapsTaskRange(dateKey, taskStart, taskEnd))
                        : [];
                    const vacationRanges = groupDateRanges(taskVacationDates);
                    const relevantWorkloadIssues = workloadIssues.filter(issue => {
                        const assigneeMatches = task?.assignee?.name ? issue.includes(task.assignee.name) : false;
                        return assigneeMatches || issue.includes(task?.title || decision.task_title);
                    });
                    const decisionBadgeClass = DECISION_BADGE_CLASSES[decision.decision_type] || 'bg-surface-subtle text-content-primary ring-border';

                    return (
                        <div key={`${decision.task_id}-${decision.decision_type}`} className="bg-surface-card/50">
                            <div className="flex items-start gap-2 py-3">
                                <button
                                    type="button"
                                    onClick={() => toggleDecision(decision.task_id)}
                                    className="mt-0.5 rounded p-1 text-feedback-purple-foreground hover:bg-feedback-purple-muted-hover"
                                    aria-expanded={isExpanded}
                                    aria-label={t(isExpanded
                                        ? 'surfaces.scheduleExplanation.collapseDecisionDetail'
                                        : 'surfaces.scheduleExplanation.expandDecisionDetail')}
                                >
                                    {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                                </button>

                                <div className="min-w-0 flex-1">
                                    <div className="flex flex-wrap items-center gap-2">
                                        <span className="font-medium text-feedback-purple-foreground">
                                            {task?.title || decision.task_title}
                                        </span>
                                        <span className="text-xs text-feedback-purple-foreground">#{decision.task_id}</span>
                                        <span className={clsx('rounded-full px-2 py-0.5 text-xs font-medium ring-1', decisionBadgeClass)}>
                                            {t(`gantt.decisionCounts.${decision.decision_type}`)}
                                        </span>
                                    </div>
                                    <div className="mt-1 text-xs text-feedback-purple-foreground">
                                        {formatRange(taskStart, taskEnd)}
                                        {!task && <span className="ml-2 text-feedback-warning-foreground">{t('surfaces.scheduleExplanation.taskNotVisibleInCurrentChart')}</span>}
                                    </div>
                                </div>

                                {task && (
                                    <Button
                                        type="button"
                                        variant="outline"
                                        size="sm"
                                        onClick={() => onOpenTask(task)}
                                        className="shrink-0"
                                    >
                                        <ExternalLink className="mr-1 h-3.5 w-3.5" />
                                        {t('surfaces.scheduleExplanation.openTask')}
                                    </Button>
                                )}
                            </div>

                            {isExpanded && (
                                <div className="space-y-4 pb-4 pl-8 pr-2 text-sm text-feedback-purple-foreground">
                                    <div>
                                        <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.rationale')}</h5>
                                        <p className="mt-1 leading-relaxed text-feedback-purple-foreground">{decision.explanation}</p>
                                    </div>

                                    <div className="grid gap-4 md:grid-cols-2">
                                        <div>
                                            <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.placement')}</h5>
                                            <dl className="mt-2 space-y-1 text-feedback-purple-foreground">
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.scheduled')}</dt>
                                                    <dd className="text-right">{formatRange(taskStart, taskEnd)}</dd>
                                                </div>
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.minStart')}</dt>
                                                    <dd className="text-right">{formatDate(task?.min_start_date)}</dd>
                                                </div>
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.maxEnd')}</dt>
                                                    <dd className="text-right">{formatDate(task?.max_end_date)}</dd>
                                                </div>
                                            </dl>
                                            {task && (
                                                <div className="mt-2 flex flex-wrap gap-1.5">
                                                    {task.is_overdue && <span className="rounded bg-feedback-danger-muted px-2 py-0.5 text-xs text-feedback-danger-foreground">{t('surfaces.scheduleExplanation.overdue')}</span>}
                                                    {task.is_delayed && <span className="rounded bg-feedback-warning-muted px-2 py-0.5 text-xs text-feedback-warning-foreground">{t('surfaces.scheduleExplanation.delayed')}</span>}
                                                    {task.is_outside_constraints && (
                                                        <span className="rounded bg-feedback-warning-muted px-2 py-0.5 text-xs text-feedback-warning-foreground">{t('surfaces.scheduleExplanation.outsideConstraints')}</span>
                                                    )}
                                                    {!task.is_overdue && !task.is_delayed && !task.is_outside_constraints && (
                                                        <span className="rounded bg-feedback-success-muted px-2 py-0.5 text-xs text-feedback-success-foreground">{t('surfaces.scheduleExplanation.withinVisibleConstraints')}</span>
                                                    )}
                                                </div>
                                            )}
                                        </div>

                                        <div>
                                            <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.capacity')}</h5>
                                            <dl className="mt-2 space-y-1 text-feedback-purple-foreground">
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.assignee')}</dt>
                                                    <dd className="text-right">{task?.assignee?.name || t('common.unassigned')}</dd>
                                                </div>
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.effort')}</dt>
                                                    <dd className="text-right">
                                                        {task
                                                            ? (task.calculated_effort_days != null
                                                                ? t('surfaces.scheduleExplanation.adjustedEffort', {
                                                                    effort: t('units.daysCompact', { count: task.effort_days }),
                                                                    adjusted: t('units.daysCompact', { count: task.calculated_effort_days }),
                                                                })
                                                                : t('units.daysCompact', { count: task.effort_days }))
                                                            : t('common.unknown')}
                                                    </dd>
                                                </div>
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.priorityStatus')}</dt>
                                                    <dd className="text-right">{task
                                                        ? t('surfaces.scheduleExplanation.priorityStatusValue', {
                                                            priority: task.priority,
                                                            status: t(`statuses.${task.status}`),
                                                        })
                                                        : t('common.unknown')}</dd>
                                                </div>
                                                <div className="flex justify-between gap-3">
                                                    <dt>{t('surfaces.scheduleExplanation.workload')}</dt>
                                                    <dd className="text-right">{t(workloadBalanced
                                                        ? 'surfaces.scheduleExplanation.balanced'
                                                        : 'surfaces.scheduleExplanation.needsReview')}</dd>
                                                </div>
                                            </dl>
                                        </div>
                                    </div>

                                    <div className="grid gap-4 md:grid-cols-2">
                                        <div>
                                            <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.dependencies')}</h5>
                                            {dependencies.length > 0 ? (
                                                <ul className="mt-2 space-y-1 text-feedback-purple-foreground">
                                                    {dependencies.map(dependencyId => {
                                                        const dependency = taskLookup.get(dependencyId);
                                                        return (
                                                            <li key={dependencyId}>
                                                                {resolveTaskLabel(dependencyId, taskLookup)}
                                                                {dependency && (
                                                                    <span className="text-feedback-purple-foreground">
                                                                        {' '}· {t(`statuses.${dependency.status}`)} · {formatRange(getTaskStart(dependency), getTaskEnd(dependency))}
                                                                    </span>
                                                                )}
                                                            </li>
                                                        );
                                                    })}
                                                </ul>
                                            ) : (
                                                <p className="mt-2 text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.noDependenciesVisibleForThisTask')}</p>
                                            )}
                                        </div>

                                        <div>
                                            <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.vacationOverlap')}</h5>
                                            {vacationRanges.length > 0 ? (
                                                <ul className="mt-2 space-y-1 text-feedback-purple-foreground">
                                                    {vacationRanges.map(range => (
                                                        <li key={`${range.start}-${range.end}`}>{formatRange(range.start, range.end)}</li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p className="mt-2 text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.noAssigneeVacationOverlapInTheScheduledRange')}</p>
                                            )}
                                        </div>
                                    </div>

                                    <div className="grid gap-4 md:grid-cols-2">
                                        <div>
                                            <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.affectedTasks')}</h5>
                                            {affectedTaskIds.length > 0 ? (
                                                <ul className="mt-2 space-y-1 text-feedback-purple-foreground">
                                                    {affectedTaskIds.map(taskId => (
                                                        <li key={taskId}>{resolveTaskLabel(taskId, taskLookup)}</li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p className="mt-2 text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.noAffectedTasksReportedByTheExplanationEndpoint')}</p>
                                            )}
                                        </div>

                                        <div>
                                            <h5 className="text-xs font-semibold uppercase text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.workloadWarnings')}</h5>
                                            {relevantWorkloadIssues.length > 0 ? (
                                                <ul className="mt-2 space-y-1 text-feedback-purple-foreground">
                                                    {relevantWorkloadIssues.map((issue, index) => (
                                                        <li key={`${issue}-${index}`} className="flex gap-2">
                                                            <AlertTriangle className="mt-0.5 h-3.5 w-3.5 shrink-0 text-feedback-warning-foreground" />
                                                            <span>{issue}</span>
                                                        </li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p className="mt-2 text-feedback-purple-foreground">{t('surfaces.scheduleExplanation.noTaskSpecificWorkloadWarningMatchedThisDecision')}</p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};
