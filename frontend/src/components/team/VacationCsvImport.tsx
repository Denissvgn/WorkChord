import { useEffect, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { teamService } from '../../services/teamService';
import { usePlanningObservation } from '../../features/usePlanningObservation';
import { useActiveMount } from '../tasks/useDraftDismissal';
import type { ObservedRevisions } from '../../services/planningInputService';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';

export const VacationCsvImport = ({ iterationId, onSuccess, onBusyChange }: { iterationId: number; onSuccess: () => void; onBusyChange?: (busy: boolean) => void }) => {
    const { t } = useTranslation();
    const active = useActiveMount();
    const context = usePlanningObservation();
    const [draft, setDraft] = useState<{ text: string; name: string } | null>(null);
    const [error, setError] = useState<unknown>(null);
    // feedback-policy: mutation pending,inline
    const write = useMutation({
        mutationFn: ({ text, revisions }: { text: string; revisions: ObservedRevisions }) => teamService.importVacationsCsv(iterationId, text, revisions),
        onSuccess: result => {
            if (!active()) return;
            if (result.errors.length) { setError(result.errors.map(row => `${row.row}: ${row.message}`).join('; ')); return; }
            setDraft(null); setError(null); onSuccess();
        }, onError: cause => { if (active()) setError(cause); },
    });
    useEffect(() => { onBusyChange?.(Boolean(draft) || write.isPending); }, [draft, write.isPending, onBusyChange]);
    useEffect(() => () => onBusyChange?.(false), [onBusyChange]);
    const chooseFile = async (file: File | undefined) => {
        if (!file || write.isPending) return;
        try {
            const text = await file.text();
            if (!active()) return;
            setDraft({ text, name: file.name }); setError(null);
            await context.read('member', iterationId, false, true, { csv_text: text });
        } catch (cause) { if (active()) setError(cause); }
    };
    return <div className="space-y-2">
        <label className="btn secondary cursor-pointer">{t('teamVacations.importCsv')}
            <input type="file" accept=".csv,text/csv" className="hidden" disabled={write.isPending || context.loading}
                onChange={event => { void chooseFile(event.target.files?.[0]); event.currentTarget.value = ''; }} />
        </label>
        {context.loading && <p role="status">{t('common.loading')}</p>}
        {(Boolean(error) || Boolean(context.error)) && <p role="alert" className="text-sm text-feedback-danger-foreground">{typeof error === 'string' ? error : getApiErrorMessage(error ?? context.error, t('teamVacations.importFailed'))}</p>}
        {draft && <div className="flex flex-wrap items-center gap-2 text-sm">
            <span>{draft.name}</span>
            <Button type="button" variant="secondary" size="sm" disabled={write.isPending || context.loading}
                onClick={() => void context.read('member', iterationId, true, true, { csv_text: draft.text })}>{t('planningInput.reviewAgain')}</Button>
            <Button type="button" size="sm" disabled={!context.observation || context.loading} isLoading={write.isPending}
                onClick={() => { if (context.observation) write.mutate({ text: draft.text, revisions: context.observation.expected_revisions }); }}>{t('actions.import')}</Button>
            <Button type="button" variant="ghost" size="sm" disabled={write.isPending} onClick={() => setDraft(null)}>{t('actions.cancel')}</Button>
        </div>}
    </div>;
};
