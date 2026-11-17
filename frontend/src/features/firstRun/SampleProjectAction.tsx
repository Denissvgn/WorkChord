import { useLayoutEffect, useRef, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '../../components/common/Button';
import { ButtonLink } from '../../components/common/ButtonLink';
import { ConfirmDialog } from '../../components/common/ConfirmDialog';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { useIdentity } from '../identity/identityContext';
import { loadSampleProject, removeSampleProject, type SampleManifest } from './sampleProject';
import { useSampleProject } from './sampleProjectStore';
import { useSetWorkScope } from '../scope/useWorkScope';
import { resolveWorkScope, sameScope, type ScopeIterationRecord, type WorkScope } from '../scope/workScope';
import { useScopeStore } from '../scope/scopeStore';
import { navigateWithoutLeaveGuards } from '../../components/common/leaveGuardBypass';
import { parseScope } from '../../navigation/scopeParams';
import { projectService } from '../../services/projectService';
import { iterationService } from '../../services/iterationService';

export const SampleProjectAction = () => {
    const { t, i18n } = useTranslation();
    const identity = useIdentity()?.identity;
    const { hasAdminAccess } = useAdminAccess();
    const client = useQueryClient();
    const navigate = useNavigate();
    const { setScope } = useSetWorkScope();
    const location = useLocation();
    const remembered = useScopeStore();
    const urlScope = parseScope(location.search);
    const scope = resolveWorkScope(urlScope, remembered, client.getQueryData<ScopeIterationRecord[]>(['iterations']) ?? []);
    const currentScope = useRef(scope);
    useLayoutEffect(() => {
        currentScope.current = { project: urlScope.project ?? remembered.project ?? scope.project,
            iteration: urlScope.iteration ?? remembered.iteration ?? scope.iteration };
    }, [urlScope.project, urlScope.iteration, remembered.project, remembered.iteration, scope.project, scope.iteration]);
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
        const receipt: SampleManifest = { owner, records: [...records], complete: own?.complete ?? false,
            previousScope: remove ? own?.previousScope : scope };
        try {
            if (remove) {
                try {
                    await removeSampleProject(receipt, save);
                } finally {
                    const removed = records.filter(record => !receipt.records.some(item => item.kind === record.kind && item.id === record.id));
                    const selected = currentScope.current;
                    // Move the scope off the deleted records before any page refetches them.
                    if (removed.some(record => record.kind === 'project' && record.id === selected?.project
                        || record.kind === 'iteration' && record.id === selected?.iteration)) {
                        let restored: WorkScope = { project: 'all', iteration: 'backlog' };
                        let repaired = selected;
                        try {
                            const [projects, iterations] = await Promise.all([projectService.getAll(), iterationService.getAll()]);
                            repaired = resolveWorkScope(selected, {}, iterations);
                            const previous = receipt.previousScope;
                            const available = previous && (previous.project === 'all' || projects.some(item => item.id === previous.project))
                                && (previous.iteration === 'backlog' || iterations.some(item => item.id === previous.iteration));
                            restored = resolveWorkScope(available ? previous : { project: 'all' }, {}, iterations);
                        } catch { /* Keep a safe scope when the remaining workspace cannot be read. */ }
                        // Iteration validation may repair the scope while these reads are pending.
                        // A scope still pointing at deleted sample data also needs restoration.
                        const stillRemoved = removed.some(record => record.kind === 'project' && record.id === currentScope.current.project
                            || record.kind === 'iteration' && record.id === currentScope.current.iteration);
                        if (sameScope(currentScope.current, selected) || sameScope(currentScope.current, repaired) || stillRemoved) setScope(restored);
                    }
                    await client.invalidateQueries();
                }
                setConfirming(false);
            } else if (identity.profile) {
                // Verify durable receipt storage before making the first REST write.
                save(receipt);
                const result = await loadSampleProject(receipt, identity.profile, i18n.language, save);
                // Scope validation must know the new iteration before its URL is opened.
                await client.invalidateQueries({ queryKey: ['iterations'] });
                navigateWithoutLeaveGuards(() => navigate(`/plan?project=${result.projectId}&iteration=${result.iterationId}`));
            }
        } catch { setError(true); setRemovalFailed(remove); }
        finally {
            if (!remove) await client.invalidateQueries();
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
                    {own?.complete && project && iteration && <ButtonLink variant="secondary" to={`/plan?project=${project.id}&iteration=${iteration.id}`}>{t('firstRun.openPlan')}</ButtonLink>}
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
