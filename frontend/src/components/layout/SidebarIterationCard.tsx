import { type KeyboardEvent, useEffect, useId, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { usePlanningNavigationSummary } from '../../features/planningMasters/usePlanningNavigationSummary';

const ChevD = () => (
    <svg width={10} height={10} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
        <polyline points="6 9 12 15 18 9"/>
    </svg>
);

export const SidebarIterationCard = ({ onNavigate }: { onNavigate?: () => void }) => {
    const [pickerOpen, setPickerOpen] = useState(false);
    const pickerId = useId();
    const pickerTriggerRef = useRef<HTMLButtonElement>(null);
    const restorePickerFocusRef = useRef(false);
    const { t } = useTranslation();
    const {
        iterations,
        currentIteration: current,
        selectedIterationId,
        selectIteration,
        ready,
        isIterationsLoading,
        isIterationsError,
        isIterationsFetching,
        isReadinessLoading,
        isReadinessError,
        isReadinessFetching,
        refetch,
    } = usePlanningNavigationSummary();

    const closePickerAndRestoreFocus = () => {
        restorePickerFocusRef.current = true;
        setPickerOpen(false);
    };

    const handlePickerKeyDown = (event: KeyboardEvent<HTMLElement>) => {
        if (event.key !== 'Escape' || !pickerOpen) return;

        event.preventDefault();
        closePickerAndRestoreFocus();
    };

    useEffect(() => {
        if (pickerOpen || !restorePickerFocusRef.current) return;

        restorePickerFocusRef.current = false;
        pickerTriggerRef.current?.focus();
    }, [pickerOpen]);

    if (isIterationsLoading && iterations.length === 0) {
        return (
            <div className="sb-bottom" aria-busy="true">
                <div className="sb-plan-sub" role="status">{t('plan.sidebar.loadingPeriods')}</div>
            </div>
        );
    }

    if (isIterationsError && iterations.length === 0) {
        return (
            <div className="sb-bottom" aria-busy={isIterationsFetching}>
                <div className="sb-plan-sub" role="status">{t('plan.sidebar.periodsUnavailable')}</div>
                <button
                    type="button"
                    className="btn ghost sm"
                    disabled={isIterationsFetching}
                    onClick={() => { void refetch(); }}
                >
                    {isIterationsFetching ? t('plan.sidebar.retrying') : t('plan.sidebar.retry')}
                </button>
            </div>
        );
    }

    const mode = !current ? 'empty' : ready.pct === 100 ? 'review' : 'partial';
    const progressUnavailable = isIterationsError || isReadinessError;
    const progressLoading = !progressUnavailable && isReadinessLoading;
    const progressRetrying = progressUnavailable && (isIterationsFetching || isReadinessFetching);
    const ctaLabel = (progressUnavailable || progressLoading) && current
        ? t('plan.sidebar.open')
        : mode === 'empty'
        ? t('plan.sidebar.start')
        : mode === 'review'
            ? t('plan.sidebar.review')
            : t('plan.sidebar.resume', { percent: ready.pct });

    if (iterations.length === 0) {
        return (
            <div className="sb-bottom">
                <Link to="/plan" className="sb-plan-title" onClick={onNavigate}>{t('plan.sidebar.start')}</Link>
                <div className="sb-plan-sub">{t('plan.sidebar.setupFirst')}</div>
            </div>
        );
    }

    return (
        <div className="sb-plan-card">
            <div className="sb-bottom">
                <div className="between">
                    <button
                        ref={pickerTriggerRef}
                        type="button"
                        onClick={() => setPickerOpen(o => !o)}
                        className="sb-plan-select"
                        aria-expanded={pickerOpen}
                        aria-controls={pickerOpen ? pickerId : undefined}
                        aria-haspopup="true"
                        onKeyDown={handlePickerKeyDown}
                    >
                        {current?.name ?? t('plan.hub.pickPeriod')}
                        <ChevD/>
                    </button>
                    {!progressUnavailable && !progressLoading && (
                        <span className="sb-plan-count">
                            {ready.done}/{ready.total}
                        </span>
                    )}
                </div>
                {pickerOpen && (
                    <div
                        id={pickerId}
                        className="sb-plan-picker"
                        role="group"
                        aria-label={t('plan.sidebar.choosePeriod')}
                    >
                        {iterations.map(it => (
                            <button
                                key={it.id}
                                type="button"
                                onClick={() => {
                                    selectIteration(it.id);
                                    closePickerAndRestoreFocus();
                                }}
                                className="sb-plan-option"
                                aria-pressed={it.id === selectedIterationId}
                                onKeyDown={handlePickerKeyDown}
                            >
                                {it.name}
                            </button>
                        ))}
                    </div>
                )}
                {progressLoading && (
                    <div className="sb-plan-sub" role="status" aria-busy="true">
                        {t('plan.sidebar.loadingProgress')}
                    </div>
                )}
                {progressUnavailable && (
                    <div aria-busy={progressRetrying}>
                        <div className="sb-plan-sub" role="status">{t('plan.sidebar.progressUnavailable')}</div>
                        <button
                            type="button"
                            className="btn ghost sm"
                            disabled={progressRetrying}
                            onClick={() => { void refetch(); }}
                        >
                            {progressRetrying ? t('plan.sidebar.retrying') : t('plan.sidebar.retry')}
                        </button>
                    </div>
                )}
                {!progressUnavailable && !progressLoading && (
                    <div className="sb-plan-progress">
                        <div className={ready.pct === 100 ? 'done' : ''} style={{width:`${ready.pct}%`}}/>
                    </div>
                )}
                <Link to="/plan/master"
                    className="sb-plan-link"
                    onClick={onNavigate}>
                    {ctaLabel} →
                </Link>
            </div>
        </div>
    );
};
