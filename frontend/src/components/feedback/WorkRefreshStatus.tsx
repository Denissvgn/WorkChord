import { useEffect, useReducer, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { WORKSPACE_QUERY_POLICIES } from '../../features/workQueryFreshness';

export const WorkRefreshStatus = () => {
    const client = useQueryClient();
    const { t } = useTranslation();
    const [, refresh] = useReducer(value => value + 1, 0);
    const [now, setNow] = useState(() => Date.now());
    useEffect(() => {
        const stop = client.getQueryCache().subscribe(() => refresh());
        const timer = window.setInterval(() => { if (document.visibilityState !== 'hidden') setNow(Date.now()); }, 1000);
        return () => { stop(); window.clearInterval(timer); };
    }, [client]);
    const active = client.getQueryCache().getAll().filter(query => query.isActive()
        && WORKSPACE_QUERY_POLICIES[String(query.queryKey[0])] === 'live' && query.state.dataUpdatedAt > 0);
    if (!active.length) return null;
    const oldest = Math.min(...active.map(query => query.state.dataUpdatedAt));
    const stale = active.some(query => query.state.error !== null);
    return <div className="px-4 py-1 text-xs text-content-secondary" role={stale ? 'status' : undefined}>
        {t(stale ? 'teamwork.staleWork' : 'teamwork.refreshAge', { seconds: Math.max(0, Math.floor((now - oldest) / 1000)) })}
    </div>;
};
