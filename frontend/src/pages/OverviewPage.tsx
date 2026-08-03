import { useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import type { TFunction } from 'i18next';
import { formatDate } from '../utils/formatDate';
import clsx from 'clsx';
import {
    Activity,
    AlertTriangle,
    ArrowRight,
    Bookmark,
    Calendar,
    CheckCircle2,
    Clock,
    FolderOpen,
    Inbox,
    Layers,
    ListTodo,
    Plus,
    Target,
    User,
    Users,
    X,
    Zap,
} from 'lucide-react';
import { STEP_DEFS } from '../features/planningMasters/masters';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import type { LucideIcon } from 'lucide-react';
import { iterationService } from '../services/iterationService';
import { teamService } from '../services/teamService';
import { projectService } from '../services/projectService';
import { SavedViewDashboardCards } from '../components/dashboard/SavedViewDashboardCards';
import { Button } from '../components/common/Button';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { TaskForm } from '../components/tasks/TaskForm';
import { InlineEmptyState, PageHeader, PageLayout, SectionCard } from '../components/ui';
import type { ProjectSummary, ProjectTargetDateRisk, ProjectUpdateFreshness } from '../types/project';
import type { MemberWorkload, TeamMember } from '../types/team';
import type { Task, TaskStatus } from '../types/task';
import type { Iteration } from '../types/iteration';
import type { PillTone } from '../components/ui/tone';
import { wcPillClass, STATUS_TONE, toneVar, toneSoftVar } from '../components/ui/tone';

type OverviewTeamMember = Pick<TeamMember, 'id' | 'name' | 'position'> & {
    taskCount: number;
};

type TaskFilter = 'all' | 'active' | 'overdue' | 'unassigned';

type AttentionItem = {
    id: string;
    tone: PillTone;
    icon: LucideIcon;
    title: string;
    meta: string;
    to: string;
    actionLabel: string;
};

const MS_PER_DAY = 24 * 60 * 60 * 1000;
const doneStatuses = new Set<TaskStatus>(['resolved', 'closed']);

const parseIsoDate = (value?: string | null) => {
    if (!value) return null;
    const timestamp = Date.parse(`${value}T00:00:00`);
    return Number.isNaN(timestamp) ? null : timestamp;
};

const formatNumber = (value: number, digits = 1) => (
    value.toFixed(digits).replace(/\.0$/, '')
);

const initialsFor = (name?: string | null) => {
    if (!name) return '?';
    const parts = name.trim().split(/\s+/).slice(0, 2);
    return parts.map(part => part[0]?.toUpperCase() ?? '').join('') || '?';
};

const iterationProgress = (iteration?: Iteration | null) => {
    if (!iteration) return { dayNo: 0, daysLeft: 0, percent: 0 };

    const workingDays = Math.max(1, iteration.working_days || 1);
    const start = parseIsoDate(iteration.start_date);
    const end = parseIsoDate(iteration.end_date);
    const today = parseIsoDate(new Date().toISOString().slice(0, 10));

    if (start === null || end === null || today === null || end < start) {
        return { dayNo: 1, daysLeft: Math.max(0, workingDays - 1), percent: Math.min(100, 100 / workingDays) };
    }

    const totalCalendarDays = Math.max(1, Math.round((end - start) / MS_PER_DAY) + 1);
    const elapsedCalendarDays = Math.min(
        totalCalendarDays,
        Math.max(1, Math.round((today - start) / MS_PER_DAY) + 1),
    );
    const dayNo = Math.min(workingDays, Math.max(1, Math.ceil((elapsedCalendarDays / totalCalendarDays) * workingDays)));

    return {
        dayNo,
        daysLeft: Math.max(0, workingDays - dayNo),
        percent: Math.min(100, (dayNo / workingDays) * 100),
    };
};

const riskTone = (risk?: ProjectTargetDateRisk | null): PillTone => {
    if (risk === 'off_track') return 'red';
    if (risk === 'at_risk') return 'yellow';
    if (risk === 'on_track') return 'green';
    return 'gray';
};

const freshnessTone = (freshness?: ProjectUpdateFreshness | null): PillTone => {
    if (freshness === 'missing') return 'red';
    if (freshness === 'stale') return 'yellow';
    if (freshness === 'fresh') return 'green';
    return 'gray';
};

const OverviewPage = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [isQuickCreateOpen, setIsQuickCreateOpen] = useState(false);
    const [taskFilter, setTaskFilter] = useState<TaskFilter>('all');
    const {
        selectedIterationId,
        currentIteration: selectedIteration,
        teamMembers,
        allTasks,
        readinessData: planR,
        ready: planReady,
        nextId: planNextId,
        isLoading: isPlanningLoading,
        isError: isPlanningError,
        error: planningError,
        refetch: refetchPlanning,
    } = usePlanningReadiness({ autoSelectFirst: true, includeInbox: true });

    const {
        data: iterationSummary,
        error: iterationSummaryError,
        isError: isIterationSummaryError,
        isLoading: isLoadingIterationSummary,
        refetch: refetchIterationSummary,
    } = useQuery({
        queryKey: ['iterationSummary', selectedIterationId],
        queryFn: () => iterationService.getSummary(selectedIterationId),
        enabled: selectedIterationId > 0,
    });

    const scopedProject = selectedIteration?.project ?? iterationSummary?.project ?? null;
    const scopedProjectId = scopedProject?.id ?? selectedIteration?.project_id ?? iterationSummary?.project_id ?? null;

    const {
        data: linkedProjectSummary,
        error: linkedProjectSummaryError,
        isError: isLinkedProjectSummaryError,
        isLoading: isLoadingLinkedProjectSummary,
        refetch: refetchLinkedProjectSummary,
    } = useQuery({
        queryKey: ['projectSummary', scopedProjectId],
        queryFn: () => projectService.getSummary(scopedProjectId as number),
        enabled: Boolean(scopedProjectId),
        staleTime: 30000,
    });

    const completedTasks = allTasks.filter(task => doneStatuses.has(task.status)).length;
    const overdueTaskList = allTasks.filter(task => task.is_overdue);
    const unassignedTaskList = allTasks.filter(task => !task.assignee);
    const totalEffortDays = allTasks.reduce((sum, task) => sum + (task.effort_days || 0), 0);
    const completedEffortDays = allTasks
        .filter(task => doneStatuses.has(task.status))
        .reduce((sum, task) => sum + (task.effort_days || 0), 0);

    const totalTasks = iterationSummary?.total_tasks ?? allTasks.length;
    const shippedTasks = iterationSummary?.completed_tasks ?? completedTasks;
    const effortDays = iterationSummary?.total_effort_days ?? totalEffortDays;
    const progress = selectedIteration ? iterationProgress(selectedIteration) : { dayNo: 0, daysLeft: 0, percent: 0 };
    const completionPercent = totalTasks > 0 ? (shippedTasks / totalTasks) * 100 : 0;

    const teamWorkloadData: OverviewTeamMember[] = teamMembers.map(member => ({
        id: member.id,
        name: member.name,
        position: member.position,
        taskCount: allTasks.filter(task => task.assignee?.id === member.id).length,
    }));

    const taskCounts: Record<TaskStatus, number> = {
        planned: allTasks.filter(task => task.status === 'planned').length,
        active: allTasks.filter(task => task.status === 'active').length,
        resolved: allTasks.filter(task => task.status === 'resolved').length,
        closed: allTasks.filter(task => task.status === 'closed').length,
    };

    const attentionItems = useMemo<AttentionItem[]>(() => {
        const items: AttentionItem[] = [];
        if (overdueTaskList.length > 0) {
            items.push({
                id: 'overdue',
                tone: 'red',
                icon: Clock,
                title: t('overview.attention.overdueTitle', { count: overdueTaskList.length }),
                meta: t('overview.attention.overdueMeta'),
                to: '/tasks',
                actionLabel: t('overview.focus.reviewTasks'),
            });
        }
        if (linkedProjectSummary?.target_date_risk === 'at_risk' || linkedProjectSummary?.target_date_risk === 'off_track') {
            items.push({
                id: 'project-risk',
                tone: riskTone(linkedProjectSummary.target_date_risk),
                icon: AlertTriangle,
                title: t('overview.attention.projectRiskTitle'),
                meta: linkedProjectSummary.target_date_risk_reason || t(`overview.riskLabels.${linkedProjectSummary.target_date_risk}`),
                to: scopedProjectId ? `/projects/${scopedProjectId}` : '/projects',
                actionLabel: t('overview.focus.openProject'),
            });
        }
        if (unassignedTaskList.length > 0) {
            items.push({
                id: 'unassigned',
                tone: 'gray',
                icon: User,
                title: t('overview.attention.unassignedTitle', { count: unassignedTaskList.length }),
                meta: unassignedTaskList[0]?.title ?? t('common.unassigned'),
                to: '/tasks',
                actionLabel: t('overview.focus.reviewTasks'),
            });
        }
        if (planR.inboxCount > 0) {
            items.push({
                id: 'intake',
                tone: 'yellow',
                icon: Inbox,
                title: t('overview.attention.intakeTitle', { count: planR.inboxCount }),
                meta: t('overview.attention.intakeMeta'),
                to: '/triage',
                actionLabel: t('overview.focus.reviewIntake'),
            });
        }
        if (linkedProjectSummary?.is_update_stale) {
            items.push({
                id: 'project-update',
                tone: freshnessTone(linkedProjectSummary.update_freshness),
                icon: Bookmark,
                title: t('overview.attention.projectUpdateTitle'),
                meta: updateFreshnessText(linkedProjectSummary, t),
                to: scopedProjectId ? `/projects/${scopedProjectId}` : '/projects',
                actionLabel: t('overview.focus.openProject'),
            });
        }
        return items;
    }, [linkedProjectSummary, overdueTaskList, planR.inboxCount, scopedProjectId, t, unassignedTaskList]);

    const description = selectedIteration
        ? scopedProject
            ? t('overview.scopedDescription', { project: scopedProject.name })
            : t('overview.independentDescription')
        : t('overview.description');
    const isOverviewLoading = isPlanningLoading
        || isLoadingIterationSummary
        || isLoadingLinkedProjectSummary;
    const hasOverviewQueryError = isPlanningError
        || isIterationSummaryError
        || isLinkedProjectSummaryError;
    const overviewQueryError = planningError ?? iterationSummaryError ?? linkedProjectSummaryError;
    const showOverviewContent = !isOverviewLoading && !hasOverviewQueryError && selectedIteration !== null;

    return (
        <PageLayout>
            <PageHeader
                title={t('overview.title')}
                subtitle={description}
                meta={selectedIteration && (
                    <>
                        {scopedProject ? (
                            <Link to={`/projects/${scopedProject.id}`} className="overview-project-link">
                                <FolderOpen aria-hidden="true" className="h-3.5 w-3.5" />
                                <span>{scopedProject.name}</span>
                            </Link>
                        ) : (
                            <span>{t('overview.independentIteration')}</span>
                        )}
                        <span><Calendar aria-hidden="true" className="inline h-3.5 w-3.5 mr-1"/>{formatDate(selectedIteration.start_date)} - {formatDate(selectedIteration.end_date)}</span>
                        <span><Zap aria-hidden="true" className="inline h-3.5 w-3.5 mr-1"/>{iterationPhase(progress.dayNo, selectedIteration.working_days, t)}</span>
                        <span><Clock aria-hidden="true" className="inline h-3.5 w-3.5 mr-1"/>{t('overview.daysLeft', { count: progress.daysLeft })}</span>
                    </>
                )}
            />

            {isOverviewLoading && <QueryLoadingState message={t('queryFeedback.loading')} />}
            {hasOverviewQueryError && (
                <QueryErrorState
                    error={overviewQueryError}
                    fallback={t('queryFeedback.fallback')}
                    onRetry={() => {
                        void refetchPlanning();
                        void refetchIterationSummary();
                        void refetchLinkedProjectSummary();
                    }}
                />
            )}

            {!isOverviewLoading && !hasOverviewQueryError && selectedIteration === null && (
                <div className="empty">
                    <h4>{t('overview.noIterationTitle')}</h4>
                    <p>{t('overview.noIterationBody')}</p>
                    <div className="empty-actions">
                        <Link className="btn primary" to="/plan">
                            <Calendar aria-hidden="true" className="h-4 w-4" />
                            {t('overview.setUpPlanningPeriod')}
                        </Link>
                    </div>
                </div>
            )}

            {showOverviewContent && (
                <>
                    <OverviewFocusPanel
                        attentionItems={attentionItems}
                        planReady={planReady}
                        planNextId={planNextId}
                        completionPercent={completionPercent}
                        shippedTasks={shippedTasks}
                        totalTasks={totalTasks}
                        progress={progress}
                        workingDays={selectedIteration.working_days}
                    />

                    <div className="wc-panel-stack">
                        {isQuickCreateOpen && selectedIterationId > 0 && (
                            <section className="card card-pad overview-quick-create" aria-labelledby="overview-quick-create-title">
                                <div className="between overview-quick-create-head">
                                    <h2 id="overview-quick-create-title">{t('quickActions.addTask')}</h2>
                                    <button type="button" className="btn ghost sm icon" onClick={() => setIsQuickCreateOpen(false)} aria-label={t('actions.close')}>
                                        <X aria-hidden="true" className="h-4 w-4" />
                                    </button>
                                </div>
                                <TaskForm
                                    iterationId={selectedIterationId}
                                    onSuccess={() => {
                                        setIsQuickCreateOpen(false);
                                        queryClient.invalidateQueries({ queryKey: ['tasks'] });
                                        queryClient.invalidateQueries({ queryKey: ['iterationSummary', selectedIterationId] });
                                        if (scopedProjectId) {
                                            queryClient.invalidateQueries({ queryKey: ['projectSummary', scopedProjectId] });
                                        }
                                        queryClient.invalidateQueries({ queryKey: ['gantt'] });
                                    }}
                                    onCancel={() => setIsQuickCreateOpen(false)}
                                />
                            </section>
                        )}

                        <IterationTasksCard
                            tasks={allTasks}
                            filter={taskFilter}
                            onFilter={setTaskFilter}
                            onAddTask={() => setIsQuickCreateOpen(true)}
                            isProjectScoped={Boolean(scopedProject)}
                        />

                        <details className="overview-details">
                            <summary>
                                <span>
                                    <strong>{t('overview.focus.detailsSummary')}</strong>
                                    <small>{t('overview.focus.detailsHint')}</small>
                                </span>
                                <span className="overview-details-count">
                                    {t('overview.focus.detailsCount', {
                                        count: 5 + (attentionItems.length > 1 ? 1 : 0),
                                    })}
                                </span>
                            </summary>
                            <div className="overview-details-grid">
                                <div className="wc-panel-stack">
                                    <TeamWorkloadSection members={teamWorkloadData} />
                                    <TaskDistributionSection counts={taskCounts} />
                                    <SavedViewDashboardCards iterationId={selectedIterationId} title={t('overview.savedViewSignals')} />
                                </div>
                                <div className="wc-panel-stack">
                                    {attentionItems.length > 1 && (
                                        <AttentionSignalsSection items={attentionItems.slice(1)} />
                                    )}
                                    {scopedProject ? (
                                        <LinkedProjectCard summary={linkedProjectSummary} fallbackProjectName={scopedProject.name} iterationEffortDays={effortDays} />
                                    ) : (
                                        <IndependentScopeCard />
                                    )}
                                    <IterationPaceCard
                                        iteration={selectedIteration}
                                        progress={progress}
                                        totalEffortDays={effortDays}
                                        completedEffortDays={completedEffortDays}
                                        completedTasks={shippedTasks}
                                        totalTasks={totalTasks}
                                    />
                                </div>
                            </div>
                        </details>
                    </div>
                </>
            )}
        </PageLayout>
    );
};

interface OverviewFocusPanelProps {
    attentionItems: AttentionItem[];
    planReady: { done: number; total: number; pct: number };
    planNextId: string;
    completionPercent: number;
    shippedTasks: number;
    totalTasks: number;
    progress: { dayNo: number; daysLeft: number; percent: number };
    workingDays: number;
}

const OverviewFocusPanel = ({
    attentionItems,
    planReady,
    planNextId,
    completionPercent,
    shippedTasks,
    totalTasks,
    progress,
    workingDays,
}: OverviewFocusPanelProps) => {
    const { t } = useTranslation();
    const topAttention = attentionItems[0];
    const needsPlanning = planReady.pct < 100;
    const nextDef = STEP_DEFS.find(step => step.id === planNextId);
    const tone: PillTone = topAttention?.tone ?? (needsPlanning ? 'indigo' : 'green');
    const FocusIcon = topAttention?.icon ?? (needsPlanning ? Target : CheckCircle2);
    const title = topAttention?.title ?? (
        needsPlanning ? t('overview.focus.planIncompleteTitle') : t('overview.focus.planReadyTitle')
    );
    const meta = topAttention?.meta ?? (
        needsPlanning
            ? t('overview.focus.planIncompleteMeta', {
                done: planReady.done,
                total: planReady.total,
                step: nextDef ? t(`plan.steps.${nextDef.id}.title`) : t('nav.planning'),
            })
            : t('overview.focus.planReadyMeta')
    );
    const actionLabel = topAttention?.actionLabel ?? (
        needsPlanning ? t('overview.focus.continuePlanning') : t('overview.focus.reviewPlan')
    );
    const actionTo = topAttention?.to ?? '/plan/master';
    const remainingAttention = Math.max(0, attentionItems.length - 1);
    const completion = Math.max(0, Math.min(100, Math.round(completionPercent)));

    return (
        <section className="overview-focus" aria-labelledby="overview-focus-title">
            <div className="overview-focus-main">
                <div className="overview-focus-heading">
                    <span className="overview-focus-icon" style={pillBoxStyle(tone)}>
                        <FocusIcon aria-hidden="true" className="h-5 w-5" />
                    </span>
                    <div>
                        <h2 id="overview-focus-title">{title}</h2>
                        <p>{meta}</p>
                    </div>
                </div>

                <div className="overview-focus-action">
                    <Link to={actionTo} className="btn primary">
                        {actionLabel}
                        <ArrowRight aria-hidden="true" className="h-4 w-4" />
                    </Link>
                    {remainingAttention > 0 && (
                        <span>{t('overview.focus.moreSignals', { count: remainingAttention })}</span>
                    )}
                </div>
            </div>

            <div className="overview-focus-progress">
                <div className="overview-focus-progress-head">
                    <span>{t('overview.focus.deliveryProgress')}</span>
                    <strong className="tnum">{completion}%</strong>
                </div>
                <div
                    className="overview-focus-track"
                    role="progressbar"
                    aria-label={t('overview.focus.deliveryProgress')}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-valuenow={completion}
                >
                    <span style={{width: `${completion}%`}} />
                </div>
                <dl className="overview-focus-facts">
                    <div>
                        <dt>{t('overview.focus.planReadiness')}</dt>
                        <dd>{t('plan.hub.stepsComplete', { done: planReady.done, total: planReady.total })}</dd>
                    </div>
                    <div>
                        <dt>{t('overview.focus.tasksShipped')}</dt>
                        <dd>{t('overview.tasksShipped', { completed: shippedTasks, total: totalTasks })}</dd>
                    </div>
                    <div>
                        <dt>{t('overview.focus.iterationDay')}</dt>
                        <dd>{t('overview.dayOf', { day: progress.dayNo, total: workingDays })}</dd>
                    </div>
                </dl>
            </div>
        </section>
    );
};

const AttentionSignalsSection = ({ items }: { items: AttentionItem[] }) => {
    const { t } = useTranslation();

    return (
        <SectionCard
            icon={<AlertTriangle aria-hidden="true" className="h-5 w-5 text-feedback-warning" />}
            title={t('overview.focus.otherSignals')}
            count={<span className="pill warn sm">{items.length}</span>}
        >
            <ul className="space-y-2">
                {items.map(item => {
                    const Icon = item.icon;
                    return (
                        <li key={item.id}>
                            <Link
                                to={item.to}
                                className="flex min-w-0 items-start gap-3 rounded-md px-2 py-2 hover:bg-surface-hover"
                            >
                                <span className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-md" style={pillBoxStyle(item.tone)}>
                                    <Icon aria-hidden="true" className="h-4 w-4" />
                                </span>
                                <span className="min-w-0 flex-1">
                                    <strong className="block break-words text-sm text-content-primary">{item.title}</strong>
                                    <span className="block break-words text-xs text-content-secondary">{item.meta}</span>
                                </span>
                                <span className="mt-1 inline-flex shrink-0 items-center gap-1 text-xs font-semibold text-action">
                                    <span className="hidden md:inline">{item.actionLabel}</span>
                                    <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                                </span>
                            </Link>
                        </li>
                    );
                })}
            </ul>
        </SectionCard>
    );
};

const Pill = ({
    icon,
    tone = 'gray',
    children,
}: {
    icon?: ReactNode;
    tone?: PillTone;
    children: ReactNode;
}) => (
    <span className={clsx('pill', wcPillClass[tone])}>
        {icon}
        <span className="truncate">{children}</span>
    </span>
);

const IterationTasksCard = ({
    tasks,
    filter,
    onFilter,
    onAddTask,
    isProjectScoped,
}: {
    tasks: Task[];
    filter: TaskFilter;
    onFilter: (value: TaskFilter) => void;
    onAddTask: () => void;
    isProjectScoped: boolean;
}) => {
    const { t } = useTranslation();
    const filters: Array<{ id: TaskFilter; label: string; count: number }> = [
        { id: 'all', label: t('overview.taskFilters.all'), count: tasks.length },
        { id: 'active', label: t('overview.taskFilters.active'), count: tasks.filter(task => task.status === 'active').length },
        { id: 'overdue', label: t('overview.taskFilters.overdue'), count: tasks.filter(task => task.is_overdue).length },
        { id: 'unassigned', label: t('overview.taskFilters.unassigned'), count: tasks.filter(task => !task.assignee).length },
    ];

    const visibleTasks = tasks.filter(task => {
        if (filter === 'active') return task.status === 'active';
        if (filter === 'overdue') return task.is_overdue;
        if (filter === 'unassigned') return !task.assignee;
        return true;
    });

    const groups = isProjectScoped
        ? visibleTasks.reduce<Record<string, Task[]>>((acc, task) => {
            const groupName = task.milestone?.name || t('overview.noMilestone');
            acc[groupName] = acc[groupName] || [];
            acc[groupName].push(task);
            return acc;
        }, {})
        : { [t('overview.iterationTasksFlatGroup')]: visibleTasks };

    return (
        <SectionCard
            icon={<ListTodo className="h-5 w-5 text-action" />}
            title={t('overview.iterationTasks')}
            actions={(
                <div className="overview-task-actions">
                    <button type="button" className="btn ghost sm" onClick={onAddTask}>
                        <Plus aria-hidden="true" className="h-3.5 w-3.5" />
                        {t('quickActions.addTask')}
                    </button>
                    <Link to="/tasks" className="btn ghost sm">
                        {t('overview.openTaskBoard')}
                        <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                    </Link>
                </div>
            )}
        >
            <div className="mb-4 flex flex-wrap items-center gap-2">
                {filters.map(item => (
                    <button
                        key={item.id}
                        type="button"
                        onClick={() => onFilter(item.id)}
                        aria-pressed={filter === item.id}
                        className={clsx(
                            'inline-flex h-8 items-center gap-1.5 rounded-full px-3 text-xs font-semibold transition-colors',
                            filter === item.id
                                ? 'bg-content-primary text-content-emphasis'
                                : 'bg-surface-subtle text-content-primary hover:bg-surface-hover',
                        )}
                    >
                        <span>{item.label}</span>
                        <span className={clsx('rounded-full px-1.5 text-wc-micro tabular-nums', filter === item.id ? 'bg-content-emphasis/15 text-content-emphasis' : 'bg-surface-card text-content-secondary')}>
                            {item.count}
                        </span>
                    </button>
                ))}
            </div>

            {visibleTasks.length === 0 ? (
                <InlineEmptyState
                    actions={filter === 'all'
                        ? undefined
                        : <Button variant="outline" size="sm" onClick={() => onFilter('all')}>{t('actions.clear')}</Button>}
                >
                    {filter === 'all' ? t('overview.noIterationTasks') : t('overview.noTasksForFilter')}
                </InlineEmptyState>
            ) : (
                <div className="space-y-4">
                    {Object.entries(groups).map(([groupName, items]) => (
                        <div key={groupName}>
                            {isProjectScoped && (
                                <div className="mb-2 flex items-center gap-2 px-1 text-wc-micro font-semibold uppercase tracking-wide text-content-secondary">
                                    <Target className="h-3 w-3 text-content-tertiary" />
                                    <span className="truncate">{groupName}</span>
                                    <span className="tabular-nums text-content-tertiary">| {items.length}</span>
                                </div>
                            )}
                            <ul className="divide-y divide-border-subtle overflow-hidden rounded-lg border border-border-subtle">
                                {items.map(task => <TaskRow key={task.id} task={task} showProject={!isProjectScoped} />)}
                            </ul>
                        </div>
                    ))}
                </div>
            )}
        </SectionCard>
    );
};

const TaskRow = ({ task, showProject }: { task: Task; showProject: boolean }) => {
    const { t } = useTranslation();
    const status = t(`statuses.${task.status}`);
    const tone = STATUS_TONE[task.status];

    return (
        <li className="flex min-w-0 items-center gap-3 px-3 py-2.5 hover:bg-surface-hover">
            <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-medium text-content-primary">{task.title}</div>
                <div className="mt-0.5 flex min-w-0 items-center gap-2 text-xs text-content-secondary">
                    <span className="inline-flex shrink-0 items-center gap-1.5 font-medium">
                        <span
                            aria-hidden="true"
                            className="h-1.5 w-1.5 shrink-0 rounded-full"
                            style={dotStyle(tone)}
                        />
                        <span>{status}</span>
                    </span>
                    {showProject && task.project && (
                        <span className="truncate">{task.project.name}</span>
                    )}
                </div>
            </div>
            {task.is_overdue && (
                <span className="inline-flex h-5 shrink-0 items-center gap-1 rounded bg-feedback-danger-muted px-1.5 text-wc-micro font-semibold text-feedback-danger-foreground">
                    <Clock aria-hidden="true" className="h-3 w-3" />
                    {t('taskList.overdue')}
                </span>
            )}
            <span className="w-10 shrink-0 text-right text-xs tabular-nums text-content-secondary">{t('units.daysCompact', { count: formatNumber(task.effort_days || 0) })}</span>
            {task.assignee ? (
                <span
                    title={task.assignee.name}
                    role="img"
                    aria-label={task.assignee.name}
                    className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-status-active-muted text-wc-micro font-bold text-action"
                >
                    <span aria-hidden="true">{initialsFor(task.assignee.name)}</span>
                </span>
            ) : (
                <span
                    title={t('common.unassigned')}
                    role="img"
                    aria-label={t('common.unassigned')}
                    className="grid h-7 w-7 shrink-0 place-items-center rounded-full border border-dashed border-border-strong bg-surface-card text-content-tertiary"
                >
                    <User aria-hidden="true" className="h-3.5 w-3.5" />
                </span>
            )}
        </li>
    );
};

const TeamWorkloadSection = ({ members }: { members: OverviewTeamMember[] }) => {
    const { t } = useTranslation();

    return (
        <SectionCard
            icon={<Users className="h-5 w-5 text-action" />}
            title={t('overview.teamWorkload')}
        >
            {members.length === 0 ? (
                <InlineEmptyState>{t('overview.noTeamMembers')}</InlineEmptyState>
            ) : (
                <ul className="space-y-2">
                    {members.map(member => <TeamMemberRow key={member.id} member={member} />)}
                </ul>
            )}
        </SectionCard>
    );
};

const TeamMemberRow = ({ member }: { member: OverviewTeamMember }) => {
    const { t } = useTranslation();
    const {
        data: workload,
        error: workloadError,
        isError: isWorkloadError,
        isLoading: isLoadingWorkload,
        refetch: refetchWorkload,
    } = useQuery<MemberWorkload>({
        queryKey: ['workload', member.id],
        queryFn: () => teamService.getWorkload(member.id),
        staleTime: 60 * 1000,
        retry: 1,
        refetchOnMount: 'always',
    });

    const capacity = workload?.capacity_days ?? 0;
    const allocated = workload?.allocated_days ?? 0;
    const utilizationPercent = capacity > 0 ? Math.min(100, (allocated / capacity) * 100) : 0;
    const tone: PillTone = allocated > capacity && capacity > 0 ? 'red' : utilizationPercent >= 85 ? 'yellow' : 'green';

    if (isWorkloadError) {
        return (
            <li className="flex min-w-0 items-start gap-3 py-1.5">
                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-status-active-muted text-xs font-bold text-action">
                    {initialsFor(member.name)}
                </span>
                <QueryErrorState
                    className="min-w-0 flex-1"
                    error={workloadError}
                    fallback={t('queryFeedback.fallback')}
                    onRetry={() => { void refetchWorkload(); }}
                    title={member.name}
                />
            </li>
        );
    }

    return (
        <li className="flex min-w-0 items-center gap-3 py-1.5">
            <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-status-active-muted text-xs font-bold text-action">
                {initialsFor(member.name)}
            </span>
            <div className="w-36 min-w-0">
                <div className="truncate text-sm font-semibold text-content-primary">{member.name}</div>
                <div className="truncate text-xs text-content-secondary">{member.position}</div>
            </div>
            <div className="min-w-0 flex-1">
                <div className="h-2 overflow-hidden rounded-full bg-surface-subtle">
                    <div className="h-full transition-all" style={{ ...dotStyle(tone), width: `${utilizationPercent}%` }} />
                </div>
                <div className="mt-1 flex items-center justify-between text-wc-micro text-content-secondary">
                    <span className="tabular-nums">{!isLoadingWorkload && workload ? t('overview.allocatedCapacity', { allocated: formatNumber(allocated), capacity: formatNumber(capacity) }) : t('common.loading')}</span>
                    <span>{t('overview.taskCount', { count: member.taskCount })}</span>
                </div>
            </div>
            <span className="grid h-6 shrink-0 place-items-center rounded-md px-2 text-wc-micro font-bold tabular-nums" style={pillBoxStyle(tone)}>
                {Math.round(utilizationPercent)}%
            </span>
        </li>
    );
};

const TaskDistributionSection = ({ counts }: { counts: Record<TaskStatus, number> }) => {
    const { t } = useTranslation();
    const total = counts.planned + counts.active + counts.resolved + counts.closed;
    const segments: Array<{ status: TaskStatus; tone: PillTone; count: number }> = [
        { status: 'planned', tone: STATUS_TONE.planned, count: counts.planned },
        { status: 'active', tone: STATUS_TONE.active, count: counts.active },
        { status: 'resolved', tone: STATUS_TONE.resolved, count: counts.resolved },
        { status: 'closed', tone: STATUS_TONE.closed, count: counts.closed },
    ];

    return (
        <SectionCard
            icon={<CheckCircle2 className="h-5 w-5 text-action" />}
            title={t('overview.taskDistribution')}
            count={<span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs font-semibold tabular-nums text-content-secondary">{total}</span>}
        >
            {total === 0 ? (
                <InlineEmptyState>{t('overview.noIterationTasks')}</InlineEmptyState>
            ) : (
                <>
                    <div className="flex h-3 overflow-hidden rounded-full bg-surface-subtle">
                        {segments.map(segment => segment.count > 0 && (
                            <div
                                key={segment.status}
                                style={{ ...dotStyle(segment.tone), width: `${(segment.count / total) * 100}%` }}
                                title={`${t(`statuses.${segment.status}`)}: ${segment.count}`}
                            />
                        ))}
                    </div>
                    <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
                        {segments.map(segment => {
                            const percent = total > 0 ? Math.round((segment.count / total) * 100) : 0;
                            return (
                                <div key={segment.status} className="flex items-center gap-2 rounded-md px-2 py-1.5 hover:bg-surface-hover">
                                    <span className="h-2 w-2 rounded-full" style={dotStyle(segment.tone)} />
                                    <div className="min-w-0">
                                        <div className="text-wc-micro font-semibold uppercase text-content-secondary">{t(`statuses.${segment.status}`)}</div>
                                        <div className="text-sm font-semibold tabular-nums text-content-primary">{segment.count} <span className="text-xs font-normal text-content-tertiary">| {percent}%</span></div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </>
            )}
        </SectionCard>
    );
};

const LinkedProjectCard = ({
    summary,
    fallbackProjectName,
    iterationEffortDays,
}: {
    summary?: ProjectSummary;
    fallbackProjectName: string;
    iterationEffortDays: number;
}) => {
    const { t } = useTranslation();
    const risk = summary?.target_date_risk ?? 'unknown';
    const riskLabel = t(`overview.riskLabels.${risk}`);
    const projectEffort = summary?.total_effort_days ?? 0;
    const iterationShare = projectEffort > 0 ? Math.round((iterationEffortDays / projectEffort) * 100) : 0;

    return (
        <SectionCard
            icon={<FolderOpen className="h-5 w-5 text-action" />}
            title={t('overview.linkedProject')}
            actions={summary && (
                <Link to={`/projects/${summary.id}`} className="inline-flex items-center gap-1 text-sm font-medium text-action hover:text-action">
                    {t('overview.open')}
                    <ArrowRight className="h-4 w-4" />
                </Link>
            )}
        >
            <div className="flex items-center gap-3">
                <CompletionRing percent={summary?.completion_percent ?? 0} tone={riskTone(risk)} />
                <div className="min-w-0 flex-1">
                    <div className="truncate text-sm font-semibold text-content-primary">{summary?.name ?? fallbackProjectName}</div>
                    <div className="mt-1 flex flex-wrap items-center gap-1.5">
                        <Pill tone={riskTone(risk)} icon={<span className="h-1.5 w-1.5 rounded-full" style={dotStyle(riskTone(risk))} />}>{riskLabel}</Pill>
                        {summary && (
                            <Pill tone={freshnessTone(summary.update_freshness)}>{updateFreshnessText(summary, t)}</Pill>
                        )}
                    </div>
                </div>
            </div>
            <div className="mt-4 space-y-2.5">
                <FactRow label={t('overview.target')} value={formatDate(summary?.target_date)} />
                <FactRow label={t('overview.remaining')} value={summary ? t('units.daysCompact', { count: formatNumber(summary.remaining_effort_days) }) : '-'} />
                <FactRow label={t('overview.iterationShare')} value={projectEffort > 0 ? `${iterationShare}%` : '-'} />
            </div>
            {summary?.target_date_risk_reason && (
                <div className="mt-3 rounded-md border border-border-subtle bg-surface-muted px-3 py-2 text-xs text-content-secondary">
                    {summary.target_date_risk_reason}
                </div>
            )}
        </SectionCard>
    );
};

const IndependentScopeCard = () => {
    const { t } = useTranslation();
    return (
        <SectionCard
            icon={<Layers className="h-5 w-5 text-content-secondary" />}
            title={t('overview.independentIteration')}
        >
            <p className="text-sm text-content-secondary">{t('overview.independentScopeBody')}</p>
        </SectionCard>
    );
};

const IterationPaceCard = ({
    iteration,
    progress,
    totalEffortDays,
    completedEffortDays,
    completedTasks,
    totalTasks,
}: {
    iteration: Iteration;
    progress: { dayNo: number; daysLeft: number; percent: number };
    totalEffortDays: number;
    completedEffortDays: number;
    completedTasks: number;
    totalTasks: number;
}) => {
    const { t } = useTranslation();
    const effortPercent = totalEffortDays > 0 ? (completedEffortDays / totalEffortDays) * 100 : 0;
    const velocity = progress.dayNo > 0 ? completedTasks / progress.dayNo : 0;

    return (
        <SectionCard
            icon={<Activity className="h-5 w-5 text-action" />}
            title={t('overview.iterationPace')}
            count={<Pill tone={progress.daysLeft <= 1 ? 'red' : progress.daysLeft <= 2 ? 'yellow' : 'green'}>{t('overview.daysLeftShort', { count: progress.daysLeft })}</Pill>}
        >
            <div className="space-y-2.5">
                <FactRow label={t('overview.day')} value={t('overview.dayOf', { day: progress.dayNo, total: iteration.working_days })} />
                <FactRow label={t('overview.effortBurned')} value={`${formatNumber(completedEffortDays)} / ${formatNumber(totalEffortDays)}d`} />
                <FactRow label={t('overview.velocity')} value={t('overview.tasksPerDay', { count: formatNumber(velocity) })} />
            </div>
            <div className="mt-4 border-t border-border-subtle pt-3">
                <div className="mb-1.5 flex items-baseline justify-between text-xs">
                    <span className="text-content-secondary">{t('overview.burnUp')}</span>
                    <span className="tabular-nums text-content-tertiary">{t('overview.targetPercent', { percent: Math.round(progress.percent) })}</span>
                </div>
                <div className="relative h-16 rounded-lg bg-surface-muted px-2 py-2">
                    <div className="absolute inset-x-2 bottom-2 h-px bg-surface-hover" />
                    <div className="absolute inset-x-2 top-2 h-px bg-surface-hover" />
                    <div className="absolute bottom-2 left-2 right-2 h-px origin-left -rotate-[10deg] border-t border-dashed border-border-strong" />
                    <div className="absolute bottom-2 left-2 h-1 rounded-full bg-action" style={{ width: `${Math.min(100, effortPercent)}%` }} />
                    <div className="absolute bottom-1 top-1 w-px -translate-x-1/2 bg-content-primary" style={{ left: `${progress.percent}%` }} />
                </div>
                <div className="mt-1 flex justify-between text-wc-micro tabular-nums text-content-tertiary">
                    <span>{formatDate(iteration.start_date)}</span>
                    <span>{formatDate(iteration.end_date)}</span>
                </div>
            </div>
            {totalTasks === 0 && (
                <div className="mt-3 rounded-md border border-dashed border-border bg-surface-muted px-3 py-2 text-xs text-content-secondary">
                    {t('overview.noIterationTasks')}
                </div>
            )}
        </SectionCard>
    );
};

const CompletionRing = ({ percent, tone }: { percent: number; tone: PillTone }) => {
    const radius = 21;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (Math.max(0, Math.min(100, percent)) / 100) * circumference;

    return (
        <div className="relative h-14 w-14 shrink-0">
            <svg viewBox="0 0 52 52" className="-rotate-90">
                <circle cx="26" cy="26" r={radius} fill="none" stroke="rgb(var(--color-border-subtle))" strokeWidth="4" />
                <circle
                    cx="26"
                    cy="26"
                    r={radius}
                    fill="none"
                    stroke={ringColor(tone)}
                    strokeWidth="4"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                />
            </svg>
            <div className="absolute inset-0 grid place-items-center text-wc-micro font-bold tabular-nums text-content-primary">
                {Math.round(percent)}%
            </div>
        </div>
    );
};

const FactRow = ({ label, value }: { label: ReactNode; value: ReactNode }) => (
    <div className="flex items-baseline justify-between gap-3 text-sm">
        <span className="text-content-secondary">{label}</span>
        <span className="text-right font-medium tabular-nums text-content-primary">{value}</span>
    </div>
);

const updateFreshnessText = (summary: ProjectSummary, t: TFunction) => {
    if (summary.update_freshness === 'not_required') return t('overview.freshnessLabels.not_required');
    if (summary.days_since_latest_update === null || summary.days_since_latest_update === undefined) {
        return t('overview.noUpdatePosted');
    }
    if (summary.days_since_latest_update <= 0) return t('overview.updatedToday');
    if (summary.days_since_latest_update === 1) return t('overview.updatedYesterday');
    return t('overview.daysSinceUpdate', { count: summary.days_since_latest_update });
};

const iterationPhase = (dayNo: number, workingDays: number, t: TFunction) => {
    if (dayNo <= 1) return t('overview.phase.start');
    if (dayNo >= workingDays) return t('overview.phase.closeout');
    const ratio = dayNo / Math.max(1, workingDays);
    if (ratio < 0.5) return t('overview.phase.early');
    if (ratio < 0.8) return t('overview.phase.middle');
    return t('overview.phase.final');
};

// Inline style for soft-tinted "pill box" elements (badges, icon tiles).
const pillBoxStyle = (tone: PillTone) => ({
    background: toneSoftVar[tone],
    color: toneVar[tone],
});

// Background colour (WorkChord token) for dots and progress fills.
const dotStyle = (tone: PillTone) => ({ background: toneVar[tone] });

const ringColor = (tone: PillTone) => toneVar[tone];

export default OverviewPage;
