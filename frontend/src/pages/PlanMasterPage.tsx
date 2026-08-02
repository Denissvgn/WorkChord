import { useCallback, useEffect, useId, useRef, useState } from 'react';
import type { ReactNode, CSSProperties, MouseEvent as ReactMouseEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Copy, ExternalLink, RefreshCw, Share2, Trash2 } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import i18n from '../i18n/i18n';
import {
    localizeStatus,
    readiness as calculateReadiness,
    STEP_DEFS,
    nextStep,
} from '../features/planningMasters/masters';
import type { PlanReadiness, StepStatus } from '../features/planningMasters/masters';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import type { PlanningQueryFeedback } from '../features/planningMasters/usePlanningReadiness';
import { IterationForm } from '../components/iteration/IterationForm';
import { TeamForm } from '../components/team/TeamForm';
import { ImportTeamModal } from '../components/team/ImportTeamModal';
import { OverflowMenu, SlideOverDrawer } from '../components/ui';
import type { Iteration } from '../types/iteration';
import type { Task } from '../types/task';
import { planShareService } from '../services/planShareService';
import type { PlanShare } from '../services/planShareService';
import { copyText } from '../utils/copyText';
import { formatDate, formatDateTime } from '../utils/formatDate';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { useConfirmDialog } from '../components/common/useConfirmDialog';
import { useToast } from '../components/feedback/toast';

const tr = i18n.t.bind(i18n);
const TASK_ROW_LIMIT = 20;
const TEAM_ROW_LIMIT = 50;
const SCHEDULE_ROW_LIMIT = 7;

type EmbeddedFormState = {
    dirty: boolean;
    pending: boolean;
};

type PlanningTeamMember = {
    id: number;
    name: string;
    position?: string;
    capacity_hours: number;
    planned_hours: number;
};

type StepDataState = {
    loading: boolean;
    fetching: boolean;
    error: unknown;
    retry: () => Promise<unknown> | unknown;
    label: string;
};

type TeamWorkflowState = {
    kind: TeamWorkflow;
    iterationId: number;
};

const isPositiveEffort = (task: Pick<Task, 'effort_days'>) => (
    Number.isFinite(Number(task.effort_days)) && Number(task.effort_days) > 0
);

const safeNonNegative = (value: unknown) => {
    const numeric = Number(value);
    return Number.isFinite(numeric) && numeric >= 0 ? numeric : 0;
};

const formatNumber = (value: number, maximumFractionDigits = 1) => (
    new Intl.NumberFormat(i18n.language, { maximumFractionDigits }).format(value)
);

const graphemes = (value: string) => {
    if (typeof Intl.Segmenter === 'function') {
        return Array.from(
            new Intl.Segmenter(i18n.language, { granularity: 'grapheme' }).segment(value),
            segment => segment.segment,
        );
    }
    return Array.from(value);
};

const initialsFor = (name: string) => {
    const words = name.trim().split(/\s+/).filter(Boolean);
    if (words.length === 0) return '?';
    const candidates = words.length > 1
        ? [graphemes(words[0])[0], graphemes(words[words.length - 1])[0]]
        : graphemes(words[0]).slice(0, 2);
    return candidates.filter(Boolean).join('').toLocaleUpperCase(i18n.language) || '?';
};

const parseDateKey = (value: string | null | undefined) => {
    if (!value || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
    const date = new Date(`${value}T00:00:00.000Z`);
    return Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== value
        ? null
        : date;
};

const daysBetween = (start: Date, end: Date) => (
    Math.round((end.getTime() - start.getTime()) / 86_400_000)
);

const addUtcDays = (date: Date, days: number) => (
    new Date(date.getTime() + days * 86_400_000)
);

const clamp = (value: number, min: number, max: number) => (
    Math.min(max, Math.max(min, value))
);

// ── Icon helpers ─────────────────────────────────────────────────────────────
const Svg = ({ d, size = 14, stroke = 1.75, ...rest }: { d: ReactNode; size?: number; stroke?: number; style?: CSSProperties; className?: string }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round"
         aria-hidden="true" focusable="false" {...rest}>
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
const IInfo      = (p: IconProps) => <Svg {...p} d={<><circle cx="12" cy="12" r="9"/><path d="M12 8v.01M11 12h1v4h1"/></>}/>;
const IIteration = (p: IconProps) => <Svg {...p} d={<><path d="M2 12a10 10 0 0 1 17-7"/><path d="M22 12a10 10 0 0 1-17 7"/><path d="M19 2v5h-5M5 22v-5h5"/></>}/>;
const ITeam      = (p: IconProps) => <Svg {...p} d={<><circle cx="9" cy="8" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M3 20c.5-3.5 3-5 6-5s5.5 1.5 6 5"/><path d="M14.5 20c.3-2 1.7-3 3.5-3s3.2 1 3.5 3"/></>}/>;
const ITasks     = (p: IconProps) => <Svg {...p} d={<><path d="M9 11l3 3 8-8"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></>}/>;
const IGantt     = (p: IconProps) => <Svg {...p} d={<><rect x="3" y="5" width="9" height="3" rx="1"/><rect x="7" y="11" width="11" height="3" rx="1"/><rect x="5" y="17" width="7" height="3" rx="1"/></>}/>;
const IWarning   = (p: IconProps) => <Svg {...p} d={<><path d="M12 2L1 21h22z"/><path d="M12 9v5M12 18v.5"/></>}/>;
const IPlus      = (p: IconProps) => <Svg {...p} d={<><path d="M12 5v14M5 12h14"/></>}/>;
const IRefresh   = (p: IconProps) => <Svg {...p} d={<><path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/></>}/>;
const IInbox     = (p: IconProps) => <Svg {...p} d={<><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 6h13l3.5 6v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6z"/></>}/>;
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
    formState,
    editorRevision,
    onFormStateChange,
    requestDraftTransition,
}: {
    r: PlanReadiness;
    iterations: Iteration[];
    currentIteration: Iteration | null;
    selectIteration: (id: number) => void;
    formState: EmbeddedFormState;
    editorRevision: number;
    onFormStateChange: (state: EmbeddedFormState) => void;
    requestDraftTransition: (onDiscard: () => void, resetDraft?: boolean) => void;
}) {
    const [mode, setMode] = useState<FormMode>(currentIteration ? 'edit' : 'create');
    const [existingId, setExistingId] = useState(currentIteration?.id ?? iterations[0]?.id ?? 0);
    const existingSelectId = useId();

    const resetCreateDraft = () => requestDraftTransition(() => setMode('create'));

    const handleSaved = (iteration?: Iteration) => {
        if (iteration) {
            selectIteration(iteration.id);
            setExistingId(iteration.id);
        }
        onFormStateChange({ dirty: false, pending: false });
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
                    <button
                        type="button"
                        className="btn sm"
                        disabled={formState.pending}
                        onClick={() => requestDraftTransition(
                            () => currentIteration ? setMode('edit') : setMode('create'),
                        )}
                    >
                        {currentIteration ? tr('plan.master.edit') : tr('plan.master.create')}
                    </button>
                    {iterations.length > 0 && (
                        <button
                            type="button"
                            className="btn sm ghost"
                            disabled={formState.pending}
                            onClick={() => requestDraftTransition(() => setMode('select'))}
                        >
                            {tr('plan.master.useExisting')}
                        </button>
                    )}
                    {currentIteration && (
                        <button type="button" className="btn sm ghost" disabled={formState.pending} onClick={resetCreateDraft}>
                            {tr('plan.master.newPeriod')}
                        </button>
                    )}
                </div>
            </div>

            {mode === 'select' ? (
                <div className="card card-pad">
                    <div className="field" style={{marginBottom:12}}>
                        <label htmlFor={existingSelectId} className="field-lbl">{tr('plan.master.existingPeriod')}</label>
                        <select
                            id={existingSelectId}
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
                        <button
                            type="button"
                            className="btn"
                            onClick={() => setMode(currentIteration ? 'edit' : 'create')}
                        >
                            {tr('actions.cancel')}
                        </button>
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
                            key={`${mode === 'edit' ? currentIteration?.id ?? 'edit' : 'create'}:${editorRevision}`}
                            initialData={mode === 'edit' ? currentIteration ?? undefined : undefined}
                            hideProjectScope
                            onSuccess={handleSaved}
                            onCancel={() => requestDraftTransition(() => {
                                setMode(currentIteration ? 'edit' : 'create');
                            }, true)}
                            onStateChange={onFormStateChange}
                        />
                        {iterations.length > 0 && (
                            <button
                                type="button"
                                className="btn"
                                disabled={formState.pending}
                                onClick={() => requestDraftTransition(() => setMode('select'))}
                            >
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
    teamMembers: PlanningTeamMember[];
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
                        <IRefresh size={12}/> {tr('plan.master.importTeamList')}
                    </button>
                </div>
                <EmptyState
                    icon={<ITeam size={16}/>}
                    title={tr('plan.master.noTeamCapacity')}
                    msg={tr('plan.master.addPeopleBeforeSchedule')}
                    primary={tr('plan.master.addPeople')}
                    secondary={tr('plan.master.importTeamList')}
                    onPrimary={openAssign}
                    onSecondary={openImport}
                />
            </>
        );
    }
    const members = teamMembers;
    return (
        <>
            <div className="row" style={{gap:8}}>
                <button type="button" className="btn" onClick={openAssign}>
                    <IPlus size={12}/> {tr('plan.master.addPerson')}
                </button>
                <button type="button" className="btn" onClick={openImport}>
                    <IRefresh size={12}/> {tr('plan.master.importTeamList')}
                </button>
            </div>
            <div
                className="wc-table-frame"
                role="region"
                aria-label={tr('plan.master.teamCapacityTable')}
            >
                <table className="table plan-master-table">
                    <caption className="sr-only">{tr('plan.master.teamCapacityTable')}</caption>
                    <thead>
                        <tr>
                            <th scope="col">{tr('plan.master.person')}</th>
                            <th scope="col">{tr('plan.master.role')}</th>
                            <th scope="col" style={{width:110}}>{tr('plan.master.capacity')}</th>
                            <th scope="col" style={{width:220}}>{tr('plan.master.plannedLoad')}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {members.slice(0, TEAM_ROW_LIMIT).map(p => {
                            const planned = safeNonNegative(p.planned_hours);
                            const cap = safeNonNegative(p.capacity_hours);
                            const pct = cap > 0
                                ? Math.min(120, Math.round((planned / cap) * 100))
                                : planned > 0 ? 120 : 0;
                            const over = planned > cap && planned > 0;
                            return (
                                <tr key={p.id}>
                                    <td>
                                        <div className="who">
                                            <span aria-hidden="true" className="avatar" style={{...avatarStyle(p.id), width:20, height:20, fontSize:10}}>
                                                {initialsFor(p.name)}
                                            </span>
                                            <span className="plan-master-break" style={{fontWeight:500}}>{p.name}</span>
                                        </div>
                                    </td>
                                    <td className="muted plan-master-break">{p.position || '—'}</td>
                                    <td className="tnum">{tr('units.hoursCompact', { count: formatNumber(cap) })}</td>
                                    <td>
                                        <div className="row" style={{gap:8}}>
                                            <div
                                                className="cap-bar"
                                                style={{flex:1}}
                                                role="progressbar"
                                                aria-label={tr('plan.master.capacityUsageFor', { name: p.name })}
                                                aria-valuemin={0}
                                                aria-valuemax={120}
                                                aria-valuenow={pct}
                                                aria-valuetext={tr('plan.master.capacityPlanned', {
                                                    planned: formatNumber(planned),
                                                    capacity: formatNumber(cap),
                                                })}
                                            >
                                                <i className={over ? 'over' : pct > 90 ? 'warn' : ''} style={{width:`${pct}%`}}/>
                                            </div>
                                            <span className="tnum muted" style={{fontSize:'var(--wc-type-micro)'}}>
                                                {tr('plan.master.capacityFraction', {
                                                    planned: formatNumber(planned),
                                                    capacity: formatNumber(cap),
                                                })}
                                            </span>
                                        </div>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
            {members.length > TEAM_ROW_LIMIT && (
                <ActionGuidance
                    title={tr('plan.master.showingRows', { shown: TEAM_ROW_LIMIT, total: members.length })}
                    body={tr('plan.master.openTeamForAll')}
                    action={tr('nav.team')}
                    to="/team"
                />
            )}
        </>
    );
}

function BodyWork({
    r,
    tasks,
    onOpenIteration,
}: {
    r: PlanReadiness;
    tasks: Task[];
    onOpenIteration: () => void;
}) {
    const [filter, setFilter] = useState<'all'|'noOwner'|'noEffort'>('all');
    const createTaskTo = '/tasks?create=1';
    const visible = filter === 'noOwner' ? tasks.filter(t => !t.assignee)
                  : filter === 'noEffort' ? tasks.filter(t => !isPositiveEffort(t))
                  : tasks;

    if (!r.hasCurrentIteration) {
        return (
            <EmptyState
                icon={<ITasks size={16}/>}
                title={tr('plan.master.createPeriodFirst')}
                msg={tr('plan.master.workNeedsPeriod')}
                primary={tr('plan.master.goToPlanningPeriod')}
                onPrimary={onOpenIteration}
            />
        );
    }

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
                <div className="seg" role="group" aria-label={tr('plan.master.taskFilters')}>
                    <button type="button" aria-pressed={filter === 'all'} onClick={() => setFilter('all')}>{tr('plan.master.allCount', { count: r.taskCount })}</button>
                    <button type="button" aria-pressed={filter === 'noOwner'} onClick={() => setFilter('noOwner')}>{tr('plan.master.unassignedCount', { count: r.tasksWithoutAssignee })}</button>
                    <button type="button" aria-pressed={filter === 'noEffort'} onClick={() => setFilter('noEffort')}>{tr('plan.master.missingEffortCount', { count: r.tasksWithoutEffort })}</button>
                </div>
                <div className="row" style={{gap:8}}>
                    <Link to="/triage" className="btn"><IInbox size={12}/> {tr('plan.master.pullFromIntake')}</Link>
                    <Link to={createTaskTo} className="btn primary"><IPlus size={12}/> {tr('plan.master.addTask')}</Link>
                </div>
            </div>

            {visible.length === 0 ? (
                <EmptyState
                    icon={<ITasks size={16}/>}
                    title={tr('plan.master.noTasksMatchFilter')}
                    msg={tr('plan.master.noTasksMatchFilterBody')}
                    primary={tr('plan.master.clearFilter')}
                    secondary={tr('plan.master.openTasks')}
                    onPrimary={() => setFilter('all')}
                    secondaryTo="/tasks"
                />
            ) : (
                <div
                    className="wc-table-frame"
                    role="region"
                    aria-label={tr('plan.master.workReadinessTable')}
                >
                    <table className="table plan-master-table">
                        <caption className="sr-only">{tr('plan.master.workReadinessTable')}</caption>
                        <thead>
                            <tr>
                                <th scope="col" style={{width:42}}>{tr('plan.master.readiness')}</th>
                                <th scope="col">{tr('plan.master.task')}</th>
                                <th scope="col" style={{width:150}}>{tr('plan.master.project')}</th>
                                <th scope="col" style={{width:170}}>{tr('plan.master.assignee')}</th>
                                <th scope="col" style={{width:100}}>{tr('plan.master.effort')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {visible.slice(0, TASK_ROW_LIMIT).map(t => {
                                const issues: string[] = [];
                                if (!t.assignee) issues.push(tr('plan.master.assignee'));
                                if (!isPositiveEffort(t)) issues.push(tr('plan.master.effort'));
                                const readinessLabel = issues.length
                                    ? tr('plan.master.taskNeedsAttention', { title: t.title })
                                    : tr('plan.master.taskReady', { title: t.title });
                                return (
                                    <tr key={t.id}>
                                        <td>
                                            <span className="sr-only">{readinessLabel}</span>
                                            {issues.length
                                                ? <IWarning size={13} style={{color:'var(--warn)'}}/>
                                                : <ICheck size={13} stroke={3} style={{color:'var(--done)'}}/>}
                                        </td>
                                        <td>
                                            <div className="plan-master-break" style={{fontWeight:500}}>{t.title}</div>
                                            {issues.length > 0 && (
                                                <div className="muted plan-master-break" style={{fontSize:'var(--wc-type-micro)', marginTop:2}}>
                                                    {tr('plan.master.missingFields', { fields: issues.join(', ') })}
                                                </div>
                                            )}
                                        </td>
                                        <td className="muted plan-master-break">{t.project?.name || '—'}</td>
                                        <td>
                                            {t.assignee
                                                ? <div className="who">
                                                    <span aria-hidden="true" className="avatar" style={{...avatarStyle(t.assignee.id),width:20,height:20,fontSize:10}}>
                                                        {initialsFor(t.assignee.name)}
                                                    </span>
                                                    <span className="plan-master-break">{t.assignee.name}</span>
                                                  </div>
                                                : <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>}
                                        </td>
                                        <td>
                                            {isPositiveEffort(t)
                                                ? <span className="tnum">{tr('units.daysCompact', { count: formatNumber(Number(t.effort_days)) })}</span>
                                                : <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
            {visible.length > TASK_ROW_LIMIT && (
                <ActionGuidance
                    title={tr('plan.master.showingRows', { shown: TASK_ROW_LIMIT, total: visible.length })}
                    body={tr('plan.master.openTasksForAll')}
                    action={tr('plan.master.openTasks')}
                    to="/tasks"
                />
            )}
        </>
    );
}

function BodyBlockers({
    r,
    tasks,
    st,
    onOpenIteration,
}: {
    r: PlanReadiness;
    tasks: Task[];
    st: StepStatus;
    onOpenIteration: () => void;
}) {
    const ownerBlockersId = useId();
    const effortBlockersId = useId();

    if (st.state === 'done') {
        return (
            <div className="banner done">
                <ICheck size={14}/><div>{tr('plan.master.readyToBuild')}</div>
            </div>
        );
    }
    if (!r.hasCurrentIteration) {
        return (
            <EmptyState
                icon={<ILock size={16}/>}
                title={tr('plan.master.createPeriodFirst')}
                msg={tr('plan.master.blockersNeedPeriod')}
                primary={tr('plan.master.goToPlanningPeriod')}
                onPrimary={onOpenIteration}
            />
        );
    }
    if (st.state === 'blocked') {
        return <EmptyState icon={<ILock size={16}/>} title={tr('plan.master.addWorkFirst')} msg={tr('plan.master.blockersNeedTasks')} primary={tr('plan.master.addTasks')} primaryTo="/tasks?create=1"/>;
    }

    const noOwner  = tasks.filter(t => !t.assignee);
    const noEffort = tasks.filter(t => !isPositiveEffort(t));

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
                <section className="card" style={{padding:0}} aria-labelledby={ownerBlockersId}>
                    <div className="card-head">
                        <h3 id={ownerBlockersId}>{tr('plan.master.unassignedCount', { count: noOwner.length })}</h3>
                        <span className="sub">{tr('plan.master.schedulerSkipsUnassigned')}</span>
                    </div>
                    {noOwner.slice(0, TASK_ROW_LIMIT).map(t => (
                        <div key={t.id} className="cap-row" style={{gridTemplateColumns:'16px 1fr auto'}}>
                            <IWarning size={13} style={{color:'var(--warn)'}}/>
                            <div className="plan-master-min">
                                <div className="plan-master-break" style={{fontWeight:500}}>{t.title}</div>
                                <div className="muted" style={{fontSize:'var(--wc-type-micro)'}}>
                                    {isPositiveEffort(t)
                                        ? tr('units.daysCompact', { count: formatNumber(Number(t.effort_days)) })
                                        : tr('plan.master.noEffort')}
                                </div>
                            </div>
                            <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>
                        </div>
                    ))}
                    {noOwner.length > TASK_ROW_LIMIT && (
                        <div className="plan-master-row-disclosure">
                            {tr('plan.master.showingRows', { shown: TASK_ROW_LIMIT, total: noOwner.length })}
                            <Link to="/tasks" className="btn sm ghost">{tr('plan.master.openTasks')}</Link>
                        </div>
                    )}
                </section>
            )}

            {noEffort.length > 0 && (
                <section className="card" style={{padding:0}} aria-labelledby={effortBlockersId}>
                    <div className="card-head">
                        <h3 id={effortBlockersId}>{tr('plan.master.missingEffortCount', { count: noEffort.length })}</h3>
                        <span className="sub">{tr('plan.master.schedulerNeedsEstimate')}</span>
                    </div>
                    {noEffort.slice(0, TASK_ROW_LIMIT).map(t => (
                        <div key={t.id} className="cap-row" style={{gridTemplateColumns:'16px 1fr auto'}}>
                            <IWarning size={13} style={{color:'var(--warn)'}}/>
                            <div className="plan-master-min">
                                <div className="plan-master-break" style={{fontWeight:500}}>{t.title}</div>
                                <div className="muted plan-master-break" style={{fontSize:'var(--wc-type-micro)'}}>{t.assignee?.name || tr('common.unassigned')}</div>
                            </div>
                            <Link to="/tasks" className="btn sm">{tr('plan.master.openTasks')}</Link>
                        </div>
                    ))}
                    {noEffort.length > TASK_ROW_LIMIT && (
                        <div className="plan-master-row-disclosure">
                            {tr('plan.master.showingRows', { shown: TASK_ROW_LIMIT, total: noEffort.length })}
                            <Link to="/tasks" className="btn sm ghost">{tr('plan.master.openTasks')}</Link>
                        </div>
                    )}
                </section>
            )}
        </>
    );
}

function BodySchedule({ r, tasks, st, onOpenFirstIncomplete }: { r: PlanReadiness; tasks: Task[]; st: StepStatus; onOpenFirstIncomplete: () => void }) {
    if (st.state === 'blocked') {
        return <EmptyState icon={<ILock size={16}/>} title={tr('plan.master.earlierStepsNeedAttention')} msg={tr('plan.master.schedulerPrerequisites')} primary={tr('plan.master.backFirstIncomplete')} onPrimary={onOpenFirstIncomplete}/>;
    }

    if (!r.hasGanttSchedule) {
        return (
            <>
                <ActionGuidance
                    icon={<IGantt size={14}/>}
                    title={tr('plan.master.schedulingToolsTitle')}
                    body={tr('plan.master.schedulingToolsBody')}
                    action={tr('plan.master.openFullSchedule')}
                    to="/gantt"
                />
                <EmptyState
                    icon={<IGantt size={16}/>}
                    title={tr('plan.master.scheduleUnavailableTitle')}
                    msg={tr('plan.master.scheduleUnavailableBody')}
                    primary={tr('plan.master.openFullSchedule')}
                    primaryTo="/gantt"
                />
            </>
        );
    }

    const timelineStart = parseDateKey(r.currentIterationStart);
    const timelineEnd = parseDateKey(r.currentIterationEnd);
    if (!timelineStart || !timelineEnd || timelineEnd < timelineStart) {
        return (
            <EmptyState
                icon={<IWarning size={16}/>}
                title={tr('plan.master.scheduleDatesUnavailableTitle')}
                msg={tr('plan.master.scheduleDatesUnavailableBody')}
                primary={tr('plan.master.editPlanningPeriod')}
                primaryTo="/iterations"
            />
        );
    }

    const totalDays = daysBetween(timelineStart, timelineEnd) + 1;
    const tickCount = Math.min(7, totalDays);
    const tickOffsets = Array.from({ length: tickCount }, (_, index) => (
        tickCount === 1 ? 0 : Math.round(index * (totalDays - 1) / (tickCount - 1))
    ));
    const timelineFormatter = new Intl.DateTimeFormat(i18n.language, {
        day: 'numeric',
        month: 'short',
        timeZone: 'UTC',
    });
    const scheduledTasks = tasks.filter(task => (
        !task.is_deferred
        && !task.is_composite
        && isPositiveEffort(task)
        && parseDateKey(task.start_date)
        && parseDateKey(task.end_date)
    ));
    const visibleTasks = scheduledTasks.slice(0, SCHEDULE_ROW_LIMIT);

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
                <IInfo size={14}/>
                <div>
                    {tr('plan.master.scheduleFreshnessNotice')}
                </div>
            </div>

            <div className="card" style={{padding:0}}>
                <div className="card-head">
                    <h3>{tr('plan.master.savedScheduleDates')}</h3>
                    <span className="sub plan-master-break">
                        {formatIterationDates(r.currentIterationStart, r.currentIterationEnd)}
                    </span>
                </div>
                <div style={{padding:14}}>
                    {visibleTasks.length > 0 ? (
                        <div
                            className="plan-master-gantt-scroll"
                            role="region"
                            aria-label={tr('plan.master.savedScheduleDates')}
                        >
                            <div className="gantt plan-master-gantt">
                                <div className="gantt-head">
                                    <div className="gh-cell">{tr('plan.master.task')}</div>
                                    <div className="gh-cell" style={{display:'grid', gridTemplateColumns:`repeat(${tickCount}, 1fr)`, padding:0}}>
                                        {tickOffsets.map(offset => {
                                            const date = addUtcDays(timelineStart, offset);
                                            const dateKey = date.toISOString().slice(0, 10);
                                            const day = date.getUTCDay();
                                            return (
                                                <div
                                                    key={dateKey}
                                                    title={formatDate(dateKey, i18n.language)}
                                                    style={{
                                                        padding:'8px 2px',
                                                        textAlign:'center',
                                                        fontSize:'var(--wc-type-micro)',
                                                        color:'var(--ink-4)',
                                                        background:day === 0 || day === 6 ? 'var(--panel-3)' : 'var(--panel-2)',
                                                        borderInlineEnd:'1px solid var(--border)',
                                                    }}
                                                >
                                                    {timelineFormatter.format(date)}
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                                {visibleTasks.map(task => {
                                    const taskStart = parseDateKey(task.start_date)!;
                                    const taskEnd = parseDateKey(task.end_date)!;
                                    const startOffset = clamp(daysBetween(timelineStart, taskStart), 0, totalDays - 1);
                                    const endExclusive = clamp(daysBetween(timelineStart, taskEnd) + 1, startOffset + 1, totalDays);
                                    const left = startOffset / totalDays * 100;
                                    const width = (endExclusive - startOffset) / totalDays * 100;
                                    const taskRange = formatIterationDates(task.start_date ?? '', task.end_date ?? '');
                                    return (
                                        <div key={task.id} className="gantt-row">
                                            <div className="gr-cell plan-master-min" style={{display:'flex', alignItems:'center', gap:8}}>
                                                <span aria-hidden="true" className="avatar" style={{...avatarStyle(task.assignee?.id || task.id),width:18,height:18,fontSize:9}}>
                                                    {initialsFor(task.assignee?.name || '?')}
                                                </span>
                                                <span className="plan-master-task-title">{task.title}</span>
                                            </div>
                                            <div className="gr-cell bar-cell">
                                                <div className="bar-track">
                                                    <div
                                                        className="bar"
                                                        role="img"
                                                        aria-label={tr('plan.master.taskScheduleRange', {
                                                            title: task.title,
                                                            dates: taskRange,
                                                        })}
                                                        title={`${task.title} · ${taskRange}`}
                                                        style={{
                                                            insetInlineStart: `${left}%`,
                                                            width: `${width}%`,
                                                        }}
                                                    >
                                                        {task.title}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ) : (
                        <div className="muted" style={{padding:'12px 0', fontSize:'var(--wc-type-meta)'}}>
                            {tr('plan.master.scheduleDatesUnavailableBody')}
                        </div>
                    )}
                    {scheduledTasks.length > SCHEDULE_ROW_LIMIT && (
                        <div className="plan-master-row-disclosure">
                            {tr('plan.master.showingRows', {
                                shown: SCHEDULE_ROW_LIMIT,
                                total: scheduledTasks.length,
                            })}
                            <Link to="/gantt" className="btn sm ghost">{tr('plan.master.openFullSchedule')}</Link>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}

function BodyReview({
    r,
    tasks,
    teamMembers,
    st,
    onOpenFirstIncomplete,
    share,
    shareLoading,
    shareError,
    sharePending,
    onRetryShare,
    onCreateShare,
    onCopyShare,
    onRevokeShare,
}: {
    r: PlanReadiness;
    tasks: Task[];
    teamMembers: PlanningTeamMember[];
    st: StepStatus;
    onOpenFirstIncomplete: () => void;
    share: PlanShare | null;
    shareLoading: boolean;
    shareError: unknown;
    sharePending: boolean;
    onRetryShare: () => void;
    onCreateShare: () => void;
    onCopyShare: () => void;
    onRevokeShare: () => void;
}) {
    if (st.state === 'blocked' || !r.hasGanttSchedule) {
        return (
            <EmptyState
                icon={<ILock size={16}/>}
                title={tr('plan.master.earlierStepsNeedAttention')}
                msg={tr('plan.master.reviewPrerequisites')}
                primary={tr('plan.master.backFirstIncomplete')}
                onPrimary={onOpenFirstIncomplete}
            />
        );
    }

    const members = teamMembers;
    const totalPlanned = members.reduce((total, member) => (
        total + safeNonNegative(member.planned_hours)
    ), 0);
    const totalCap = members.reduce((total, member) => (
        total + safeNonNegative(member.capacity_hours)
    ), 0);
    const tasksByOwner = new Map<number, number>();
    tasks.forEach(task => {
        if (!task.assignee) return;
        tasksByOwner.set(task.assignee.id, (tasksByOwner.get(task.assignee.id) ?? 0) + 1);
    });

    return (
        <>
            {shareLoading ? (
                <QueryLoadingState message={tr('plan.master.loadingShareLink')} />
            ) : shareError ? (
                <QueryErrorState
                    error={shareError}
                    title={tr('plan.master.shareLinkUnavailable')}
                    fallback={tr('plan.master.shareLinkUnavailableBody')}
                    onRetry={onRetryShare}
                />
            ) : share ? (
                <section className="plan-share-completion" aria-labelledby="plan-share-completion-title">
                    <div className="plan-share-completion-icon done" aria-hidden="true">
                        <Share2 className="h-5 w-5" />
                    </div>
                    <div className="plan-share-completion-copy">
                        <h3 id="plan-share-completion-title">{tr('plan.master.planSharedTitle')}</h3>
                        <p>{tr('plan.master.planSharedBody', {
                            date: formatDateTime(share.created_at, i18n.language),
                        })}</p>
                        <label className="plan-share-link-field">
                            <span>{tr('plan.master.shareLinkLabel')}</span>
                            <input
                                readOnly
                                value={`${window.location.origin}/plan/share/${share.public_id}`}
                                onFocus={event => event.currentTarget.select()}
                            />
                        </label>
                    </div>
                    <div className="plan-share-completion-actions">
                        <button
                            type="button"
                            className="btn primary"
                            disabled={sharePending}
                            onClick={onCopyShare}
                        >
                            <Copy aria-hidden="true" className="h-4 w-4" />
                            {tr('plan.master.copyShareLink')}
                        </button>
                        <Link className="btn" to={`/plan/share/${share.public_id}`}>
                            <ExternalLink aria-hidden="true" className="h-4 w-4" />
                            {tr('plan.master.openSharedPlan')}
                        </Link>
                        <OverflowMenu
                            label={tr('plan.master.shareLinkActions')}
                            items={[
                                {
                                    label: tr('plan.master.refreshShareSnapshot'),
                                    icon: <RefreshCw aria-hidden="true" className="h-4 w-4" />,
                                    onSelect: onCreateShare,
                                    disabled: sharePending,
                                },
                                {
                                    label: tr('plan.master.revokeShareLink'),
                                    icon: <Trash2 aria-hidden="true" className="h-4 w-4" />,
                                    onSelect: onRevokeShare,
                                    tone: 'danger',
                                    disabled: sharePending,
                                },
                            ]}
                        />
                    </div>
                </section>
            ) : (
                <section className="plan-share-completion" aria-labelledby="plan-share-ready-title">
                    <div className="plan-share-completion-icon" aria-hidden="true">
                        <Share2 className="h-5 w-5" />
                    </div>
                    <div className="plan-share-completion-copy">
                        <h3 id="plan-share-ready-title">{tr('plan.master.readyToShareTitle')}</h3>
                        <p>{tr('plan.master.readyToShareBody')}</p>
                    </div>
                    <div className="plan-share-completion-actions">
                        <button
                            type="button"
                            className="btn primary"
                            disabled={sharePending}
                            onClick={onCreateShare}
                        >
                            <Share2 aria-hidden="true" className="h-4 w-4" />
                            {sharePending
                                ? tr('plan.master.creatingShareLink')
                                : tr('plan.master.createShareLink')}
                        </button>
                        <Link className="btn" to="/gantt">
                            <IGantt size={14}/>
                            {tr('plan.master.openSchedule')}
                        </Link>
                    </div>
                </section>
            )}

            {r.riskCount > 0 && (
                <div className="banner warn" role="status">
                    <IWarning size={14}/>
                    <div className="plan-master-min">
                        <div className="plan-master-break" style={{fontWeight:600}}>
                            {tr('plan.master.planningExceptionsCount', { count: r.riskCount })}
                        </div>
                        <div className="plan-master-break" style={{fontSize:'var(--wc-type-meta)', marginTop:2}}>
                            {tr('plan.master.planningExceptionsBody')}
                        </div>
                    </div>
                    <Link to="/gantt" className="btn sm">{tr('plan.master.openSchedule')}</Link>
                </div>
            )}

            <div className="kpi-grid kpi-grid-3">
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
                    <div className="kpi-foot muted">{tr('plan.master.capacityPlanned', {
                        planned: formatNumber(totalPlanned),
                        capacity: formatNumber(totalCap),
                    })}</div>
                </div>
                <div className="kpi">
                    <div className="kpi-lbl">{tr('plan.master.schedule')}</div>
                    <div className="kpi-val" style={{fontSize:'var(--wc-type-base)', lineHeight:1.3}}>{tr('plan.master.savedDates')}</div>
                    <div className="kpi-foot muted">{tr('plan.master.verifyScheduleAfterChanges')}</div>
                </div>
            </div>

            {members.length > 0 && (
                <div className="card" style={{padding:0}}>
                    <div className="card-head"><h3>{tr('plan.master.loadByPerson')}</h3><span className="sub">{r.currentIterationName}</span></div>
                    {members.slice(0, TEAM_ROW_LIMIT).map(p => {
                        const planned = safeNonNegative(p.planned_hours);
                        const cap = safeNonNegative(p.capacity_hours);
                        const pct = cap > 0
                            ? Math.min(120, Math.round((planned/cap)*100))
                            : planned > 0 ? 120 : 0;
                        return (
                            <div key={p.id} className="cap-row">
                                <span aria-hidden="true" className="avatar" style={{...avatarStyle(p.id),width:22,height:22,fontSize:10}}>
                                    {initialsFor(p.name)}
                                </span>
                                <div className="plan-master-min">
                                    <div className="plan-master-break" style={{fontWeight:500}}>{p.name}</div>
                                    <div className="muted plan-master-break" style={{fontSize:'var(--wc-type-micro)'}}>
                                        {p.position || ''} · {tr('plan.master.taskCount', { count: tasksByOwner.get(p.id) ?? 0 })}
                                    </div>
                                </div>
                                <div
                                    className="cap-bar"
                                    role="progressbar"
                                    aria-label={tr('plan.master.capacityUsageFor', { name: p.name })}
                                    aria-valuemin={0}
                                    aria-valuemax={120}
                                    aria-valuenow={pct}
                                    aria-valuetext={tr('plan.master.capacityPlanned', {
                                        planned: formatNumber(planned),
                                        capacity: formatNumber(cap),
                                    })}
                                >
                                    <i className={planned>cap?'over':pct>90?'warn':''} style={{width:`${pct}%`}}/>
                                </div>
                                <div className="cap-value">{tr('plan.master.capacityFraction', {
                                    planned: formatNumber(planned),
                                    capacity: formatNumber(cap),
                                })}</div>
                            </div>
                        );
                    })}
                    {members.length > TEAM_ROW_LIMIT && (
                        <div className="plan-master-row-disclosure">
                            {tr('plan.master.showingRows', { shown: TEAM_ROW_LIMIT, total: members.length })}
                            <Link to="/team" className="btn sm ghost">{tr('nav.team')}</Link>
                        </div>
                    )}
                </div>
            )}

            {r.riskCount === 0 && (
                <div className="banner done">
                    <ICheck size={14}/>
                    <div>{tr('plan.master.readyForReview')}</div>
                </div>
            )}
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
    iterationFormState,
    iterationEditorRevision,
    onIterationFormStateChange,
    requestIterationDraftTransition,
    stepDataState,
    navigationLocked,
    share,
    shareLoading,
    shareError,
    sharePending,
    onRetryShare,
    onCreateShare,
    onCopyShare,
    onRevokeShare,
}: {
    stepId: string; status: Record<string, StepStatus>; r: PlanReadiness;
    tasks: Task[]; teamMembers: PlanningTeamMember[]; setActive: (id: string) => void;
    iterations: Iteration[]; currentIteration: Iteration | null; selectIteration: (id: number) => void;
    onStartTeamWorkflow: (workflow: TeamWorkflow) => void;
    iterationFormState: EmbeddedFormState;
    iterationEditorRevision: number;
    onIterationFormStateChange: (state: EmbeddedFormState) => void;
    requestIterationDraftTransition: (onDiscard: () => void, resetDraft?: boolean) => void;
    stepDataState?: StepDataState;
    navigationLocked: boolean;
    share: PlanShare | null;
    shareLoading: boolean;
    shareError: unknown;
    sharePending: boolean;
    onRetryShare: () => void;
    onCreateShare: () => void;
    onCopyShare: () => void;
    onRevokeShare: () => void;
}) {
    const def = STEP_DEFS.find(s => s.id === stepId)!;
    const st  = status[stepId];
    const idx = STEP_DEFS.findIndex(d => d.id === stepId);
    const isIterationStep = stepId === 'iteration';
    const isTeamStep = stepId === 'team';
    const hasCurrentIteration = currentIteration !== null;
    const expertRoute = def.route;
    const secondaryRoute = def.secondaryRoute ?? def.route;
    const headingRef = useRef<HTMLHeadingElement>(null);
    const previousStepRef = useRef(stepId);

    const startTeamWorkflow = (workflow: TeamWorkflow) => {
        if (!hasCurrentIteration || navigationLocked) return;
        onStartTeamWorkflow(workflow);
    };

    useEffect(() => {
        if (previousStepRef.current !== stepId) {
            headingRef.current?.focus();
            previousStepRef.current = stepId;
        }
    }, [stepId]);

    const stepContentUnavailable = Boolean(stepDataState?.error);
    const stepContentLoading = Boolean(stepDataState?.loading && !stepDataState.error);

    return (
        <div className="step-body">
            {/* Header */}
            <div>
                <div className="row" style={{gap:10, marginBottom:8}}>
                    <span className="pill"><span className="pdot"/>{tr('plan.master.stepOf', { step: idx + 1, total: STEP_DEFS.length })}</span>
                    <StepStatePill state={st.state}/>
                    <Link
                        to={expertRoute}
                        className="btn sm ghost"
                        aria-disabled={navigationLocked || undefined}
                        tabIndex={navigationLocked ? -1 : undefined}
                        style={{marginInlineStart:'auto'}}
                    >
                        <IOpen size={11}/> {tr(`plan.steps.${def.id}.expert`)}
                    </Link>
                </div>
                <div className="step-h">
                    <div>
                        <h2 id="plan-master-active-step-heading" ref={headingRef} tabIndex={-1}>
                            {tr(`plan.steps.${def.id}.title`)}
                        </h2>
                        <p>{tr(`plan.steps.${def.id}.description`)}</p>
                    </div>
                </div>
            </div>

            <details className="why plan-master-why">
                <summary>
                    <IInfo size={14}/>
                    <span>{tr('plan.master.whyThisStep')}</span>
                </summary>
                <p>{tr(`plan.steps.${def.id}.why`)}</p>
            </details>

            {stepDataState?.fetching && !stepContentLoading && !stepContentUnavailable && (
                <div className="banner accent" role="status" aria-live="polite">
                    <IRefresh size={14}/>
                    <div>{tr('plan.master.refreshingPlanningData')}</div>
                </div>
            )}

            {/* Step-specific body */}
            {stepContentLoading ? (
                <QueryLoadingState
                    message={tr('plan.master.sectionLoading', { section: stepDataState?.label })}
                />
            ) : stepContentUnavailable ? (
                <QueryErrorState
                    error={stepDataState?.error}
                    title={tr('plan.master.sectionUnavailableTitle', { section: stepDataState?.label })}
                    fallback={tr('plan.master.sectionUnavailableBody', { section: stepDataState?.label })}
                    onRetry={stepDataState?.fetching
                        ? undefined
                        : () => { void stepDataState?.retry(); }}
                />
            ) : stepId === 'iteration' ? (
                <BodyIteration
                    key={currentIteration?.id ?? 'new-period'}
                    r={r}
                    iterations={iterations}
                    currentIteration={currentIteration}
                    selectIteration={selectIteration}
                    formState={iterationFormState}
                    editorRevision={iterationEditorRevision}
                    onFormStateChange={onIterationFormStateChange}
                    requestDraftTransition={requestIterationDraftTransition}
                />
            ) : stepId === 'team' ? (
                <BodyTeam
                    r={r}
                    teamMembers={teamMembers}
                    currentIteration={currentIteration}
                    onStartWorkflow={startTeamWorkflow}
                    onOpenIteration={() => setActive('iteration')}
                />
            ) : stepId === 'work' ? (
                <BodyWork r={r} tasks={tasks} onOpenIteration={() => setActive('iteration')}/>
            ) : stepId === 'blockers' ? (
                <BodyBlockers
                    r={r}
                    tasks={tasks}
                    st={st}
                    onOpenIteration={() => setActive('iteration')}
                />
            ) : stepId === 'schedule' ? (
                <BodySchedule r={r} tasks={tasks} st={st} onOpenFirstIncomplete={() => setActive(nextStep(status))}/>
            ) : stepId === 'review' ? (
                <BodyReview
                    r={r}
                    tasks={tasks}
                    teamMembers={teamMembers}
                    st={st}
                    onOpenFirstIncomplete={() => setActive(nextStep(status))}
                    share={share}
                    shareLoading={shareLoading}
                    shareError={shareError}
                    sharePending={sharePending}
                    onRetryShare={onRetryShare}
                    onCreateShare={onCreateShare}
                    onCopyShare={onCopyShare}
                    onRevokeShare={onRevokeShare}
                />
            ) : null}

            {/* Footer nav */}
            <div className="divider"/>
            <div className="between plan-master-step-footer">
                <div className="row plan-master-step-footer-group" style={{gap:8}}>
                    <button type="button" className="btn" disabled={idx === 0 || navigationLocked}
                            onClick={() => { if (idx > 0) setActive(STEP_DEFS[idx-1].id); }}>
                        <IArrowL size={12}/> {tr('plan.master.back')}
                    </button>
                    {!isIterationStep && idx < STEP_DEFS.length - 1 && (
                        <button
                            type="button"
                            className="btn ghost"
                            disabled={navigationLocked}
                            onClick={() => { if (idx < STEP_DEFS.length - 1) setActive(STEP_DEFS[idx + 1].id); }}
                        >
                            <IChevR size={12}/> {tr('plan.master.viewNextStep')}
                        </button>
                    )}
                </div>
                <div className="row plan-master-step-footer-group" style={{gap:8}}>
                    {stepContentLoading || stepContentUnavailable ? (
                        <span className="muted plan-master-break" role="status" style={{fontSize:'var(--wc-type-meta)'}}>
                            {stepContentUnavailable
                                ? tr('plan.master.sectionUnavailableTitle', { section: stepDataState?.label })
                                : tr('plan.master.sectionLoading', { section: stepDataState?.label })}
                        </span>
                    ) : isIterationStep ? (st.state !== 'done' ? (
                        <span className="muted" role="status" style={{fontSize:'var(--wc-type-meta)'}}>
                            {tr('plan.master.completePeriodToContinue')}
                        </span>
                    ) : (
                        <button
                            type="button"
                            className="btn primary"
                            disabled={navigationLocked}
                            onClick={() => { if (idx < STEP_DEFS.length - 1) setActive(STEP_DEFS[idx + 1].id); }}
                        >
                            {tr('plan.master.continue')} <IArrow size={12}/>
                        </button>
                    )) : isTeamStep ? (!hasCurrentIteration ? (
                        <button type="button" className="btn primary" disabled={navigationLocked} onClick={() => setActive('iteration')}>
                            {tr('plan.master.goToPlanningPeriod')} <IArrow size={12}/>
                        </button>
                    ) : (
                        <>
                            <button
                                type="button"
                                className="btn"
                                disabled={navigationLocked}
                                onClick={() => startTeamWorkflow('import')}
                            >
                                {tr('plan.master.importTeamList')}
                            </button>
                            <button
                                type="button"
                                className="btn primary"
                                disabled={navigationLocked}
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
                        !hasCurrentIteration ? (
                            <button type="button" className="btn primary" disabled={navigationLocked} onClick={() => setActive('iteration')}>
                                {tr('plan.master.goToPlanningPeriod')} <IArrow size={12}/>
                            </button>
                        ) : <>
                            <Link to="/triage" className="btn" aria-disabled={navigationLocked || undefined}>
                                {tr(`plan.steps.${def.id}.secondaryAction`)}
                            </Link>
                            <Link to="/tasks?create=1" className="btn primary" aria-disabled={navigationLocked || undefined}>
                                {tr(`plan.steps.${def.id}.primaryAction`)} <IArrow size={12}/>
                            </Link>
                        </>
                    ) : stepId === 'blockers' ? (
                        st.state === 'blocked' ? (
                            <button type="button" className="btn primary" disabled={navigationLocked} onClick={() => setActive(nextStep(status))}>
                                {tr('plan.master.backFirstIncomplete')} <IArrow size={12}/>
                            </button>
                        ) : (
                            <Link to="/tasks" className="btn primary" aria-disabled={navigationLocked || undefined}>
                                {tr(`plan.steps.${def.id}.primaryAction`)} <IArrow size={12}/>
                            </Link>
                        )
                    ) : stepId === 'schedule' ? (
                        st.state === 'blocked' ? (
                            <button type="button" className="btn primary" disabled={navigationLocked} onClick={() => setActive(nextStep(status))}>
                                {tr('plan.master.backFirstIncomplete')} <IArrow size={12}/>
                            </button>
                        ) : (
                            <Link to="/gantt" className="btn primary" aria-disabled={navigationLocked || undefined}>
                                {tr('plan.master.openFullSchedule')} <IArrow size={12}/>
                            </Link>
                        )
                    ) : stepId === 'review' ? (
                        st.state === 'blocked' ? (
                            <button type="button" className="btn primary" disabled={navigationLocked} onClick={() => setActive(nextStep(status))}>
                                {tr('plan.master.backFirstIncomplete')} <IArrow size={12}/>
                            </button>
                        ) : (
                            <Link to="/gantt" className="btn" aria-disabled={navigationLocked || undefined}>
                                {tr('plan.master.openSchedule')} <IArrow size={12}/>
                            </Link>
                        )
                    ) : (
                        <>
                            <Link to={secondaryRoute} className="btn" aria-disabled={navigationLocked || undefined}>
                                {tr(`plan.steps.${def.id}.secondaryAction`)}
                            </Link>
                            <Link to={def.route} className="btn primary" aria-disabled={navigationLocked || undefined}>
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
function ReadinessAux({ status, ready, setActive, dataCaveat, share, shareLoading, shareError }: {
    status: Record<string, StepStatus>;
    ready: { done: number; total: number; pct: number };
    setActive: (id: string) => void;
    dataCaveat?: 'refreshing' | 'stale';
    share: PlanShare | null;
    shareLoading: boolean;
    shareError: unknown;
}) {
    const nextId = nextStep(status);
    const nextDef = STEP_DEFS.find(def => def.id === nextId) ?? STEP_DEFS[0];
    const attention = STEP_DEFS.flatMap(def => {
        const stepState = status[def.id];
        return stepState && (stepState.state === 'warn' || stepState.state === 'blocked')
            ? [{ def, state: stepState }]
            : [];
    });
    const firstAttention = attention[0];
    const additionalAttention = attention.slice(1);
    const actionId = firstAttention?.def.id ?? (ready.pct === 100 ? 'review' : nextDef.id);
    const iconTone = dataCaveat === 'stale'
        ? 'var(--warn)'
        : firstAttention?.state.state === 'blocked'
            ? 'var(--blocked)'
            : firstAttention
                ? 'var(--warn)'
                : 'var(--done)';
    const title = firstAttention
        ? tr(`plan.steps.${firstAttention.def.id}.title`)
        : ready.pct === 100
            ? tr('plan.master.readyForReview')
            : tr(`plan.steps.${nextDef.id}.title`);
    const message = dataCaveat === 'stale'
        ? tr('plan.master.stalePlanningData')
        : dataCaveat === 'refreshing'
            ? tr('plan.master.refreshingPlanningData')
            : firstAttention?.state.missing?.[0]
                ?? (ready.pct === 100
                    ? tr('plan.master.allStepsGood')
                    : tr('plan.master.nextStepNamed', { step: tr(`plan.steps.${nextDef.id}.title`) }));

    return (
        <>
            <section className="aux-sect" aria-labelledby="plan-master-next-action-heading">
                <h4 id="plan-master-next-action-heading">{tr('plan.master.nextAction')}</h4>
                <div className="aux-item" aria-live="polite">
                    <div className="ai-icon" style={{color: iconTone}}>
                        {dataCaveat === 'refreshing'
                            ? <IRefresh size={13}/>
                            : firstAttention?.state.state === 'blocked'
                                ? <ILock size={13}/>
                                : firstAttention || dataCaveat === 'stale'
                                    ? <IWarning size={13}/>
                                    : <ICheck size={13} stroke={3}/>}
                    </div>
                    <div style={{flex:1, minWidth:0}}>
                        <div className="ai-title">{title}</div>
                        <div className="ai-sub plan-master-break">{message}</div>
                        <div className="ai-action">
                            <button type="button" className="btn sm" onClick={() => setActive(actionId)}>
                                {ready.pct === 100 && !firstAttention
                                    ? tr('plan.overview.openReview')
                                    : tr('plan.master.openStep')}
                                <IChevR size={10}/>
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            {additionalAttention.length > 0 && (
                <section className="aux-sect" aria-labelledby="plan-master-other-exceptions-heading">
                    <h4 id="plan-master-other-exceptions-heading">{tr('plan.master.otherExceptions')}</h4>
                    <div className="plan-master-aux-list">
                        {additionalAttention.map(({ def, state }) => (
                            <div className="aux-item" key={def.id}>
                                <div
                                    className="ai-icon"
                                    style={{color: state.state === 'blocked' ? 'var(--blocked)' : 'var(--warn)'}}
                                >
                                    {state.state === 'blocked' ? <ILock size={13}/> : <IWarning size={13}/>}
                                </div>
                                <div className="plan-master-min">
                                    <div className="ai-title">{tr(`plan.steps.${def.id}.title`)}</div>
                                    <div className="ai-sub plan-master-break">
                                        {state.missing?.[0] ?? state.summary ?? tr('plan.master.needsAttention')}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            )}

            <section className="aux-sect" aria-labelledby="plan-master-sharing-heading">
                <h4 id="plan-master-sharing-heading">{tr('plan.master.shareSummary')}</h4>
                <div className="aux-item" aria-live="polite">
                    <div
                        className="ai-icon"
                        style={{
                            color: shareError
                                ? 'var(--blocked)'
                                : share
                                    ? 'var(--done)'
                                    : 'var(--ink-3)',
                        }}
                    >
                        {shareLoading
                            ? <IRefresh size={13}/>
                            : shareError
                                ? <IWarning size={13}/>
                                : <Share2 aria-hidden="true" className="h-3.5 w-3.5"/>}
                    </div>
                    <div className="plan-master-min">
                        <div className="ai-title">
                            {shareLoading
                                ? tr('plan.master.loadingShareLink')
                                : shareError
                                    ? tr('plan.master.shareLinkUnavailable')
                                    : share
                                        ? tr('plan.master.sharingActiveTitle')
                                        : ready.pct === 100
                                            ? tr('plan.master.sharingReadyTitle')
                                            : tr('plan.master.sharingNeedsReviewTitle')}
                        </div>
                        <div className="ai-sub plan-master-break">
                            {shareLoading
                                ? tr('plan.master.refreshingPlanningData')
                                : shareError
                                    ? tr('plan.master.shareLinkUnavailableBody')
                                    : share
                                        ? tr('plan.master.planSharedBody', {
                                            date: formatDateTime(share.created_at, i18n.language),
                                        })
                                        : ready.pct === 100
                                            ? tr('plan.master.readyToShareSnapshot')
                                            : tr('plan.master.sharingNeedsReviewBody')}
                        </div>
                    </div>
                </div>
            </section>
        </>
    );
}

function ResponsiveReadinessSummary({ status, ready, currentStepId, setActive, dataCaveat, navigationLocked }: {
    status: Record<string, StepStatus>;
    ready: { done: number; total: number; pct: number };
    currentStepId: string;
    setActive: (id: string) => void;
    dataCaveat?: 'refreshing' | 'stale';
    navigationLocked: boolean;
}) {
    const attention = STEP_DEFS.flatMap(def => {
        const stepState = status[def.id];
        return stepState && (stepState.state === 'warn' || stepState.state === 'blocked')
            ? [{ def, state: stepState }]
            : [];
    });
    const firstAttention = attention[0];
    const nextId = nextStep(status);
    const nextDef = STEP_DEFS.find(def => def.id === nextId) ?? STEP_DEFS[0];
    const actionId = nextDef.id;
    const actionTargetsCurrentStep = actionId === currentStepId;
    const message = dataCaveat === 'stale'
        ? tr('plan.master.stalePlanningData')
        : dataCaveat === 'refreshing'
            ? tr('plan.master.refreshingPlanningData')
            : firstAttention?.state.missing?.[0]
                ?? (ready.pct === 100
                    ? tr('plan.master.readyForReview')
                    : tr('plan.master.nextStepNamed', { step: tr(`plan.steps.${nextDef.id}.title`) }));

    return (
        <section className="plan-master-responsive-readiness" aria-label={tr('plan.master.planReadiness')}>
            <div className="plan-master-responsive-readiness-main">
                <div className="plan-master-responsive-readiness-score tnum" aria-hidden="true">
                    {ready.pct}%
                </div>
                <div className="plan-master-responsive-readiness-copy" aria-live="polite">
                    <div className="between">
                        <strong>{tr('plan.master.stepsComplete', { done: ready.done, total: ready.total })}</strong>
                        {attention.length > 0 && (
                            <span className="pill warn sm">
                                <span className="pdot"/>
                                {attention.length}
                            </span>
                        )}
                    </div>
                    <div
                        className="plan-master-responsive-readiness-track"
                        role="progressbar"
                        aria-label={tr('plan.master.planReadiness')}
                        aria-valuemin={0}
                        aria-valuemax={100}
                        aria-valuenow={ready.pct}
                        aria-busy={dataCaveat === 'refreshing' || undefined}
                    >
                        <span className={ready.pct === 100 ? 'done' : ''} style={{width: `${ready.pct}%`}} />
                    </div>
                    <p className="plan-master-break">{message}</p>
                </div>
                <button
                    type="button"
                    className="btn sm primary"
                    disabled={navigationLocked}
                    onClick={() => {
                        if (actionTargetsCurrentStep) {
                            document.getElementById('plan-master-active-step-heading')?.focus();
                            return;
                        }
                        setActive(actionId);
                    }}
                >
                    {actionTargetsCurrentStep
                        ? tr('plan.master.goToCurrentStep')
                        : ready.pct === 100 && !firstAttention
                        ? tr('plan.overview.openReview')
                        : tr('plan.master.openStep')}
                    <IChevR size={10}/>
                </button>
            </div>

            <details className="plan-master-responsive-readiness-details">
                <summary>
                    <span>{tr('plan.master.viewReadinessDetails')}</span>
                    <span className="tnum">{tr('plan.master.stepsComplete', { done: ready.done, total: ready.total })}</span>
                </summary>
                <div className="plan-master-responsive-readiness-list">
                    {STEP_DEFS.map(def => {
                        const stepState = status[def.id];
                        if (!stepState) return null;
                        return (
                            <div key={def.id} className="plan-master-responsive-readiness-row">
                                <div className="plan-master-min">
                                    <div className="row">
                                        <strong>{tr(`plan.steps.${def.id}.title`)}</strong>
                                        <StepStatePill state={stepState.state}/>
                                    </div>
                                    <p className="plan-master-break">
                                        {stepState.missing?.[0] ?? stepState.summary ?? tr('plan.master.notStarted')}
                                    </p>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </details>
        </section>
    );
}

// ── Main master page ──────────────────────────────────────────────────────────
const PlanMasterPage = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const {
        iterations,
        currentIteration,
        selectIteration,
        teamMembers,
        planningLeafTasks,
        readinessData: r,
        status: rawStatus,
        queryStates,
        isFetching,
        refetch,
    } = usePlanningReadiness();

    const [activeId, setActiveId] = useState<string | null>(null);
    const [iterationFormState, setIterationFormState] = useState<EmbeddedFormState>({
        dirty: false,
        pending: false,
    });
    const [iterationEditorRevision, setIterationEditorRevision] = useState(0);
    const [teamWorkflow, setTeamWorkflow] = useState<TeamWorkflowState | null>(null);
    const [teamFormState, setTeamFormState] = useState<EmbeddedFormState>({
        dirty: false,
        pending: false,
    });
    const [retryPending, setRetryPending] = useState(false);
    // feedback-policy: query loading,error,retry,empty - review renders all states and retains the saved plan on failure.
    const shareQuery = useQuery({
        queryKey: ['plan-share', currentIteration?.id],
        queryFn: () => planShareService.getCurrent(currentIteration!.id),
        enabled: Boolean(currentIteration),
        retry: false,
    });
    // feedback-policy: mutation pending,inline - share actions lock and the review step exposes a recoverable failure state.
    const createShareMutation = useMutation({
        mutationFn: (iterationId: number) => planShareService.create(iterationId),
        onSuccess: share => {
            queryClient.setQueryData(['plan-share', share.iteration_id], share);
            toast.success(t('plan.master.shareLinkCreated'), {
                dedupeKey: `plan-share-created-${share.id}`,
            });
        },
    });
    // feedback-policy: mutation pending,inline - revocation is confirmed, locked while pending, and retryable without changing the plan.
    const revokeShareMutation = useMutation({
        mutationFn: ({ shareId }: { shareId: number; iterationId: number }) => (
            planShareService.revoke(shareId)
        ),
        onSuccess: (_response, variables) => {
            queryClient.setQueryData(['plan-share', variables.iterationId], null);
            toast.success(t('plan.master.shareLinkRevoked'), {
                dedupeKey: 'plan-share-revoked',
            });
        },
    });

    const localizedStatus = localizeStatus(rawStatus, r, t);
    const status: Record<string, StepStatus> = { ...localizedStatus };
    const markDataUnavailable = (
        query: typeof queryStates.team,
        affectedStepIds: string[],
        label: string,
    ) => {
        if (!query.enabled || (query.hasData && !query.isBlockingError)) return;
        const unavailable = query.isBlockingError;
        const missing = unavailable
            ? t('plan.master.sectionUnavailableTitle', { section: label })
            : t('plan.master.sectionLoading', { section: label });
        affectedStepIds.forEach(id => {
            status[id] = { state: 'blocked', missing: [missing] };
        });
    };

    markDataUnavailable(
        queryStates.team,
        ['team', 'schedule', 'review'],
        t('plan.steps.team.title'),
    );
    markDataUnavailable(
        queryStates.tasks,
        ['work', 'blockers', 'schedule', 'review'],
        t('plan.steps.work.title'),
    );
    markDataUnavailable(
        queryStates.gantt,
        ['schedule', 'review'],
        t('plan.steps.schedule.title'),
    );

    const ready = calculateReadiness(status);
    const autoId = nextStep(status);
    const stepId = activeId ?? autoId;
    const activeDef = STEP_DEFS.find(def => def.id === stepId) ?? STEP_DEFS[0];
    const workflowIteration = teamWorkflow
        ? iterations.find(iteration => iteration.id === teamWorkflow.iterationId) ?? null
        : null;
    const workflowIterationSubtitle = workflowIteration
        ? `${workflowIteration.name} · ${formatDate(workflowIteration.start_date, i18n.language)} - ${formatDate(workflowIteration.end_date, i18n.language)}`
        : '';
    const hasRefetchError = Object.values(queryStates).some(query => query.isRefetchError);
    const navigationLocked = stepId === 'iteration' && iterationFormState.pending;
    const currentShare = shareQuery.data ?? null;
    const sharePending = createShareMutation.isPending || revokeShareMutation.isPending;

    const createShare = useCallback(() => {
        if (!currentIteration || sharePending) return;
        createShareMutation.mutate(currentIteration.id);
    }, [createShareMutation, currentIteration, sharePending]);

    const copyShare = useCallback(async () => {
        if (!currentShare) return;
        const shareUrl = `${window.location.origin}/plan/share/${currentShare.public_id}`;
        if (await copyText(shareUrl)) {
            toast.success(t('plan.master.shareLinkCopied'), {
                dedupeKey: `plan-share-copy-${currentShare.id}`,
            });
            return;
        }
        toast.error(t('plan.master.shareLinkCopyFailed'), {
            dedupeKey: `plan-share-copy-failed-${currentShare.id}`,
        });
    }, [currentShare, t, toast]);

    const requestShareRevoke = useCallback(() => {
        if (!currentShare || sharePending) return;
        requestConfirmation({
            title: t('plan.master.revokeShareTitle'),
            description: t('plan.master.revokeShareBody'),
            confirmLabel: t('plan.master.revokeShareLink'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'danger',
            onConfirm: () => revokeShareMutation.mutateAsync({
                shareId: currentShare.id,
                iterationId: currentShare.iteration_id,
            }),
        });
    }, [
        currentShare,
        requestConfirmation,
        revokeShareMutation,
        sharePending,
        t,
    ]);

    const onIterationFormStateChange = useCallback((next: EmbeddedFormState) => {
        setIterationFormState(current => (
            current.dirty === next.dirty && current.pending === next.pending ? current : next
        ));
    }, []);

    const onTeamFormStateChange = useCallback((next: EmbeddedFormState) => {
        setTeamFormState(current => (
            current.dirty === next.dirty && current.pending === next.pending ? current : next
        ));
    }, []);

    const completeIterationDraftTransition = useCallback((
        action: () => void,
        resetDraft = false,
    ) => {
        setIterationFormState({ dirty: false, pending: false });
        if (resetDraft) setIterationEditorRevision(revision => revision + 1);
        action();
    }, []);

    const requestIterationDraftTransition = useCallback((
        action: () => void,
        resetDraft = false,
    ) => {
        if (iterationFormState.pending) {
            toast.info(t('plan.master.savePendingNavigation'), {
                dedupeKey: 'plan-master-period-save-pending',
            });
            return;
        }
        if (!iterationFormState.dirty) {
            completeIterationDraftTransition(action, resetDraft);
            return;
        }

        requestConfirmation({
            title: t('plan.master.draftDiscardTitle'),
            description: t('plan.master.draftDiscardBody'),
            confirmLabel: t('plan.master.draftDiscardConfirm'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'warning',
            onConfirm: () => completeIterationDraftTransition(action, resetDraft),
        });
    }, [
        completeIterationDraftTransition,
        iterationFormState.dirty,
        iterationFormState.pending,
        requestConfirmation,
        t,
        toast,
    ]);

    const setActive = useCallback((id: string) => {
        if (id === stepId) return;
        if (stepId === 'iteration') {
            requestIterationDraftTransition(() => setActiveId(id));
            return;
        }
        setActiveId(id);
    }, [requestIterationDraftTransition, stepId]);

    const closeTeamWorkflowNow = useCallback(() => {
        setTeamWorkflow(null);
        setTeamFormState({ dirty: false, pending: false });
    }, []);

    const requestTeamWorkflowClose = useCallback(() => {
        if (teamFormState.pending) {
            toast.info(t('plan.master.savePendingNavigation'), {
                dedupeKey: 'plan-master-team-save-pending',
            });
            return;
        }
        if (!teamFormState.dirty) {
            closeTeamWorkflowNow();
            return;
        }

        requestConfirmation({
            title: t('plan.master.teamDraftDiscardTitle'),
            description: t('plan.master.teamDraftDiscardBody'),
            confirmLabel: t('plan.master.draftDiscardConfirm'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'warning',
            onConfirm: closeTeamWorkflowNow,
        });
    }, [
        closeTeamWorkflowNow,
        requestConfirmation,
        t,
        teamFormState.dirty,
        teamFormState.pending,
        toast,
    ]);

    const startTeamWorkflow = useCallback((workflow: TeamWorkflow) => {
        if (!currentIteration) {
            setActive('iteration');
            return;
        }
        setActiveId('team');
        setTeamFormState({ dirty: false, pending: false });
        setTeamWorkflow({ kind: workflow, iterationId: currentIteration.id });
    }, [currentIteration, setActive]);

    const retryQueries = useCallback(async (queries?: PlanningQueryFeedback[]) => {
        if (retryPending) return;
        setRetryPending(true);
        try {
            if (queries) {
                await Promise.allSettled(
                    queries.filter(query => query.enabled).map(query => query.refetch()),
                );
            } else {
                await refetch();
            }
        } finally {
            setRetryPending(false);
        }
    }, [refetch, retryPending]);

    const relevantQueries = stepId === 'team'
        ? [queryStates.team]
        : stepId === 'work' || stepId === 'blockers'
            ? [queryStates.tasks]
            : stepId === 'schedule' || stepId === 'review'
                ? [queryStates.team, queryStates.tasks, queryStates.gantt]
                : [];
    const blockingStepQuery = relevantQueries.find(query => query.enabled && query.isBlockingError);
    const stepDataState: StepDataState | undefined = relevantQueries.length > 0
        ? {
            loading: relevantQueries.some(query => (
                query.enabled && query.isLoading && !query.hasData
            )),
            fetching: relevantQueries.some(query => query.enabled && query.isFetching),
            error: blockingStepQuery?.error ?? null,
            retry: () => retryQueries(relevantQueries),
            label: t(`plan.steps.${activeDef.id}.title`),
        }
        : undefined;

    const handlePageClickCapture = useCallback((event: ReactMouseEvent<HTMLDivElement>) => {
        if (
            stepId !== 'iteration'
            || (!iterationFormState.dirty && !iterationFormState.pending)
            || event.defaultPrevented
            || event.button !== 0
            || event.metaKey
            || event.ctrlKey
            || event.shiftKey
            || event.altKey
        ) {
            return;
        }

        const target = event.target;
        if (!(target instanceof Element)) return;
        const anchor = target.closest<HTMLAnchorElement>('a[href]');
        if (!anchor || anchor.target === '_blank' || anchor.hasAttribute('download')) {
            return;
        }
        if (anchor.getAttribute('aria-disabled') === 'true') {
            event.preventDefault();
            requestIterationDraftTransition(() => undefined);
            return;
        }

        const href = anchor.getAttribute('href');
        if (!href || href.startsWith('#')) return;
        event.preventDefault();
        requestIterationDraftTransition(() => navigate(href));
    }, [
        iterationFormState.dirty,
        iterationFormState.pending,
        navigate,
        requestIterationDraftTransition,
        stepId,
    ]);

    useEffect(() => {
        if (!teamWorkflow || workflowIteration) return;
        closeTeamWorkflowNow();
        toast.info(t('plan.master.teamWorkflowPeriodUnavailable'), {
            dedupeKey: 'plan-master-team-period-unavailable',
        });
    }, [closeTeamWorkflowNow, t, teamWorkflow, toast, workflowIteration]);

    useEffect(() => {
        if (
            !iterationFormState.dirty
            && !iterationFormState.pending
            && !teamFormState.dirty
            && !teamFormState.pending
        ) {
            return undefined;
        }
        const warnBeforeUnload = (event: BeforeUnloadEvent) => {
            event.preventDefault();
            event.returnValue = '';
        };
        window.addEventListener('beforeunload', warnBeforeUnload);
        return () => window.removeEventListener('beforeunload', warnBeforeUnload);
    }, [
        iterationFormState.dirty,
        iterationFormState.pending,
        teamFormState.dirty,
        teamFormState.pending,
    ]);

    if (queryStates.iterations.isLoading && !queryStates.iterations.hasData) {
        return <div className="wc" style={{height:'100%', display:'grid', placeItems:'center'}}>
            <div className="empty" role="status" aria-live="polite" aria-busy="true">
                <div className="empty-icon"><IRefresh size={16}/></div>
                <h4>{t('plan.master.planningDataLoading')}</h4>
                <p>{t('plan.master.planningDataLoadingBody')}</p>
            </div>
        </div>;
    }

    if (queryStates.iterations.isBlockingError) {
        return <div className="wc" style={{height:'100%', display:'grid', placeItems:'center'}}>
            <div className="empty" role="alert">
                <div className="empty-icon"><IWarning size={16}/></div>
                <h4>{t('plan.master.planningDataUnavailable')}</h4>
                <p>{t('plan.master.planningDataUnavailableBody')}</p>
                <div className="empty-actions">
                    <button
                        type="button"
                        className="btn primary"
                        disabled={retryPending}
                        onClick={() => { void retryQueries(); }}
                    >
                        <IRefresh size={12}/>
                        {retryPending ? t('plan.master.retryingPlanningData') : t('plan.master.retryPlanningData')}
                    </button>
                </div>
            </div>
            {confirmationDialog}
        </div>;
    }

    return (
        <div
            className="wc"
            style={{height:'100%', display:'flex', flexDirection:'column'}}
            aria-busy={isFetching || undefined}
            onClickCapture={handlePageClickCapture}
        >
            {/* Master header */}
            <header className="plan-master-header">
                <Breadcrumbs items={[
                    { label: t('plan.title'), path: '/plan' },
                    { label: t('plan.hub.planIterationTitle') },
                ]} />
                <div className="between plan-master-header-row">
                    <div className="row plan-master-header-title">
                        <h1 className="wc-page-title">{t('plan.hub.planIterationTitle')}</h1>
                        <span className="muted plan-master-break" style={{fontSize:'var(--wc-type-meta)'}}>
                            {currentIteration
                                ? `${currentIteration.name} · ${formatIterationDates(r.currentIterationStart, r.currentIterationEnd)}`
                                : t('plan.master.noPeriodYet')}
                        </span>
                    </div>
                </div>

                <label className="plan-master-mobile-step-select">
                    <span>{t('plan.master.selectStep')}</span>
                    <select
                        className="input"
                        value={stepId}
                        disabled={navigationLocked}
                        onChange={event => setActive(event.target.value)}
                    >
                        {STEP_DEFS.map((def, index) => (
                            <option key={def.id} value={def.id}>
                                {index + 1}. {t(`plan.steps.${def.id}.title`)}
                            </option>
                        ))}
                    </select>
                </label>
            </header>

            {hasRefetchError && (
                <div className="banner warn plan-master-data-banner" role="status">
                    <IWarning size={14}/>
                    <div className="plan-master-min plan-master-break">
                        {t('plan.master.stalePlanningData')}
                    </div>
                    <button
                        type="button"
                        className="btn sm"
                        disabled={retryPending}
                        onClick={() => { void retryQueries(); }}
                    >
                        <IRefresh size={11}/>
                        {retryPending ? t('plan.master.retryingPlanningData') : t('plan.master.retryPlanningData')}
                    </button>
                </div>
            )}
            {!hasRefetchError && isFetching && (
                <div
                    className="plan-master-refresh-status muted"
                    role="status"
                    aria-live="polite"
                >
                    <IRefresh size={11}/> {t('plan.master.refreshingPlanningData')}
                </div>
            )}

            {/* 3-column master body */}
            <div className="wc-master" style={{flex:1, minHeight:0}}>
                {/* Left rail */}
                <aside className="wc-master-rail" aria-label={t('plan.master.steps')}>
                    <nav className="step-rail plan-master-step-rail" aria-label={t('plan.master.steps')}>
                        {STEP_DEFS.map((def, i) => {
                            const st = status[def.id];
                            const isCurrent = def.id === stepId;
                            const cls = `step-item ${st.state === 'done' ? 'done' : ''} ${isCurrent ? 'current' : ''}`;
                            return (
                                <button type="button" key={def.id} className={cls}
                                     aria-current={isCurrent ? 'step' : undefined}
                                     disabled={navigationLocked}
                                     onClick={() => setActive(def.id)}>
                                    <div className="step-num">
                                        {st.state === 'done' ? <ICheck size={11} stroke={3}/> : (i+1)}
                                    </div>
                                    <div>
                                        <div className="step-title">{t(`plan.steps.${def.id}.title`)}</div>
                                        <span className="sr-only">
                                            {st.state === 'done'
                                                ? t('plan.master.done')
                                                : t('plan.master.incomplete')}
                                        </span>
                                    </div>
                                </button>
                            );
                        })}
                    </nav>
                </aside>

                {/* Main step body */}
                <section className="wc-master-main" aria-labelledby="plan-master-active-step-heading">
                    <ResponsiveReadinessSummary
                        status={status}
                        ready={ready}
                        currentStepId={stepId}
                        setActive={setActive}
                        dataCaveat={hasRefetchError ? 'stale' : isFetching ? 'refreshing' : undefined}
                        navigationLocked={navigationLocked}
                    />
                    <StepBody
                        stepId={stepId}
                        status={status}
                        r={r}
                        tasks={planningLeafTasks}
                        teamMembers={teamMembers}
                        setActive={setActive}
                        iterations={iterations}
                        currentIteration={currentIteration}
                        selectIteration={selectIteration}
                        onStartTeamWorkflow={startTeamWorkflow}
                        iterationFormState={iterationFormState}
                        iterationEditorRevision={iterationEditorRevision}
                        onIterationFormStateChange={onIterationFormStateChange}
                        requestIterationDraftTransition={requestIterationDraftTransition}
                        stepDataState={stepDataState}
                        navigationLocked={navigationLocked}
                        share={currentShare}
                        shareLoading={shareQuery.isLoading}
                        shareError={shareQuery.error ?? createShareMutation.error ?? revokeShareMutation.error}
                        sharePending={sharePending}
                        onRetryShare={() => {
                            createShareMutation.reset();
                            revokeShareMutation.reset();
                            void shareQuery.refetch();
                        }}
                        onCreateShare={createShare}
                        onCopyShare={() => { void copyShare(); }}
                        onRevokeShare={requestShareRevoke}
                    />
                </section>

                {/* Right aux */}
                <aside className="wc-master-aux" aria-label={t('plan.master.planReadiness')}>
                    <ReadinessAux
                        status={status}
                        ready={ready}
                        setActive={setActive}
                        dataCaveat={hasRefetchError ? 'stale' : isFetching ? 'refreshing' : undefined}
                        share={currentShare}
                        shareLoading={shareQuery.isLoading}
                        shareError={shareQuery.error}
                    />
                </aside>
            </div>

            {teamWorkflow?.kind === 'assign' && workflowIteration && (
                <SlideOverDrawer
                    open
                    title={t('plan.master.addPersonToIteration')}
                    subtitle={workflowIterationSubtitle}
                    icon={<ITeam size={14}/>}
                    onClose={requestTeamWorkflowClose}
                    closeDisabled={teamFormState.pending}
                    ariaLabel={t('plan.master.addPersonToIteration')}
                    className="max-w-[720px]"
                >
                    <div className="p-5">
                        <TeamForm
                            key={workflowIteration.id}
                            iterationId={workflowIteration.id}
                            onSuccess={closeTeamWorkflowNow}
                            onCancel={requestTeamWorkflowClose}
                            onStateChange={onTeamFormStateChange}
                        />
                    </div>
                </SlideOverDrawer>
            )}

            {teamWorkflow?.kind === 'import' && workflowIteration && (
                <ImportTeamModal
                    key={workflowIteration.id}
                    iterationId={workflowIteration.id}
                    onClose={requestTeamWorkflowClose}
                    onSuccess={closeTeamWorkflowNow}
                    onStateChange={onTeamFormStateChange}
                />
            )}
            {confirmationDialog}
        </div>
    );
};

export default PlanMasterPage;
