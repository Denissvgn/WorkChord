import { useCallback, useEffect, useState, useSyncExternalStore } from 'react';
import { notifyManager, useQueryClient, type Query, type QueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { WORKSPACE_QUERY_POLICIES } from '../../features/workQueryFreshness';

import { Button } from '../../components/common/Button';
/** Live data older than this reads as possibly out of date. */
const STALE_AFTER_MS = 5 * 60 * 1000;
const RECHECK_MS = 30 * 1000;

/** The live queries on screen that have answered at least once. */
const activeLiveQueries = (client: QueryClient) => client.getQueryCache().getAll().filter(query => query.isActive()
    && WORKSPACE_QUERY_POLICIES[String(query.queryKey[0])] === 'live' && query.state.dataUpdatedAt > 0);

/** Everything the status reads from those queries, as one comparable value. */
const freshnessKey = (queries: Query[]) => queries
    .map(query => [query.queryHash, query.state.dataUpdatedAt, query.state.error === null ? 0 : 1, query.state.fetchStatus].join(':'))
    .join('|');

/** Silent while work data is fresh; says so, with a way to refresh, only when it may be out of date. */
export const WorkRefreshStatus = () => {
    const client = useQueryClient();
    const { t } = useTranslation();
    const [now, setNow] = useState(() => Date.now());
    // The cache also notifies while a page renders its queries. Re-rendering on every notice would
    // interrupt a page that needs more than one time slice to render; that page then renders again,
    // notifies again and may never appear. So the status re-renders only when what it reads changed,
    // and after the notice rather than during another component's render.
    const subscribe = useCallback(
        (onChange: () => void) => client.getQueryCache().subscribe(() => notifyManager.schedule(onChange)),
        [client],
    );
    useSyncExternalStore(subscribe, () => freshnessKey(activeLiveQueries(client)));
    useEffect(() => {
        const timer = window.setInterval(() => { if (document.visibilityState !== 'hidden') setNow(Date.now()); }, RECHECK_MS);
        return () => window.clearInterval(timer);
    }, []);
    const active = activeLiveQueries(client);
    if (!active.length) return null;
    const failed = active.some(query => query.state.error !== null);
    const old = now - Math.min(...active.map(query => query.state.dataUpdatedAt)) > STALE_AFTER_MS;
    if (!failed && !old) return null;
    const refreshing = active.some(query => query.state.fetchStatus === 'fetching');
    return <div className="flex items-center gap-2 px-4 py-1 text-xs text-content-secondary" role="status">
        <span>{t(failed ? 'teamwork.staleWork' : 'teamwork.mayBeStale')}</span>
        <Button type="button" className="font-medium text-action underline disabled:opacity-60" disabled={refreshing}
            onClick={() => { void client.refetchQueries({ predicate: query => active.includes(query) }); }} variant="secondary">
            {t('workFreshness.refresh')}
        </Button>
    </div>;
};
