import i18n from '../../i18n/i18n';
import { useMemo, useState, type KeyboardEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { AlertCircle, Link2, Loader2, Plus, Search, Trash2, X } from 'lucide-react';
import clsx from 'clsx';
import { requestSourceService } from '../../services/requestSourceService';
import type {
    RequestSource,
    RequestSourceLinkCreate,
    RequestSourceTargetType,
    RequestSourceType,
} from '../../types/requestSource';
import { getApiErrorMessage } from '../../utils/apiError';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { safeExternalHref } from '../../utils/safeUrl';

const t = i18n.t.bind(i18n);

interface RequestSourceLinksPanelProps {
    targetType: RequestSourceTargetType;
    targetId: number;
    initialCount?: number;
    title?: string;
    compact?: boolean;
    onChanged?: () => void;
}

const sourceTypeOptions: Array<{ value: RequestSourceType; labelKey: string }> = [
    { value: 'customer', labelKey: 'surfaces.requestSourceLinks.sourceTypes.customer' },
    { value: 'support', labelKey: 'surfaces.requestSourceLinks.sourceTypes.support' },
    { value: 'email', labelKey: 'surfaces.requestSourceLinks.sourceTypes.email' },
    { value: 'web', labelKey: 'surfaces.requestSourceLinks.sourceTypes.web' },
    { value: 'internal', labelKey: 'surfaces.requestSourceLinks.sourceTypes.internal' },
    { value: 'import', labelKey: 'surfaces.requestSourceLinks.sourceTypes.import' },
];

const nullableTrim = (value: string) => {
    const trimmed = value.trim();
    return trimmed || null;
};

const requestLabel = (source: RequestSource) => (
    source.title || source.external_key || source.source_url || `Request #${source.id}`
);

const sourceTypeLabel = (sourceType: string) => (
    sourceTypeOptions.find(option => option.value === sourceType)?.labelKey
        ? t(sourceTypeOptions.find(option => option.value === sourceType)!.labelKey)
        : sourceType
);

export const RequestSourceLinksPanel = ({
    targetType,
    targetId,
    initialCount = 0,
    title,
    compact = false,
    onChanged,
}: RequestSourceLinksPanelProps) => {
    const queryClient = useQueryClient();
    const resolvedTitle = title ?? t('surfaces.requestSourceLinks.requests');
    const linkQueryKey = ['request-source-links', targetType, targetId];
    const [newTitle, setNewTitle] = useState('');
    const [newUrl, setNewUrl] = useState('');
    const [sourceType, setSourceType] = useState<RequestSourceType>('customer');
    const [sourceName, setSourceName] = useState('');
    const [priorityHint, setPriorityHint] = useState('');
    const [searchText, setSearchText] = useState('');
    const [searchType, setSearchType] = useState<RequestSourceType | ''>('');
    const [error, setError] = useState<string | null>(null);
    const [deletingLinkId, setDeletingLinkId] = useState<number | null>(null);
    const [linkingSourceId, setLinkingSourceId] = useState<number | null>(null);

    const linksQuery = useQuery({
        queryKey: linkQueryKey,
        queryFn: () => requestSourceService.getLinks(targetType, targetId),
        enabled: targetId > 0,
    });

    const trimmedSearch = searchText.trim();
    const searchQuery = useQuery({
        queryKey: ['request-sources', trimmedSearch, searchType],
        queryFn: () => requestSourceService.search({
            q: trimmedSearch,
            source_type: searchType,
            limit: 8,
        }),
        enabled: trimmedSearch.length > 0,
    });
    const links = useMemo(() => linksQuery.data ?? [], [linksQuery.data]);
    const linksAreLoading = linksQuery.isLoading;
    const linksAreFetching = linksQuery.isFetching;
    const sourceResults = searchQuery.data ?? [];
    const searchIsFetching = searchQuery.isFetching;

    const linkedSourceIds = useMemo(
        () => new Set(links.map(link => link.request_source_id)),
        [links],
    );
    const count = linksAreLoading ? initialCount : links.length;

    const resetCreateForm = () => {
        setNewTitle('');
        setNewUrl('');
        setSourceName('');
        setPriorityHint('');
        setSourceType('customer');
    };

    const handleMutationSuccess = () => {
        setError(null);
        queryClient.invalidateQueries({ queryKey: linkQueryKey });
        queryClient.invalidateQueries({ queryKey: ['request-sources'] });
        onChanged?.();
    };

    const createLinkMutation = useMutation({
        mutationFn: (data: RequestSourceLinkCreate) => requestSourceService.createLink(data),
        onSuccess: () => {
            resetCreateForm();
            handleMutationSuccess();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.requestSourceLinks.linkFailed')));
        },
    });

    const linkExistingMutation = useMutation({
        mutationFn: (requestSourceId: number) => requestSourceService.createLink({
            target_type: targetType,
            target_id: targetId,
            request_source_id: requestSourceId,
        }),
        onSuccess: () => {
            setSearchText('');
            setLinkingSourceId(null);
            handleMutationSuccess();
        },
        onError: (err: unknown) => {
            setLinkingSourceId(null);
            setError(getApiErrorMessage(err, t('surfaces.requestSourceLinks.linkExistingFailed')));
        },
    });

    const deleteLinkMutation = useMutation({
        mutationFn: (linkId: number) => requestSourceService.deleteLink(linkId),
        onSuccess: () => {
            setDeletingLinkId(null);
            handleMutationSuccess();
        },
        onError: (err: unknown) => {
            setDeletingLinkId(null);
            setError(getApiErrorMessage(err, t('surfaces.requestSourceLinks.unlinkFailed')));
        },
    });

    const handleCreate = () => {
        const titleValue = nullableTrim(newTitle) || nullableTrim(newUrl);
        if (!titleValue) {
            setError(t('surfaces.requestSourceLinks.titleOrUrlRequired'));
            return;
        }

        const parsedPriority = priorityHint ? Number(priorityHint) : null;
        createLinkMutation.mutate({
            target_type: targetType,
            target_id: targetId,
            request_source: {
                title: titleValue,
                source_type: sourceType,
                source_name: nullableTrim(sourceName),
                source_url: nullableTrim(newUrl),
                priority_hint: Number.isFinite(parsedPriority) ? parsedPriority : null,
            },
        });
    };

    const handleCreateKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
        if (
            event.key !== 'Enter'
            || event.nativeEvent.isComposing
        ) {
            return;
        }

        event.preventDefault();
        if (
            createLinkMutation.isPending
            || (!newTitle.trim() && !newUrl.trim())
        ) {
            return;
        }
        handleCreate();
    };

    return (
        <section className={clsx(
            'rounded-lg border border-border bg-surface-card',
            compact ? 'p-3' : 'p-5',
        )}>
            <div className="mb-3 flex items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                    <Link2 className="h-4 w-4 text-action" />
                    <h3 className={clsx('font-semibold text-content-primary', compact ? 'text-sm' : 'text-lg')}>
                        {resolvedTitle}
                    </h3>
                    <span className="rounded-full bg-action-muted px-2 py-0.5 text-xs font-medium text-action">
                        {count}
                    </span>
                </div>
                {linksAreFetching && !linksAreLoading && (
                    <Loader2 className="h-4 w-4 animate-spin text-content-tertiary" />
                )}
            </div>

            {linksQuery.isLoading && <QueryLoadingState className="mb-3 min-h-16 py-3" />}
            {linksQuery.isError && (
                <QueryErrorState className="mb-3" error={linksQuery.error} onRetry={() => void linksQuery.refetch()} />
            )}
            {searchQuery.isError && (
                <QueryErrorState
                    className="mb-3"
                    error={searchQuery.error}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => void searchQuery.refetch()}
                />
            )}

            {error && (
                <div className="mb-3 flex items-start justify-between gap-2 rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-xs text-feedback-danger-foreground">
                    <span>{error}</span>
                    <button
                        type="button"
                        onClick={() => setError(null)}
                        className="rounded p-0.5 text-feedback-danger hover:bg-feedback-danger-muted-hover"
                        aria-label={t('surfaces.requestSourceLinks.dismissRequestSourceError')}
                    >
                        <X className="h-3.5 w-3.5" />
                    </button>
                </div>
            )}

            <div className="space-y-2">
                <div className="grid grid-cols-1 gap-2 md:grid-cols-[1fr_1fr_auto]">
                    <input
                        type="text"
                        value={newTitle}
                        onKeyDown={handleCreateKeyDown}
                        onChange={event => setNewTitle(event.target.value)}
                        placeholder={t('surfaces.requestSourceLinks.requestTitle')}
                        className="rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                    <input
                        type="url"
                        value={newUrl}
                        onKeyDown={handleCreateKeyDown}
                        onChange={event => setNewUrl(event.target.value)}
                        placeholder={t('surfaces.requestSourceLinks.requestURL')}
                        className="rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                    <button
                        type="button"
                        onClick={handleCreate}
                        disabled={createLinkMutation.isPending || (!newTitle.trim() && !newUrl.trim())}
                        className="inline-flex items-center justify-center gap-1 rounded-md bg-action px-3 py-2 text-sm font-medium text-content-emphasis hover:bg-action-hover disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {createLinkMutation.isPending ? (
                            <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                            <Plus className="h-4 w-4" />
                        )}
                        {t('surfaces.requestSourceLinks.add')}
                    </button>
                </div>

                <div className="grid grid-cols-1 gap-2 md:grid-cols-[150px_1fr_110px]">
                    <select
                        value={sourceType}
                        onChange={event => setSourceType(event.target.value as RequestSourceType)}
                        className="rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    >
                        {sourceTypeOptions.map(option => (
                            <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                        ))}
                    </select>
                    <input
                        type="text"
                        value={sourceName}
                        onKeyDown={handleCreateKeyDown}
                        onChange={event => setSourceName(event.target.value)}
                        placeholder={t('surfaces.requestSourceLinks.sourceName')}
                        className="rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                    <input
                        type="number"
                        min={1}
                        max={10}
                        value={priorityHint}
                        onKeyDown={handleCreateKeyDown}
                        onChange={event => setPriorityHint(event.target.value)}
                        placeholder={t('surfaces.requestSourceLinks.priority')}
                        className="rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </div>
            </div>

            <div className="mt-4 space-y-2">
                <div className="grid grid-cols-1 gap-2 md:grid-cols-[1fr_150px]">
                    <div className="relative">
                        <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
                        <input
                            type="text"
                            value={searchText}
                            onChange={event => setSearchText(event.target.value)}
                            placeholder={t('surfaces.requestSourceLinks.searchExistingRequests')}
                            className="w-full rounded-md border border-border-strong py-2 pl-9 pr-3 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                        />
                    </div>
                    <select
                        value={searchType}
                        onChange={event => setSearchType(event.target.value as RequestSourceType | '')}
                        className="rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    >
                        <option value="">{t('surfaces.requestSourceLinks.anyType')}</option>
                        {sourceTypeOptions.map(option => (
                            <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                        ))}
                    </select>
                </div>

                {trimmedSearch && (
                    <div className="rounded-md border border-border bg-surface-muted">
                        {searchIsFetching ? (
                            <div className="flex items-center gap-2 px-3 py-2 text-xs text-content-secondary">
                                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                                {t('surfaces.requestSourceLinks.searching')}
                            </div>
                        ) : searchQuery.isError ? null : sourceResults.length > 0 ? (
                            <div className="max-h-44 divide-y divide-border-subtle overflow-y-auto">
                                {sourceResults.map(source => {
                                    const alreadyLinked = linkedSourceIds.has(source.id);
                                    return (
                                        <div key={source.id} className="flex items-center justify-between gap-3 px-3 py-2">
                                            <div className="min-w-0">
                                                <p className="truncate text-sm font-medium text-content-primary">{requestLabel(source)}</p>
                                                <p className="truncate text-xs text-content-secondary">
                                                    {sourceTypeLabel(source.source_type)}
                                                    {source.source_name ? ` · ${source.source_name}` : ''}
                                                    {source.external_key ? ` · ${source.external_key}` : ''}
                                                </p>
                                            </div>
                                            <button
                                                type="button"
                                                onClick={() => {
                                                    setLinkingSourceId(source.id);
                                                    linkExistingMutation.mutate(source.id);
                                                }}
                                                disabled={alreadyLinked || linkExistingMutation.isPending}
                                                className="shrink-0 rounded-md border border-border-strong bg-surface-card px-2 py-1 text-xs font-medium text-content-primary hover:bg-surface-subtle disabled:cursor-not-allowed disabled:opacity-50"
                                            >
                                                {alreadyLinked
                                                    ? t('surfaces.requestSourceLinks.linked')
                                                    : linkingSourceId === source.id
                                                        ? t('surfaces.requestSourceLinks.linking')
                                                        : t('surfaces.requestSourceLinks.link')}
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <div className="px-3 py-2 text-xs text-content-secondary">{t('surfaces.requestSourceLinks.noMatchingRequests')}</div>
                        )}
                    </div>
                )}
            </div>

            <div className="mt-4 space-y-2">
                {linksAreLoading ? (
                    <div className="text-sm text-content-secondary">{t('surfaces.requestSourceLinks.loadingRequests')}</div>
                ) : linksQuery.isError ? null : links.length > 0 ? (
                    links.map(link => {
                        const source = link.request_source;
                        return (
                            <div key={link.id} className="flex items-start justify-between gap-3 rounded-md border border-border bg-surface-muted px-3 py-2">
                                <div className="min-w-0">
                                    <div className="flex flex-wrap items-center gap-2">
                                        {source.source_url ? (
                                            <a
                                                href={safeExternalHref(source.source_url)}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="break-words text-sm font-medium text-action hover:text-action"
                                            >
                                                {requestLabel(source)}
                                            </a>
                                        ) : (
                                            <span className="break-words text-sm font-medium text-content-primary">
                                                {requestLabel(source)}
                                            </span>
                                        )}
                                        <span className="rounded-full bg-surface-card px-2 py-0.5 text-wc-micro font-medium text-content-secondary">
                                            {sourceTypeLabel(source.source_type)}
                                        </span>
                                        {source.priority_hint && (
                                            <span className="rounded-full bg-feedback-warning-muted px-2 py-0.5 text-wc-micro font-medium text-feedback-warning-foreground">
                                                P{source.priority_hint}
                                            </span>
                                        )}
                                    </div>
                                    {(source.source_name || source.external_key || source.description) && (
                                        <p className="mt-1 break-words text-xs text-content-secondary">
                                            {[source.source_name, source.external_key, source.description].filter(Boolean).join(' · ')}
                                        </p>
                                    )}
                                </div>
                                <button
                                    type="button"
                                    onClick={() => {
                                        setDeletingLinkId(link.id);
                                        deleteLinkMutation.mutate(link.id);
                                    }}
                                    disabled={deleteLinkMutation.isPending}
                                    className="shrink-0 rounded-md p-1.5 text-content-tertiary hover:bg-feedback-danger-muted hover:text-feedback-danger-foreground disabled:cursor-not-allowed disabled:opacity-50"
                                    title={t('surfaces.requestSourceLinks.unlinkRequest')}
                                    aria-label={t('surfaces.requestSourceLinks.unlinkNamedRequest', { name: requestLabel(source) })}
                                >
                                    {deletingLinkId === link.id ? (
                                        <Loader2 className="h-4 w-4 animate-spin" />
                                    ) : (
                                        <Trash2 className="h-4 w-4" />
                                    )}
                                </button>
                            </div>
                        );
                    })
                ) : (
                    <div className="rounded-md border border-dashed border-border bg-surface-muted p-3 text-sm text-content-secondary">
                        {t('surfaces.requestSourceLinks.noLinkedRequestsYet')}
                    </div>
                )}
            </div>

            {error && (
                <div className="mt-3 flex items-center gap-1 text-xs text-feedback-danger-foreground">
                    <AlertCircle className="h-3.5 w-3.5" />
                    {t('surfaces.requestSourceLinks.requestLinksWereNotChanged')}
                </div>
            )}
        </section>
    );
};
