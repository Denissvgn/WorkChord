import type { ReactNode, CSSProperties } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { localizeStatus, STEP_DEFS } from '../features/planningMasters/masters';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import { PageHeader, PageLayout } from '../components/ui';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { formatDate } from '../utils/formatDate';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';

// ── Inline SVG icon subset matching the design's icons.jsx ──────────────────
const Svg = ({ d, size = 14, stroke = 1.75, ...rest }: { d: ReactNode; size?: number; stroke?: number; style?: CSSProperties; className?: string }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
         stroke="currentColor" strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" {...rest}>
        {d}
    </svg>
);
const IIteration = (p: { size?: number }) => <Svg {...p} d={<><path d="M2 12a10 10 0 0 1 17-7"/><path d="M22 12a10 10 0 0 1-17 7"/><path d="M19 2v5h-5M5 22v-5h5"/></>}/>;
const ILayers    = (p: { size?: number }) => <Svg {...p} d={<><polygon points="12 2 22 8 12 14 2 8 12 2"/><polyline points="2 12 12 18 22 12"/><polyline points="2 16 12 22 22 16"/></>}/>;
const IInbox     = (p: { size?: number }) => <Svg {...p} d={<><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 6h13l3.5 6v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6z"/></>}/>;
const IWarning   = (p: { size?: number }) => <Svg {...p} d={<><path d="M12 2L1 21h22z"/><path d="M12 9v5M12 18v.5"/></>}/>;
const ISparkle   = (p: { size?: number }) => <Svg {...p} d={<><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"/></>}/>;
const ITeam      = (p: { size?: number }) => <Svg {...p} d={<><circle cx="9" cy="8" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M3 20c.5-3.5 3-5 6-5s5.5 1.5 6 5"/><path d="M14.5 20c.3-2 1.7-3 3.5-3s3.2 1 3.5 3"/></>}/>;
const ITasks     = (p: { size?: number }) => <Svg {...p} d={<><path d="M9 11l3 3 8-8"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></>}/>;
const IGantt     = (p: { size?: number }) => <Svg {...p} d={<><rect x="3" y="5" width="9" height="3" rx="1"/><rect x="7" y="11" width="11" height="3" rx="1"/><rect x="5" y="17" width="7" height="3" rx="1"/></>}/>;
const IArrow     = (p: { size?: number }) => <Svg {...p} d={<><path d="M5 12h14M13 5l7 7-7 7"/></>}/>;
const IChevR     = (p: { size?: number }) => <Svg {...p} d={<polyline points="9 6 15 12 9 18"/>}/>;
const IChevD     = (p: { size?: number }) => <Svg {...p} d={<polyline points="6 9 12 15 18 9"/>}/>;
const ICheck     = (p: { size?: number; stroke?: number }) => <Svg {...p} d={<polyline points="20 6 9 17 4 12"/>}/>;
const ILock      = (p: { size?: number }) => <Svg {...p} d={<><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></>}/>;
const IRefresh   = (p: { size?: number }) => <Svg {...p} d={<><path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/></>}/>;

// ── Step state → CSS class ────────────────────────────────────────────────────
const stepCls = (state: string, isNext: boolean) =>
    state === 'done' ? 'done' : state === 'warn' ? 'warn' : state === 'blocked' ? 'blocked' : isNext ? 'current' : '';

// ── Primary master card (hero with mini-step grid) ────────────────────────────
function PrimaryCard({ ready, status, nextId, onOpen }: {
    ready: { done: number; total: number; pct: number };
    status: Record<string, { state: string; summary?: string; missing?: string[] }>;
    nextId: string;
    onOpen: () => void;
}) {
    const { t } = useTranslation();
    const m = {
        icon: <IIteration size={16}/>,
        title: t('plan.hub.planIterationTitle'),
        desc: t('plan.hub.planIterationDescription'),
        cta: ready.done === 0 ? t('plan.hub.start') : ready.done === ready.total ? t('plan.hub.review') : t('plan.hub.resume'),
    };
    const nextDef = STEP_DEFS.find(s => s.id === nextId);

    return (
        <div className="mcard primary">
            <div className="between" style={{alignItems:'flex-start'}}>
                <div className="row" style={{alignItems:'flex-start', gap: 14}}>
                    <div className="mc-icon">{m.icon}</div>
                    <div>
                        <div className="mc-title">{m.title}</div>
                        <div className="mc-desc">{m.desc}</div>
                    </div>
                </div>
                <button className="btn primary lg" onClick={(e) => { e.stopPropagation(); onOpen(); }}>
                    {m.cta}{nextId !== 'review' && nextDef && <> — {t(`plan.steps.${nextDef.id}.title`).toLowerCase()}</>}
                    <IArrow size={13}/>
                </button>
            </div>

            <div style={{display:'grid', gridTemplateColumns:`repeat(${STEP_DEFS.length}, 1fr)`, gap: 8, marginTop: 10}}>
                {STEP_DEFS.map((def, i) => {
                    const st = status[def.id];
                    const cls = stepCls(st.state, def.id === nextId);
                    return (
                        <div key={def.id} className={`mini-step ${cls}`}
                             style={{border:0, padding:'10px 12px', background:'var(--panel-2)',
                                    borderRadius: 8, display:'grid', gridTemplateColumns:'22px 1fr', gap: 8, alignItems:'flex-start'}}>
                            <div className="ms-dot" style={{width:22, height:22}}>
                                {st.state === 'done'    ? <ICheck size={11} stroke={3}/> :
                                 st.state === 'blocked' ? <ILock size={10}/> :
                                 (i+1)}
                            </div>
                            <div>
                                <div style={{fontSize:'var(--wc-type-meta)', fontWeight:500, color:'var(--ink)', lineHeight:1.3}}>
                                    {t(`plan.steps.${def.id}.title`)}
                                </div>
                                <div className="muted" style={{fontSize:'var(--wc-type-micro)', marginTop:2}}>
                                    {st.state === 'done'    ? (st.summary || t('plan.hub.done')) :
                                     st.state === 'warn'    ? (st.missing?.[0] || t('plan.hub.needsAttention')) :
                                     st.state === 'blocked' ? t('plan.hub.locked') :
                                     def.id === nextId       ? t('plan.hub.nextStep') : t('plan.hub.notStarted')}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

// ── Secondary master card ──────────────────────────────────────────────────────
function MasterCard({ icon, title, desc, meta, cta, muted, onOpen }: {
    icon: ReactNode; title: string; desc: string;
    meta: string; cta: string; muted?: boolean; onOpen: () => void;
}) {
    return (
        <div className={`mcard ${muted ? 'disabled' : ''}`}>
            <div className="row" style={{justifyContent:'space-between'}}>
                <div className="mc-icon">{icon}</div>
                {muted && <span className="pill opt sm">{meta}</span>}
            </div>
            <div>
                <div className="mc-title">{title}</div>
                <div className="mc-desc">{desc}</div>
            </div>
            <div className="mc-foot">
                <div className="mc-meta">{!muted && meta}</div>
                <button className="btn sm" type="button" onClick={onOpen} disabled={muted}>{cta} <IChevR size={11}/></button>
            </div>
        </div>
    );
}

// ── Main page ──────────────────────────────────────────────────────────────────
const PlanPage = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const {
        currentIteration,
        readinessData,
        status: rawStatus,
        ready,
        nextId,
        isLoading,
        isError,
        refetch,
    } = usePlanningReadiness({ includeInbox: true });
    const status = localizeStatus(rawStatus, readinessData, t);
    const nextDef = STEP_DEFS.find(s => s.id === nextId);
    const refreshPlanning = () => { void refetch(); };

    const openMaster = (id: string) => {
        if (id === 'iteration') navigate('/plan/master');
        else if (id === 'project') navigate('/projects');
        else if (id === 'intake')  navigate('/triage');
        else if (id === 'replan')  navigate('/gantt');
        else if (id === 'agent')   navigate('/agent-pipeline');
    };

    const otherMasters = [
        {
            id: 'project', title: t('plan.masters.planProject.title'),
            desc: t('plan.masters.planProject.description'),
            icon: <ILayers size={16}/>, meta: t('plan.hub.acrossIterations'), cta: t('plan.hub.open'),
        },
        {
            id: 'intake', title: t('plan.masters.processIntake.title'),
            desc: t('plan.masters.processIntake.description'),
            icon: <IInbox size={16}/>, meta: t('plan.hub.inQueue', { count: readinessData.inboxCount || 0 }), cta: t('plan.hub.open'),
        },
        {
            id: 'replan', title: t('plan.masters.replanAtRisk.title'),
            desc: t('plan.masters.replanAtRisk.description'),
            icon: <IWarning size={16}/>,
            meta: readinessData.riskCount > 0 ? t('plan.hub.activeSignals', { count: readinessData.riskCount }) : t('plan.hub.noActiveSignals'),
            cta: t('plan.hub.open'),
            muted: readinessData.riskCount === 0,
        },
        {
            id: 'agent', title: t('plan.masters.agentReady.title'),
            desc: t('plan.masters.agentReady.description'),
            icon: <ISparkle size={16}/>, meta: t('plan.hub.beta'), cta: t('plan.hub.open'),
        },
    ];

    if (isLoading) {
        return <PageLayout variant="wide">
            <QueryLoadingState message={t('plan.master.planningDataLoading')} />
        </PageLayout>;
    }

    if (isError) {
        return <PageLayout variant="wide">
            <QueryErrorState
                title={t('plan.master.planningDataUnavailable')}
                message={t('plan.master.planningDataUnavailableBody')}
                onRetry={refreshPlanning}
            />
        </PageLayout>;
    }

    return (
        <PageLayout variant="wide">
                <Breadcrumbs items={[
                    { label: t('nav.workspace'), path: '/' },
                    { label: t('plan.title') },
                ]} />
                {/* Page header */}
                <PageHeader
                    title={t('plan.title')}
                    subtitle={t('plan.hub.subtitle')}
                    actions={(
                    <>
                        <button className="iter-pick" onClick={() => navigate('/plan/master')}>
                            <IIteration size={13}/>
                            <span style={{fontWeight:500}}>
                                {currentIteration?.name || t('plan.hub.pickPeriod')}
                            </span>
                            {currentIteration && (
                                <span className="iter-dates">
                                    · {formatDate(readinessData.currentIterationStart)}–{formatDate(readinessData.currentIterationEnd)}
                                </span>
                            )}
                            <IChevD size={11}/>
                        </button>
                        <button className="btn" onClick={refreshPlanning}><IRefresh size={12}/> {t('plan.hub.refresh')}</button>
                    </>
                    )}
                />

                {/* Readiness summary strip */}
                <div className="card" style={{padding:14, marginBottom:16}}>
                    <div className="between">
                        <div className="row" style={{gap:14}}>
                            <div
                                className={`ring sm ${ready.pct === 100 ? 'done' : ''}`}
                                style={{'--p': ready.pct} as CSSProperties}
                            >
                                <span>{ready.pct}%</span>
                            </div>
                            <div>
                                <div style={{fontWeight:600, fontSize:'var(--wc-type-base)'}}>
                                    {ready.pct === 0
                                        ? t('plan.hub.nothingSetUp')
                                        : ready.pct === 100
                                            ? t('plan.hub.planReadyShare')
                                            : t('plan.hub.stepsComplete', { done: ready.done, total: ready.total })}
                                </div>
                                <div className="muted" style={{fontSize:'var(--wc-type-meta)', marginTop:2}}>
                                    {ready.pct < 100
                                        ? <>{t('plan.hub.next')}: <b style={{color:'var(--ink)'}}>{nextDef ? t(`plan.steps.${nextDef.id}.title`) : ''}</b>
                                            {status[nextId]?.missing?.[0] && <> · {status[nextId].missing![0]}</>}
                                           </>
                                        : t('plan.hub.noActiveRisks')}
                                </div>
                            </div>
                        </div>

                        <div className="row" style={{gap:6}}>
                            {STEP_DEFS.map((def, i) => {
                                const state = status[def.id].state;
                                const cls = state === 'done' ? 'done' : state === 'warn' ? 'warn' : state === 'blocked' ? 'blocked' : 'opt';
                                return (
                                    <span key={def.id} className={`pill ${cls} sm`}>
                                        <span className="pdot"/>
                                        <span style={{fontSize:'var(--wc-type-micro)'}}>{i+1}</span>
                                    </span>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* Recommended heading */}
                <div className="row" style={{marginBottom:10}}>
                    <h3 style={{margin:0, fontSize:'var(--wc-type-label)', fontWeight:600, letterSpacing:'-0.005em'}}>
                        {ready.pct === 0 ? t('plan.hub.recommendedStart')
                          : ready.pct === 100 ? t('plan.hub.recommendedWrap')
                          : t('plan.hub.recommendedResume')}
                    </h3>
                </div>

                {/* Primary card */}
                <PrimaryCard
                    ready={ready}
                    status={status}
                    nextId={nextId}
                    onOpen={() => openMaster('iteration')}
                />

                {/* Other masters */}
                <div className="row" style={{marginTop:28, marginBottom:10}}>
                    <h3 style={{margin:0, fontSize:'var(--wc-type-label)', fontWeight:600, letterSpacing:'-0.005em'}}>{t('plan.hub.otherMasters')}</h3>
                </div>
                <div className="master-grid master-grid-four">
                    {otherMasters.map(m => (
                        <MasterCard
                            key={m.id}
                            icon={m.icon}
                            title={m.title}
                            desc={m.desc}
                            meta={m.meta}
                            cta={m.cta}
                            muted={(m as { muted?: boolean }).muted}
                            onOpen={() => openMaster(m.id)}
                        />
                    ))}
                </div>

                {/* Expert links */}
                <div className="divider" style={{margin:'28px 0 14px'}}/>
                <div className="row" style={{gap:10, color:'var(--ink-3)', fontSize:'var(--wc-type-meta)', flexWrap:'wrap'}}>
                    <span>{t('plan.hub.preferDirect')}</span>
                    <Link to="/iterations" className="btn sm ghost"><IIteration size={12}/> {t('nav.iterations')}</Link>
                    <Link to="/team" className="btn sm ghost"><ITeam size={12}/> {t('nav.team')}</Link>
                    <Link to="/tasks" className="btn sm ghost"><ITasks size={12}/> {t('nav.tasks')}</Link>
                    <Link to="/gantt" className="btn sm ghost"><IGantt size={12}/> {t('nav.gantt')}</Link>
                </div>
            </PageLayout>
    );
};

export default PlanPage;
