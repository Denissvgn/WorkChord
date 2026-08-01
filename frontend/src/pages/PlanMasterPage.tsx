import { useState } from 'react';
import type { ReactNode, CSSProperties } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import i18n from '../i18n/i18n';
import { localizeStatus, STEP_DEFS, nextStep } from '../features/planningMasters/masters';
import type { PlanReadiness, StepStatus } from '../features/planningMasters/masters';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import { IterationForm } from '../components/iteration/IterationForm';
import { TeamForm } from '../components/team/TeamForm';
import { ImportTeamModal } from '../components/team/ImportTeamModal';
import { SlideOverDrawer } from '../components/ui';
import type { Iteration } from '../types/iteration';
import type { Task } from '../types/task';
import { formatDate } from '../utils/formatDate';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';

const tr = i18n.t.bind(i18n);

// ── Icon helpers ─────────────────────────────────────────────────────────────
const Svg = ({ d, size = 14, stroke = 1.75, ...rest }: { d: ReactNode; size?: number; stroke?: number; style?: CSSProperties; className?: string }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" {...rest}>
        {d}
    </svg>
);
type IconProps = { size?: number; stroke?: number; style?: CSSProperties; className?: string };
const ICheck     = (p: IconProps) => <Svg {...p} d={<polyline points="20 6 9 17 4 12"/>}/>;
const ILock      = (p: IconProps) => <Svg {...p} d={<><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></>}/>;
const IArrow     = (p: IconProps) => <Svg {...p} d={<><path d="M5 12h14M13 5l7 7-7 7"/></>}/>;
const IArrowL    = (p: IconProps) => <Svg {...p} d={<><path d="M19 12H5M11 5l-7 7 7 7"/></>}/>;
const IChevR     = (p: IconProps) => <Svg {...p} d={<polyline points="9 6 15 12 9 18"/>}/>;
const IOpen      = (p: IconProps) => <Svg {...p} d={<><path d="M14 3h7v7"/><path d="M10 14L21 3"/><path d="M21 14v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5"/></>}/>;
const ISkip      = (p: IconProps) => <Svg {...p} d={<><polyline points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></>}/>;
const IInfo      = (p: IconProps) => <Svg {...p} d={<><circle cx="12" cy="12" r="9"/><path d="M12 8v.01M11 12h1v4h1"/></>}/>;
const ICalendar  = (p: IconProps) => <Svg {...p} d={<><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/></>}/>;
const IIteration = (p: IconProps) => <Svg {...p} d={<><path d="M2 12a10 10 0 0 1 17-7"/><path d="M22 12a10 10 0 0 1-17 7"/><path d="M19 2v5h-5M5 22v-5h5"/></>}/>;
const ITeam      = (p: IconProps) => <Svg {...p} d={<><circle cx="9" cy="8" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M3 20c.5-3.5 3-5 6-5s5.5 1.5 6 5"/><path d="M14.5 20c.3-2 1.7-3 3.5-3s3.2 1 3.5 3"/></>}/>;
const ITasks     = (p: IconProps) => <Svg {...p} d={<><path d="M9 11l3 3 8-8"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></>}/>;
const IGantt     = (p: IconProps) => <Svg {...p} d={<><rect x="3" y="5" width="9" height="3" rx="1"/><rect x="7" y="11" width="11" height="3" rx="1"/><rect x="5" y="17" width="7" height="3" rx="1"/></>}/>;
const IWarning   = (p: IconProps) => <Svg {...p} d={<><path d="M12 2L1 21h22z"/><path d="M12 9v5M12 18v.5"/></>}/>;
const IPlus      = (p: IconProps) => <Svg {...p} d={<><path d="M12 5v14M5 12h14"/></>}/>;
const IRefresh   = (p: IconProps) => <Svg {...p} d={<><path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/></>}/>;
const IInbox     = (p: IconProps) => <Svg {...p} d={<><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 6h13l3.5 6v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6z"/></>}/>;
const ISparkle   = (p: IconProps) => <Svg {...p} d={<><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></>}/>;

type TeamWorkflow = 'assign' | 'import';

const avatarTones: CSSProperties[] = [
    { background: 'rgb(var(--color-feedback-warning))', color: 'rgb(var(--color-feedback-warning-on-solid))' },
    { background: 'rgb(var(--color-feedback-info))', color: 'rgb(var(--color-feedback-info-on-solid))' },
    { background: 'rgb(var(--color-feedback-purple))', color: 'rgb(var(--color-feedback-purple-on-solid))' },
    { background: 'rgb(var(--color-feedback-success))', color: 'rgb(var(--color-feedback-success-on-solid))' },
    { background: 'rgb(var(--color-feedback-danger))', color: 'rgb(var(--color-feedback-danger-on-solid))' },
    { background: 'rgb(var(--color-feedback-indigo))', color: 'rgb(var(--color-feedback-indigo-on-solid))' },
];

const avatarStyle = (id: string | number) => {
    const h = String(id).split('').reduce((a,c)=>a+c.charCodeAt(0),0);
    return avatarTones[h % avatarTones.length];
};

type FormMode = 'create' | 'edit' | 'select';

const formatIterationDates = (startDate: string, endDate: string) => (
    startDate && endDate ? `${formatDate(startDate, i18n.language)} - ${formatDate(endDate, i18n.language)}` : ''
);

// ── Step state pills ─────────────────────────────────────────────────────────
function StepPill({ state }: { state: string }) {
    if (state === 'done')    return <span className="pill done sm"><ICheck size={9} stroke={3}/></span>;
    if (state === 'warn')    return <span className="pill warn sm"><span className="pdot"/></span>;
    if (state === 'blocked') return <span className="pill blocked sm"><span className="pdot"/></span>;
    return <span className="pill opt sm"><span className="pdot"/></span>;
}
function StepStatePill({ state }: { state: string }) {
    if (state === 'done')    return <span className="pill done"><span className="pdot"/>{tr('plan.master.done')}</span>;
    if (state === 'warn')    return <span className="pill warn"><span className="pdot"/>{tr('plan.master.needsAttention')}</span>;
    if (state === 'blocked') return <span className="pill blocked"><span className="pdot"/>{tr('plan.master.blocked')}</span>;
    return <span className="pill opt"><span className="pdot"/>{tr('plan.master.notStarted')}</span>;
}

// ── Empty state ───────────────────────────────────────────────────────────────
function EmptyState({
    icon,
    title,
    msg,
    primary,
    secondary,
    primaryTo,
    secondaryTo,
    onPrimary,
    onSecondary,
}: {
    icon: ReactNode;
    title: string;
    msg: string;
    primary?: string;
    secondary?: string;
    primaryTo?: string;
    secondaryTo?: string;
    onPrimary?: () => void;
    onSecondary?: () => void;
}) {
    const renderAction = (label: string | undefined, className: string, to?: string, onClick?: () => void) => {
        if (!label || (!to && !onClick)) return null;
        return to
            ? <Link to={to} className={className}>{label}</Link>
            : <button type="button" className={className} onClick={onClick}>{label}</button>;
    };
    const primaryAction = renderAction(primary, 'btn primary', primaryTo, onPrimary);
    const secondaryAction = renderAction(secondary, 'btn', secondaryTo, onSecondary);

    return (
        <div className="empty">
            <div className="empty-icon">{icon}</div>
            <h4>{title}</h4>
            <p>{msg}</p>
            {(primaryAction || secondaryAction) && <div className="empty-actions">
                {primaryAction}
                {secondaryAction}
            </div>}
        </div>
    );
}

function ActionGuidance({
    icon = <IInfo size={14}/>,
    title,
    body,
    action,
    to,
}: {
    icon?: ReactNode;
    title: string;
    body: string;
    action?: string;
    to?: string;
}) {
    return (
        <div className="action-guidance" role="note">
            <span className="action-guidance-icon" aria-hidden="true">{icon}</span>
            <div className="action-guidance-copy">
                <div className="action-guidance-title">{title}</div>
                <div className="action-guidance-body">{body}</div>
            </div>
            {action && to && <Link to={to} className="btn sm ghost"><IOpen size={11}/>{action}</Link>}
        </div>
    );
}

// ── Step bodies ───────────────────────────────────────────────────────────────
function BodyIteration({
    r,
    iterations,
    currentIteration,
    selectIteration,
}: {
    r: PlanReadiness;
    iterations: Iteration[];
    currentIteration: Iteration | null;
    selectIteration: (id: number) => void;
}) {
    const [mode, setMode] = useState<FormMode>(currentIteration ? 'edit' : 'create');
    const [existingId, setExistingId] = useState(currentIteration?.id ?? iterations[0]?.id ?? 0);

    const resetCreateDraft = () => {
        setMode('create');
    };

    const handleSaved = (iteration?: Iteration) => {
        if (iteration) {
            selectIteration(iteration.id);
            setExistingId(iteration.id);
        }
        setMode('edit');
    };

    return (
        <>
            <div className="data-row">
                <div style={{color: r.hasCurrentIteration ? 'var(--done)' : 'var(--ink-3)'}}>
                    {r.hasCurrentIteration ? <ICheck size={14} stroke={3}/> : <IIteration size={14}/>}
                </div>
                <div>
                    <div className="dr-title">{r.currentIterationName || tr('plan.master.noPeriodYet')}</div>
                    <div className="dr-sub">
                        {r.hasCurrentIteration
                            ? tr('plan.master.periodSummary', { dates: formatIterationDates(r.currentIterationStart, r.currentIterationEnd), days: r.currentIterationDays })
                            : tr('plan.master.pickDateRange')}
                    </div>
                </div>
                <div className="period-row-actions">
                    <button type="button" className="btn sm" onClick={() => currentIteration ? setMode('edit') : resetCreateDraft()}>
                        {currentIteration ? tr('plan.master.edit') : tr('plan.master.create')}
                    </button>
                    {iterations.length > 0 && (
                        <button type="button" className="btn sm ghost" onClick={() => setMode('select')}>
                            {tr('plan.master.useExisting')}
                        </button>
                    )}
                    {currentIteration && (
                        <button type="button" className="btn sm ghost" onClick={resetCreateDraft}>
                            {tr('plan.master.newPeriod')}
                        </button>
                    )}
                </div>
            </div>

            {mode === 'select' ? (
                <div className="card card-pad">
                    <div className="field" style={{marginBottom:12}}>
                        <div className="field-lbl">{tr('plan.master.existingPeriod')}</div>
                        <select
                            className="input"
                            value={existingId || ''}
                            onChange={(event) => setExistingId(Number(event.target.value))}
                        >
                            {iterations.map(iteration => (
                                <option key={iteration.id} value={iteration.id}>
                                    {iteration.name} · {formatIterationDates(iteration.start_date, iteration.end_date)}
                                </option>
                            ))}
                        </select>
                        <div className="field-hint">{tr('plan.master.switchPeriodHelp')}</div>
                    </div>
                    <div className="row" style={{justifyContent:'flex-end'}}>
                        <button type="button" className="btn" onClick={() => setMode(currentIteration ? 'edit' : 'create')}>{tr('actions.cancel')}</button>
                        <button
                            type="button"
                            className="btn primary"
                            disabled={!existingId}
                            onClick={() => {
                                if (!existingId) return;
                                selectIteration(existingId);
                                setMode('edit');
                            }}
                        >
                            {tr('plan.master.useSelectedPeriod')}
                        </button>
                    </div>
                </div>
            ) : (
                <div id="planning-period-form" className="card planning-period-form">
                    <div className="card-head">
                        <h3>{mode === 'edit' ? tr('plan.master.periodDetails') : tr('plan.master.newPlanningPeriod')}</h3>
                        <span className="sub">{tr('plan.master.savedAsIterations')}</span>
                    </div>
                    <div className="planning-period-editor">
                        <IterationForm
                            key={mode === 'edit' ? currentIteration?.id ?? 'edit' : 'create'}
                            initialData={mode === 'edit' ? currentIteration ?? undefined : undefined}
                            hideProjectScope
                            onSuccess={handleSaved}
                            onCancel={() => setMode(currentIteration ? 'edit' : 'create')}
                        />
                        {iterations.length > 0 && (
                            <button type="button" className="btn" onClick={() => setMode('select')}>
                                {tr('plan.master.useExistingIteration')}
                            </button>
                        )}
                    </div>
                </div>
            )}
        </>
    );
}

function BodyTeam({
    r,
    teamMembers,
    currentIteration,
    onStartWorkflow,
    onOpenIteration,
}: {
    r: PlanReadiness;
    teamMembers: unknown[];
    currentIteration: Iteration | null;
    onStartWorkflow: (workflow: TeamWorkflow) => void;
    onOpenIteration: () => void;
}) {
    const hasIteration = currentIteration !== null;
    const openAssign = () => onStartWorkflow('assign');
    const openImport = () => onStartWorkflow('import');

    if (!hasIteration) {
        return <EmptyState
            icon={<ITeam size={16}/>}
            title={tr('plan.master.createPeriodFirst')}
            msg={tr('plan.master.teamNeedsPeriod')}
            primary={tr('plan.master.goToPlanningPeriod')}
            onPrimary={onOpenIteration}
        />;
    }

    if (r.teamMemberCount === 0) {
        return (
            <>
                <div className="row" style={{gap:8}}>
                    <button type="button" className="btn" onClick={openAssign}>
                        <IPlus size={12}/> {tr('plan.master.addPerson')}
                    </button>
                    <button type="button" className="btn" onClick={openImport}>
                        <IRefresh size={12}/> {tr('plan.master.importPrevious')}
                    </button>
                </div>
                <EmptyState
                    icon={<ITeam size={16}/>}
                    title={tr('plan.master.noTeamCapacity')}
                    msg={tr('plan.master.addPeopleBeforeSchedule')}
                    primary={tr('plan.master.addPeople')}
                    secondary={tr('plan.master.importPrevious')}
                    onPrimary={openAssign}
                    onSecondary={openImport}
                />
            </>
        );
    }
    type TM = { id: string; name: string; position?: string; cap?: number; planned?: number | null };
    const members = teamMembers as TM[];
    return (
        <>
            <div className="row" style={{gap:8}}>
                <button type="button" className="btn" onClick={openAssign}>
                    <IPlus size={12}/> {tr('plan.master.addPerson')}
                </button>
                <button type="button" className="btn" onClick={openImport}>
                    <IRefresh size={12}/> {tr('plan.master.importPrevious')}
                </button>
            </div>
            <div className="card" style={{padding:0}}>
                <table className="table">
                    <thead>
                        <tr><th>{tr('plan.master.person')}</th><th>{tr('plan.master.role')}</th><th style={{width:90}}>{tr('plan.master.capacity')}</th><th style={{width:200}}>{tr('plan.master.plannedLoad')}</th></tr>
                    </thead>
                    <tbody>
                        {members.map(p => {
                            const planned = p.planned ?? 0;
                            const cap = p.cap ?? 0;
                            const pct = cap > 0 ? Math.min(120, Math.round((Number(planned) / cap) * 100)) : 0;
                            const over = Number(planned) > cap;
                            const noLoad = p.planned === null || p.planned === undefined;
                            return (
                                <tr key={p.id}>
                                    <td>
                                        <div className="who">
                                            <span className="avatar" style={{...avatarStyle(p.id), width:20, height:20, fontSize:10}}>
                                                {(p.name||'?').split(' ').map((w:string)=>w[0]).join('')}
                                            </span>
                                            <span style={{fontWeight:500}}>{p.name}</span>
                                        </div>
                                    </td>
                                    <td className="muted">{p.position || '—'}</td>
                                    <td className="tnum">{cap}h</td>
                                    <td>
                                        {noLoad ? (
                                            <span className="pill warn"><span className="pdot"/>{tr('plan.master.notSet')}</span>
                                        ) : (
                                            <div className="row" style={{gap:8}}>
                                                <div className="cap-bar" style={{flex:1}}>
                                                    <i className={over ? 'over' : pct > 90 ? 'warn' : ''} style={{width:`${pct}%`}}/>
                                                </div>
                                                <span className="tnum muted" style={{fontSize:11}}>{planned}/{cap}h</span>
                                            </div>
                                        )}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </>
    );
}

function BodyWork({ r, tasks }: { r: PlanReadiness; tasks: Task[] }) {
    const [filter, setFilter] = useState<'all'|'noOwner'|'noEffort'>('all');
    const createTaskTo = '/tasks?create=1';
    const visible = filter === 'noOwner' ? tasks.filter(t => !t.assignee)
                  : filter === 'noEffort' ? tasks.filter(t => !t.effort_days)
                  : tasks;

    if (r.taskCount === 0) {
        return (
            <>
                <div className="row" style={{justifyContent:'flex-end', gap:8}}>
                    <Link to="/triage" className="btn"><IInbox size={12}/> {tr('plan.master.pullFromIntake')}</Link>
                    <Link to={createTaskTo} className="btn primary"><IPlus size={12}/> {tr('plan.master.addTask')}</Link>
                </div>
                <EmptyState
                    icon={<ITasks size={16}/>}
                    title={tr('plan.master.noTasks')}
                    msg={tr('plan.master.bringInWork')}
                    primary={tr('plan.master.addTasks')}
                    secondary={tr('plan.master.pullFromIntake')}
                    primaryTo={createTaskTo}
                    secondaryTo="/triage"
                />
            </>
        );
    }

    return (
        <>
            <div className="row" style={{justifyContent:'space-between', flexWrap:'wrap', gap:8}}>
                <div className="seg">
                    <button aria-pressed={filter === 'all'} onClick={() => setFilter('all')}>{tr('plan.master.allCount', { count: r.taskCount })}</button>
                    <button aria-pressed={filter === 'noOwner'} onClick={() => setFilter('noOwner')}>{tr('plan.master.unassignedCount', { count: r.tasksWithoutAssignee })}</button>
                    <button aria-pressed={filter === 'noEffort'} onClick={() => setFilter('noEffort')}>{tr('plan.master.missingEffortCount', { count: r.tasksWithoutEffort })}</button>
                </div>
                <div className="row" style={{gap:8}}>
                    <Link to="/triage" className="btn"><IInbox size={12}/> {tr('plan.master.pullFromIntake')}</Link>
                    <Link to={createTaskTo} className="btn primary"><IPlus size={12}/> {tr('plan.master.addTask')}</Link>
                </div>
            </div>

            <div className="card" style={{padding:0}}>
                <table className="table">
                    <thead>
                        <tr><th style={{width:24}} aria-label={tr('plan.master.readiness')} /><th>{tr('plan.master.task')}</th><th style={{width:150}}>{tr('plan.master.project')}</th><th style={{width:150}}>{tr('plan.master.assignee')}</th><th style={{width:90}}>{tr('plan.master.effort')}</th></tr>
                    </thead>
                    <tbody>
                        {visible.slice(0,20).map(t => {
                            const issues: string[] = [];
                            if (!t.assignee) issues.push('owner');
                            if (!t.effort_days) issues.push('effort');
                            return (
                                <tr key={t.id}>
                                    <td>
                                        {issues.length
                                            ? <IWarning size={13} style={{color:'var(--warn)'}}/>
                                            : <ICheck size={13} stroke={3} style={{color:'var(--done)'}}/>}
                                    </td>
                                    <td>
                                        <div style={{fontWeight:500}}>{t.title}</div>
                                        {issues.length > 0 && (
                                            <div className="muted" style={{fontSize:11, marginTop:2}}>{tr('plan.master.missingFields', { fields: issues.join(', ') })}</div>
                                        )}
                                    </td>
                                    <td className="muted">{(t as { project?: { name?: string } }).project?.name || '—'}</td>
                                    <td>
                                        {t.assignee
                                            ? <div className="who">
                                                <span className="avatar" style={{...avatarStyle(t.assignee.id),width:20,height:20,fontSize:10}}>
                                                    {t.assignee.name.split(' ').map(w=>w[0]).join('')}
                                                </span>
                                                {t.assignee.name}
                                              </div>
                                            : <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>}
                                    </td>
                                    <td>
                                        {t.effort_days
                                            ? <span className="tnum">{t.effort_days}d</span>
                                            : <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </>
    );
}

function BodyBlockers({ tasks, st }: { tasks: Task[]; st: StepStatus }) {
    if (st.state === 'done') {
        return (
            <div className="banner done">
                <ICheck size={14}/><div>{tr('plan.master.readyToBuild')}</div>
            </div>
        );
    }
    if (st.state === 'blocked') {
        return <EmptyState icon={<ILock size={16}/>} title={tr('plan.master.addWorkFirst')} msg={tr('plan.master.blockersNeedTasks')} primary={tr('plan.master.addTasks')} primaryTo="/tasks?create=1"/>;
    }

    const noOwner  = tasks.filter(t => !t.assignee);
    const noEffort = tasks.filter(t => !t.effort_days);

    return (
        <>
            <div className="row" style={{gap:8}}>
                <Link to="/tasks" className="btn primary"><ITasks size={12}/> {tr('plan.steps.blockers.primaryAction')}</Link>
            </div>
            <ActionGuidance
                icon={<ILock size={14}/>}
                title={tr('plan.master.moveUnavailableTitle')}
                body={tr('plan.master.moveUnavailableBody')}
            />

            {noOwner.length > 0 && (
                <div className="card" style={{padding:0}}>
                    <div className="card-head"><h3>{tr('plan.master.unassignedCount', { count: noOwner.length })}</h3><span className="sub">{tr('plan.master.schedulerSkipsUnassigned')}</span></div>
                    {noOwner.map(t => (
                        <div key={t.id} className="cap-row" style={{gridTemplateColumns:'16px 1fr auto'}}>
                            <IWarning size={13} style={{color:'var(--warn)'}}/>
                            <div>
                                <div style={{fontWeight:500}}>{t.title}</div>
                                <div className="muted" style={{fontSize:11}}>{t.effort_days ? tr('units.daysCompact', { count: t.effort_days }) : tr('plan.master.noEffort')}</div>
                            </div>
                            <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>
                        </div>
                    ))}
                </div>
            )}

            {noEffort.length > 0 && (
                <div className="card" style={{padding:0}}>
                    <div className="card-head"><h3>{tr('plan.master.missingEffortCount', { count: noEffort.length })}</h3><span className="sub">{tr('plan.master.schedulerNeedsEstimate')}</span></div>
                    {noEffort.map(t => (
                        <div key={t.id} className="cap-row" style={{gridTemplateColumns:'16px 1fr auto'}}>
                            <IWarning size={13} style={{color:'var(--warn)'}}/>
                            <div>
                                <div style={{fontWeight:500}}>{t.title}</div>
                                <div className="muted" style={{fontSize:11}}>{t.assignee?.name || tr('common.unassigned')}</div>
                            </div>
                            <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>
                        </div>
                    ))}
                </div>
            )}
        </>
    );
}

function BodySchedule({ r, tasks, st, onOpenFirstIncomplete }: { r: PlanReadiness; tasks: Task[]; st: StepStatus; onOpenFirstIncomplete: () => void }) {
    const days = 14;
    const ganttTasks = tasks.slice(0, 7).map((t, i) => ({
        ...t,
        ganttStart: (i * 1.4) % 12,
        ganttSpan: t.effort_days ? Math.max(1, Math.min(4, t.effort_days)) : 2,
    }));

    if (st.state === 'blocked') {
        return <EmptyState icon={<ILock size={16}/>} title={tr('plan.master.earlierStepsNeedAttention')} msg={tr('plan.master.schedulerPrerequisites')} primary={tr('plan.master.backFirstIncomplete')} onPrimary={onOpenFirstIncomplete}/>;
    }

    return (
        <>
            <ActionGuidance
                icon={<IGantt size={14}/>}
                title={tr('plan.master.schedulingToolsTitle')}
                body={tr('plan.master.schedulingToolsBody')}
                action={tr('plan.master.openFullSchedule')}
                to="/gantt"
            />

            <div className="banner accent">
                <ISparkle size={14}/>
                <div>
                    {tr('plan.master.scheduleExplanation')}
                </div>
            </div>

            <div className="card" style={{padding:0}}>
                <div className="card-head">
                    <h3>{st.state === 'done' ? tr('plan.master.currentSchedule') : tr('plan.master.schedulePreview')}</h3>
                    <span className="sub">{r.currentIterationName}</span>
                </div>
                <div style={{padding:14}}>
                    <div className="gantt">
                        <div className="gantt-head">
                            <div className="gh-cell">{tr('plan.master.task')}</div>
                            <div className="gh-cell" style={{display:'grid', gridTemplateColumns:`repeat(${days}, 1fr)`, padding:0}}>
                                {Array.from({length:days}, (_, i) => (
                                    <div key={i} style={{
                                        padding:'8px 0', textAlign:'center', fontSize:10.5, color:'var(--ink-4)',
                                        background:(i%7===5||i%7===6)?'var(--panel-3)':'var(--panel-2)',
                                        borderRight:'1px solid var(--border)',
                                    }}>{i+2}</div>
                                ))}
                            </div>
                        </div>
                        {ganttTasks.map(t => (
                            <div key={t.id} className="gantt-row">
                                <div className="gr-cell" style={{display:'flex', alignItems:'center', gap:8}}>
                                    <span className="avatar" style={{...avatarStyle(t.assignee?.id||t.id),width:18,height:18,fontSize:9}}>
                                        {(t.assignee?.name || '??').split(' ').map(w=>w[0]).join('')}
                                    </span>
                                    <span style={{fontSize:11.5, overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap'}}>{t.title}</span>
                                </div>
                                <div className="gr-cell bar-cell">
                                    <div className="bar-track">
                                        <div className={`bar ${!t.assignee || !t.effort_days ? 'warn' : ''}`}
                                             style={{
                                                 left:`calc(${t.ganttStart} / ${days} * 100%)`,
                                                 width:`calc(${t.ganttSpan} / ${days} * 100%)`,
                                             }}>
                                            {t.title.length > 14 ? t.title.slice(0,14)+'…' : t.title}
                                        </div>
                                        <div className="today-line" style={{left:`calc(3 / ${days} * 100%)`}}/>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    {ganttTasks.length === 0 && <div className="muted" style={{padding:'12px 0', fontSize:12}}>{tr('plan.master.addTasksForPreview')}</div>}
                </div>
            </div>
        </>
    );
}

function BodyReview({ r, tasks, teamMembers }: { r: PlanReadiness; tasks: Task[]; teamMembers: unknown[] }) {
    if (!r.hasGanttSchedule) {
        return <EmptyState icon={<ILock size={16}/>} title={tr('plan.master.buildScheduleFirst')} msg={tr('plan.master.reviewNeedsSchedule')} primary={tr('plan.master.openSchedule')} primaryTo="/gantt"/>;
    }

    type TM = { id: string; name: string; cap?: number; planned?: number | null; position?: string };
    const members = teamMembers as TM[];
    const totalPlanned = members.reduce((a, p) => a + Number(p.planned || 0), 0);
    const totalCap     = members.reduce((a, p) => a + (p.cap || 0), 0);
    const tasksByOwner: Record<string, number> = {};
    tasks.forEach(t => { if (t.assignee?.name) tasksByOwner[t.assignee.name] = (tasksByOwner[t.assignee.name] || 0) + 1; });

    return (
        <>
            <ActionGuidance
                icon={<IGantt size={14}/>}
                title={tr('plan.master.sharingUnavailableTitle')}
                body={tr('plan.master.sharingUnavailableBody')}
                action={tr('plan.master.openSchedule')}
                to="/gantt"
            />

            <div className="kpi-grid">
                <div className="kpi">
                    <div className="kpi-lbl">{tr('plan.master.tasks')}</div>
                    <div className="kpi-val tnum">{tasks.length}</div>
                    <div className="kpi-foot muted">{tr('plan.master.inPlanningPeriod')}</div>
                </div>
                <div className="kpi">
                    <div className="kpi-lbl">{tr('plan.master.capacityUsed')}</div>
                    <div className="kpi-val tnum">
                        {totalCap > 0 ? Math.round(totalPlanned/totalCap*100) : 0}<span className="unit">%</span>
                    </div>
                    <div className="kpi-foot muted">{tr('plan.master.capacityPlanned', { planned: totalPlanned, capacity: totalCap })}</div>
                </div>
                <div className="kpi">
                    <div className="kpi-lbl">{tr('plan.master.risks')}</div>
                    <div className="kpi-val tnum">{r.riskCount || 0}</div>
                    <div className="kpi-foot muted">{r.riskCount === 0 ? tr('plan.hub.noActiveSignals') : tr('plan.master.overdueTasks')}</div>
                </div>
                <div className="kpi">
                    <div className="kpi-lbl">{tr('plan.master.schedule')}</div>
                    <div className="kpi-val" style={{fontSize:14, lineHeight:1.3}}>{tr('plan.master.built')}</div>
                    <div className="kpi-foot muted">{tr('plan.master.autoRebuilt')}</div>
                </div>
            </div>

            {members.length > 0 && (
                <div className="card" style={{padding:0}}>
                    <div className="card-head"><h3>{tr('plan.master.loadByPerson')}</h3><span className="sub">{r.currentIterationName}</span></div>
                    {members.map(p => {
                        const planned = Number(p.planned || 0);
                        const cap = p.cap || 0;
                        const pct = cap > 0 ? Math.min(120, Math.round((planned/cap)*100)) : 0;
                        return (
                            <div key={p.id} className="cap-row">
                                <span className="avatar" style={{...avatarStyle(p.id),width:22,height:22,fontSize:10}}>
                                    {(p.name||'?').split(' ').map((w:string)=>w[0]).join('')}
                                </span>
                                <div>
                                    <div style={{fontWeight:500}}>{p.name}</div>
                                    <div className="muted" style={{fontSize:11}}>{p.position || ''} · {tr('plan.master.taskCount', { count: tasksByOwner[p.name] || 0 })}</div>
                                </div>
                                <div className="cap-bar">
                                    <i className={planned>cap?'over':pct>90?'warn':''} style={{width:`${pct}%`}}/>
                                </div>
                                <div className="cap-value">{planned}/{cap}h</div>
                            </div>
                        );
                    })}
                </div>
            )}

            <div className="banner done">
                <ICheck size={14}/>
                <div>{tr('plan.master.readyToShareSnapshot')}</div>
            </div>
        </>
    );
}

// ── Step body dispatcher ──────────────────────────────────────────────────────
function StepBody({
    stepId,
    status,
    r,
    tasks,
    teamMembers,
    setActive,
    iterations,
    currentIteration,
    selectIteration,
    onStartTeamWorkflow,
}: {
    stepId: string; status: Record<string, StepStatus>; r: PlanReadiness;
    tasks: Task[]; teamMembers: unknown[]; setActive: (id: string) => void;
    iterations: Iteration[]; currentIteration: Iteration | null; selectIteration: (id: number) => void;
    onStartTeamWorkflow: (workflow: TeamWorkflow) => void;
}) {
    const def = STEP_DEFS.find(s => s.id === stepId)!;
    const st  = status[stepId];
    const idx = STEP_DEFS.findIndex(d => d.id === stepId);
    const isIterationStep = stepId === 'iteration';
    const isTeamStep = stepId === 'team';
    const hasCurrentIteration = currentIteration !== null;
    const expertRoute = def.route;
    const secondaryRoute = def.secondaryRoute ?? def.route;

    const startTeamWorkflow = (workflow: TeamWorkflow) => {
        if (!hasCurrentIteration) return;
        onStartTeamWorkflow(workflow);
    };

    return (
        <div className="step-body">
            {/* Header */}
            <div>
                <div className="row" style={{gap:10, marginBottom:8}}>
                    <span className="pill"><span className="pdot"/>{tr('plan.master.stepOf', { step: idx + 1, total: STEP_DEFS.length })}</span>
                    <StepStatePill state={st.state}/>
                    <Link to={expertRoute} className="btn sm ghost" style={{marginLeft:'auto'}}>
                        <IOpen size={11}/> {tr(`plan.steps.${def.id}.expert`)}
                    </Link>
                </div>
                <div className="step-h">
                    <div>
                        <h2>{tr(`plan.steps.${def.id}.title`)}</h2>
                        <p>{tr(`plan.steps.${def.id}.description`)}</p>
                    </div>
                </div>
            </div>

            {/* Why callout */}
            <div className="why">
                <div className="why-icon"><IInfo size={14}/></div>
                <div>
                    <div style={{color:'var(--ink)', fontWeight:500, marginBottom:2, fontSize:12.5}}>{tr('plan.master.whyThisStep')}</div>
                    {tr(`plan.steps.${def.id}.why`)}
                </div>
            </div>

            {/* Step-specific body */}
            {stepId === 'iteration' && (
                <BodyIteration
                    r={r}
                    iterations={iterations}
                    currentIteration={currentIteration}
                    selectIteration={selectIteration}
                />
            )}
            {stepId === 'team'      && (
                <BodyTeam
                    r={r}
                    teamMembers={teamMembers}
                    currentIteration={currentIteration}
                    onStartWorkflow={onStartTeamWorkflow}
                    onOpenIteration={() => setActive('iteration')}
                />
            )}
            {stepId === 'work'      && <BodyWork r={r} tasks={tasks}/>}
            {stepId === 'blockers'  && <BodyBlockers tasks={tasks} st={st}/>}
            {stepId === 'schedule'  && <BodySchedule r={r} tasks={tasks} st={st} onOpenFirstIncomplete={() => setActive(nextStep(status))}/>}
            {stepId === 'review'    && <BodyReview r={r} tasks={tasks} teamMembers={teamMembers}/>}

            {/* Footer nav */}
            <div className="divider"/>
            <div className="between">
                <div className="row" style={{gap:8}}>
                    <button className="btn" disabled={idx === 0}
                            onClick={() => { if (idx > 0) setActive(STEP_DEFS[idx-1].id); }}>
                        <IArrowL size={12}/> {tr('plan.master.back')}
                    </button>
                    {!isIterationStep && (
                        <button
                            type="button"
                            className="btn ghost"
                            onClick={() => { if (idx < STEP_DEFS.length - 1) setActive(STEP_DEFS[idx + 1].id); }}
                        >
                            <ISkip size={12}/> {tr('plan.master.skipStep')}
                        </button>
                    )}
                </div>
                <div className="row" style={{gap:8}}>
                    {isIterationStep ? (st.state !== 'done' ? (
                        <span className="muted" role="status" style={{fontSize:12}}>
                            {tr('plan.master.completePeriodToContinue')}
                        </span>
                    ) : (
                        <button
                            type="button"
                            className="btn primary"
                            onClick={() => { if (idx < STEP_DEFS.length - 1) setActive(STEP_DEFS[idx + 1].id); }}
                        >
                            {tr('plan.master.continue')} <IArrow size={12}/>
                        </button>
                    )) : isTeamStep ? (!hasCurrentIteration ? (
                        <button type="button" className="btn primary" onClick={() => setActive('iteration')}>
                            {tr('plan.master.goToPlanningPeriod')} <IArrow size={12}/>
                        </button>
                    ) : (
                        <>
                            <button
                                type="button"
                                className="btn"
                                onClick={() => startTeamWorkflow('import')}
                            >
                                {tr(`plan.steps.${def.id}.secondaryAction`)}
                            </button>
                            <button
                                type="button"
                                className="btn primary"
                                onClick={() => {
                                    if (st.state === 'done') {
                                        if (idx < STEP_DEFS.length - 1) setActive(STEP_DEFS[idx + 1].id);
                                        return;
                                    }
                                    startTeamWorkflow('assign');
                                }}
                            >
                                {st.state === 'done' ? tr('plan.master.continue') : tr(`plan.steps.${def.id}.primaryAction`)} <IArrow size={12}/>
                            </button>
                        </>
                    )) : stepId === 'work' ? (
                        <>
                            <Link to="/triage" className="btn">{tr(`plan.steps.${def.id}.secondaryAction`)}</Link>
                            <Link to="/tasks?create=1" className="btn primary">
                                {tr(`plan.steps.${def.id}.primaryAction`)} <IArrow size={12}/>
                            </Link>
                        </>
                    ) : stepId === 'blockers' ? (
                        <Link to="/tasks" className="btn primary">
                            {tr(`plan.steps.${def.id}.primaryAction`)} <IArrow size={12}/>
                        </Link>
                    ) : stepId === 'schedule' ? (
                        <Link to="/gantt" className="btn primary">
                            {tr('plan.master.openFullSchedule')} <IArrow size={12}/>
                        </Link>
                    ) : stepId === 'review' ? (
                        <Link to="/gantt" className="btn primary">
                            {tr('plan.master.openSchedule')} <IArrow size={12}/>
                        </Link>
                    ) : (
                        <>
                            <Link to={secondaryRoute} className="btn">{tr(`plan.steps.${def.id}.secondaryAction`)}</Link>
                            <Link to={def.route} className="btn primary">
                                {st.state === 'done' ? tr('plan.master.continue') : tr(`plan.steps.${def.id}.primaryAction`)} <IArrow size={12}/>
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

// ── Right aux rail ────────────────────────────────────────────────────────────
function ReadinessAux({ status, ready, setActive }: {
    status: Record<string, StepStatus>;
    ready: { done: number; total: number; pct: number };
    setActive: (id: string) => void;
}) {
    const nextId = nextStep(status);
    const nextDef = STEP_DEFS.find(d => d.id === nextId);
    const attention = Object.entries(status).filter(([, st]) => st.state === 'warn' || st.state === 'blocked');

    return (
        <>
            <div className="aux-sect">
                <h4>{tr('plan.master.planReadiness')}</h4>
                <div className="ready-card">
                    <div
                        className={`ring ${ready.pct === 100 ? 'done' : ''}`}
                        style={{'--p': ready.pct} as CSSProperties}
                    >
                        <span>{ready.pct}%</span>
                    </div>
                    <div>
                        <div style={{fontWeight:600, fontSize:13}}>{tr('plan.master.stepsComplete', { done: ready.done, total: ready.total })}</div>
                        <div className="muted" style={{fontSize:11.5, marginTop:2, lineHeight:1.45}}>
                            {ready.pct === 100 ? tr('plan.hub.planReadyShare') : tr('plan.master.nextStepNamed', { step: nextDef ? tr(`plan.steps.${nextDef.id}.title`) : '' })}
                        </div>
                    </div>
                </div>
            </div>

            <div className="aux-sect">
                <h4>{tr('plan.master.whatNeedsAttention')}</h4>
                {attention.length === 0 ? (
                    <div className="aux-item">
                        <div className="ai-icon" style={{color:'var(--done)'}}><ICheck size={13} stroke={3}/></div>
                        <div><div className="ai-title">{tr('plan.master.nothingFlagged')}</div><div className="ai-sub">{tr('plan.master.allStepsGood')}</div></div>
                    </div>
                ) : (
                    attention.map(([id, st]) => {
                        const def = STEP_DEFS.find(d => d.id === id)!;
                        return (
                            <div key={id} className="aux-item">
                                <div className="ai-icon" style={{color: st.state === 'blocked' ? 'var(--blocked)' : 'var(--warn)'}}>
                                    {st.state === 'blocked' ? <ILock size={13}/> : <IWarning size={13}/>}
                                </div>
                                <div style={{flex:1, minWidth:0}}>
                                    <div className="ai-title">{tr(`plan.steps.${def.id}.title`)}</div>
                                    <div className="ai-sub">{st.missing?.[0]}</div>
                                    <div className="ai-action">
                                        <button className="btn sm" onClick={() => setActive(id)}>{tr('plan.master.openStep')} <IChevR size={10}/></button>
                                    </div>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>

            <div className="aux-sect">
                <h4>{tr('plan.master.jumpToExpert')}</h4>
                <div style={{display:'flex', flexDirection:'column', gap:4}}>
                    {[
                        {l:tr('nav.calendar'), icon:<ICalendar size={12}/>, to:'/calendar'},
                        {l:tr('nav.iterations'), icon:<IIteration size={12}/>, to:'/iterations'},
                        {l:tr('nav.team'), icon:<ITeam size={12}/>, to:'/team'},
                        {l:tr('nav.tasks'), icon:<ITasks size={12}/>, to:'/tasks'},
                        {l:tr('nav.gantt'), icon:<IGantt size={12}/>, to:'/gantt'},
                    ].map(x => (
                        <Link key={x.l} to={x.to} className="btn sm ghost" style={{justifyContent:'flex-start'}}>
                            {x.icon} {x.l} <IOpen size={10} style={{marginLeft:'auto'}}/>
                        </Link>
                    ))}
                </div>
            </div>
        </>
    );
}

// ── Main master page ──────────────────────────────────────────────────────────
const PlanMasterPage = () => {
    const { t } = useTranslation();
    const {
        iterations,
        currentIteration,
        selectIteration,
        teamMembers,
        allTasks,
        readinessData: r,
        status: rawStatus,
        ready,
        nextId: autoId,
        isLoading,
        isError,
        refetch,
    } = usePlanningReadiness();
    const status = localizeStatus(rawStatus, r, t);
    const [activeId, setActiveId] = useState<string | null>(null);
    const [teamWorkflow, setTeamWorkflow] = useState<TeamWorkflow | null>(null);
    const stepId = activeId ?? autoId;
    const activeDef = STEP_DEFS.find(def => def.id === stepId) ?? STEP_DEFS[0];
    const currentIterationSubtitle = currentIteration
        ? `${currentIteration.name} · ${formatDate(currentIteration.start_date, i18n.language)} - ${formatDate(currentIteration.end_date, i18n.language)}`
        : '';
    const closeTeamWorkflow = () => setTeamWorkflow(null);
    const startTeamWorkflow = (workflow: TeamWorkflow) => {
        setActiveId('team');
        setTeamWorkflow(workflow);
    };

    if (isLoading) {
        return <div className="wc" style={{height:'100%', display:'grid', placeItems:'center'}}>
            <div className="empty" role="status" aria-live="polite" aria-busy="true">
                <div className="empty-icon"><IRefresh size={16}/></div>
                <h4>{t('plan.master.planningDataLoading')}</h4>
                <p>{t('plan.master.planningDataLoadingBody')}</p>
            </div>
        </div>;
    }

    if (isError) {
        return <div className="wc" style={{height:'100%', display:'grid', placeItems:'center'}}>
            <div className="empty" role="alert">
                <div className="empty-icon"><IWarning size={16}/></div>
                <h4>{t('plan.master.planningDataUnavailable')}</h4>
                <p>{t('plan.master.planningDataUnavailableBody')}</p>
                <div className="empty-actions">
                    <button type="button" className="btn primary" onClick={() => { void refetch(); }}>{t('plan.master.retryPlanningData')}</button>
                </div>
            </div>
        </div>;
    }

    return (
        <div className="wc" style={{height:'100%', display:'flex', flexDirection:'column'}}>
            {/* Master header */}
            <div style={{padding:'14px 24px 0', borderBottom:'1px solid var(--wc-border)', background:'var(--wc-panel)', flexShrink:0}}>
                <Breadcrumbs items={[
                    { label: t('plan.title'), path: '/plan' },
                    { label: t('plan.hub.planIterationTitle') },
                ]} />
                <div className="between" style={{paddingBottom:12}}>
                    <div className="row" style={{gap:10, alignItems:'baseline'}}>
                        <h1 className="wc-page-title">{t('plan.hub.planIterationTitle')}</h1>
                        <span className="muted" style={{fontSize:12}}>
                            {currentIteration
                                ? `${currentIteration.name} · ${formatIterationDates(r.currentIterationStart, r.currentIterationEnd)}`
                                : t('plan.master.noPeriodYet')}
                        </span>
                    </div>
                    <div className="row" style={{gap:10}}>
                        <div className="row" style={{gap:4, fontSize:11.5, color:'var(--wc-ink-3)'}}>
                            <span>{t('plan.master.progress')}</span>
                            <span style={{fontWeight:600, color:'var(--wc-ink)'}}>{ready.done}/{ready.total}</span>
                        </div>
                        <Link to={activeDef.route} className="btn sm ghost"><IOpen size={11}/> {t(`plan.steps.${activeDef.id}.expert`)}</Link>
                    </div>
                </div>
            </div>

            {/* 3-column master body */}
            <div className="wc-master" style={{flex:1, minHeight:0}}>
                {/* Left rail */}
                <aside className="wc-master-rail">
                    <div className="wc-master-rail-head">
                        <div className="row" style={{justifyContent:'space-between'}}>
                            <div style={{fontSize:11, fontWeight:600, letterSpacing:'0.06em', textTransform:'uppercase', color:'var(--wc-ink-3)'}}>{t('plan.master.steps')}</div>
                            <span className="pill sm">{ready.pct}%</span>
                        </div>
                    </div>
                    <div className="step-rail">
                        {STEP_DEFS.map((def, i) => {
                            const st = status[def.id];
                            const isCurrent = def.id === stepId;
                            const cls = `step-item ${st.state === 'done' ? 'done' : ''} ${isCurrent ? 'current' : ''} ${st.state === 'warn' ? 'warn' : ''} ${st.state === 'blocked' ? 'blocked' : ''}`;
                            return (
                                <button type="button" key={def.id} className={cls}
                                     aria-current={isCurrent ? 'step' : undefined}
                                     onClick={() => setActiveId(def.id)}>
                                    <div className="step-num">
                                        {st.state === 'done'              ? <ICheck size={11} stroke={3}/> :
                                         st.state === 'blocked' && !isCurrent ? <ILock size={10}/> :
                                         (i+1)}
                                    </div>
                                    <div>
                                        <div className="step-title">{t(`plan.steps.${def.id}.title`)}</div>
                                        <div className="step-sub">
                                            {st.state === 'done'    && (st.summary || t('plan.master.done'))}
                                            {st.state === 'warn'    && (st.missing?.[0] || t('plan.master.needsAttention'))}
                                            {st.state === 'blocked' && (st.missing?.[0] || t('plan.master.blocked'))}
                                            {st.state === 'todo'    && t('plan.master.notStarted')}
                                        </div>
                                    </div>
                                    <StepPill state={st.state}/>
                                </button>
                            );
                        })}
                    </div>
                    <div style={{padding:'8px 14px 16px'}}>
                        <div className="divider"/>
                        <div style={{fontSize:11, color:'var(--wc-ink-3)', lineHeight:1.5}}>
                            {t('plan.master.returnAnyTime')}
                        </div>
                    </div>
                </aside>

                {/* Main step body */}
                <main className="wc-master-main">
                    <StepBody
                        stepId={stepId}
                        status={status}
                        r={r}
                        tasks={allTasks}
                        teamMembers={teamMembers}
                        setActive={setActiveId}
                        iterations={iterations}
                        currentIteration={currentIteration}
                        selectIteration={selectIteration}
                        onStartTeamWorkflow={startTeamWorkflow}
                    />
                </main>

                {/* Right aux */}
                <aside className="wc-master-aux">
                    <ReadinessAux status={status} ready={ready} setActive={setActiveId}/>
                </aside>
            </div>

            {currentIteration && (
                <SlideOverDrawer
                    open={teamWorkflow === 'assign'}
                    title={t('plan.master.addPersonToIteration')}
                    subtitle={currentIterationSubtitle}
                    icon={<ITeam size={14}/>}
                    onClose={closeTeamWorkflow}
                    ariaLabel={t('plan.master.addPersonToIteration')}
                    className="max-w-[720px]"
                >
                    <div className="p-5">
                        <TeamForm
                            iterationId={currentIteration.id}
                            onSuccess={closeTeamWorkflow}
                            onCancel={closeTeamWorkflow}
                        />
                    </div>
                </SlideOverDrawer>
            )}

            {currentIteration && teamWorkflow === 'import' && (
                <ImportTeamModal
                    iterationId={currentIteration.id}
                    onClose={closeTeamWorkflow}
                />
            )}
        </div>
    );
};

export default PlanMasterPage;
