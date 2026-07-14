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

const viewTypeTone: Record<SavedViewType, string> = {
    tasks: 'bg-action-muted text-action border-action',
    triage: 'bg-feedback-purple-muted text-feedback-purple-foreground border-feedback-purple-border',
    projects: 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border',
};

const DashboardCardContent = ({ card }: { card: SavedViewDashboardCard }) => {
    const { t } = useTranslation();
    const Icon = viewTypeIcons[card.view_type];
    const display = savedViewDisplay(card);

    return (
        <>
            <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                        <span className={clsx('inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-medium', viewTypeTone[card.view_type])}>
                            <Icon className="mr-1 h-3 w-3" />
                            {t(viewTypeLabelKeys[card.view_type])}
                        </span>
                        <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-[11px] font-medium text-content-secondary">
                            {t('surfaces.savedViewDashboard.system')}
                        </span>
                    </div>
                    <h3 className="mt-3 truncate text-sm font-semibold text-content-primary">{display.name}</h3>
                    {display.description && (
                        <p className="mt-1 line-clamp-2 min-h-[2rem] text-xs text-content-secondary">
                            {display.description}
                        </p>
                    )}
                    {!display.description && <div className="mt-1 min-h-[2rem]" />}
                </div>
                <div className="shrink-0 text-right">
                    <div className="text-3xl font-bold text-content-primary">{card.count}</div>
                </div>
            </div>
            <div className="mt-4 flex items-center justify-between border-t border-border-subtle pt-3 text-xs font-medium">
                {card.is_valid ? (
                    <>
                        <span className="text-content-secondary">{t('surfaces.savedViewDashboard.openSavedView')}</span>
                        <ArrowRight className="h-4 w-4 text-content-tertiary" />
                    </>
                ) : (
                    <span className="flex min-w-0 items-center gap-1 text-feedback-danger">
                        <AlertTriangle className="h-4 w-4 shrink-0" />
                        <span className="truncate">{card.invalid_reason || t('surfaces.savedViewDashboard.invalidSavedView')}</span>
                    </span>
                )}
            </div>
        </>
    );
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
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
                    {cards.map(card => {
                    const className = clsx(
                        'block min-h-40 rounded-lg border border-border bg-surface-card p-4 shadow-sm transition-colors',
                        card.is_valid
                            ? 'hover:border-action hover:bg-action-muted/30'
                            : 'cursor-not-allowed border-feedback-danger-border bg-feedback-danger-muted/40 opacity-80'
                    );

                    if (!card.is_valid) {
                        return (
                            <div key={card.saved_view_id} className={className}>
                                <DashboardCardContent card={card} />
                            </div>
                        );
                    }

                    return (
                        <Link key={card.saved_view_id} to={card.target_path} className={className}>
                            <DashboardCardContent card={card} />
                        </Link>
                    );
                    })}
                </div>
            )}
        </section>
    );
};
