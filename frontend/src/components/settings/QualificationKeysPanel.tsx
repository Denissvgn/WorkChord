import { useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { BadgeCheck, Plus } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { agentService } from '../../services/agentService';
import type { RoutingQualificationKey } from '../../types/agent';
import { normalizeApiError } from '../../utils/apiError';
import { formatDateTime } from '../../utils/formatDate';
import { createAgentCommandMetadata } from '../../utils/modelRouting';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import { Modal } from '../common/Modal';
import { Textarea } from '../common/Textarea';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';

const REGISTRY_QUERY_KEY = 'routing-qualification-keys';

type Dialog =
    | { kind: 'declare'; key: string; label: string; description: string; locked: boolean }
    | { kind: 'revise'; entry: RoutingQualificationKey; label: string; description: string }
    | { kind: 'retire'; entry: RoutingQualificationKey }
    | { kind: 'history'; entry: RoutingQualificationKey };

interface InUseDetail {
    code?: string;
    catalog_entries?: { key: string }[];
    task_ids?: number[];
    catalog_entries_omitted?: number;
    task_ids_omitted?: number;
    calibration_contracts?: { key: string }[];
    calibration_contracts_omitted?: number;
}

/** A list of names, with how many more the bounded or scoped response left out. */
const namedWithOmitted = (names: string[], omitted: number | undefined, more: (count: number) => string) => {
    const parts = names.length > 0 ? [names.join(', ')] : [];
    if (omitted) parts.push(more(omitted));
    return parts.join(' ') || '—';
};

const inUseDetail = (error: unknown): InUseDetail | null => {
    const detail = (error as { response?: { data?: { detail?: InUseDetail } } })?.response?.data?.detail;
    return detail?.code === 'routing_qualification_key_in_use' ? detail : null;
};

/**
 * The deployment's declared qualification keys beside the fixed built-in keys.
 * Every change asks for a reason, which the server keeps with the key's revision.
 */
export const QualificationKeysPanel = () => {
    const { t } = useTranslation();
    const toast = useToast();
    const queryClient = useQueryClient();
    const [showRetired, setShowRetired] = useState(false);
    const [dialog, setDialog] = useState<Dialog | null>(null);
    const [reason, setReason] = useState('');
    const [dialogError, setDialogError] = useState<string | null>(null);

    // feedback-policy: query loading,error,retry,empty
    const registryQuery = useQuery({
        queryKey: [REGISTRY_QUERY_KEY, showRetired],
        queryFn: () => agentService.getQualificationKeys(showRetired),
        retry: protectedQueryRetry,
    });
    const historyKey = dialog?.kind === 'history' ? dialog.entry.key : null;
    // feedback-policy: query loading,error,retry,empty
    const historyQuery = useQuery({
        queryKey: [REGISTRY_QUERY_KEY, 'detail', historyKey],
        queryFn: () => agentService.getQualificationKey(historyKey ?? ''),
        enabled: historyKey !== null,
        retry: protectedQueryRetry,
    });

    const open = (next: Dialog) => {
        setReason('');
        setDialogError(null);
        setDialog(next);
    };
    const finished = (message: string) => {
        void queryClient.invalidateQueries({ queryKey: [REGISTRY_QUERY_KEY] });
        void queryClient.invalidateQueries({ queryKey: ['agent-model-catalog'] });
        setDialog(null);
        toast.success(message);
    };
    const failed = (error: unknown) => {
        const inUse = inUseDetail(error);
        if (inUse) {
            const more = (count: number) => t('qualificationKeys.andMore', { count });
            setDialogError(t('qualificationKeys.inUse', {
                entries: namedWithOmitted((inUse.catalog_entries ?? []).map(entry => entry.key), inUse.catalog_entries_omitted, more),
                contracts: namedWithOmitted((inUse.calibration_contracts ?? []).map(contract => contract.key), inUse.calibration_contracts_omitted, more),
                tasks: namedWithOmitted((inUse.task_ids ?? []).map(id => `#${id}`), inUse.task_ids_omitted, more),
            }));
            return;
        }
        setDialogError(normalizeApiError(error, t('qualificationKeys.mutationFailed')).message);
        void queryClient.invalidateQueries({ queryKey: [REGISTRY_QUERY_KEY] });
    };

    // feedback-policy: mutation pending,inline
    const declareMutation = useMutation({
        mutationFn: (values: { key: string; label: string; description: string }) => agentService.declareQualificationKey(
            { key: values.key.trim().toLowerCase(), label: values.label.trim(), description: values.description.trim() || null },
            createAgentCommandMetadata(reason),
        ),
        onSuccess: () => finished(t('qualificationKeys.declareSuccess')),
        onError: failed,
    });
    // feedback-policy: mutation pending,inline
    const reviseMutation = useMutation({
        mutationFn: (values: { entry: RoutingQualificationKey; label: string; description: string }) => agentService.reviseQualificationKey(
            values.entry.key,
            { expected_revision: values.entry.revision, label: values.label.trim(), description: values.description.trim() || null },
            createAgentCommandMetadata(reason),
        ),
        onSuccess: () => finished(t('qualificationKeys.reviseSuccess')),
        onError: failed,
    });
    // feedback-policy: mutation pending,inline
    const retireMutation = useMutation({
        mutationFn: (entry: RoutingQualificationKey) => agentService.retireQualificationKey(
            entry.key,
            entry.revision,
            createAgentCommandMetadata(reason),
        ),
        onSuccess: () => finished(t('qualificationKeys.retireSuccess')),
        onError: failed,
    });
    const pending = declareMutation.isPending || reviseMutation.isPending || retireMutation.isPending;

    const submit = (event: FormEvent) => {
        event.preventDefault();
        if (!dialog || !reason.trim() || pending) return;
        setDialogError(null);
        if (dialog.kind === 'declare') declareMutation.mutate(dialog);
        if (dialog.kind === 'revise') reviseMutation.mutate(dialog);
        if (dialog.kind === 'retire') retireMutation.mutate(dialog.entry);
    };

    if (registryQuery.isPending) return <QueryLoadingState message={t('qualificationKeys.loading')} />;
    if (registryQuery.isError) {
        return <QueryErrorState error={registryQuery.error} fallback={t('qualificationKeys.loadFailed')} />;
    }
    const { builtin_keys: builtinKeys, keys } = registryQuery.data;

    const reasonField = (
        <Input
            label={t('qualificationKeys.reason')}
            value={reason}
            onChange={event => setReason(event.target.value)}
            placeholder={t('qualificationKeys.reasonPlaceholder')}
            disabled={pending}
            required
        />
    );
    const dialogActions = (submitLabel: string) => (
        <>
            {dialogError && <p className="text-sm text-feedback-danger-foreground" role="alert">{dialogError}</p>}
            <div className="flex justify-end gap-2">
                <Button type="button" variant="ghost" onClick={() => setDialog(null)} disabled={pending}>{t('actions.cancel')}</Button>
                <Button type="submit" isLoading={pending} disabled={pending || !reason.trim()}>{submitLabel}</Button>
            </div>
        </>
    );

    const dialogTitle = (() => {
        if (!dialog) return '';
        if (dialog.kind === 'declare') return t('qualificationKeys.declareTitle');
        if (dialog.kind === 'revise') return t('qualificationKeys.reviseTitle', { key: dialog.entry.key });
        if (dialog.kind === 'retire') return t('qualificationKeys.retireTitle', { key: dialog.entry.key });
        return t('qualificationKeys.historyTitle', { key: dialog.entry.key });
    })();

    return (
        <div className="wc-panel-stack max-w-3xl">
            <section className="card card-pad space-y-4" aria-labelledby="qualification-keys-heading">
                <div className="flex flex-wrap items-start justify-between gap-3">
                    <div className="min-w-0">
                        <h3 id="qualification-keys-heading" className="flex items-center gap-2 font-semibold text-content-primary">
                            <BadgeCheck aria-hidden="true" className="h-4 w-4 text-action" />
                            {t('qualificationKeys.title')}
                        </h3>
                        <p className="text-sm text-content-secondary">{t('qualificationKeys.description')}</p>
                    </div>
                    <Button type="button" onClick={() => open({ kind: 'declare', key: '', label: '', description: '', locked: false })}>
                        <Plus aria-hidden="true" className="h-4 w-4" />
                        {t('qualificationKeys.declare')}
                    </Button>
                </div>
                <Checkbox checked={showRetired} onChange={setShowRetired} label={t('qualificationKeys.showRetired')} />
                {keys.length === 0 ? (
                    <p className="text-sm text-content-tertiary">{t('qualificationKeys.empty')}</p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead>
                                <tr>
                                    <th className="p-2">{t('qualificationKeys.key')}</th>
                                    <th className="p-2">{t('qualificationKeys.label')}</th>
                                    <th className="p-2">{t('qualificationKeys.state')}</th>
                                    <th className="p-2">{t('qualificationKeys.revision')}</th>
                                    <th className="p-2"><span className="sr-only">{t('actions.edit')}</span></th>
                                </tr>
                            </thead>
                            <tbody>
                                {keys.map(entry => (
                                    <tr key={entry.id} className="border-t border-border">
                                        <td className="p-2 font-mono text-xs">{entry.key}</td>
                                        <td className="p-2">
                                            {entry.label}
                                            {entry.description && <div className="text-xs text-content-secondary">{entry.description}</div>}
                                        </td>
                                        <td className="p-2">{t(`qualificationKeys.state_${entry.state}`)}</td>
                                        <td className="p-2 tnum">{entry.revision}</td>
                                        <td className="p-2">
                                            <div className="flex flex-wrap gap-2">
                                                <Button size="sm" variant="ghost" aria-label={t('qualificationKeys.historyAction', { key: entry.key })} onClick={() => open({ kind: 'history', entry })}>
                                                    {t('qualificationKeys.history')}
                                                </Button>
                                                {entry.state === 'active' ? (
                                                    <>
                                                        <Button size="sm" variant="secondary" aria-label={t('qualificationKeys.reviseAction', { key: entry.key })} onClick={() => open({ kind: 'revise', entry, label: entry.label, description: entry.description ?? '' })}>
                                                            {t('qualificationKeys.revise')}
                                                        </Button>
                                                        <Button size="sm" variant="outline" aria-label={t('qualificationKeys.retireAction', { key: entry.key })} onClick={() => open({ kind: 'retire', entry })}>
                                                            {t('qualificationKeys.retire')}
                                                        </Button>
                                                    </>
                                                ) : (
                                                    <Button size="sm" variant="secondary" aria-label={t('qualificationKeys.declareAgainAction', { key: entry.key })} onClick={() => open({ kind: 'declare', key: entry.key, label: entry.label, description: entry.description ?? '', locked: true })}>
                                                        {t('qualificationKeys.declareAgain')}
                                                    </Button>
                                                )}
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>

            <section className="card card-pad space-y-3" aria-labelledby="qualification-builtin-heading">
                <h3 id="qualification-builtin-heading" className="font-semibold text-content-primary">{t('qualificationKeys.builtinTitle')}</h3>
                <p className="text-sm text-content-secondary">{t('qualificationKeys.builtinDescription')}</p>
                <ul className="flex flex-wrap gap-2">
                    {builtinKeys.map(key => (
                        <li key={key} className="rounded-full border border-border px-2 py-0.5 font-mono text-xs text-content-secondary">{key}</li>
                    ))}
                </ul>
            </section>

            <Modal open={dialog !== null} title={dialogTitle} onClose={() => !pending && setDialog(null)} closeLabel={t('actions.close')} closeDisabled={pending}>
                {dialog?.kind === 'history' ? (
                    historyQuery.isPending ? <QueryLoadingState message={t('qualificationKeys.loading')} />
                        : historyQuery.isError ? <QueryErrorState error={historyQuery.error} fallback={t('qualificationKeys.loadFailed')} />
                            : (
                                <div className="space-y-4">
                                    <ol className="space-y-2">
                                        {historyQuery.data.revisions.map(revision => (
                                            <li key={revision.revision} className="rounded-md border border-border p-3 text-sm">
                                                <p className="font-semibold text-content-primary">
                                                    {t('qualificationKeys.revision')} {revision.revision} · {t(`qualificationKeys.action_${revision.action}`)}
                                                </p>
                                                <p className="text-content-secondary">{revision.reason}</p>
                                                <p className="text-xs text-content-tertiary">{revision.label} · {formatDateTime(revision.created_at)}</p>
                                            </li>
                                        ))}
                                    </ol>
                                    <div>
                                        <p className="mb-1 text-xs font-medium text-content-secondary">{t('qualificationKeys.usage')}</p>
                                        {historyQuery.data.usage.catalog_entries.length === 0 && historyQuery.data.usage.task_ids.length === 0 && (historyQuery.data.usage.calibration_contracts ?? []).length === 0 ? (
                                            <p className="text-sm text-content-tertiary">{t('qualificationKeys.noUsage')}</p>
                                        ) : (
                                            <dl className="space-y-1 text-sm">
                                                <div><dt className="inline text-content-tertiary">{t('qualificationKeys.usageCatalog')}: </dt><dd className="inline">{historyQuery.data.usage.catalog_entries.map(entry => entry.key).join(', ') || '—'}</dd></div>
                                                <div><dt className="inline text-content-tertiary">{t('qualificationKeys.usageTasks')}: </dt><dd className="inline">{historyQuery.data.usage.task_ids.map(id => `#${id}`).join(', ') || '—'}</dd></div>
                                                <div><dt className="inline text-content-tertiary">{t('qualificationKeys.usageContracts')}: </dt><dd className="inline">{(historyQuery.data.usage.calibration_contracts ?? []).map(contract => contract.key).join(', ') || '—'}</dd></div>
                                            </dl>
                                        )}
                                    </div>
                                </div>
                            )
                ) : dialog ? (
                    <form className="space-y-3" onSubmit={submit} aria-busy={pending}>
                        {dialog.kind === 'declare' && (
                            <>
                                <div>
                                    <Input
                                        label={t('qualificationKeys.key')}
                                        value={dialog.key}
                                        onChange={event => setDialog({ ...dialog, key: event.target.value })}
                                        aria-describedby="qualification-key-hint"
                                        disabled={pending || dialog.locked}
                                        required
                                    />
                                    <p id="qualification-key-hint" className="mt-1 text-xs text-content-secondary">{t('qualificationKeys.keyHint')}</p>
                                </div>
                                <Input label={t('qualificationKeys.label')} value={dialog.label} onChange={event => setDialog({ ...dialog, label: event.target.value })} disabled={pending} required />
                                <Textarea label={t('qualificationKeys.keyDescription')} value={dialog.description} onChange={event => setDialog({ ...dialog, description: event.target.value })} disabled={pending} />
                            </>
                        )}
                        {dialog.kind === 'revise' && (
                            <>
                                <Input label={t('qualificationKeys.label')} value={dialog.label} onChange={event => setDialog({ ...dialog, label: event.target.value })} disabled={pending} required />
                                <Textarea label={t('qualificationKeys.keyDescription')} value={dialog.description} onChange={event => setDialog({ ...dialog, description: event.target.value })} disabled={pending} />
                            </>
                        )}
                        {dialog.kind === 'retire' && <p className="text-sm text-content-secondary">{t('qualificationKeys.retireDescription')}</p>}
                        {reasonField}
                        {dialogActions(
                            dialog.kind === 'declare' ? t('qualificationKeys.declare')
                                : dialog.kind === 'revise' ? t('actions.save') : t('qualificationKeys.retire'),
                        )}
                    </form>
                ) : null}
            </Modal>
        </div>
    );
};
