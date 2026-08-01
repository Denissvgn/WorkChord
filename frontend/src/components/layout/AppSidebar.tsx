import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Bookmark, ChevronRight, Sparkles, TriangleAlert } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { savedViewService } from '../../services/savedViewService';
import { savedViewDisplay } from '../../i18n/seedDisplay';
import type { SavedView } from '../../types/savedView';
import { getWorkspaceForPath } from '../../navigation/workspaces';
import type { NavItem } from '../../navigation/workspaces';
import { SidebarIterationCard } from './SidebarIterationCard';

const SYSTEM_VIEW_ORDER = [
    'tasks_unassigned', 'tasks_blocked', 'tasks_overdue', 'tasks_high_priority',
    'tasks_ready_for_agent', 'tasks_active_this_iteration',
    'triage_needs_triage', 'projects_at_risk',
];

const SAVED_VIEW_ROUTE_PATHS = new Set(['/tasks', '/triage', '/projects']);

const systemOrderIndex = (view: SavedView) => {
    const index = SYSTEM_VIEW_ORDER.indexOf(view.seed_key ?? '');
    return index === -1 ? SYSTEM_VIEW_ORDER.length : index;
};

const systemViews = (views: SavedView[]) => (
    views
        .filter(view => view.scope === 'system' && view.seed_key)
        .sort((left, right) => systemOrderIndex(left) - systemOrderIndex(right) || left.name.localeCompare(right.name))
);

const viewRoutePath = (view: SavedView) => {
    if (view.view_type === 'tasks') return '/tasks';
    if (view.view_type === 'triage') return '/triage';
    return '/projects';
};

const viewPath = (view: SavedView) => `${viewRoutePath(view)}?view=${view.id}`;

const isRouteCurrent = (pathname: string, to: string) => (
    to === '/' ? pathname === '/' : pathname === to || pathname.startsWith(`${to}/`)
);

const SidebarNavItem = ({
    item,
    isCurrent,
    onNavigate,
}: {
    item: NavItem;
    isCurrent: boolean;
    onNavigate?: () => void;
}) => {
    const { t } = useTranslation();
    const label = t(item.labelKey, item.defaultLabel);
    const Icon = item.icon;
    return (
        <Link
            to={item.to}
            className="sb-item"
            aria-current={isCurrent ? 'page' : undefined}
            aria-label={label}
            title={label}
            onClick={onNavigate}
        >
            <Icon aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
            <span className="sb-label">{label}</span>
        </Link>
    );
};

const useCurrentWorkspace = () => {
    const location = useLocation();
    return getWorkspaceForPath(location.pathname);
};

const SavedViewsDisclosure = ({
    allViews,
    hasError,
    isFetching,
    isLoading,
    onNavigate,
    onRetry,
    pathname,
    selectedSavedViewId,
}: {
    allViews: SavedView[];
    hasError: boolean;
    isFetching: boolean;
    isLoading: boolean;
    onNavigate?: () => void;
    onRetry: () => void;
    pathname: string;
    selectedSavedViewId: string | null;
}) => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(selectedSavedViewId !== null);
    const errorMessage = allViews.length > 0
        ? t('nav.someSavedViewsUnavailable')
        : t('nav.savedViewsUnavailable');

    return (
        <details
            className="sb-views"
            open={open}
            onToggle={event => setOpen(event.currentTarget.open)}
        >
            <summary>
                <span className="sb-views-label">
                    <Bookmark aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
                    <span>{t('nav.views')}</span>
                </span>
                <span className="sb-views-summary-state">
                    {hasError ? (
                        <span className="sb-views-warning">
                            <TriangleAlert aria-hidden="true" className="h-3.5 w-3.5" />
                            <span className="sr-only">{errorMessage}</span>
                        </span>
                    ) : isLoading ? (
                        <span role="status" aria-label={t('nav.loadingSavedViews')}>…</span>
                    ) : (
                        <span className="sb-count">{Math.min(allViews.length, 6)}</span>
                    )}
                    <ChevronRight aria-hidden="true" className="sb-views-chevron h-3.5 w-3.5" />
                </span>
            </summary>
            <div className="sb-views-list">
                {allViews.slice(0, 6).map(view => {
                    const label = savedViewDisplay(view).name;
                    const WarningIcon = view.seed_key === 'tasks_overdue' || view.seed_key === 'projects_at_risk'
                        ? TriangleAlert
                        : Sparkles;
                    return (
                        <Link
                            key={view.id}
                            to={viewPath(view)}
                            className="sb-item"
                            aria-current={
                                pathname === viewRoutePath(view)
                                && selectedSavedViewId === String(view.id)
                                    ? 'page'
                                    : undefined
                            }
                            aria-label={label}
                            title={label}
                            onClick={onNavigate}
                        >
                            <WarningIcon aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
                            <span className="sb-label">{label}</span>
                        </Link>
                    );
                })}
                {isLoading && (
                    <div className="sb-status" role="status" aria-live="polite" aria-busy="true">
                        {t('nav.loadingSavedViews')}
                    </div>
                )}
                {hasError && (
                    <div className="sb-recovery" aria-busy={isFetching}>
                        <p role="status" aria-live="polite">{errorMessage}</p>
                        <button
                            type="button"
                            className="btn ghost sm"
                            disabled={isFetching}
                            onClick={onRetry}
                        >
                            {isFetching ? t('nav.retryingSavedViews') : t('nav.retrySavedViews')}
                        </button>
                    </div>
                )}
                {!isLoading && !hasError && allViews.length === 0 && (
                    <div className="sb-status"><span className="sb-label">{t('nav.noSystemViews')}</span></div>
                )}
            </div>
        </details>
    );
};

export const SidebarContent = ({ onNavigate }: { onNavigate?: () => void }) => {
    const { t } = useTranslation();
    const location = useLocation();
    const currentWorkspace = useCurrentWorkspace();
    const CurrentWorkspaceIcon = currentWorkspace.icon;
    const isDeliveryWorkspace = currentWorkspace.key === 'delivery';
    const selectedSavedViewId = new URLSearchParams(location.search).get('view');
    const {
        data: savedViewGroups = { tasks: [], triage: [], projects: [] },
        error: savedViewsError,
        isFetching: savedViewsFetching,
        isLoading: savedViewsLoading,
        refetch: refetchSavedViews,
    } = useQuery({
        queryKey: ['saved-views', 'system-shortcuts'],
        queryFn: async () => {
            const [tasks, triage, projects] = await Promise.all([
                savedViewService.getAll({ view_type: 'tasks' }),
                savedViewService.getAll({ view_type: 'triage' }),
                savedViewService.getAll({ view_type: 'projects' }),
            ]);
            return { tasks: systemViews(tasks), triage: systemViews(triage), projects: systemViews(projects) };
        },
        enabled: isDeliveryWorkspace,
        staleTime: 60000,
    });

    const allViews = [...savedViewGroups.tasks, ...savedViewGroups.triage, ...savedViewGroups.projects];

    return (
        <>
            <div className="sidebar-context">
                <div className="sb-context-heading">
                    <CurrentWorkspaceIcon aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                    <span>{t(currentWorkspace.labelKey, currentWorkspace.defaultLabel)}</span>
                </div>
                {currentWorkspace.items.map(item => (
                    <SidebarNavItem
                        key={item.to}
                        item={item}
                        isCurrent={isRouteCurrent(location.pathname, item.to) && (
                            !SAVED_VIEW_ROUTE_PATHS.has(item.to) || selectedSavedViewId === null
                        )}
                        onNavigate={onNavigate}
                    />
                ))}
            </div>

            {isDeliveryWorkspace && (
                <SavedViewsDisclosure
                    key={selectedSavedViewId ?? 'saved-views'}
                    allViews={allViews}
                    hasError={Boolean(savedViewsError)}
                    isFetching={savedViewsFetching}
                    isLoading={savedViewsLoading}
                    onNavigate={onNavigate}
                    onRetry={() => { void refetchSavedViews(); }}
                    pathname={location.pathname}
                    selectedSavedViewId={selectedSavedViewId}
                />
            )}

            <div className="sb-spacer" />
            {isDeliveryWorkspace && <SidebarIterationCard onNavigate={onNavigate} />}
        </>
    );
};

export const AppSidebar = () => {
    const { t } = useTranslation();
    const currentWorkspace = useCurrentWorkspace();

    return (
        <aside
            className="sidebar"
            data-testid="app-sidebar"
            aria-label={`${t(currentWorkspace.labelKey, currentWorkspace.defaultLabel)} ${t('nav.primaryNavigation')}`}
        >
            <SidebarContent />
        </aside>
    );
};
