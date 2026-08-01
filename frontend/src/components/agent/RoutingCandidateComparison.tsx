import { CheckCircle2, ShieldX } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type {
    AgentActorRosterItem,
    AgentRoutingCandidate,
    AgentRoutingExclusion,
    AgentRoutingPreviewResponse,
} from '../../types/agent';
import { formatRoutingCode } from '../../utils/modelRouting';

const routingCandidateKey = (
    candidate: Pick<AgentRoutingCandidate, 'actor_id' | 'model_binding_id'>,
) => `${candidate.actor_id}:${candidate.model_binding_id}`;

interface RoutingCandidateComparisonProps {
    preview: AgentRoutingPreviewResponse;
    roster: AgentActorRosterItem[];
    selectedCandidateKey: string | null;
    onSelectCandidate: (candidate: AgentRoutingCandidate) => void;
    selectionDisabled?: boolean;
}

const EvidenceList = ({ values }: { values: string[] }) => (
    <div className="flex flex-wrap gap-1">
        {values.map(value => (
            <span key={value} className="rounded-full border border-border bg-surface-card px-2 py-0.5 text-xs text-content-secondary">
                {formatRoutingCode(value)}
            </span>
        ))}
    </div>
);

const candidateIdentity = (
    candidate: AgentRoutingCandidate | AgentRoutingExclusion,
    roster: AgentActorRosterItem[],
) => {
    const actor = roster.find(item => item.id === candidate.actor_id);
    return {
        actorName: actor?.display_name ?? `Actor #${candidate.actor_id}`,
        profileName: actor?.profile?.display_name
            ?? (candidate.profile_id ? `Profile #${candidate.profile_id}` : null),
    };
};

export const RoutingCandidateComparison = ({
    preview,
    roster,
    selectedCandidateKey,
    onSelectCandidate,
    selectionDisabled = false,
}: RoutingCandidateComparisonProps) => {
    const { t } = useTranslation();

    return (
        <div className="space-y-4">
            <fieldset className="space-y-3" disabled={selectionDisabled}>
                <legend className="text-sm font-semibold text-content-primary">
                    {t('taskRouting.eligibleCandidates', { count: preview.eligible_candidates.length })}
                </legend>
                {preview.eligible_candidates.length === 0 ? (
                    <div className="rounded-lg border border-dashed border-feedback-warning-border bg-feedback-warning-muted p-4 text-sm text-feedback-warning-foreground">
                        {t('taskRouting.noEligibleCandidates')}
                    </div>
                ) : (
                    preview.eligible_candidates.map(candidate => {
                        const key = routingCandidateKey(candidate);
                        const inputId = `routing-candidate-${preview.preview_id}-${candidate.actor_id}-${candidate.model_binding_id}`;
                        const identity = candidateIdentity(candidate, roster);
                        const selected = key === selectedCandidateKey;
                        return (
                            <label
                                key={key}
                                htmlFor={inputId}
                                aria-label={t('taskRouting.selectCandidate', {
                                    actor: identity.actorName,
                                    profile: identity.profileName ?? t('common.unknownProfile'),
                                    model: candidate.configured_model_alias,
                                })}
                                className={`block cursor-pointer rounded-lg border p-4 transition-colors ${
                                    selected
                                        ? 'border-action bg-action-muted'
                                        : 'border-feedback-success-border bg-surface-muted'
                                }`}
                            >
                                <div className="flex items-start gap-3">
                                    <input
                                        id={inputId}
                                        type="radio"
                                        name={`routing-candidate-${preview.preview_id}`}
                                        value={key}
                                        checked={selected}
                                        onChange={() => onSelectCandidate(candidate)}
                                        className="mt-1 h-4 w-4 border-border-strong text-action focus:ring-focus"
                                    />
                                    <div className="min-w-0 flex-1">
                                        <div className="flex flex-wrap items-start justify-between gap-2">
                                            <div>
                                                <p className="font-semibold text-content-primary">
                                                    {t('taskRouting.rankActor', { rank: candidate.rank, actor: identity.actorName })}
                                                </p>
                                                <p className="text-xs text-content-secondary">
                                                    {identity.profileName ?? t('common.unknownProfile')}
                                                    {' · '}{candidate.configured_model_alias}
                                                </p>
                                                <p className="text-xs text-content-tertiary">
                                                    {candidate.model_catalog_key}
                                                    {' · '}
                                                    {t('taskRouting.bindingIdentity', {
                                                        id: candidate.model_binding_id,
                                                        revision: candidate.model_binding_revision,
                                                    })}
                                                </p>
                                            </div>
                                            <span className="inline-flex items-center gap-1 rounded-full border border-feedback-success-border bg-feedback-success-muted px-2 py-0.5 text-xs font-medium text-feedback-success-foreground">
                                                <CheckCircle2 aria-hidden="true" className="h-3.5 w-3.5" />
                                                {t('taskRouting.eligible')}
                                            </span>
                                        </div>
                                        <dl className="mt-3 grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                                            <div><dt className="text-content-tertiary">{t('taskRouting.modelEnvelope')}</dt><dd className="text-content-primary">{candidate.reasoning_tier} / {candidate.context_tier}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.costLatency')}</dt><dd className="text-content-primary">{candidate.cost_tier} / {candidate.latency_tier}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.availableCapacity')}</dt><dd className="text-content-primary tnum">{candidate.available_capacity_days}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.committedEffort')}</dt><dd className="text-content-primary tnum">{candidate.committed_effort_days}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.queue')}</dt><dd className="text-content-primary tnum">{candidate.queued_assignments} / {candidate.accepted_assignments}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.runningRuns')}</dt><dd className="text-content-primary tnum">{candidate.running_runs}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.workload')}</dt><dd className="text-content-primary tnum">{Math.round(candidate.workload_ratio * 100)}%</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.vacationConflict')}</dt><dd className="text-content-primary">{t('common.no')}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.scheduleDelay')}</dt><dd className="text-content-primary tnum">{candidate.schedule_delay_days}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.bindingRevision')}</dt><dd className="text-content-primary tnum">{candidate.model_binding_revision}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('taskRouting.confidence')}</dt><dd className="text-content-primary tnum">{Math.round(candidate.confidence * 100)}%</dd></div>
                                        </dl>
                                        <div className="mt-3 space-y-2">
                                            <div>
                                                <p className="mb-1 text-xs font-medium text-content-secondary">{t('taskRouting.matchedSkills')}</p>
                                                <EvidenceList values={Object.entries(candidate.matched_skill_levels).map(([keyName, level]) => `${keyName} L${level}`)} />
                                            </div>
                                            <div>
                                                <p className="mb-1 text-xs font-medium text-content-secondary">{t('taskRouting.toolsDataPolicy')}</p>
                                                <EvidenceList values={[...candidate.tool_tags, ...candidate.data_policy_tags]} />
                                            </div>
                                        </div>
                                        <p className="mt-3 text-sm text-content-secondary">{candidate.rationale}</p>
                                    </div>
                                </div>
                            </label>
                        );
                    })
                )}
                {preview.eligible_candidates_omitted > 0 && (
                    <p className="text-xs text-content-tertiary">
                        {t('taskRouting.candidatesOmitted', { count: preview.eligible_candidates_omitted })}
                    </p>
                )}
            </fieldset>

            <section aria-labelledby={`routing-exclusions-${preview.preview_id}`} className="space-y-3">
                <h4 id={`routing-exclusions-${preview.preview_id}`} className="text-sm font-semibold text-content-primary">
                    {t('taskRouting.excludedCandidates', { count: preview.exclusions.length })}
                </h4>
                {preview.exclusions.length === 0 ? (
                    <p className="text-sm text-content-tertiary">{t('taskRouting.noExclusions')}</p>
                ) : (
                    preview.exclusions.map((exclusion, index) => {
                        const identity = candidateIdentity(exclusion, roster);
                        return (
                            <article
                                key={`${exclusion.actor_id}:${exclusion.model_binding_id ?? 'none'}:${index}`}
                                className="rounded-lg border border-feedback-danger-border bg-feedback-danger-muted p-4"
                            >
                                <div className="flex flex-wrap items-start justify-between gap-2">
                                    <div>
                                        <p className="font-semibold text-content-primary">{identity.actorName}</p>
                                        <p className="text-xs text-content-secondary">
                                            {identity.profileName ?? t('common.unknownProfile')}
                                            {exclusion.configured_model_alias ? ` · ${exclusion.configured_model_alias}` : ''}
                                        </p>
                                        <p className="text-xs text-content-tertiary">
                                            {exclusion.model_catalog_key ?? t('taskRouting.noCatalogMatch')}
                                            {' · '}
                                            {exclusion.model_binding_id
                                                ? t('taskRouting.bindingIdentity', {
                                                    id: exclusion.model_binding_id,
                                                    revision: exclusion.model_binding_revision ?? t('common.unknown'),
                                                })
                                                : t('taskRouting.noBindingMatch')}
                                        </p>
                                    </div>
                                    <span className="inline-flex items-center gap-1 rounded-full border border-feedback-danger-border bg-surface-card px-2 py-0.5 text-xs font-medium text-feedback-danger-foreground">
                                        <ShieldX aria-hidden="true" className="h-3.5 w-3.5" />
                                        {t('taskRouting.excluded')}
                                    </span>
                                </div>
                                <div className="mt-3">
                                    <p className="mb-1 text-xs font-medium text-feedback-danger-foreground">{t('taskRouting.hardBlockers')}</p>
                                    <EvidenceList values={exclusion.hard_blocker_codes} />
                                </div>
                                {(exclusion.missing_skill_keys.length > 0
                                    || exclusion.insufficient_skill_keys.length > 0
                                    || exclusion.blocking_weakness_keys.length > 0) && (
                                    <div className="mt-2">
                                        <p className="mb-1 text-xs font-medium text-content-secondary">{t('taskRouting.missingSkills')}</p>
                                        <EvidenceList values={[
                                            ...exclusion.missing_skill_keys,
                                            ...exclusion.insufficient_skill_keys,
                                            ...exclusion.blocking_weakness_keys,
                                        ]} />
                                    </div>
                                )}
                                {(exclusion.missing_modality_tags.length > 0 || exclusion.missing_tool_tags.length > 0 || exclusion.missing_data_policy_tags.length > 0) && (
                                    <div className="mt-2">
                                        <p className="mb-1 text-xs font-medium text-content-secondary">{t('taskRouting.missingCapabilities')}</p>
                                        <EvidenceList values={[
                                            ...exclusion.missing_modality_tags,
                                            ...exclusion.missing_tool_tags,
                                            ...exclusion.missing_data_policy_tags,
                                        ]} />
                                    </div>
                                )}
                                <dl className="mt-3 grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.costLatency')}</dt>
                                        <dd className="text-content-primary">
                                            {exclusion.cost_tier ?? t('common.unknown')}
                                            {' / '}
                                            {exclusion.latency_tier ?? t('common.unknown')}
                                        </dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.availableCapacity')}</dt>
                                        <dd className="text-content-primary tnum">{exclusion.available_capacity_days ?? t('common.unknown')}</dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.committedEffort')}</dt>
                                        <dd className="text-content-primary tnum">{exclusion.committed_effort_days ?? t('common.unknown')}</dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.queue')}</dt>
                                        <dd className="text-content-primary tnum">
                                            {exclusion.queued_assignments ?? t('common.unknown')}
                                            {' / '}
                                            {exclusion.accepted_assignments ?? t('common.unknown')}
                                        </dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.runningRuns')}</dt>
                                        <dd className="text-content-primary tnum">{exclusion.running_runs ?? t('common.unknown')}</dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.workload')}</dt>
                                        <dd className="text-content-primary tnum">
                                            {exclusion.workload_ratio === null
                                                ? t('common.unknown')
                                                : `${Math.round(exclusion.workload_ratio * 100)}%`}
                                        </dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.vacationConflict')}</dt>
                                        <dd className="text-content-primary">
                                            {exclusion.vacation_conflict === null
                                                ? t('common.unknown')
                                                : exclusion.vacation_conflict
                                                    ? t('common.yes')
                                                    : t('common.no')}
                                        </dd>
                                    </div>
                                    <div>
                                        <dt className="text-content-tertiary">{t('taskRouting.scheduleDelay')}</dt>
                                        <dd className="text-content-primary tnum">{exclusion.schedule_delay_days ?? t('common.unknown')}</dd>
                                    </div>
                                </dl>
                                <p className="mt-3 text-sm text-content-secondary">{exclusion.rationale}</p>
                            </article>
                        );
                    })
                )}
                {preview.exclusions_omitted > 0 && (
                    <p className="text-xs text-content-tertiary">
                        {t('taskRouting.exclusionsOmitted', { count: preview.exclusions_omitted })}
                    </p>
                )}
            </section>
        </div>
    );
};
