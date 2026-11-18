import { useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { agentService } from '../../services/agentService';
import { teamService } from '../../services/teamService';
import type { AgentModelCatalogCreate, AgentTeamMaster, AgentTeamMemberSpec, AgentTeamPlan, AgentTeamRole } from '../../types/agent';
import {
    AGENT_RUNTIMES, CONNECT_STEPS, RUNTIME_PRODUCT_NAMES, STEP_INDEX, applyOutcomeUnknown, buildConnectedMember, connectIssue, hasPM, isConnected,
    replacesPendingPM, waitingMembers, type AgentRuntime, type ConnectIssue,
} from '../../features/agentTeamSetup/connectAgent';
import { assertAgentTeamMasterSecretFree } from '../../features/agentTeamSetup/manifest';
import { AGENT_PROFILE_PRESET_NAMES } from '../../features/agentTeamSetup/profilePresetNames';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { createAgentCommandMetadata } from '../../utils/modelRouting';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Select } from '../common/Select';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { AdminAccessPanel } from '../settings/AdminAccessPanel';
import { SharedUnlockContext } from '../settings/sharedUnlock';
import { InlineEmptyState } from '../ui/InlineEmptyState';
import AgentManifestWorkflow from './AgentManifestWorkflow';
import { ConnectionSteps } from './ConnectionSteps';

/** A member the Connect steps are working on. A resumed member has no plan: it already exists and only waits for its runtime. */
type Candidate = { manifest: AgentTeamMaster; member: AgentTeamMemberSpec; plan?: AgentTeamPlan };
const emptyModel: AgentModelCatalogCreate = {
    key: '', provider: '', configured_model_alias: '', reasoning_tier: 2, context_tier: 'medium', cost_tier: 'medium', latency_tier: 'balanced', modality_tags: ['text'],
};
const tierOptions = {
    context_tier: ['small', 'medium', 'large'], cost_tier: ['low', 'medium', 'high'], latency_tier: ['fast', 'balanced', 'slow'],
} as const;
const tierLabels = { context_tier: 'contextTier', cost_tier: 'costTier', latency_tier: 'latencyTier' } as const;
const P = 'agentTeamSetup.connect';
type ModelErrorKind = 'refused' | 'input' | 'unavailable';
const MODEL_ERROR_MESSAGES = { refused: 'addModelRefused', input: 'addModelFailed', unavailable: 'addModelUnavailable' } as const;
/** A refused credential is not an input mistake; only a rejected entry blames the fields. */
const modelErrorKind = (error: unknown): ModelErrorKind => {
    if (!axios.isAxiosError(error)) return 'input';
    const code = error.response?.status;
    if (code === 401 || code === 403) return 'refused';
    if (code === 400 || code === 409 || code === 422) return 'input';
    return 'unavailable';
};

/**
 * Connects one agent by five answers. The manifest is the current topology plus
 * the new member; the server validates, plans and applies it, and writes the new
 * member's key only to its credential folder. No key reaches this page.
 */
/** The server's own reason for a failed read: its message and code, when it sent them. */
const serverReason = (error: unknown): { message: string | null; code: string | null } => {
    const detail = axios.isAxiosError(error) ? error.response?.data?.detail : null;
    const text = (value: unknown) => (typeof value === 'string' && value.trim() ? value.trim().slice(0, 300) : null);
    if (typeof detail === 'string') return { message: text(detail), code: null };
    const code = text(detail?.code);
    const status = axios.isAxiosError(error) ? error.response?.status : undefined;
    return { message: text(detail?.message), code: code ? (status ? `${code} (${status})` : code) : null };
};
const SETUP_GUIDE_URL = 'https://github.com/Denissvgn/WorkChord/blob/main/docs/agent-team-setup.md#prerequisites';

export const ConnectAgentSteps = ({ showTitle = true }: { showTitle?: boolean }) => {
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
    // The server created the member but could not confirm the key delivery; only an explicit replacement recovers it.
    const [deliveryBlocked, setDeliveryBlocked] = useState(false);
    const command = useRef<ReturnType<typeof createAgentCommandMetadata> | null>(null);
    const previousAttempt = useRef<string | undefined>(undefined);
    const [adding, setAdding] = useState(false);
    const [draft, setDraft] = useState<AgentModelCatalogCreate>(emptyModel);
    const [modelError, setModelError] = useState<ModelErrorKind | null>(null);
    const heading = useRef<HTMLHeadingElement>(null);
    const previousStep = useRef(step);

    // feedback-policy: query loading,error,retry,empty - access prompt and loading/retry states precede the steps.
    const status = useQuery({ queryKey: ['agent-team-setup', 'current'], queryFn: () => agentService.getAgentTeamStatus(),
        enabled: hasAdminKey, retry: false, refetchInterval: applied ? 3000 : false });
    // feedback-policy: query loading,error,retry,empty - a server template covers an empty topology.
    const points = useQuery({ queryKey: ['agent-team-setup', 'starting-points'], queryFn: () => agentService.getAgentTeamStartingPoints(),
        enabled: hasAdminKey && status.data?.can_mutate === true, retry: false });
    // feedback-policy: query loading,error,retry,empty - the model step offers an empty state and Add a model entry.
    const catalog = useQuery({ queryKey: ['agent-model-catalog', false], queryFn: () => agentService.getModelCatalog(),
        enabled: hasAdminKey && status.data?.can_mutate === true, retry: false });

    // feedback-policy: query loading,error,retry,empty - the name is a courtesy; without it the member's own name is announced.
    const profiles = useQuery({ queryKey: ['team-member-profiles'], queryFn: () => teamService.getProfiles(),
        enabled: hasAdminKey && status.data?.can_mutate === true, retry: false });

    useEffect(() => {
        if (previousStep.current !== step) heading.current?.focus();
        previousStep.current = step;
    }, [step]);

    const runtimeName = (value: AgentRuntime) => RUNTIME_PRODUCT_NAMES[value] ?? t(`${P}.runtimes.${value}`);
    /** The name Team and the assignee lists show: the profile's display name, which the profile preset names when the server creates the profile. */
    const announcedName = (member: AgentTeamMemberSpec) => (Array.isArray(profiles.data) ? profiles.data.find(item => item.seed_key === member.profile_key)?.display_name : undefined)
        ?? AGENT_PROFILE_PRESET_NAMES[member.profile_key]
        ?? member.display_name;
    const memberStatus = status.data?.members.find(member => member.actor_key === candidate?.member.actor_key);
    const connected = applied && !status.isError && isConnected(memberStatus);
    const reset = () => { setCandidate(null); setIssues([]); command.current = null; setUncertain(false); };
    const showIssues = (next: ConnectIssue[]) => { setIssues(next); setStep(Math.min(...next.map(issue => issue.step), STEP_INDEX.review)); };
    const requestIssues = (error: unknown): ConnectIssue[] => {
        const detail = axios.isAxiosError(error) ? error.response?.data?.detail : null;
        if (Array.isArray(detail)) {
            return detail.map(item => connectIssue(String(item?.type ?? 'invalid_answer'), Array.isArray(item?.loc) ? item.loc.join('.') : ''));
        }
        if (typeof detail?.code === 'string') return [connectIssue(detail.code)];
        return [{ step: STEP_INDEX.review, reason: axios.isAxiosError(error) ? 'other' : 'unavailable', code: 'request_failed' }];
    };
    const review = async () => {
        if (inFlight.current) return;
        inFlight.current = true; setBusy(true); reset();
        try {
            // Read both snapshots again together; the plan is fenced to the topology revision read here.
            const [freshStatus, freshPoints] = await Promise.all([status.refetch(), points.refetch()]);
            if (!freshStatus.data || freshStatus.error || !freshPoints.data || freshPoints.error || !freshStatus.data.can_mutate) {
                setIssues([{ step: STEP_INDEX.review, reason: 'unavailable', code: 'team_unavailable' }]); setStep(STEP_INDEX.review); return;
            }
            const built = buildConnectedMember(freshPoints.data, freshStatus.data, role, runtime, model, previousAttempt.current);
            const validation = await agentService.validateAgentTeamMaster(built.manifest);
            if (!validation.valid || validation.blocker_codes.length) {
                showIssues((validation.blocker_codes.length ? validation.blocker_codes : ['validation_failed']).map(code => connectIssue(code)));
                return;
            }
            const plan = await agentService.planAgentTeamMaster(built.manifest, freshStatus.data.topology_revision ?? 0);
            const action = plan.actions.find(item => item.actor_key === built.member.actor_key && item.operation === 'create_member');
            const blockers = [...plan.blocker_codes, ...plan.actions.filter(item => item.actor_key === built.member.actor_key && item.blocker_code).map(item => item.blocker_code!)];
            if (blockers.length || !action) {
                showIssues((blockers.length ? blockers : ['create_action_unavailable']).map(code => connectIssue(code)));
                return;
            }
            setCandidate({ ...built, plan });
            setStep(STEP_INDEX.review);
        } catch (error) {
            showIssues(error instanceof Error && error.message === 'role_unavailable'
                ? [{ step: STEP_INDEX.role, reason: 'role', code: 'role_unavailable' }] : requestIssues(error));
        } finally { inFlight.current = false; setBusy(false); }
    };
    const apply = async () => {
        const plan = candidate?.plan;
        if (!candidate || !plan || inFlight.current) return;
        const action = plan.actions.find(item => item.actor_key === candidate.member.actor_key && item.operation === 'create_member');
        if (!action) return;
        inFlight.current = true; setBusy(true); setIssues([]);
        previousAttempt.current = candidate.member.actor_key;
        // One idempotency key per candidate, so a retry recovers the first receipt instead of creating a second agent.
        command.current ??= createAgentCommandMetadata(`Connect ${candidate.member.display_name} with model ${candidate.member.default_model_binding_key}.`);
        // A settled refusal: the server keeps and replays it for this idempotency key, so the change is reviewed again.
        const reviewAgain = (next: ConnectIssue[]) => { setCandidate(null); command.current = null; setUncertain(false); showIssues(next); };
        try {
            const receipt = await agentService.applyAgentTeamAction(candidate.manifest, plan, action.action_id, true, command.current);
            const ownReceipt = receipt.receipts.find(item => item.action_id === action.action_id);
            if (ownReceipt?.status !== 'applied' && ownReceipt?.status !== 'no_change') {
                const code = ownReceipt?.blocker_code ?? receipt.blocker_codes[0] ?? 'apply_incomplete';
                if (code === 'credential_delivery_uncertain') {
                    setUncertain(false); setDeliveryBlocked(true);
                    setIssues([{ step: STEP_INDEX.connect, reason: 'deliveryUncertain', code }]);
                } else reviewAgain([connectIssue(code)]);
                return;
            }
            setUncertain(false); setApplied(true); await status.refetch();
        } catch (error) {
            if (!applyOutcomeUnknown(error)) { reviewAgain(requestIssues(error)); return; }
            setUncertain(true);
            setIssues([{ step: STEP_INDEX.connect, reason: 'applyUnconfirmed', code: 'apply_unconfirmed' }]);
        } finally { inFlight.current = false; setBusy(false); }
    };
    const addModel = async () => {
        if (inFlight.current) return;
        inFlight.current = true; setBusy(true); setModelError(null);
        try {
            assertAgentTeamMasterSecretFree(draft);
            const result = await agentService.createModelCatalogEntry(draft, createAgentCommandMetadata(`Add model ${draft.key} to connect an agent.`));
            await catalog.refetch(); setModel(result.result.key); reset(); setAdding(false); setDraft(emptyModel);
        } catch (error) { setModelError(modelErrorKind(error)); }
        finally { inFlight.current = false; setBusy(false); }
    };
    const loading = status.isPending || (status.data?.can_mutate && (points.isPending || catalog.isPending));
    const failed = status.isError || points.isError || catalog.isError;
    const loadReasons = [status, points, catalog].map(query => (query.isError ? serverReason(query.error) : null))
        .filter((reason): reason is NonNullable<typeof reason> => Boolean(reason && (reason.message || reason.code)))
        .filter((reason, index, all) => all.findIndex(item => item.code === reason.code && item.message === reason.message) === index);
    const available = hasAdminKey && status.data?.can_mutate && points.data && catalog.data;
    const pmAvailable = Boolean(available && !hasPM(points.data.current, status.data!));
    const roles: AgentTeamRole[] = ['worker', 'verifier', ...(pmAvailable ? ['pm' as const] : [])];
    const locked = applied || uncertain || deliveryBlocked;
    const editStep = (index: number) => { if (!locked && !busy) setStep(index); };
    const stepIssues = issues.filter(issue => issue.step === step);
    const waiting = points.data && status.data ? waitingMembers(points.data.current, status.data) : [];
    // Leaving Connect discards the local steps, so a member that still waits is offered back from the team's own status.
    const resume = (member: AgentTeamMemberSpec) => {
        if (!points.data?.current || inFlight.current) return;
        reset(); setApplied(true); setStep(STEP_INDEX.connect);
        setCandidate({ manifest: points.data.current, member });
    };

    return <SharedUnlockContext.Provider value={{ noteId: 'connect-unlock-note' }}>
        <div className="space-y-6">
            <div className="flex items-start justify-between gap-4">
                <div>
                    {showTitle && <h2 className="text-lg font-semibold">{t(`${P}.title`)}</h2>}
                    <p id="connect-unlock-note" className="mt-1 text-sm text-content-secondary">{t(`${P}.intro`)}</p>
                </div>
                {hasAdminKey && (status.isError || status.data?.can_mutate === false) && (
                    <Button variant="secondary" aria-expanded={unlock} aria-controls="connect-unlock-panel" onClick={() => setUnlock(!unlock)}>
                        {t('settings.unlockEditing')}
                    </Button>
                )}
            </div>
            {unlock && <div id="connect-unlock-panel"><AdminAccessPanel headingLevel={3} /></div>}
            {!hasAdminKey ? <InlineEmptyState
                title={t('emptyStates.team.connectTitle')}
                description={t('emptyStates.team.connectBody')}
                actions={<Button variant="secondary" aria-expanded={unlock} aria-controls="connect-unlock-panel" onClick={() => setUnlock(!unlock)}>
                    {t('emptyStates.team.unlock')}
                </Button>}
            /> : <>
                {loading && <p role="status" className="text-sm">{t(`${P}.loading`)}</p>}
                {failed && <div role="alert" className="space-y-2 text-sm">
                    <p>{t(`${P}.loadFailed`)}</p>
                    {loadReasons.map(reason => <p key={reason.code ?? reason.message}>
                        {reason.message && <span>{t(`${P}.serverReason`, { reason: reason.message })}</span>}
                        {reason.message && reason.code && ' '}
                        {reason.code && <span>{t(`${P}.serverCode`)}: <code>{reason.code}</code></span>}
                    </p>)}
                    <Button variant="secondary" onClick={() => { void status.refetch(); void points.refetch(); void catalog.refetch(); }}>{t(`${P}.retryLoading`)}</Button>
                </div>}
                {!loading && !failed && !status.data?.can_mutate && <p role="alert" className="text-sm">{t(`${P}.cannotEdit`)}</p>}
                {available && !advanced && <>
                    {waiting.length > 0 && !candidate && <section aria-labelledby="connect-resume-title" className="max-w-3xl space-y-3 border-b border-border pb-5">
                        <h3 id="connect-resume-title" className="text-base font-semibold">{t(`${P}.resumeTitle`)}</h3>
                        <p className="text-sm text-content-secondary">{t(`${P}.resumeIntro`)}</p>
                        <div className="flex flex-wrap gap-3">
                            {waiting.map(({ member }) => <Button key={member.actor_key} variant="secondary" disabled={busy}
                                onClick={() => resume(member)}>{t(`${P}.resume`, { name: announcedName(member) })}</Button>)}
                        </div>
                    </section>}
                    <ol aria-label={t(`${P}.stepsLabel`)} className="grid grid-cols-5 border-b border-border">
                        {CONNECT_STEPS.map((id, index) => <li key={id}>
                            <Button type="button" aria-current={step === index ? 'step' : undefined}
                                disabled={busy || locked || index > step} onClick={() => editStep(index)}
                                className={`w-full border-b-2 px-3 py-3 text-left text-sm disabled:cursor-default ${step === index ? 'border-action font-semibold text-action' : 'border-transparent text-content-secondary'}`} variant="secondary">
                                {t(`${P}.stepHeading`, { number: index + 1, name: t(`${P}.steps.${id}`) })}
                            </Button>
                        </li>)}
                    </ol>
                    <section aria-labelledby="connect-step-title" aria-busy={busy} className="max-w-3xl space-y-5">
                        <h3 ref={heading} tabIndex={-1} id="connect-step-title" className="text-base font-semibold">
                            {t(`${P}.stepHeading`, { number: step + 1, name: t(`${P}.steps.${CONNECT_STEPS[step]}`) })}
                        </h3>
                        {step === STEP_INDEX.role && <fieldset className="space-y-3">
                            <legend className="mb-3 text-sm">{t(`${P}.roleQuestion`)}</legend>
                            {roles.map(value => <label key={value} className="flex cursor-pointer items-start gap-3 py-2">
                                <input type="radio" aria-label={t(`${P}.roles.${value}.name`)} aria-describedby={`role-description-${value}`} name="agent-role"
                                    checked={role === value} disabled={busy} onChange={() => { setRole(value); reset(); }} className="mt-1" />
                                <span>
                                    <strong className="text-sm">{t(`${P}.roles.${value}.name`)}</strong>
                                    <span id={`role-description-${value}`} className="block text-sm text-content-secondary">{t(`${P}.roles.${value}.description`)}</span>
                                </span>
                            </label>)}
                            {!pmAvailable && <p className="text-sm text-content-secondary">{t(`${P}.pmTaken`)}</p>}
                        </fieldset>}
                        {step === STEP_INDEX.runtime && <fieldset className="space-y-3">
                            <legend className="mb-3 text-sm">{t(`${P}.runtimeQuestion`)}</legend>
                            {AGENT_RUNTIMES.map(value => <label key={value} htmlFor={`runtime-${value}`} className="flex cursor-pointer items-center gap-3 py-2 text-sm">
                                <input id={`runtime-${value}`} type="radio" name="agent-runtime" checked={runtime === value} disabled={busy} onChange={() => { setRuntime(value); reset(); }} />
                                {runtimeName(value)}
                            </label>)}
                        </fieldset>}
                        {step === STEP_INDEX.model && <div className="space-y-3">
                            <Select label={t(`${P}.modelQuestion`)} value={model} disabled={busy} onChange={event => { setModel(event.target.value); reset(); }}
                                help={runtime === 'pi' ? t(`${P}.piModelNote`) : undefined}>
                                <option value="">{t(`${P}.chooseModel`)}</option>
                                {catalog.data.filter(entry => entry.enabled).map(entry => <option key={entry.key} value={entry.key}>
                                    {t(`${P}.modelOption`, { name: entry.configured_model_alias, provider: entry.provider })}
                                </option>)}
                            </Select>
                            {!catalog.data.some(entry => entry.enabled) && <p className="text-sm">{t(`${P}.noModels`)}</p>}
                            <Button variant="secondary" disabled={busy} onClick={() => setAdding(true)}>{t(`${P}.addModel`)}</Button>
                        </div>}
                        {step === STEP_INDEX.review && candidate && <>
                            <p className="text-sm">{t(`${P}.reviewIntro`)}</p>
                            <dl className="divide-y divide-border text-sm">{([
                                ['member', announcedName(candidate.member)], ['role', t(`${P}.roles.${role}.name`)], ['runtime', runtimeName(runtime)],
                                ['profile', candidate.member.profile_key], ['model', candidate.member.default_model_binding_key],
                                ['package', t(`${P}.packageName`, { name: candidate.member.skill_package.name, version: candidate.member.skill_package.version })],
                            ] as const).map(([label, value]) => <div key={label} className="grid grid-cols-[160px_1fr] gap-4 py-3">
                                <dt className="text-content-secondary">{t(`${P}.reviewList.${label}`)}</dt><dd className="break-words font-medium">{value}</dd>
                            </div>)}</dl>
                            {!points.data.current && <p className="text-sm text-content-secondary">{t(`${P}.templateNote`)}</p>}
                            {role === 'pm' && replacesPendingPM(points.data.current, status.data!) && (
                                <p className="text-sm text-content-secondary">{t(`${P}.pendingPmNote`, { name: points.data.current!.controller.display_name })}</p>
                            )}
                            <p className="text-sm text-content-secondary">{t(`${P}.preserved`)}</p>
                        </>}
                        {step === STEP_INDEX.connect && candidate && <>
                            {!applied ? <p className="text-sm">{t(`${P}.connectIntro`, { name: announcedName(candidate.member) })}</p> : <>
                                <ConnectionSteps manifest={candidate.manifest} member={candidate.member} memberStatus={memberStatus} connected={connected}
                                    checking={status.isFetching} onCheck={() => void status.refetch()} />
                            </>}
                        </>}
                        {stepIssues.map(issue => <div key={`${issue.reason}-${issue.code}`} role="alert" className="space-y-2 text-sm text-feedback-danger-foreground">
                            <p>{t(`${P}.issues.${issue.reason}`)}</p>
                            <details><summary className="cursor-pointer">{t(`${P}.serverCode`)}</summary><code>{issue.code}</code></details>
                            {issue.reason === 'sink' && <p><a href={SETUP_GUIDE_URL} target="_blank" rel="noreferrer" className="underline">{t(`${P}.issues.sinkGuide`)}</a></p>}
                            {issue.reason === 'deliveryUncertain' && (
                                <Button variant="secondary" onClick={() => setAdvanced(true)}>{t(`${P}.openAdvanced`)}</Button>
                            )}
                        </div>)}
                        <div className="flex gap-3 border-t border-border pt-4">
                            {step > 0 && !locked && <Button variant="secondary" disabled={busy} onClick={() => editStep(step - 1)}>{t(`${P}.back`)}</Button>}
                            {step < STEP_INDEX.model && <Button disabled={busy || (role === 'pm' && !pmAvailable)} onClick={() => { setIssues([]); setStep(step + 1); }}>{t(`${P}.continue`)}</Button>}
                            {(step === STEP_INDEX.model || (step === STEP_INDEX.review && !candidate)) && (
                                <Button disabled={busy || !model} onClick={() => void review()}>{busy ? t(`${P}.reviewing`) : t(`${P}.review`)}</Button>
                            )}
                            {step === STEP_INDEX.review && candidate && <Button onClick={() => setStep(STEP_INDEX.connect)}>{t(`${P}.toConnect`)}</Button>}
                            {step === STEP_INDEX.connect && !applied && !deliveryBlocked && (
                                <Button disabled={busy || !candidate} onClick={() => void apply()}>
                                    {busy ? t(`${P}.connecting`) : uncertain ? t(`${P}.retry`) : t(`${P}.connectAction`)}
                                </Button>
                            )}
                        </div>
                    </section>
                </>}
            </>}
            <details open={advanced} onToggle={event => setAdvanced(event.currentTarget.open)} className="border-t border-border pt-4">
                <summary className="cursor-pointer text-sm font-medium">{t(`${P}.advanced`)}</summary>
                {advanced && <div className="mt-5"><AgentManifestWorkflow embedded /></div>}
            </details>
        </div>
        <SlideOverDrawer open={adding} title={t(`${P}.addModel`)} onClose={() => { if (!busy) setAdding(false); }} closeDisabled={busy}
            footer={<Button disabled={busy || !draft.key || !draft.provider || !draft.configured_model_alias} onClick={() => void addModel()}>
                {busy ? t(`${P}.adding`) : t(`${P}.addModel`)}
            </Button>}>
            <div className="space-y-4">
                <Input label={t('modelAdministration.catalogKey')} value={draft.key} onChange={event => setDraft({ ...draft, key: event.target.value })} required />
                <Input label={t('modelAdministration.provider')} value={draft.provider} onChange={event => setDraft({ ...draft, provider: event.target.value })} required />
                <Input label={t('modelAdministration.configuredAlias')} value={draft.configured_model_alias} onChange={event => setDraft({ ...draft, configured_model_alias: event.target.value })} required />
                <Select label={t('modelAdministration.reasoningTier')} value={draft.reasoning_tier} onChange={event => setDraft({ ...draft, reasoning_tier: Number(event.target.value) as 1 | 2 | 3 })}>
                    {[1, 2, 3].map(value => <option key={value} value={value}>{value}</option>)}
                </Select>
                {(Object.keys(tierOptions) as (keyof typeof tierOptions)[]).map(field => (
                    <Select key={field} label={t(`modelAdministration.${tierLabels[field]}`)} value={draft[field]} onChange={event => setDraft({ ...draft, [field]: event.target.value })}>
                        {tierOptions[field].map(value => <option key={value} value={value}>{t(`modelAdministration.${value}`)}</option>)}
                    </Select>
                ))}
                {modelError && <p role="alert" className="text-sm text-feedback-danger-foreground">{t(`${P}.${MODEL_ERROR_MESSAGES[modelError]}`)}</p>}
            </div>
        </SlideOverDrawer>
    </SharedUnlockContext.Provider>;
};
