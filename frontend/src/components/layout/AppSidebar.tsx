import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowRight, Bookmark, ChevronRight, ListFilter, Search, Sparkles, TriangleAlert } from 'lucide-react';
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
const COMPACT_SAVED_VIEW_LIMIT = 5;
const SAVED_VIEW_SEARCH_LIMIT = 8;
const SAVED_VIEW_TYPES = ['tasks', 'triage', 'projects'] as const;

export interface SidebarAttentionAction {
    to: string;
    label: string;
    isError?: boolean;
}

const systemOrderIndex = (view: SavedView) => {
    const index = SYSTEM_VIEW_ORDER.indexOf(view.seed_key ?? '');
    return index === -1 ? SYSTEM_VIEW_ORDER.length : index;
};

const systemViews = (views: SavedView[]) => (
    views
        .filter(view => view.scope === 'system' && view.seed_key)
        .sort((left, right) => (
            systemOrderIndex(left) - systemOrderIndex(right)
            || left.name.localeCompare(right.name, undefined, { numeric: true, sensitivity: 'base' })
        ))
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

const isNavItemCurrent = (
    item: NavItem,
    pathname: string,
    selectedSavedViewId: string | null,
) => (
    isRouteCurrent(pathname, item.to)
    && (!SAVED_VIEW_ROUTE_PATHS.has(item.to) || selectedSavedViewId === null)
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
    const [showAll, setShowAll] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const searchInputRef = useRef<HTMLInputElement>(null);
    const errorMessage = allViews.length > 0
        ? t('nav.someSavedViewsUnavailable')
        : t('nav.savedViewsUnavailable');
    const selectedView = selectedSavedViewId === null
        ? undefined
        : allViews.find(view => String(view.id) === selectedSavedViewId);
    const compactViews = allViews.slice(0, COMPACT_SAVED_VIEW_LIMIT);
    if (selectedView && !compactViews.some(view => view.id === selectedView.id)) {
        compactViews.splice(Math.max(compactViews.length - 1, 0), 1, selectedView);
    }
    const normalizedSearchQuery = searchQuery.trim().toLocaleLowerCase();
    const savedViewTypeLabels = {
        tasks: t('nav.savedViewGroups.tasks'),
        triage: t('nav.savedViewGroups.triage'),
        projects: t('nav.savedViewGroups.projects'),
    };
    const matchingViews = normalizedSearchQuery
        ? allViews.filter(view => (
            savedViewDisplay(view).name.toLocaleLowerCase().includes(normalizedSearchQuery)
            || savedViewTypeLabels[view.view_type].toLocaleLowerCase().includes(normalizedSearchQuery)
        ))
        : allViews;
    const browseViews = matchingViews.slice(0, SAVED_VIEW_SEARCH_LIMIT);
    const browseGroups = SAVED_VIEW_TYPES
        .map(viewType => ({
            viewType,
            label: savedViewTypeLabels[viewType],
            views: browseViews.filter(view => view.view_type === viewType),
        }))
        .filter(group => group.views.length > 0);

    useEffect(() => {
        if (showAll) searchInputRef.current?.focus();
    }, [showAll]);

    const renderViewLink = (view: SavedView) => {
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
    };

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
                        <span
                            className="sb-count"
                            aria-label={t('nav.savedViewCount', { count: allViews.length })}
                        >
                            {allViews.length > COMPACT_SAVED_VIEW_LIMIT && !showAll
                                ? `${COMPACT_SAVED_VIEW_LIMIT}+`
                                : allViews.length}
                        </span>
                    )}
                    <ChevronRight aria-hidden="true" className="sb-views-chevron h-3.5 w-3.5" />
                </span>
            </summary>
            <div className="sb-views-list">
                {showAll ? (
                    <>
                        <label className="sb-views-search">
                            <span className="sr-only">{t('nav.searchSavedViews')}</span>
                            <Search aria-hidden="true" className="h-3.5 w-3.5" />
                            <input
                                ref={searchInputRef}
                                type="search"
                                value={searchQuery}
                                onChange={event => setSearchQuery(event.target.value)}
                                placeholder={t('nav.searchSavedViewsPlaceholder')}
                                aria-label={t('nav.searchSavedViews')}
                            />
                        </label>
                        <p className="sb-views-result-count" role="status">
                            {t('nav.savedViewSearchResults', { count: matchingViews.length })}
                        </p>
                        {browseGroups.map(group => (
                            <section
                                key={group.viewType}
                                className="sb-views-group"
                                aria-labelledby={`saved-view-group-${group.viewType}`}
                            >
                                <h3 id={`saved-view-group-${group.viewType}`}>{group.label}</h3>
                                <div>{group.views.map(renderViewLink)}</div>
                            </section>
                        ))}
                        {matchingViews.length === 0 && (
                            <div className="sb-status">{t('nav.noSavedViewMatches')}</div>
                        )}
                        {matchingViews.length > SAVED_VIEW_SEARCH_LIMIT && (
                            <div className="sb-status">
                                {t('nav.savedViewSearchLimit', {
                                    shown: SAVED_VIEW_SEARCH_LIMIT,
                                    count: matchingViews.length,
                                })}
                            </div>
                        )}
                    </>
                ) : compactViews.map(renderViewLink)}
                {!isLoading
                    && (allViews.length > COMPACT_SAVED_VIEW_LIMIT || showAll)
                    && (
                    <button
                        type="button"
                        className="sb-item sb-views-toggle"
                        aria-expanded={showAll}
                        onClick={() => {
                            if (showAll) setSearchQuery('');
                            setShowAll(!showAll);
                        }}
                    >
                        <ListFilter aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
                        <span className="sb-label">
                            {showAll
                                ? t('nav.showFewerSavedViews')
                                : t('nav.viewAllSavedViews', { count: allViews.length })}
                        </span>
                    </button>
                )}
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

const MoreDestinationsDisclosure = ({
    items,
    onNavigate,
    pathname,
    selectedSavedViewId,
}: {
    items: NavItem[];
    onNavigate?: () => void;
    pathname: string;
    selectedSavedViewId: string | null;
}) => {
    const { t } = useTranslation();
    const hasCurrentItem = items.some(item => isNavItemCurrent(item, pathname, selectedSavedViewId));
    const [open, setOpen] = useState(hasCurrentItem);

    return (
        <details
            className="sb-views sb-more"
            open={open}
            onToggle={event => setOpen(event.currentTarget.open)}
        >
            <summary>
                <span className="sb-views-label">
                    <span>{t('nav.more')}</span>
                </span>
                <ChevronRight aria-hidden="true" className="sb-views-chevron h-3.5 w-3.5" />
            </summary>
            <div className="sb-views-list">
                {items.map(item => (
                    <SidebarNavItem
                        key={item.to}
                        item={item}
                        isCurrent={isNavItemCurrent(item, pathname, selectedSavedViewId)}
                        onNavigate={onNavigate}
                    />
                ))}
            </div>
        </details>
    );
};

export const SidebarContent = ({
    attentionAction,
    onNavigate,
}: {
    attentionAction?: SidebarAttentionAction;
    onNavigate?: () => void;
}) => {
    const { t } = useTranslation();
    const location = useLocation();
    const currentWorkspace = useCurrentWorkspace();
    const CurrentWorkspaceIcon = currentWorkspace.icon;
    const isDeliveryWorkspace = currentWorkspace.key === 'delivery';
    const isPlanningWorkspace = currentWorkspace.key === 'planning';
    const selectedSavedViewId = new URLSearchParams(location.search).get('view');
    const {
        data: savedViewGroups = {
            tasks: [],
            triage: [],
            projects: [],
            hasPartialError: false,
        },
        error: savedViewsError,
        isFetching: savedViewsFetching,
        isLoading: savedViewsLoading,
        refetch: refetchSavedViews,
    } = useQuery({
        queryKey: ['saved-views', 'system-shortcuts'],
        queryFn: async () => {
            const [tasks, triage, projects] = await Promise.allSettled([
                savedViewService.getAll({ view_type: 'tasks' }),
                savedViewService.getAll({ view_type: 'triage' }),
                savedViewService.getAll({ view_type: 'projects' }),
            ]);
            const results = [tasks, triage, projects];
            if (results.every(result => result.status === 'rejected')) {
                throw tasks.status === 'rejected'
                    ? tasks.reason
                    : new Error('Saved views are unavailable');
            }
            return {
                tasks: tasks.status === 'fulfilled' ? systemViews(tasks.value) : [],
                triage: triage.status === 'fulfilled' ? systemViews(triage.value) : [],
                projects: projects.status === 'fulfilled' ? systemViews(projects.value) : [],
                hasPartialError: results.some(result => result.status === 'rejected'),
            };
        },
        enabled: isDeliveryWorkspace,
        staleTime: 60000,
    });

    const allViews = [...savedViewGroups.tasks, ...savedViewGroups.triage, ...savedViewGroups.projects];
    const coreItems = currentWorkspace.items.filter(item => !item.secondary);
    const secondaryItems = currentWorkspace.items.filter(item => item.secondary);

    return (
        <>
            <div className="sidebar-context">
                <div
                    className="sb-context-heading"
                    data-sidebar-context-heading
                    tabIndex={-1}
                >
                    <CurrentWorkspaceIcon aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                    <span>{t(currentWorkspace.labelKey, currentWorkspace.defaultLabel)}</span>
                </div>
                {attentionAction && (
                    <Link
                        to={attentionAction.to}
                        className={`sb-item sb-attention-action${attentionAction.isError ? ' error' : ''}`}
                        data-sidebar-attention-action
                        onClick={onNavigate}
                    >
                        {attentionAction.isError ? (
                            <TriangleAlert aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
                        ) : (
                            <ArrowRight aria-hidden="true" className="h-[14px] w-[14px] shrink-0" />
                        )}
                        <span className="sb-label">{attentionAction.label}</span>
                    </Link>
                )}
                {coreItems.map(item => (
                    <SidebarNavItem
                        key={item.to}
                        item={item}
                        isCurrent={isNavItemCurrent(item, location.pathname, selectedSavedViewId)}
                        onNavigate={onNavigate}
                    />
                ))}
                {secondaryItems.length > 0 && (
                    <MoreDestinationsDisclosure
                        key={`${currentWorkspace.key}:${location.pathname}`}
                        items={secondaryItems}
                        pathname={location.pathname}
                        selectedSavedViewId={selectedSavedViewId}
                        onNavigate={onNavigate}
                    />
                )}
            </div>

            {isDeliveryWorkspace && (
                <SavedViewsDisclosure
                    key={selectedSavedViewId ?? 'saved-views'}
                    allViews={allViews}
                    hasError={Boolean(savedViewsError) || savedViewGroups.hasPartialError}
                    isFetching={savedViewsFetching}
                    isLoading={savedViewsLoading}
                    onNavigate={onNavigate}
                    onRetry={() => { void refetchSavedViews(); }}
                    pathname={location.pathname}
                    selectedSavedViewId={selectedSavedViewId}
                />
            )}

            <div className="sb-spacer" />
            {isPlanningWorkspace && <SidebarIterationCard onNavigate={onNavigate} />}
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
            aria-label={t('nav.areaDestinations', {
                area: t(currentWorkspace.labelKey, currentWorkspace.defaultLabel),
            })}
        >
            <SidebarContent />
        </aside>
    );
};
