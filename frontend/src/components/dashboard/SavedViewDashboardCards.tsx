import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { AlertTriangle, ArrowRight, Bookmark, FolderOpen, Inbox, ListTodo } from 'lucide-react';
import clsx from 'clsx';
import { useTranslation } from 'react-i18next';
import { savedViewService } from '../../services/savedViewService';
import type { SavedViewDashboardCard, SavedViewType } from '../../types/savedView';
import { savedViewDisplay } from '../../i18n/seedDisplay';
import { QueryEmptyState, QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

interface SavedViewDashboardCardsProps {
    iterationId: number;
    title?: string;
    className?: string;
}

const viewTypeLabelKeys: Record<SavedViewType, string> = {
    tasks: 'surfaces.savedViewDashboard.tasks',
    triage: 'surfaces.savedViewDashboard.triage',
    projects: 'surfaces.savedViewDashboard.projects',
};

const viewTypeIcons = {
    tasks: ListTodo,
    triage: Inbox,
    projects: FolderOpen,
};

// A view's type is a category: one neutral chip, told apart by its icon and word, not by status hues.
const viewTypeChip = 'border-border bg-surface-subtle text-content-secondary';

/** One saved view as a compact row: what it is, how many items it holds, and where it opens. */
const DashboardRow = ({ card }: { card: SavedViewDashboardCard }) => {
    const { t } = useTranslation();
    const Icon = viewTypeIcons[card.view_type];
    const display = savedViewDisplay(card);
    const body = <>
        <span className={clsx('inline-flex shrink-0 items-center rounded-full border px-2 py-0.5 text-wc-micro font-medium', viewTypeChip)}>
            <Icon aria-hidden="true" className="mr-1 h-3 w-3" />
            {t(viewTypeLabelKeys[card.view_type])}
        </span>
        <span className="min-w-0 flex-1">
            <span className="block truncate text-sm font-medium text-content-primary">{display.name}</span>
            {!card.is_valid && <span className="flex items-center gap-1 text-xs text-feedback-danger">
                <AlertTriangle aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />{card.invalid_reason || t('surfaces.savedViewDashboard.invalidSavedView')}
            </span>}
        </span>
        <span className="shrink-0 text-base font-semibold tabular-nums text-content-primary">{card.count}</span>
        {card.is_valid && <ArrowRight aria-hidden="true" className="h-4 w-4 shrink-0 text-content-tertiary" />}
    </>;
    const className = 'flex min-h-11 items-center gap-3 px-3 py-2';
    return card.is_valid
        ? <Link to={card.target_path} className={clsx(className, 'hover:bg-surface-hover')} title={display.description ?? undefined}>{body}</Link>
        : <div className={clsx(className, 'bg-feedback-danger-muted/40')}>{body}</div>;
};

export const SavedViewDashboardCards = ({
    iterationId,
    title,
    className,
}: SavedViewDashboardCardsProps) => {
    const { t } = useTranslation();
    const resolvedTitle = title ?? t('surfaces.savedViewDashboard.savedViewSignals');
    const { data: cards = [], isLoading, error, isError, refetch } = useQuery({
        queryKey: ['saved-view-dashboard-cards', iterationId],
        queryFn: () => savedViewService.getDashboardCards(iterationId),
        enabled: iterationId > 0,
        staleTime: 30000,
    });

    if (iterationId <= 0) return null;

    return (
        <section className={clsx('space-y-3', className)}>
            <div className="flex items-center gap-2">
                <Bookmark className="h-5 w-5 text-action" />
                <h2 className="text-lg font-semibold text-content-primary">{resolvedTitle}</h2>
            </div>

            {isError && (
                <QueryErrorState
                    error={error}
                    fallback={t('surfaces.savedViewDashboard.failedToLoadSavedViewCards')}
                    onRetry={() => { void refetch(); }}
                    title={t('surfaces.savedViewDashboard.failedToLoadSavedViewCards')}
                />
            )}

            {isLoading && <QueryLoadingState />}
            {!isLoading && !isError && cards.length === 0 && (
                <QueryEmptyState title={t('queryFeedback.emptyTitle')} />
            )}

            {!isLoading && !isError && cards.length > 0 && (
                <ul className="divide-y divide-border-subtle rounded-lg border border-border bg-surface-card">
                    {cards.map(card => <li key={card.saved_view_id}><DashboardRow card={card} /></li>)}
                </ul>
            )}
        </section>
    );
};
