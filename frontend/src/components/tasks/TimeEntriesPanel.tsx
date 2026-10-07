import { useCallback, useEffect, useId, useState } from 'react';
import type { KeyboardEvent } from 'react';
import { createPortal } from 'react-dom';
import { useInfiniteQuery, useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { format } from 'date-fns';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { QueryErrorState } from '../feedback/QueryState';
import { useTimeEntries } from '../../features/timeEntries/useTimeEntries';
import { timeEntryService, timeAccessDenied } from '../../services/timeEntryService';
import type { TimeEntry } from '../../services/timeEntryService';
import { taskService } from '../../services/taskService';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';
import { useDraftDismissal } from './useDraftDismissal';
import { DraftDismissalDialog } from './DraftDismissalDialog';

type Draft = { work_date: string; timezone: string; minutes: string; note: string; reason: string;
    task: string; request: string; editing?: Pick<TimeEntry, 'id' | 'version'> };
const emptyDraft = (taskId?: number): Draft => ({ work_date: format(new Date(), 'yyyy-MM-dd'),
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC', minutes: '', note: '', reason: '',
    task: taskId ? String(taskId) : '', request: crypto.randomUUID() });
const readDraft = (key: string): Draft | null => {
    try {
        const stored = JSON.parse(sessionStorage.getItem(key) ?? 'null');
        const d = stored?.values;
        if (Date.now() - stored?.savedAt < 0 || Date.now() - stored?.savedAt > 86400000 || !d
            || !['work_date', 'timezone', 'minutes', 'note', 'reason', 'task', 'request'].every(k => typeof d[k] === 'string')
            || d.note.length > 2000 || d.reason.length > 1000 || d.timezone.length > 64
            || !/^[0-9a-f-]{36}$/i.test(d.request)
            || d.editing && (!Number.isSafeInteger(d.editing.id) || !Number.isSafeInteger(d.editing.version))) return null;
        return d;
    } catch { return null; }
};

export const TimeEntriesPanel = (props: { projectId: number; taskId?: number; disabled?: boolean;
    start?: string; end?: string; embedded?: boolean; draftKey?: string | null; onDirty?: (dirty: boolean) => void; onPending?: (pending: boolean) => void }) => {
    const { t } = useTranslation();
    const { enabled, capability, identity } = useTimeEntries();
    const scope = JSON.stringify([identity?.principal?.id, props.projectId, props.taskId ?? null, props.draftKey ?? null]);
    const storageKey = props.draftKey ? `${props.draftKey}:time:${scope}` : `workchord-draft:${identity?.principal?.id}:time:${scope}`;
    if (capability.isError) return <QueryErrorState error={capability.error} fallback={t('timeEntries.loadFailed')} onRetry={() => void capability.refetch()} />;
    if (!enabled) return null;
    if (props.embedded) return <div className="space-y-3 border-t border-border pt-4"><h3 className="font-medium">{t('timeEntries.title')}</h3><TimeEntriesContent key={scope} {...props} storageKey={storageKey} /></div>;
    return <CollapsibleSection title={t('timeEntries.title')}><TimeEntriesContent key={scope} {...props} storageKey={storageKey} /></CollapsibleSection>;
};

const TimeEntriesContent = ({ projectId, taskId, start, end, disabled = false, storageKey, onDirty, onPending }: {
    projectId: number; taskId?: number; disabled?: boolean; storageKey: string;
    start?: string; end?: string;
    onDirty?: (dirty: boolean) => void; onPending?: (pending: boolean) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const formId = `${id}-time-form`;
    const { identity } = useTimeEntries();
    const queryClient = useQueryClient();
    const key = storageKey;
    const [baseline, setBaseline] = useState(() => emptyDraft(taskId));
    const [draft, setDraft] = useState<Draft>(() => readDraft(key) ?? baseline);
    const [search, setSearch] = useState('');
    const [historyId, setHistoryId] = useState<number | null>(null);
    const [current, setCurrent] = useState<TimeEntry | null>(null);
    const [message, setMessage] = useState('');
    const [validation, setValidation] = useState('');
    const guard = useDraftDismissal(() => undefined);
    const { setDirty: setGuardDirty, setPending: setGuardPending, onDiscardReady: guardDiscardReady } = guard;
    const dirty = Boolean(draft.minutes || draft.note || draft.reason || draft.editing
        || draft.work_date !== baseline.work_date || draft.timezone !== baseline.timezone || draft.task !== baseline.task);
    const canCreate = identity?.workspace_role === 'owner' || identity?.workspace_role === 'operator'
        || ['editor', 'executor', 'reviewer', 'manager'].includes(identity?.projects[String(projectId)] ?? '');
    const clear = useCallback(() => { try { sessionStorage.removeItem(key); } catch { /* In-memory inputs still clear when storage is unavailable. */ } }, [key]);
    useEffect(() => {
        onDirty?.(dirty); setGuardDirty(!onDirty && dirty);
        try { if (dirty) sessionStorage.setItem(key, JSON.stringify({ savedAt: Date.now(), values: draft })); else sessionStorage.removeItem(key); } catch { /* Keep inputs in memory if storage is unavailable. */ }
    }, [dirty, draft, key, onDirty, setGuardDirty]);
    useEffect(() => () => onDirty?.(false), [onDirty]);
    useEffect(() => { guardDiscardReady(clear); return () => guardDiscardReady(null); }, [clear, guardDiscardReady]);
    // feedback-policy: query loading,error,retry,empty - errors hide cached private entries and actions.
    const entries = useInfiniteQuery({ queryKey: ['time-entries', projectId, taskId, start, end], initialPageParam: { after: 0, upper: undefined as number | undefined },
        queryFn: ({ pageParam, signal }) => timeEntryService.list({ project_id: projectId, task_id: taskId, start, end }, pageParam.after, pageParam.upper, signal),
        getNextPageParam: page => page.has_more ? { after: page.next_after_id!, upper: page.upper_id } : undefined });
    // feedback-policy: query loading,error,retry,empty - bounded task choices show loading, retry and incomplete-list copy.
    const options = useQuery({ queryKey: ['time-task-options', projectId, search], enabled: taskId === undefined && !draft.editing,
        queryFn: ({ signal }) => taskService.lookup({ project_id: projectId, q: search, limit: 100 }, signal) });
    // feedback-policy: query loading,error,retry,empty - history errors hide prior contents and expose retry.
    const history = useInfiniteQuery({ queryKey: ['time-history', historyId], enabled: historyId !== null,
        initialPageParam: 0, queryFn: ({ pageParam, signal }) => timeEntryService.history(historyId!, pageParam, signal),
        getNextPageParam: page => page.has_more ? page.next_after_version! : undefined });
    // feedback-policy: mutation pending,inline - preserve values and request identity on failure.
    const save = useMutation({ mutationFn: (voiding: boolean) => {
        const values = { work_date: draft.work_date, timezone: draft.timezone, minutes: Number(draft.minutes), note: draft.note };
        if (voiding) return timeEntryService.void(draft.editing!, draft.reason);
        return draft.editing ? timeEntryService.correct(draft.editing, values, draft.reason)
            : timeEntryService.create(projectId, draft.task ? Number(draft.task) : null, draft.request, values);
    }, onSuccess: async () => {
        clear(); const next = emptyDraft(taskId); setBaseline(next); setDraft(next); setCurrent(null); setMessage(t('timeEntries.saved')); setValidation('');
        await queryClient.invalidateQueries({ queryKey: ['time-entries'] });
        await queryClient.invalidateQueries({ queryKey: ['time-report'] });
        await queryClient.invalidateQueries({ queryKey: ['time-history'] });
    } });
    // feedback-policy: mutation pending,inline - reload requires an explicit choice before adopting a newer version.
    const reload = useMutation({ mutationFn: () => timeEntryService.get(draft.editing!.id), onSuccess: setCurrent });
    const pending = save.isPending || reload.isPending;
    const privateUnavailable = entries.isError || timeAccessDenied(save.error) || timeAccessDenied(reload.error);
    useEffect(() => { onPending?.(pending); setGuardPending(!onDirty && pending); }, [pending, onPending, onDirty, setGuardPending]);
    useEffect(() => () => onPending?.(false), [onPending]);
    const run = (voiding = false) => {
        if (!Number.isInteger(Number(draft.minutes)) || Number(draft.minutes) < 1 || Number(draft.minutes) > 1440
            || !/^\d{4}-\d{2}-\d{2}$/.test(draft.work_date) || !draft.timezone.trim()
            || (draft.editing || voiding) && !draft.reason.trim()) { setValidation(t('timeEntries.invalid')); return; }
        setValidation(''); setMessage(''); save.mutate(voiding);
    };
    const discard = () => { clear(); const next = emptyDraft(taskId); setBaseline(next); setDraft(next); setCurrent(null); save.reset(); setValidation(''); };
    const field = (name: keyof Draft, value: string) => setDraft(values => ({ ...values, [name]: value }));
    const preventParentSubmit = (event: KeyboardEvent<HTMLInputElement>) => { if (event.key === 'Enter') event.preventDefault(); };
    return <section className="space-y-4" aria-label={t('timeEntries.title')}>
        {createPortal(<form id={formId} onSubmit={event => { event.preventDefault(); run(); }} />, document.body)}
        <p className="text-sm text-content-secondary">{t('timeEntries.privacy')}</p>
        {entries.isLoading && <p role="status">{t('common.loading')}</p>}
        {entries.isError && <QueryErrorState error={entries.error} fallback={t('timeEntries.loadFailed')} onRetry={() => void entries.refetch()} />}
        {!privateUnavailable && <>
            {entries.isSuccess && !entries.data.pages.flatMap(p => p.items).length && <p className="text-sm text-content-secondary">{t('timeEntries.empty')}</p>}
            <ul className="divide-y divide-border">{entries.data?.pages.flatMap(p => p.items).map(row => <li key={row.id} className="space-y-2 py-3">
                <p className="text-sm"><strong>{t('timeEntries.duration', { count: row.minutes })}</strong> · {formatDate(row.work_date)} · {row.timezone} {row.voided && <span className="text-content-secondary">· {t('timeEntries.voided')}</span>}</p>
                {!taskId && <p className="text-sm text-content-secondary">{row.task_title ?? t('timeEntries.projectWork')}</p>}
                {row.note && <p className="whitespace-pre-wrap break-words text-sm">{row.note}</p>}
                <div className="flex flex-wrap gap-2">
                    {!row.voided && <Button type="button" variant="ghost" size="sm" disabled={dirty || disabled || pending} onClick={() => {
                        setDraft({ ...emptyDraft(taskId), ...row, minutes: String(row.minutes), task: row.task_id ? String(row.task_id) : '', reason: '', editing: { id: row.id, version: row.version } }); setCurrent(null); save.reset();
                    }}>{t('timeEntries.edit')}</Button>}
                    <Button type="button" variant="ghost" size="sm" onClick={() => setHistoryId(historyId === row.id ? null : row.id)}>{t('timeEntries.history')}</Button>
                </div>
                {historyId === row.id && <div className="space-y-2 bg-surface-muted p-3">
                    {history.isLoading && <p role="status">{t('common.loading')}</p>}
                    {history.isError && <QueryErrorState error={history.error} fallback={t('timeEntries.loadFailed')} onRetry={() => void history.refetch()} />}
                    {!history.isError && history.data?.pages.flatMap(p => p.items).map(revision => <p className="whitespace-pre-wrap break-words text-sm" key={revision.version}>v{revision.version} · {t('timeEntries.duration', { count: revision.minutes })} · {formatDate(revision.work_date)} · {revision.timezone} · {revision.reason}{revision.voided ? ` · ${t('timeEntries.voided')}` : ''}<br />{revision.note}</p>)}
                    {history.hasNextPage && <Button type="button" variant="ghost" size="sm" disabled={history.isFetchingNextPage} onClick={() => void history.fetchNextPage()}>{t('timeEntries.more')}</Button>}
                </div>}
            </li>)}</ul>
            {entries.hasNextPage && <Button type="button" variant="secondary" size="sm" disabled={entries.isFetchingNextPage} onClick={() => void entries.fetchNextPage()}>{t('timeEntries.more')}</Button>}
        </>}
        <fieldset form={formId} disabled={disabled || pending || privateUnavailable || !draft.editing && !canCreate} className="space-y-3">
            <legend className="mb-2 font-medium">{t(draft.editing ? 'timeEntries.edit' : 'timeEntries.save')}</legend>
            <p className="text-sm text-content-secondary">{t('timeEntries.help')}</p>
            {taskId === undefined && !draft.editing && <>
                <Input form={formId} onKeyDown={preventParentSubmit} label={t('timeEntries.search')} value={search} maxLength={200} onChange={event => setSearch(event.target.value)} />
                {options.isLoading && <p role="status">{t('common.loading')}</p>}
                {options.isError && <QueryErrorState error={options.error} fallback={t('timeEntries.loadFailed')} onRetry={() => void options.refetch()} />}
                <label className="field-lbl" htmlFor={`${id}-task`}>{t('timeEntries.task')}</label>
                <select form={formId} id={`${id}-task`} className="input w-full" value={draft.task} onChange={event => field('task', event.target.value)}>
                    <option value="">{t('timeEntries.projectWork')}</option>
                    {!options.isError && options.data?.items.map(task => <option key={task.id} value={task.id}>#{task.id} · {task.title}</option>)}
                </select>
                {options.data?.has_more && !options.isError && <p className="text-sm text-content-secondary">{t('timeEntries.partialTasks')}</p>}
            </>}
            <div className="grid gap-3 sm:grid-cols-3">
                <Input form={formId} onKeyDown={preventParentSubmit} label={t('timeEntries.date')} type="date" value={draft.work_date} onChange={event => field('work_date', event.target.value)} required />
                <Input form={formId} onKeyDown={preventParentSubmit} label={t('timeEntries.zone')} value={draft.timezone} maxLength={64} onChange={event => field('timezone', event.target.value)} required />
                <Input form={formId} onKeyDown={preventParentSubmit} label={t('timeEntries.minutes')} type="number" min={1} max={1440} step={1} value={draft.minutes} onChange={event => field('minutes', event.target.value)} required />
            </div>
            <label className="field-lbl" htmlFor={`${id}-note`}>{t('timeEntries.note')}</label>
            <textarea form={formId} id={`${id}-note`} className="input min-h-20 w-full" value={draft.note} maxLength={2000} onChange={event => field('note', event.target.value)} />
            {draft.editing && <Input form={formId} onKeyDown={preventParentSubmit} label={t('timeEntries.reason')} value={draft.reason} maxLength={1000} onChange={event => field('reason', event.target.value)} required />}
            <div className="flex flex-wrap gap-2">
                <Button type="button" variant="secondary" size="sm" onClick={() => run()} isLoading={save.isPending}>{t(draft.editing ? 'timeEntries.correct' : 'timeEntries.save')}</Button>
                {draft.editing && <Button type="button" variant="danger" size="sm" onClick={() => run(true)} disabled={!draft.reason.trim()}>{t('timeEntries.void')}</Button>}
            </div>
        </fieldset>
        {dirty && <Button type="button" variant="ghost" size="sm" disabled={pending} onClick={discard}>{t('timeEntries.discard')}</Button>}
        {!canCreate && !draft.editing && <p className="text-sm text-content-secondary">{t('timeEntries.createDenied')}</p>}
        {validation && <p role="alert" className="text-sm text-feedback-danger-foreground">{validation}</p>}
        {(save.isError || reload.isError) && <div role="alert" className="space-y-2 text-sm text-feedback-danger-foreground">
            <p>{getApiErrorMessage(save.error ?? reload.error, t('timeEntries.failed'))}</p>
            <Button type="button" variant="secondary" size="sm" disabled={pending || entries.isFetching} onClick={async () => {
                const result = await entries.refetch(); if (!result.isError) { save.reset(); reload.reset(); setCurrent(null); }
            }}>{t('timeEntries.reloadEntries')}</Button>
            {draft.editing && <Button type="button" variant="secondary" size="sm" disabled={pending} onClick={() => reload.mutate()}>{t('timeEntries.reload')}</Button>}
        </div>}
        {current && !privateUnavailable && !reload.isError && <div className="space-y-2 border border-feedback-warning-border p-3 text-sm">
            <p>{t('timeEntries.current')} · v{current.version}: {t('timeEntries.duration', { count: current.minutes })} · {formatDate(current.work_date)}</p>
            <p className="whitespace-pre-wrap break-words">{current.note}</p>
            <Button type="button" variant="secondary" size="sm" disabled={current.voided || pending} onClick={() => { setDraft(values => ({ ...values, editing: { id: current.id, version: current.version } })); setCurrent(null); save.reset(); }}>{t('timeEntries.reapply')}</Button>
            {current.voided && <p>{t('timeEntries.voided')}</p>}
        </div>}
        {message && <p role="status" className="text-sm text-content-secondary">{message}</p>}
        {!onDirty && <DraftDismissalDialog guard={guard} />}
    </section>;
};
