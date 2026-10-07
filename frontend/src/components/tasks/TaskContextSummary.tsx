import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import type { TaskDetail } from '../../types/task';
import { taskService } from '../../services/taskService';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

export const TaskContextSummary = ({ detail, onNavigate, onReload }: { detail: TaskDetail; onNavigate?: (id: number) => void; onReload?: () => void }) => {
    const { t } = useTranslation();
    const [childrenCursor, setChildrenCursor] = useState(0);
    const [dependenciesCursor, setDependenciesCursor] = useState(0);
    // feedback-policy: query loading,error,retry,empty
    const query = useQuery({
        queryKey: ['taskContext', detail.task.id, detail.task.version, childrenCursor, dependenciesCursor],
        queryFn: async () => {
            const page = await taskService.getDetail(detail.task.id, { children_after_id: childrenCursor, dependencies_after_id: dependenciesCursor });
            if (page.task.version !== detail.task.version) throw new Error('Task changed while paging. Refresh current work.');
            return page;
        },
        initialData: childrenCursor === 0 && dependenciesCursor === 0 ? detail : undefined,
        staleTime: 30_000,
    });
    return <details className="mb-5 border-b border-border pb-4 text-sm">
        <summary className="cursor-pointer font-medium text-content-primary">{t('domain.contextComplete')}</summary>
        {query.isLoading && <QueryLoadingState className="min-h-12" />}
        {query.isError && <QueryErrorState error={query.error} fallback={t('taskEditor.loadFailed')} onRetry={() => onReload ? onReload() : void query.refetch()} />}
        {!query.isError && query.data && <div className="mt-3 space-y-3">
            {query.data.ancestors.length > 0 && <nav aria-label={t('domain.ancestors')} className="flex flex-wrap gap-2">
                {query.data.ancestors.map(item => <Link className="text-action underline" key={item.id} to={`/tasks?task=${item.id}`} onClick={event => { if (onNavigate) { event.preventDefault(); onNavigate(item.id); } }}>{item.title}</Link>)}
            </nav>}
            {(['children', 'dependencies'] as const).map(kind => <div key={kind}>
                <h4 className="mb-1 font-medium text-content-primary">{t(kind === 'children' ? 'domain.children' : 'surfaces.taskForm.dependencies')}</h4>
                <ul className="space-y-1">{query.data![kind].items.map(item => <li key={item.id}>
                    <Link className="break-words text-action underline" to={`/tasks?task=${item.id}`} onClick={event => { if (onNavigate) { event.preventDefault(); onNavigate(item.id); } }}>{item.title}</Link>
                </li>)}</ul>
                {query.data![kind].items.length === 0 && <p className="text-content-secondary">{t('common.none')}</p>}
                {query.data![kind].has_more && <Button type="button" size="sm" variant="ghost" onClick={() => (kind === 'children' ? setChildrenCursor : setDependenciesCursor)(query.data![kind].next_after_id!)}>{t('domain.moreResults')}</Button>}
            </div>)}
            {(childrenCursor > 0 || dependenciesCursor > 0) && <Button type="button" size="sm" variant="ghost" onClick={() => { setChildrenCursor(0); setDependenciesCursor(0); }}>{t('domain.firstPage')}</Button>}
            {(!query.data.execution_context_complete || !query.data.ancestors_complete || query.data.children.has_more || query.data.dependencies.has_more) && <p className="text-content-secondary">{t('domain.boundedContext')}</p>}
        </div>}
    </details>;
};
