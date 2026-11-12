import { useEffect, useReducer, useState } from 'react';
import { notifyManager, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { WORKSPACE_QUERY_POLICIES } from '../../features/workQueryFreshness';

/** Live data older than this reads as possibly out of date. */
const STALE_AFTER_MS = 5 * 60 * 1000;
const RECHECK_MS = 30 * 1000;

/** Silent while work data is fresh; says so, with a way to refresh, only when it may be out of date. */
export const WorkRefreshStatus = () => {
    const client = useQueryClient();
    const { t } = useTranslation();
    const [, refresh] = useReducer(value => value + 1, 0);
    const [now, setNow] = useState(() => Date.now());
    useEffect(() => {
        // The cache notifies while other components render their queries; re-render after that, not during it.
        const stop = client.getQueryCache().subscribe(() => notifyManager.schedule(refresh));
        const timer = window.setInterval(() => { if (document.visibilityState !== 'hidden') setNow(Date.now()); }, RECHECK_MS);
        return () => { stop(); window.clearInterval(timer); };
    }, [client]);
    const active = client.getQueryCache().getAll().filter(query => query.isActive()
        && WORKSPACE_QUERY_POLICIES[String(query.queryKey[0])] === 'live' && query.state.dataUpdatedAt > 0);
    if (!active.length) return null;
    const failed = active.some(query => query.state.error !== null);
    const old = now - Math.min(...active.map(query => query.state.dataUpdatedAt)) > STALE_AFTER_MS;
    if (!failed && !old) return null;
    const refreshing = active.some(query => query.state.fetchStatus === 'fetching');
    return <div className="flex items-center gap-2 px-4 py-1 text-xs text-content-secondary" role="status">
        <span>{t(failed ? 'teamwork.staleWork' : 'teamwork.mayBeStale')}</span>
        <button type="button" className="font-medium text-action underline disabled:opacity-60" disabled={refreshing}
            onClick={() => { void client.refetchQueries({ predicate: query => active.includes(query) }); }}>
            {t('workFreshness.refresh')}
        </button>
    </div>;
};
