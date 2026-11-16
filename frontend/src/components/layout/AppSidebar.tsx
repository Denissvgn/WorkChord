import { useId } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { triageService } from '../../services/triageService';
import { usePlanningNavigationSummary } from '../../features/planningMasters/usePlanningNavigationSummary';
import {
    DESTINATION_GROUPS,
    formatDestinationCounter,
    getCounterSource,
    getDestinationForPath,
} from '../../navigation/destinations';
import type { Destination, DestinationCounterValues } from '../../navigation/destinations';

/**
 * The numbers behind the sidebar counters. A value that is still loading or could not be
 * loaded is left out, so the sidebar shows no counter rather than a wrong one.
 */
const useDestinationCounterValues = (): DestinationCounterValues => {
    const {
        ready,
        isIterationsLoading,
        isIterationsError,
        isReadinessLoading,
        isReadinessError,
    } = usePlanningNavigationSummary();
    // feedback-policy: query loading,error,retry,empty - a counter that is loading or unavailable
    // is hidden; the Triage and Plan pages own the loading and retry states.
    const { data: waiting } = useQuery({
        queryKey: ['triage', { active: true, limit: 100 }],
        queryFn: () => triageService.getAll({ active: true, limit: 100 }),
        staleTime: 60000,
    });

    const planProgressKnown = !isIterationsLoading
        && !isIterationsError
        && !isReadinessLoading
        && !isReadinessError;

    return {
        requestsWaiting: waiting?.length,
        planProgress: planProgressKnown ? { done: ready.done, total: ready.total } : undefined,
    };
};

const isDestinationCurrent = (destination: Destination, pathname: string) => (
    getDestinationForPath(pathname)?.id === destination.id
);

const SidebarDestination = ({
    destination,
    isCurrent,
    counterValues,
    onNavigate,
}: {
    destination: Destination;
    isCurrent: boolean;
    counterValues: DestinationCounterValues;
    onNavigate?: () => void;
}) => {
    const { t } = useTranslation();
    const counterDescriptionId = useId();
    const label = t(destination.labelKey, destination.defaultLabel);
    const Icon = destination.icon;
    const counter = formatDestinationCounter(destination, counterValues);
    const source = getCounterSource(destination);
    const counterDescription = counter === null
        ? undefined
        : source === 'requestsWaiting'
            ? t('nav.counters.requestsWaiting', { count: counterValues.requestsWaiting ?? 0 })
            : t('nav.counters.planProgress', {
                done: counterValues.planProgress?.done ?? 0,
                total: counterValues.planProgress?.total ?? 0,
            });

    return (
        <Link
            to={destination.path}
            className="sb-item"
            aria-current={isCurrent ? 'page' : undefined}
            aria-label={label}
            aria-describedby={counterDescription ? counterDescriptionId : undefined}
            data-destination={destination.id}
            onClick={onNavigate}
        >
            <Icon aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
            <span className="sb-label">{label}</span>
            {counter !== null && (
                <>
                    <span className="sb-count" aria-hidden="true">{counter}</span>
                    <span id={counterDescriptionId} className="sr-only">{counterDescription}</span>
                </>
            )}
        </Link>
    );
};

/** The ten destinations in their groups. The desktop sidebar and the drawer both render this. */
export const SidebarContent = ({ onNavigate }: { onNavigate?: () => void }) => {
    const { t } = useTranslation();
    const location = useLocation();
    const counterValues = useDestinationCounterValues();
    const groupHeadingPrefix = useId();

    return (
        <div className="sidebar-context">
            {DESTINATION_GROUPS.map(group => {
                const headingId = `${groupHeadingPrefix}-${group.id}`;
                const items = group.destinations.map(destination => (
                    <SidebarDestination
                        key={destination.id}
                        destination={destination}
                        isCurrent={isDestinationCurrent(destination, location.pathname)}
                        counterValues={counterValues}
                        onNavigate={onNavigate}
                    />
                ));
                if (!group.labelKey) {
                    return <div key={group.id} className="sb-group sb-group-start">{items}</div>;
                }
                return (
                    <div
                        key={group.id}
                        className="sb-group"
                        role="group"
                        aria-labelledby={headingId}
                    >
                        <p id={headingId} className="sb-group-lbl">
                            {t(group.labelKey)}
                        </p>
                        {items}
                    </div>
                );
            })}
        </div>
    );
};

export const AppSidebar = () => {
    const { t } = useTranslation();

    return (
        <aside
            className="sidebar"
            data-testid="app-sidebar"
            aria-label={t('nav.sidebar')}
        >
            <nav className="sidebar-navigation" aria-label={t('nav.primaryNavigation')}>
                <SidebarContent />
            </nav>
        </aside>
    );
};
