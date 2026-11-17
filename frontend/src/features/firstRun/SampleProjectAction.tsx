import { useRef, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../../components/common/Button';
import { ConfirmDialog } from '../../components/common/ConfirmDialog';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { useIdentity } from '../identity/identityContext';
import { loadSampleProject, removeSampleProject, type SampleManifest } from './sampleProject';
import { useSampleProject } from './sampleProjectStore';

export const SampleProjectAction = () => {
    const { t, i18n } = useTranslation();
    const identity = useIdentity()?.identity;
    const { hasAdminAccess } = useAdminAccess();
    const client = useQueryClient();
    const navigate = useNavigate();
    const { manifest, busy, save, setBusy } = useSampleProject();
    const [error, setError] = useState(false);
    const [removalFailed, setRemovalFailed] = useState(false);
    const [confirming, setConfirming] = useState(false);
    const locked = useRef(false);
    const owner = identity?.principal ? `principal:${identity.principal.id}` : 'local';
    const own = manifest?.owner === owner ? manifest : null;
    const records = own?.records ?? [];
    // The fixture also creates a reusable profile, so it needs workspace editing authority.
    const canWrite = identity && identity.access !== 'observe' && identity.principal?.kind !== 'agent'
        && (identity.mode === 'trusted_local' && !identity.principal || hasAdminAccess);
    const canLoad = canWrite && identity.profile && (!manifest?.records.length || own);
    if (!canWrite) return null;

    const run = async (remove: boolean) => {
        if (locked.current || useSampleProject.getState().busy) return;
        locked.current = true;
        setBusy(true);
        setError(false);
        setRemovalFailed(false);
        const receipt: SampleManifest = { owner, records: [...records], complete: own?.complete ?? false };
        try {
            if (remove) {
                await removeSampleProject(receipt, save);
                setConfirming(false);
            } else if (identity.profile) {
                // Verify durable receipt storage before making the first REST write.
                save(receipt);
                const result = await loadSampleProject(receipt, identity.profile, i18n.language, save);
                navigate(`/plan?project=${result.projectId}&iteration=${result.iterationId}`);
            }
        } catch { setError(true); setRemovalFailed(remove); }
        finally {
            await client.invalidateQueries();
            setBusy(false);
            locked.current = false;
        }
    };
    const project = records.find(record => record.kind === 'project');
    const iteration = records.find(record => record.kind === 'iteration');
    const inventory = <ul className="list-disc pl-5 text-sm">{records.map(record => (
        <li key={`${record.kind}:${record.id}`}>{t(`firstRun.sample.kinds.${record.kind}`)}: {record.name} (#{record.id})</li>
    ))}</ul>;
    return (
        <div className="space-y-3">
            {records.length === 0 ? <>
                <p className="text-sm text-fg-muted">{t('firstRun.sample.body')}</p>
                <Button variant="secondary" disabled={!canLoad || busy} isLoading={busy} onClick={() => void run(false)}>
                    {t('firstRun.sample.load')}
                </Button>
                {!identity.profile && <p className="text-sm text-fg-muted">{t('firstRun.sample.choosePerson')}</p>}
            </> : <>
                <p role="status" className="text-sm">{t(busy ? 'firstRun.sample.working' : own?.complete ? 'firstRun.sample.loaded' : 'firstRun.sample.partial')}</p>
                <details open={!own?.complete}><summary className="cursor-pointer text-sm">{t('firstRun.sample.exists', { count: records.length })}</summary>{inventory}</details>
                <div className="flex flex-wrap gap-2">
                    {own?.complete && project && iteration && <Link className="btn secondary" to={`/plan?project=${project.id}&iteration=${iteration.id}`}>{t('firstRun.openPlan')}</Link>}
                    <Button variant="secondary" disabled={busy} onClick={() => setConfirming(true)}>{t('firstRun.sample.remove')}</Button>
                </div>
            </>}
            {error && <p role="alert" className="text-sm text-feedback-danger-foreground">{t('firstRun.sample.failed')}</p>}
            {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- The scrollable record list must be keyboard-accessible. */}
            <ConfirmDialog open={confirming} title={t('firstRun.sample.remove')} description={<div className="max-h-[50vh] space-y-3 overflow-y-auto" role="region" tabIndex={0}
                aria-label={t('firstRun.sample.exists', { count: records.length })}>
                <p>{t('firstRun.sample.confirm')}</p>{inventory}
                {removalFailed && <p role="alert">{t('firstRun.sample.removeFailed')}</p>}
            </div>} confirmLabel={t('firstRun.sample.remove')} cancelLabel={t('actions.cancel')} closeLabel={t('actions.close')}
                pending={busy} onCancel={() => { if (!busy) { setConfirming(false); setError(false); } }} onConfirm={() => void run(true)} />
        </div>
    );
};
