import { useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { agentService } from '../../services/agentService';
import type { AgentModelCatalogCreate, AgentTeamMaster, AgentTeamMemberSpec, AgentTeamPlan, AgentTeamRole } from '../../types/agent';
import { buildConnectedMember, connectIssue, credentialFilename, hasPM, roleNames, runtimeNames, runtimeSnippet, type AgentRuntime, type ConnectIssue } from '../../features/agentTeamSetup/connectAgent';
import { assertAgentTeamMasterSecretFree } from '../../features/agentTeamSetup/manifest';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { createAgentCommandMetadata } from '../../utils/modelRouting';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { AdminAccessPanel } from '../settings/AdminAccessPanel';
import { SharedUnlockContext } from '../settings/sharedUnlock';
import AgentManifestWorkflow from './AgentManifestWorkflow';

const steps = ['Role', 'Runtime', 'Model', 'Review', 'Connect'];
const descriptions: Record<AgentTeamRole, string> = {
    pm: 'Plans work and coordinates the team.', worker: 'Carries out assigned work and supplies evidence.',
    verifier: 'Checks completed work against its acceptance criteria.',
};
type Candidate = { manifest: AgentTeamMaster; member: AgentTeamMemberSpec; plan: AgentTeamPlan; filename: string };
const emptyModel: AgentModelCatalogCreate = {
    key: '', provider: '', configured_model_alias: '', reasoning_tier: 2, context_tier: 'medium', cost_tier: 'medium', latency_tier: 'balanced', modality_tags: ['text'],
};
const selectClass = 'w-full rounded-md border border-border bg-surface px-3 py-2 text-sm';

export const ConnectAgentSteps = () => {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const [unlock, setUnlock] = useState(false);
    const [advanced, setAdvanced] = useState(false);
    const [step, setStep] = useState(0);
    const [role, setRole] = useState<AgentTeamRole>('worker');
    const [runtime, setRuntime] = useState<AgentRuntime>('codex');
    const [model, setModel] = useState('');
    const [candidate, setCandidate] = useState<Candidate | null>(null);
    const [issues, setIssues] = useState<ConnectIssue[]>([]);
    const [busy, setBusy] = useState(false);
    const inFlight = useRef(false);
    const [applied, setApplied] = useState(false);
    const [uncertain, setUncertain] = useState(false);
    const command = useRef<ReturnType<typeof createAgentCommandMetadata> | null>(null);
    const [adding, setAdding] = useState(false);
    const [draft, setDraft] = useState<AgentModelCatalogCreate>(emptyModel);
    const [modelError, setModelError] = useState(false);
    const heading = useRef<HTMLHeadingElement>(null);
    const previousStep = useRef(step);

    // feedback-policy: query loading,error,retry,empty - access prompt and loading/retry states precede the steps.
    const status = useQuery({ queryKey: ['agent-team-setup', 'current'], queryFn: () => agentService.getAgentTeamStatus(),
        enabled: hasAdminKey, retry: false, refetchInterval: applied ? 3000 : false });
    // feedback-policy: query loading,error,retry,empty - a server template covers an empty topology.
    const points = useQuery({ queryKey: ['agent-team-setup', 'starting-points'], queryFn: () => agentService.getAgentTeamStartingPoints(),
        enabled: hasAdminKey && status.data?.can_mutate === true, retry: false });
    // feedback-policy: query loading,error,retry,empty - model step offers an empty state and Add entry.
    const catalog = useQuery({ queryKey: ['agent-model-catalog'], queryFn: () => agentService.getModelCatalog(),
        enabled: hasAdminKey && status.data?.can_mutate === true, retry: false });

    useEffect(() => {
        if (previousStep.current !== step) heading.current?.focus();
        previousStep.current = step;
    }, [step]);

    const memberStatus = status.data?.members.find(member => member.actor_key === candidate?.member.actor_key);
    const connected = applied && !status.isError && memberStatus?.package_acknowledged
        && memberStatus.acknowledgement_state === 'current' && memberStatus.connection_state === 'observed';
    const reset = () => { setCandidate(null); setIssues([]); command.current = null; setUncertain(false); };
    const showIssues = (next: ConnectIssue[]) => { setIssues(next); setStep(next[0]?.step ?? 3); };
    const requestIssues = (error: unknown) => {
        const detail = axios.isAxiosError(error) ? error.response?.data?.detail : null;
        if (Array.isArray(detail)) return detail.map(item => connectIssue(String(item.type ?? 'invalid_answer'), Array.isArray(item.loc) ? item.loc.join('.') : ''));
        return [connectIssue(typeof detail?.code === 'string' ? detail.code : 'request_failed')];
    };
    const review = async () => {
        if (inFlight.current) return;
        inFlight.current = true; setBusy(true); reset();
        try {
            // Re-read both snapshots together; planning fences against a subsequent topology change.
            const [freshStatus, freshPoints] = await Promise.all([status.refetch(), points.refetch()]);
            if (!freshStatus.data || freshStatus.error || !freshPoints.data || freshPoints.error || !freshStatus.data.can_mutate) throw new Error('unavailable');
            const built = buildConnectedMember(freshPoints.data, freshStatus.data, role, runtime, model);
            const validation = await agentService.validateAgentTeamMaster(built.manifest);
            if (!validation.valid || validation.blocker_codes.length) { showIssues(validation.blocker_codes.length ? validation.blocker_codes.map(code => connectIssue(code)) : [connectIssue('validation_failed')]); return; }
            const plan = await agentService.planAgentTeamMaster(built.manifest, freshStatus.data.topology_revision ?? 0);
            const action = plan.actions.find(item => item.actor_key === built.member.actor_key && item.operation === 'create_member');
            const blockers = [...plan.blocker_codes, ...plan.actions.filter(item => item.actor_key === built.member.actor_key && item.blocker_code).map(item => item.blocker_code!)];
            if (blockers.length || !action) { showIssues(blockers.length ? blockers.map(code => connectIssue(code)) : [connectIssue('create_action_unavailable')]); return; }
            setCandidate({ ...built, plan, filename: await credentialFilename(built.member) });
            setStep(3);
        } catch (error) { showIssues(requestIssues(error)); }
        finally { inFlight.current = false; setBusy(false); }
    };
    const apply = async () => {
        if (!candidate || inFlight.current) return;
        const action = candidate.plan.actions.find(item => item.actor_key === candidate.member.actor_key && item.operation === 'create_member');
        if (!action) return;
        inFlight.current = true; setBusy(true); setIssues([]);
        command.current ??= createAgentCommandMetadata(`Connect ${candidate.member.display_name} using ${runtimeNames[runtime]} and model ${model}.`);
        try {
            const receipt = await agentService.applyAgentTeamAction(candidate.manifest, candidate.plan, action.action_id, true, command.current);
            const ownReceipt = receipt.receipts.find(item => item.action_id === action.action_id);
            if (ownReceipt?.status !== 'applied' && ownReceipt?.status !== 'no_change') {
                setIssues((receipt.blocker_codes.length ? receipt.blocker_codes : ['apply_incomplete']).map(code => ({ ...connectIssue(code), step: 4 })));
                setUncertain(true); return;
            }
            setUncertain(false); setApplied(true); await status.refetch();
        } catch {
            setUncertain(true);
            setIssues([{ step: 4, code: 'apply_unconfirmed', message: 'The server response was interrupted. Retry this same request to recover its receipt; do not create another agent.' }]);
        } finally { inFlight.current = false; setBusy(false); }
    };
    const addModel = async () => {
        if (inFlight.current) return;
        inFlight.current = true; setBusy(true); setModelError(false);
        try {
            assertAgentTeamMasterSecretFree(draft);
            const result = await agentService.createModelCatalogEntry(draft, createAgentCommandMetadata(`Add model ${draft.key} for agent connection.`));
            await catalog.refetch(); setModel(result.result.key); reset(); setAdding(false);
        } catch { setModelError(true); }
        finally { inFlight.current = false; setBusy(false); }
    };
    const loading = status.isPending || (status.data?.can_mutate && (points.isPending || catalog.isPending));
    const failed = status.isError || points.isError || catalog.isError;
    const available = hasAdminKey && status.data?.can_mutate && points.data && catalog.data;
    const pmAvailable = available && !hasPM(points.data.current, status.data!);
    const editStep = (index: number) => { if (!applied && !uncertain && !busy) { setStep(index); } };

    return <SharedUnlockContext.Provider value={{ noteId: 'connect-unlock-note' }}>
        <div className="space-y-6">
            <div className="flex items-start justify-between gap-4">
                <div><h2 className="text-lg font-semibold">Connect an agent</h2><p id="connect-unlock-note" className="mt-1 text-sm text-content-secondary">Choose a role, runtime and model, then review and connect.</p></div>
                {(!hasAdminKey || status.isError || status.data?.can_mutate === false) && <Button variant="secondary" aria-expanded={unlock} onClick={() => setUnlock(!unlock)}>{t('settings.unlockEditing')}</Button>}
            </div>
            {unlock && <AdminAccessPanel headingLevel={3} />}
            {!hasAdminKey ? <p className="text-sm text-content-secondary">Unlock editing to read the current team and connect an agent.</p> : <>
                {loading && <p role="status">Loading the team and model catalog…</p>}
                {failed && <div role="alert" className="space-y-2"><p>Could not load the team. Check access and try again.</p><Button variant="secondary" onClick={() => { void status.refetch(); void points.refetch(); void catalog.refetch(); }}>Retry loading</Button></div>}
                {!loading && !failed && !status.data?.can_mutate && <p role="alert">This session cannot edit the team. Use Unlock editing with an administrator key.</p>}
                {available && !advanced && <>
                    <ol aria-label="Connection steps" className="grid grid-cols-5 border-b border-border">
                        {steps.map((label, index) => <li key={label}><button type="button" aria-current={step === index ? 'step' : undefined}
                            disabled={busy || applied || uncertain || index > step} onClick={() => editStep(index)}
                            className={`w-full border-b-2 px-3 py-3 text-left text-sm disabled:cursor-default ${step === index ? 'border-action font-semibold text-action' : 'border-transparent text-content-secondary'}`}>{index + 1}. {label}</button></li>)}
                    </ol>
                    <section aria-labelledby="connect-step-title" aria-busy={busy} className="max-w-3xl space-y-5">
                        <h3 ref={heading} tabIndex={-1} id="connect-step-title" className="text-base font-semibold">{step + 1}. {steps[step]}</h3>
                        {step === 0 && <fieldset className="space-y-3"><legend className="mb-3 text-sm">What will this agent do?</legend>
                            {(['worker', 'verifier', ...(pmAvailable ? ['pm'] : [])] as AgentTeamRole[]).map(value => <label key={value} className="flex cursor-pointer items-start gap-3 py-2">
                                <input type="radio" aria-label={roleNames[value]} aria-describedby={`role-description-${value}`} name="agent-role" checked={role === value} disabled={busy} onChange={() => { setRole(value); reset(); }} className="mt-1" />
                                <span><strong className="text-sm">{roleNames[value]}</strong><span id={`role-description-${value}`} className="block text-sm text-content-secondary">{descriptions[value]}</span></span>
                            </label>)}
                            {!pmAvailable && <p className="text-sm text-content-secondary">This team already has a PM. A team can have one PM.</p>}
                        </fieldset>}
                        {step === 1 && <fieldset className="space-y-3"><legend className="mb-3 text-sm">Where will the agent run?</legend>
                            {(Object.keys(runtimeNames) as AgentRuntime[]).map(value => <label key={value} htmlFor={`runtime-${value}`} className="flex cursor-pointer items-center gap-3 py-2 text-sm"><input id={`runtime-${value}`} type="radio" name="agent-runtime" checked={runtime === value} disabled={busy} onChange={() => { setRuntime(value); reset(); }} />{runtimeNames[value]}</label>)}
                        </fieldset>}
                        {step === 2 && <div className="space-y-3">
                            <label className="block space-y-2 text-sm"><span>Which model will it use?</span><select className={selectClass} value={model} disabled={busy} onChange={event => { setModel(event.target.value); reset(); }}><option value="">Choose a catalog model</option>{catalog.data.filter(entry => entry.enabled).map(entry => <option key={entry.key} value={entry.key}>{entry.configured_model_alias} · {entry.provider}</option>)}</select></label>
                            {!catalog.data.some(entry => entry.enabled) && <p className="text-sm">No enabled models yet. Add an entry to continue.</p>}
                            {runtime === 'pi' && <p className="text-sm text-content-secondary">Choose the local model configured in Pi. Catalog entries describe models; they do not install them.</p>}
                            <Button variant="secondary" disabled={busy} onClick={() => setAdding(true)}>Add a model entry</Button>
                        </div>}
                        {step === 3 && candidate && <>
                            <p className="text-sm">The server validated and planned this change. Connect applies only this member’s create action.</p>
                            <dl className="divide-y divide-border text-sm">{[
                                ['Member to create', candidate.member.display_name], ['Role', roleNames[role]], ['Runtime', runtimeNames[runtime]],
                                ['Profile', candidate.member.profile_key], ['Model binding', candidate.member.default_model_binding_key],
                                ['Skill package', `${candidate.member.skill_package.name} ${candidate.member.skill_package.version}`],
                            ].map(([label, value]) => <div key={label} className="grid grid-cols-[160px_1fr] gap-4 py-3"><dt className="text-content-secondary">{label}</dt><dd className="break-words font-medium">{value}</dd></div>)}</dl>
                            {!points.data.current && <p className="text-sm text-content-secondary">The server template also declares a PM and a Worker so the manifest is complete. Other declared members stay pending until you apply them in Advanced.</p>}
                            <p className="text-sm text-content-secondary">Existing members are preserved. The server will write the new key to its credential folder.</p>
                        </>}
                        {step === 4 && candidate && <>
                            {!applied ? <p className="text-sm">Create {candidate.member.display_name} and deliver its key to the server’s credential folder.</p> : <>
                                <p role="status" className="font-medium">{connected ? 'Connected' : 'Waiting for the runtime acknowledgement…'}</p>
                                <dl className="space-y-3 text-sm"><div><dt className="text-content-secondary">Credential folder reference</dt><dd className="break-all font-mono">{candidate.manifest.credential_sink_ref}</dd></div>
                                    <div><dt className="text-content-secondary">Credential file</dt><dd className="break-all font-mono">{candidate.filename}</dd></div>
                                    <div><dt className="text-content-secondary">Skill package to install</dt><dd>{candidate.member.skill_package.name} {candidate.member.skill_package.version}</dd><dd className="break-all font-mono text-xs">SHA-256: {candidate.member.skill_package.sha256}</dd></div></dl>
                                <p className="text-sm text-content-secondary">On the runtime host, set WORKCHORD_CREDENTIAL_DIR to the private folder for this sink reference. For a remote runtime, the operator must deliver the credential file through the approved secure channel. Run the snippet with jq installed; the key stays in that runtime’s environment.</p>
                                <pre aria-label={`${runtimeNames[runtime]} configuration`} className="overflow-x-auto rounded-md border border-border bg-surface-muted p-4 text-xs"><code>{runtimeSnippet(runtime, candidate.manifest.server_url, candidate.filename)}</code></pre>
                                <p className="text-sm">Install the exact role package from the server skill catalog. Give the runtime the handoff below and ask it to acknowledge onboarding using its own key, then connect to WorkChord.</p>
                                {memberStatus?.handoff && <details><summary className="cursor-pointer text-sm">Runtime handoff</summary><pre className="mt-2 overflow-x-auto rounded-md border border-border p-3 text-xs">{JSON.stringify(memberStatus.handoff, null, 2)}</pre></details>}
                                <Button variant="secondary" disabled={status.isFetching} onClick={() => void status.refetch()}>Check connection</Button>
                            </>}
                        </>}
                        {issues.filter(issue => issue.step === step).map((issue, index) => <div key={index} role="alert" className="space-y-2 text-sm text-feedback-danger-foreground"><p>{issue.message}</p><details><summary className="cursor-pointer">Server code</summary><code>{issue.code}</code></details></div>)}
                        <div className="flex gap-3 border-t border-border pt-4">
                            {step > 0 && !applied && !uncertain && <Button variant="secondary" disabled={busy} onClick={() => editStep(step - 1)}>Back</Button>}
                            {step < 2 && <Button disabled={busy || (role === 'pm' && !pmAvailable)} onClick={() => { setIssues([]); setStep(step + 1); }}>Continue</Button>}
                            {(step === 2 || (step === 3 && !candidate)) && <Button disabled={busy || !model} onClick={() => void review()}>{busy ? 'Reviewing…' : 'Review change'}</Button>}
                            {step === 3 && candidate && <Button onClick={() => setStep(4)}>Continue to Connect</Button>}
                            {step === 4 && !applied && <Button disabled={busy || !candidate} onClick={() => void apply()}>{busy ? 'Connecting…' : uncertain ? 'Retry connection' : 'Connect agent'}</Button>}
                        </div>
                    </section>
                </>}
            </>}
            <details open={advanced} onToggle={event => setAdvanced(event.currentTarget.open)} className="border-t border-border pt-4">
                <summary className="cursor-pointer text-sm font-medium">Advanced: apply a team manifest</summary>
                {advanced && <div className="mt-5"><AgentManifestWorkflow embedded /></div>}
            </details>
        </div>
        <SlideOverDrawer open={adding} title="Add a model entry" onClose={() => { if (!busy) setAdding(false); }} closeDisabled={busy}
            footer={<Button disabled={busy || !draft.key || !draft.provider || !draft.configured_model_alias} onClick={() => void addModel()}>{busy ? 'Adding…' : 'Add model'}</Button>}>
            <div className="space-y-4">
                <Input label="Catalog key" value={draft.key} onChange={event => setDraft({ ...draft, key: event.target.value })} />
                <Input label="Provider" value={draft.provider} onChange={event => setDraft({ ...draft, provider: event.target.value })} />
                <Input label="Model name" value={draft.configured_model_alias} onChange={event => setDraft({ ...draft, configured_model_alias: event.target.value })} />
                <label className="block space-y-2 text-sm"><span>Reasoning tier</span><select className={selectClass} value={draft.reasoning_tier} onChange={event => setDraft({ ...draft, reasoning_tier: Number(event.target.value) as 1 | 2 | 3 })}>{[1, 2, 3].map(value => <option key={value}>{value}</option>)}</select></label>
                {(['context_tier', 'cost_tier', 'latency_tier'] as const).map(field => <label key={field} className="block space-y-2 text-sm"><span>{field === 'context_tier' ? 'Context size' : field === 'cost_tier' ? 'Cost' : 'Latency'}</span><select className={selectClass} value={draft[field]} onChange={event => setDraft({ ...draft, [field]: event.target.value })}>{(field === 'context_tier' ? ['small', 'medium', 'large'] : field === 'cost_tier' ? ['low', 'medium', 'high'] : ['fast', 'balanced', 'slow']).map(value => <option key={value}>{value}</option>)}</select></label>)}
                {modelError && <p role="alert">Could not add this model. Use a unique lowercase catalog key and check the provider and model name.</p>}
            </div>
        </SlideOverDrawer>
    </SharedUnlockContext.Provider>;
};
