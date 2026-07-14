import { useMemo, useState } from 'react';
import type { ReactNode, CSSProperties } from 'react';
import { Link, useNavigate } from 'react-router-dom';
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
import { MetricGrid, PageHeader, PageLayout, SectionCard } from '../components/ui';
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
        status: planStatus,
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
    const overdueTasks = iterationSummary?.overdue_tasks_count ?? overdueTaskList.length;
    const effortDays = iterationSummary?.total_effort_days ?? totalEffortDays;
    const progress = selectedIteration ? iterationProgress(selectedIteration) : { dayNo: 0, daysLeft: 0, percent: 0 };
    const completionPercent = totalTasks > 0 ? (shippedTasks / totalTasks) * 100 : 0;
    const healthTone: PillTone = linkedProjectSummary?.target_date_risk === 'off_track' || overdueTasks > 0
        ? 'red'
        : linkedProjectSummary?.target_date_risk === 'at_risk'
            ? 'yellow'
            : 'green';

    const planTeamCapacity = planR.teamCapacity;

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
            });
        }
        if (unassignedTaskList.length > 0) {
            items.push({
                id: 'unassigned',
                tone: 'gray',
                icon: User,
                title: t('overview.attention.unassignedTitle', { count: unassignedTaskList.length }),
                meta: unassignedTaskList[0]?.title ?? t('common.unassigned'),
            });
        }
        if (linkedProjectSummary?.target_date_risk === 'at_risk' || linkedProjectSummary?.target_date_risk === 'off_track') {
            items.push({
                id: 'project-risk',
                tone: riskTone(linkedProjectSummary.target_date_risk),
                icon: AlertTriangle,
                title: t('overview.attention.projectRiskTitle'),
                meta: linkedProjectSummary.target_date_risk_reason || t(`overview.riskLabels.${linkedProjectSummary.target_date_risk}`),
            });
        }
        if (linkedProjectSummary?.is_update_stale) {
            items.push({
                id: 'project-update',
                tone: freshnessTone(linkedProjectSummary.update_freshness),
                icon: Bookmark,
                title: t('overview.attention.projectUpdateTitle'),
                meta: updateFreshnessText(linkedProjectSummary, t),
            });
        }
        return items;
    }, [linkedProjectSummary, overdueTaskList, t, unassignedTaskList]);

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
            {isQuickCreateOpen && selectedIterationId > 0 && (
                <div className="card card-pad" style={{maxWidth:640, margin:'0 auto', width:'100%'}}>
                    <div className="between" style={{marginBottom:16}}>
                        <h2 style={{fontSize:16, fontWeight:600, margin:0}}>{t('quickActions.addTask')}</h2>
                        <button type="button" className="btn ghost sm" onClick={() => setIsQuickCreateOpen(false)} aria-label={t('actions.close')}>
                            <X className="h-4 w-4" />
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
                </div>
            )}

            <PageHeader
                title={t('overview.title')}
                subtitle={description}
                eyebrow={(
                    <div className="row wrap" style={{gap:6, marginBottom:6}}>
                        <span className="pill accent"><span className="pdot"/>{t('overview.deliveryHub')}</span>
                        {selectedIteration && (
                            <span className={`pill ${healthTone === 'green' ? 'done' : healthTone === 'yellow' ? 'warn' : healthTone === 'red' ? 'blocked' : 'opt'}`}>
                                <span className="pdot"/>{t(`overview.iterationHealth.${healthTone}`)}
                            </span>
                        )}
                        {scopedProject ? (
                            <Link to={`/projects/${scopedProject.id}`} className="pill accent" style={{textDecoration:'none'}}>
                                <FolderOpen className="h-3 w-3" />
                                <span style={{maxWidth:'14rem', overflow:'hidden', textOverflow:'ellipsis'}}>{scopedProject.name}</span>
                                <ArrowRight className="h-3 w-3" />
                            </Link>
                        ) : selectedIteration ? (
                            <span className="pill opt"><span className="pdot"/>{t('overview.independentIteration')}</span>
                        ) : null}
                    </div>
                )}
                meta={selectedIteration && (
                        <div className="row wrap" style={{gap:14}}>
                            <span><Calendar className="inline h-3.5 w-3.5 mr-1"/>{formatDate(selectedIteration.start_date)} - {formatDate(selectedIteration.end_date)}</span>
                            <span><Zap className="inline h-3.5 w-3.5 mr-1"/>{iterationPhase(progress.dayNo, selectedIteration.working_days, t)}</span>
                            <span><Clock className="inline h-3.5 w-3.5 mr-1"/>{t('overview.daysLeft', { count: progress.daysLeft })}</span>
                        </div>
                )}
                actions={(
                    <button className="btn primary" onClick={() => setIsQuickCreateOpen(true)} disabled={selectedIterationId <= 0}>
                    <Plus className="h-4 w-4"/> {t('quickActions.addTask')}
                    </button>
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
                </div>
            )}

            {showOverviewContent && (
            <>
            {/* Progress bar */}
            <div>
                <div style={{display:'flex', flexWrap:'wrap', justifyContent:'space-between', gap:8, fontSize:11.5, color:'var(--ink-3)', marginBottom:6}}>
                    <span style={{fontWeight:500, color:'var(--ink)'}}>{t('overview.iterationProgress')}</span>
                    <span className="tnum">
                        {t('overview.dayOf', { day: progress.dayNo, total: selectedIteration?.working_days ?? 0 })}
                        <span style={{margin:'0 8px', color:'var(--border-3)'}}>|</span>
                        {t('overview.tasksShipped', { completed: shippedTasks, total: totalTasks })}
                    </span>
                </div>
                <div style={{position:'relative', height:6, background:'var(--panel-3)', borderRadius:999, overflow:'hidden'}}>
                    <div style={{position:'absolute', insetBlock:0, left:0, background:'var(--done)', width:`${completionPercent}%`}} />
                    <div style={{position:'absolute', top:-3, bottom:-3, width:2, background:'var(--ink)', left:`${progress.percent}%`}} />
                </div>
            </div>

            <MetricGrid columns={5}>
                <div className="kpi"><div className="kpi-lbl">{t('overview.workingDays')}</div><div className="kpi-val tnum">{selectedIteration?.working_days || 0}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('overview.teamMembers')}</div><div className="kpi-val tnum">{teamMembers.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('overview.totalEffort')}</div><div className="kpi-val tnum">{t('units.daysCompact', { count: formatNumber(effortDays) })}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('overview.tasks')}</div><div className="kpi-val tnum">{shippedTasks}/{totalTasks}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('overview.overdue')}</div><div className="kpi-val tnum">{overdueTasks}</div></div>
            </MetricGrid>

            <OverviewMasterHero
                hasIteration={selectedIterationId > 0 && selectedIteration !== null}
                hasWarnings={planReady.pct < 100}
                planStatus={planStatus}
                planReady={planReady}
                planNextId={planNextId}
                taskCount={allTasks.length}
                teamCapacity={planTeamCapacity}
                riskCount={overdueTaskList.length}
                inboxCount={planR.inboxCount}
            />

            {!selectedIteration ? null : (
                <div className="wc-content-rail">
                    <div className="wc-panel-stack">
                        <OverdueTasksCard tasks={overdueTaskList} />
                        <IterationTasksCard
                            tasks={allTasks}
                            filter={taskFilter}
                            onFilter={setTaskFilter}
                            isProjectScoped={Boolean(scopedProject)}
                        />
                        <TeamWorkloadSection members={teamWorkloadData} />
                        <TaskDistributionSection counts={taskCounts} />
                        <SavedViewDashboardCards iterationId={selectedIterationId} title={t('overview.savedViewSignals')} />
                    </div>

                    <aside className="wc-panel-stack sticky-rail">
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
                        <NeedsAttentionCard items={attentionItems} />
                    </aside>
                </div>
            )}
            </>
            )}
        </PageLayout>
    );
};

// ── Plan Work hero card (design's OverviewMasterHero) ────────────────────────
const Svg = ({ d, size = 14, stroke = 1.75, ...rest }: { d: ReactNode; size?: number; stroke?: number; style?: CSSProperties }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" {...rest}>
        {d}
    </svg>
);
const ICheck = (p: { size?: number; stroke?: number }) => <Svg {...p} d={<polyline points="20 6 9 17 4 12"/>}/>;
const IArrowPM = (p: { size?: number }) => <Svg {...p} d={<><path d="M5 12h14M13 5l7 7-7 7"/></>}/>;

interface OverviewMasterHeroProps {
    hasIteration: boolean;
    hasWarnings: boolean;
    planStatus: Record<string, { state: string; summary?: string; missing?: string[] }>;
    planReady: { done: number; total: number; pct: number };
    planNextId: string;
    taskCount: number;
    teamCapacity: number;
    riskCount: number;
    inboxCount: number;
}

const OverviewMasterHero = ({
    hasIteration, hasWarnings, planStatus, planReady, planNextId,
    taskCount, teamCapacity, riskCount, inboxCount,
}: OverviewMasterHeroProps) => {
    const navigate = useNavigate();
    const { t } = useTranslation();

    const mode = !hasIteration ? 'empty' : hasWarnings ? 'partial' : 'review';
    const nextDef = STEP_DEFS.find(s => s.id === planNextId);

    const eyebrow = mode === 'empty' ? t('plan.overview.welcome')
                  : mode === 'review' ? t('plan.overview.inFlight')
                  : t('plan.overview.inProgress');

    const title = mode === 'empty' ? t('plan.overview.startPlanning')
                : mode === 'review' ? t('plan.overview.reviewCurrent')
                : t('plan.overview.continueSetup');

    const desc = mode === 'empty'
        ? t('plan.overview.emptyDescription')
        : mode === 'review'
            ? t('plan.overview.reviewDescription')
            : t('plan.overview.progressDescription', {
                done: planReady.done,
                total: planReady.total,
                next: nextDef ? t(`plan.steps.${nextDef.id}.title`).toLowerCase() : '…',
            });

    const ctaLabel = mode === 'empty'
        ? t('plan.sidebar.start')
        : mode === 'review'
            ? t('plan.overview.openReview')
            : t('plan.overview.resumeStep', { step: nextDef ? t(`plan.steps.${nextDef.id}.title`) : t('nav.planning') });

    return (
        <div className="hero-master">
                <div className="hm-left">
                    <div className="hm-eyebrow">{eyebrow}</div>
                    <h3>{title}</h3>
                    <div className="hm-desc">{desc}</div>

                    <div className="row" style={{marginTop:4, gap:10}}>
                        <button className="btn primary" onClick={() => navigate('/plan/master')}>
                            {ctaLabel}<IArrowPM size={13}/>
                        </button>
                        <button className="btn ghost" onClick={() => navigate('/plan')}>{t('plan.overview.seeAllMasters')}</button>
                    </div>

                    {mode !== 'empty' && (
                        <div style={{display:'flex', gap:6, marginTop:6}}>
                            {STEP_DEFS.map((s, i) => {
                                const st = planStatus[s.id]?.state;
                                const cls = st === 'done' ? 'done' : st === 'warn' ? 'warn' : st === 'blocked' ? 'blocked' : s.id === planNextId ? 'current' : '';
                                return (
                                    <div key={s.id} title={t(`plan.steps.${s.id}.title`)} style={{flex:1}}>
                                        <div className={`mini-step ${cls}`} style={{border:0, padding:'4px 0'}}>
                                            <div className="ms-dot" style={{width:14, height:14}}>
                                                {st === 'done' ? <ICheck size={9} stroke={3}/> : (i+1)}
                                            </div>
                                            <div style={{fontSize:11}}>{t(`plan.steps.${s.id}.title`).split(' ').slice(0,2).join(' ')}</div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </div>

                <div className="hm-right">
                    <div className="row" style={{gap:12}}>
                        <div
                            className={`ring ${planReady.pct === 100 ? 'done' : ''}`}
                            style={{'--p': planReady.pct} as CSSProperties}
                        >
                            <span>{planReady.pct}%</span>
                        </div>
                        <div>
                            <div style={{fontWeight:600, fontSize:13}}>{t('plan.master.planReadiness')}</div>
                            <div className="muted" style={{fontSize:11.5, marginTop:2}}>
                                {t('plan.hub.stepsComplete', { done: planReady.done, total: planReady.total })}
                            </div>
                        </div>
                    </div>
                    <div className="divider" style={{margin:'4px 0'}}/>
                    <div style={{display:'flex', flexDirection:'column', gap:6, fontSize:11.5}}>
                        <div className="between"><div className="muted">{t('plan.overview.tasks')}</div><div className="tnum">{taskCount}</div></div>
                        <div className="between"><div className="muted">{t('plan.overview.teamCapacity')}</div><div className="tnum">{teamCapacity}h</div></div>
                        <div className="between"><div className="muted">{t('plan.overview.openRisks')}</div><div className="tnum">{riskCount || '—'}</div></div>
                        <div className="between"><div className="muted">{t('plan.overview.intakeQueue')}</div><div className="tnum">{inboxCount}</div></div>
                    </div>
                </div>
            </div>
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

const OverdueTasksCard = ({ tasks }: { tasks: Task[] }) => {
    const { t } = useTranslation();
    if (tasks.length === 0) return null;

    return (
        <SectionCard
            className="border-feedback-danger-border bg-feedback-danger-muted"
            icon={<AlertTriangle className="h-5 w-5 text-feedback-danger" />}
            title={<span className="text-feedback-danger-foreground">{t('overview.overdueTasks', { count: tasks.length })}</span>}
            actions={(
                <Link to="/tasks" className="inline-flex items-center gap-1 text-sm font-medium text-feedback-danger-foreground hover:underline">
                    {t('overview.openTaskBoard')}
                    <ArrowRight className="h-4 w-4" />
                </Link>
            )}
        >
            <ul className="space-y-2">
                {tasks.slice(0, 5).map(task => (
                    <li key={task.id} className="flex min-w-0 items-center gap-3 rounded-lg border border-feedback-danger-border bg-surface-card px-3 py-2">
                        <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-feedback-danger" />
                        <span className="min-w-0 flex-1 truncate text-sm font-medium text-content-primary">{task.title}</span>
                        <span className="shrink-0 text-xs font-semibold tabular-nums text-feedback-danger-foreground">{t('units.daysCompact', { count: formatNumber(task.effort_days || 0) })}</span>
                    </li>
                ))}
                {tasks.length > 5 && (
                    <li className="pt-1 text-center text-xs text-content-secondary">{t('overview.moreTasks', { count: tasks.length - 5 })}</li>
                )}
            </ul>
        </SectionCard>
    );
};

const IterationTasksCard = ({
    tasks,
    filter,
    onFilter,
    isProjectScoped,
}: {
    tasks: Task[];
    filter: TaskFilter;
    onFilter: (value: TaskFilter) => void;
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
                <Link to="/tasks" className="inline-flex items-center gap-1 text-sm font-medium text-action hover:text-action">
                    {t('overview.openTaskBoard')}
                    <ArrowRight className="h-4 w-4" />
                </Link>
            )}
        >
            <div className="mb-4 flex flex-wrap items-center gap-2">
                {filters.map(item => (
                    <button
                        key={item.id}
                        type="button"
                        onClick={() => onFilter(item.id)}
                        className={clsx(
                            'inline-flex h-8 items-center gap-1.5 rounded-full px-3 text-xs font-semibold transition-colors',
                            filter === item.id
                                ? 'bg-content-primary text-content-emphasis'
                                : 'bg-surface-subtle text-content-primary hover:bg-surface-hover',
                        )}
                    >
                        <span>{item.label}</span>
                        <span className={clsx('rounded-full px-1.5 text-[10.5px] tabular-nums', filter === item.id ? 'bg-content-emphasis/15 text-content-emphasis' : 'bg-surface-card text-content-secondary')}>
                            {item.count}
                        </span>
                    </button>
                ))}
            </div>

            {visibleTasks.length === 0 ? (
                <InlineEmptyState action={<Button variant="outline" size="sm" onClick={() => onFilter('all')}>{t('actions.clear')}</Button>}>
                    {t('overview.noTasksForFilter')}
                </InlineEmptyState>
            ) : (
                <div className="space-y-4">
                    {Object.entries(groups).map(([groupName, items]) => (
                        <div key={groupName}>
                            {isProjectScoped && (
                                <div className="mb-2 flex items-center gap-2 px-1 text-[11px] font-semibold uppercase tracking-wide text-content-secondary">
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
            <span className="h-1.5 w-1.5 shrink-0 rounded-full" style={dotStyle(tone)} title={status} />
            <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-medium text-content-primary">{task.title}</div>
                {showProject && task.project && (
                    <div className="mt-0.5 truncate text-xs text-content-secondary">{task.project.name}</div>
                )}
            </div>
            {task.is_overdue && (
                <span className="inline-flex h-5 shrink-0 items-center gap-1 rounded bg-feedback-danger-muted px-1.5 text-[11px] font-semibold text-feedback-danger-foreground">
                    <Clock className="h-3 w-3" />
                    {t('taskList.overdue')}
                </span>
            )}
            <span className="w-10 shrink-0 text-right text-xs tabular-nums text-content-secondary">{t('units.daysCompact', { count: formatNumber(task.effort_days || 0) })}</span>
            {task.assignee ? (
                <span title={task.assignee.name} className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-status-active-muted text-[10px] font-bold text-action">
                    {initialsFor(task.assignee.name)}
                </span>
            ) : (
                <span title={t('common.unassigned')} className="grid h-7 w-7 shrink-0 place-items-center rounded-full border border-dashed border-border-strong bg-surface-card text-content-tertiary">
                    <User className="h-3.5 w-3.5" />
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
                <div className="mt-1 flex items-center justify-between text-[11px] text-content-secondary">
                    <span className="tabular-nums">{!isLoadingWorkload && workload ? t('overview.allocatedCapacity', { allocated: formatNumber(allocated), capacity: formatNumber(capacity) }) : t('common.loading')}</span>
                    <span>{t('overview.taskCount', { count: member.taskCount })}</span>
                </div>
            </div>
            <span className="grid h-6 shrink-0 place-items-center rounded-md px-2 text-[11px] font-bold tabular-nums" style={pillBoxStyle(tone)}>
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
                                        <div className="text-[11px] font-semibold uppercase text-content-secondary">{t(`statuses.${segment.status}`)}</div>
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
                <div className="mt-1 flex justify-between text-[11px] tabular-nums text-content-tertiary">
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

const NeedsAttentionCard = ({ items }: { items: AttentionItem[] }) => {
    const { t } = useTranslation();

    return (
        <SectionCard
            icon={<AlertTriangle className="h-5 w-5 text-action" />}
            title={t('overview.needsAttention')}
            count={<span className={clsx('rounded-full px-2 py-0.5 text-xs font-semibold tabular-nums', items.length > 0 ? 'bg-feedback-danger-muted text-feedback-danger-foreground' : 'bg-feedback-success-muted text-feedback-success-foreground')}>{items.length}</span>}
        >
            {items.length === 0 ? (
                <div className="inline-flex items-center gap-1.5 text-sm font-medium text-feedback-success-foreground">
                    <CheckCircle2 className="h-4 w-4" />
                    {t('overview.attention.clear')}
                </div>
            ) : (
                <ul className="space-y-2">
                    {items.map(item => {
                        const Icon = item.icon;
                        return (
                            <li key={item.id} className="flex min-w-0 items-center gap-2.5 rounded-md px-2 py-1.5 hover:bg-surface-hover">
                                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-md" style={pillBoxStyle(item.tone)}>
                                    <Icon className="h-4 w-4" />
                                </span>
                                <div className="min-w-0 flex-1">
                                    <div className="truncate text-sm font-semibold text-content-primary">{item.title}</div>
                                    <div className="truncate text-xs text-content-secondary">{item.meta}</div>
                                </div>
                            </li>
                        );
                    })}
                </ul>
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
            <div className="absolute inset-0 grid place-items-center text-[11px] font-bold tabular-nums text-content-primary">
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

const InlineEmptyState = ({
    children,
    action,
}: {
    children: ReactNode;
    action?: ReactNode;
}) => (
    <div className="flex items-center justify-between gap-3 rounded-lg border border-dashed border-border bg-surface-muted/70 px-4 py-3">
        <p className="text-sm text-content-secondary">{children}</p>
        {action}
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
