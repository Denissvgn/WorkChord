import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { usePlanningReadiness } from '../../features/planningMasters/usePlanningReadiness';

const ChevD = () => (
    <svg width={10} height={10} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
        <polyline points="6 9 12 15 18 9"/>
    </svg>
);

export const SidebarIterationCard = () => {
    const [pickerOpen, setPickerOpen] = useState(false);
    const { t } = useTranslation();
    const { iterations, currentIteration: current, selectedIterationId, selectIteration, ready } = usePlanningReadiness();

    const mode = !current ? 'empty' : ready.pct === 100 ? 'review' : 'partial';
    const ctaLabel = mode === 'empty'
        ? t('plan.sidebar.start')
        : mode === 'review'
            ? t('plan.sidebar.review')
            : t('plan.sidebar.resume', { percent: ready.pct });

    if (iterations.length === 0) {
        return (
            <div className="sb-bottom">
                <Link to="/plan" className="sb-plan-title">{t('plan.sidebar.start')}</Link>
                <div className="sb-plan-sub">{t('plan.sidebar.setupFirst')}</div>
            </div>
        );
    }

    return (
        <div className="sb-plan-card">
            {pickerOpen && (
                <div className="sb-plan-picker">
                    {iterations.map(it => (
                        <button key={it.id}
                            type="button"
                            onClick={() => { selectIteration(it.id); setPickerOpen(false); }}
                            className="sb-plan-option"
                            aria-current={it.id === selectedIterationId ? 'true' : undefined}>
                            {it.name}
                        </button>
                    ))}
                </div>
            )}
            <div className="sb-bottom">
                <div className="between">
                    <button type="button"
                        onClick={() => setPickerOpen(o => !o)}
                        className="sb-plan-select">
                        {current?.name ?? t('plan.hub.pickPeriod')}
                        <ChevD/>
                    </button>
                    <span className="sb-plan-count">
                        {ready.done}/{ready.total}
                    </span>
                </div>
                <div className="sb-plan-progress">
                    <div className={ready.pct === 100 ? 'done' : ''} style={{width:`${ready.pct}%`}}/>
                </div>
                <Link to="/plan/master"
                    className="sb-plan-link">
                    {ctaLabel} →
                </Link>
            </div>
        </div>
    );
};
