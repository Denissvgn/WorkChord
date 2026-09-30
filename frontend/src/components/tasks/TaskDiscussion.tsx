import { useEffect, useId, useState } from 'react';
import { useInfiniteQuery, useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useIdentity } from '../../features/identity/identityContext';
import { discussionService } from '../../services/discussionService';
import type { TaskComment } from '../../services/discussionService';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';

type EditingComment = Pick<TaskComment, 'id' | 'version'>;
const readDiscussionDraft = (key: string | null): { body: string; mentions: number[]; editing?: EditingComment } | null => {
    try {
        const value = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null');
        if (!value || typeof value.savedAt !== 'number' || Date.now() - value.savedAt < 0 || Date.now() - value.savedAt >= 86400000
            || typeof value.body !== 'string' || value.body.length > 12000 || !Array.isArray(value.mentions)
            || value.mentions.length > 25 || !value.mentions.every((item: unknown) => Number.isSafeInteger(item) && Number(item) > 0)) return null;
        if (value.editing && (!Number.isSafeInteger(value.editing.id) || value.editing.id < 1 || !Number.isSafeInteger(value.editing.version) || value.editing.version < 1)) return null;
        return value;
    } catch { return null; }
};

export const TaskDiscussion = ({ taskId, draftKey, disabled, onDirty, onPending }: {
    taskId: number; draftKey: string | null; disabled: boolean;
    onDirty: (dirty: boolean) => void; onPending: (pending: boolean) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const identity = useIdentity()?.identity;
    const enabled = identity?.principal?.kind === 'human';
    const storageKey = draftKey ? `${draftKey}:discussion` : null;
    const [recovered] = useState(() => readDiscussionDraft(storageKey));
    const [body, setBody] = useState(recovered?.body ?? '');
    const [editing, setEditing] = useState<EditingComment | undefined>(recovered?.editing);
    const [mentions, setMentions] = useState<number[]>(recovered?.mentions ?? []);
    const [mentionSearch, setMentionSearch] = useState('');
    const [historyId, setHistoryId] = useState<number | null>(null);
    const [message, setMessage] = useState('');
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const comments = useInfiniteQuery({ queryKey: ['discussion', taskId], enabled,
        initialPageParam: 0, queryFn: ({ pageParam }) => discussionService.list(taskId, pageParam),
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const options = useQuery({ queryKey: ['mention-options', taskId, mentionSearch], enabled: enabled && mentionSearch.length > 0,
        queryFn: () => discussionService.mentions(taskId, mentionSearch) });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const subscription = useQuery({ queryKey: ['subscription', taskId], enabled, queryFn: () => discussionService.subscription(taskId) });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const history = useInfiniteQuery({ queryKey: ['comment-history', taskId, historyId], enabled: enabled && historyId !== null,
        initialPageParam: 0, queryFn: ({ pageParam }) => discussionService.history(taskId, historyId!, pageParam),
        getNextPageParam: page => page.has_more ? page.next_after_version : undefined });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const save = useMutation({ mutationFn: (removed?: TaskComment) => discussionService.save(taskId, removed ? '' : body, removed ? [] : mentions, removed ?? editing, Boolean(removed)),
        onSuccess: async () => { setBody(''); setMentions([]); setEditing(undefined); setMessage(t('teamwork.commentSaved')); await comments.refetch(); if (historyId !== null) await history.refetch(); } });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const subscribe = useMutation({ mutationFn: ({ enabled, events }: { enabled: boolean; events?: string[] }) => discussionService.subscribe(taskId, subscription.data!, enabled, events),
        onSuccess: () => subscription.refetch() });
    const dirty = body.length > 0 || editing !== undefined || mentions.length > 0;
    const latestEdit = comments.data?.pages.flatMap(page => page.items).find(comment => comment.id === editing?.id);
    const pending = save.isPending || subscribe.isPending;
    useEffect(() => { onDirty(dirty); if (!storageKey) return;
        try { if (dirty) sessionStorage.setItem(storageKey, JSON.stringify({ body, mentions, editing, savedAt: Date.now() })); else sessionStorage.removeItem(storageKey); } catch { /* Keep the in-page draft usable. */ }
    }, [body, mentions, editing, dirty, onDirty, storageKey]);
    useEffect(() => { onPending(pending); }, [pending, onPending]);
    useEffect(() => () => onDirty(false), [onDirty]);

    return <section className="space-y-3 border-t border-border pt-4" aria-labelledby={`${id}-title`}>
        <h3 id={`${id}-title`} className="text-base font-semibold text-content-primary">{t('teamwork.discussion')}</h3>
        <p className="text-sm text-content-secondary">{t('teamwork.discussionHelp')}</p>
        {!enabled ? <p>{t('teamwork.signInDiscussion')}</p> : <>
            {comments.isLoading && <p role="status">{t('common.loading')}</p>}
            {comments.isError && <QueryErrorState error={comments.error} fallback={t('teamwork.loadFailed')} onRetry={() => void comments.refetch()} />}
            {comments.data && comments.data.pages.every(page => page.items.length === 0) && <p className="text-sm text-content-secondary">{t('teamwork.noComments')}</p>}
            <ol className="space-y-4">{comments.data?.pages.flatMap(page => page.items).map(comment => <li key={comment.id} className="space-y-1">
                <p className="text-sm text-content-secondary"><strong className="text-content-primary">{comment.author_name}</strong> · {new Date(comment.updated_at).toLocaleString()}</p>
                <p className="whitespace-pre-wrap break-words text-sm text-content-primary">{comment.deleted ? t('teamwork.commentRemoved') : comment.body}</p>
                <div className="flex flex-wrap gap-2">
                    {!comment.deleted && comment.principal_id === identity?.principal?.id && <>
                        <Button type="button" size="sm" variant="ghost" disabled={dirty || disabled} onClick={() => { setEditing(comment); setBody(comment.body); setMentions(comment.mentions); save.reset(); }}>{t('teamwork.edit')}</Button>
                        <Button type="button" size="sm" variant="ghost" disabled={dirty || disabled} onClick={() => save.mutate(comment)}>{t('teamwork.remove')}</Button>
                    </>}
                    <Button type="button" size="sm" variant="ghost" onClick={() => setHistoryId(historyId === comment.id ? null : comment.id)}>{t('domain.history')}</Button>
                </div>
                {historyId === comment.id && <div className="space-y-2 rounded-md bg-surface-muted p-3">
                    {history.isLoading && <p role="status">{t('common.loading')}</p>}
                    {history.isError && <QueryErrorState error={history.error} fallback={t('teamwork.loadFailed')} onRetry={() => void history.refetch()} />}
                    {history.data?.pages.flatMap(page => page.items).map(revision => <p key={revision.version} className="whitespace-pre-wrap break-words text-sm">v{revision.version}: {revision.deleted ? t('teamwork.commentRemoved') : revision.body}</p>)}
                    {history.hasNextPage && <Button type="button" size="sm" variant="ghost" onClick={() => void history.fetchNextPage()} disabled={history.isFetchingNextPage}>{t('teamwork.loadMore')}</Button>}
                </div>}
            </li>)}</ol>
            {comments.hasNextPage && <Button type="button" size="sm" variant="secondary" onClick={() => void comments.fetchNextPage()} disabled={comments.isFetchingNextPage}>{t('teamwork.loadMore')}</Button>}
            <label className="field-lbl" htmlFor={`${id}-body`}>{t(editing ? 'teamwork.editComment' : 'teamwork.newComment')}</label>
            <textarea id={`${id}-body`} className="input min-h-24 w-full" value={body} maxLength={12000} disabled={disabled || pending} onChange={event => { setBody(event.target.value); setMessage(''); }} />
            <label className="field-lbl" htmlFor={`${id}-mentions`}>{t('teamwork.mention')}</label>
            <input id={`${id}-mentions`} className="input w-full" value={mentionSearch} maxLength={200} disabled={disabled || pending} onChange={event => setMentionSearch(event.target.value)} />
            {mentionSearch && options.isLoading && <p role="status">{t('common.loading')}</p>}
            {mentionSearch && options.isSuccess && options.data.items.length === 0 && <p className="text-sm text-content-secondary">{t('teamwork.noResults')}</p>}
            {options.isError && <QueryErrorState error={options.error} fallback={t('teamwork.loadFailed')} onRetry={() => void options.refetch()} />}
            {options.data?.items.map(person => <label key={person.id} className="flex items-center gap-2 text-sm"><input type="checkbox" disabled={disabled || pending} checked={mentions.includes(person.id)} onChange={event => setMentions(values => event.target.checked ? [...values, person.id] : values.filter(value => value !== person.id))} />{person.name}</label>)}
            {mentions.length > 0 && <p className="text-sm text-content-secondary">{t('teamwork.mentionedCount', { count: mentions.length })} <Button type="button" size="sm" variant="ghost" onClick={() => setMentions([])}>{t('teamwork.clear')}</Button></p>}
            {latestEdit && editing && latestEdit.version !== editing.version && <div className="space-y-2 rounded-md border border-feedback-warning-border p-3 text-sm">
                <p className="font-medium">{t('teamwork.currentComment')} · v{latestEdit.version}</p>
                <p className="whitespace-pre-wrap break-words">{latestEdit.deleted ? t('teamwork.commentRemoved') : latestEdit.body}</p>
                <Button type="button" size="sm" variant="secondary" disabled={pending} onClick={() => { setEditing(latestEdit.deleted ? undefined : latestEdit); save.reset(); }}>{t(latestEdit.deleted ? 'teamwork.newInstead' : 'teamwork.reapplyComment')}</Button>
            </div>}
            {save.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(save.error, t('teamwork.saveFailed'))} <Button type="button" size="sm" variant="ghost" onClick={() => void comments.refetch()}>{t('teamwork.reloadComments')}</Button></p>}
            {message && <p role="status" className="text-sm text-content-secondary">{message}</p>}
            <div className="flex flex-wrap gap-2">
                <Button type="button" size="sm" disabled={disabled || pending || !body.trim()} isLoading={save.isPending} onClick={() => save.mutate(undefined)}>{t(editing ? 'teamwork.saveComment' : 'teamwork.postComment')}</Button>
                {dirty && <Button type="button" size="sm" variant="ghost" disabled={pending} onClick={() => { setEditing(undefined); setBody(''); setMentions([]); save.reset(); }}>{t('teamwork.discardComment')}</Button>}
            </div>
            {subscription.isLoading && <p role="status">{t('common.loading')}</p>}
            {subscription.isError && <QueryErrorState error={subscription.error} fallback={t('teamwork.loadFailed')} onRetry={() => void subscription.refetch()} />}
            {subscription.data && <fieldset disabled={pending || disabled} className="space-y-2">
                <legend className="text-sm font-medium">{t('teamwork.notifications')}</legend>
                <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={subscription.data.enabled} onChange={event => subscribe.mutate({ enabled: event.target.checked })} />{t('teamwork.subscribe')}</label>
                {subscription.data.enabled && ['discussion', 'mention', 'review', 'block'].map(kind => <label key={kind} className="inline-flex items-center gap-2 pr-4 text-sm"><input type="checkbox" checked={subscription.data!.events.includes(kind)} onChange={event => subscribe.mutate({ enabled: true, events: event.target.checked ? [...subscription.data!.events, kind] : subscription.data!.events.filter(value => value !== kind) })} />{t(`teamwork.event_${kind}`)}</label>)}
            </fieldset>}
            {subscribe.isPending && <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>}
            {subscribe.isError && <div role="alert" className="text-sm text-feedback-danger-foreground"><p>{getApiErrorMessage(subscribe.error, t('teamwork.saveFailed'))}</p><Button type="button" size="sm" variant="ghost" onClick={() => { void subscription.refetch(); subscribe.reset(); }}>{t('teamwork.reloadNotifications')}</Button></div>}
        </>}
    </section>;
};
