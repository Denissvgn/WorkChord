import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    CheckCircle2,
    Plus,
    RefreshCw,
    Route,
    Trash2,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { agentService } from '../../services/agentService';
import type {
    AgentAssignmentPurpose,
    AgentRoutingCandidate,
    AgentTaskAssignment,
    AssessmentReasonCode,
    ModelContextTier,
    ModelReasoningTier,
    TaskDifficultyAxes,
    TaskDifficultyScore,
    TaskReviewMode,
    TaskRoutingAssessment,
    TaskRoutingAssessmentCommand,
    TaskSkillLevel,
} from '../../types/agent';
import type { Task } from '../../types/task';
import { normalizeApiError } from '../../utils/apiError';
import { formatDateTime } from '../../utils/formatDate';
import {
    ASSESSMENT_REASON_CODES,
    createAgentCommandMetadata,
    deriveDifficultyBand,
    formatRoutingCode,
    minimumReviewMode,
    MODEL_AWARE_ROUTING_FEATURE,
    parseRoutingTags,
    reviewModeMeets,
} from '../../utils/modelRouting';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { Input, RequiredIndicator } from '../common/Input';
import {
    QueryEmptyState,
    QueryErrorState,
    QueryLoadingState,
} from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { RoutingCandidateComparison } from './RoutingCandidateComparison';

interface TaskRoutingPanelProps {
    task: Task;
    onAssigned?: () => void;
}

interface AssessmentDraft {
    axes: TaskDifficultyAxes;
    requiredSkillLevels: Record<string, TaskSkillLevel>;
    minimumReasoningTier: ModelReasoningTier;
    minimumContextTier: ModelContextTier;
    modalityTags: string;
    toolTags: string;
    dataPolicyTags: string;
    reviewMode: TaskReviewMode;
    confidence: number;
    reasonCodes: AssessmentReasonCode[];
    rationale: string;
}

const DEFAULT_DRAFT: AssessmentDraft = {
    axes: {
        reasoning: 2,
        ambiguity: 2,
        context_breadth: 2,
        risk: 2,
        verification_burden: 2,
    },
    requiredSkillLevels: {},
    minimumReasoningTier: 2,
    minimumContextTier: 'medium',
    modalityTags: 'text',
    toolTags: '',
    dataPolicyTags: '',
    reviewMode: 'standard',
    confidence: 0.75,
    reasonCodes: [],
    rationale: '',
};

const AXIS_KEYS = [
    'reasoning',
    'ambiguity',
    'context_breadth',
    'risk',
    'verification_burden',
] as const;

const REVIEW_MODES: TaskReviewMode[] = [
    'none',
    'standard',
    'independent',
    'specialist-independent',
];

const SKILL_CATALOG_READ_SCOPES = new Set([
    'planning:read',
    'team:read',
    'tasks:read',
    'admin',
]);

const TEAM_ASSIGNMENT_READ_SCOPES = new Set([
    'planning:read',
    'admin',
]);

const isPendingExecutionSelection = (assignment: AgentTaskAssignment) => (
    assignment.purpose === 'execution'
    && assignment.state === 'queued'
    && (assignment.queue_class === 'rework' || assignment.queue_class === 'recovery')
    && assignment.routing_snapshot.schema_version === 'routing-lineage-snapshot-v1'
    && assignment.routing_snapshot.selection_pending === true
);

const assignmentLineageReviewFloor = (
    assignment: AgentTaskAssignment,
): TaskReviewMode => {
    const reviewFloor = assignment.routing_snapshot.review_floor;
    if (!reviewFloor || typeof reviewFloor !== 'object' || Array.isArray(reviewFloor)) {
        return 'none';
    }
    const reviewMode = reviewFloor.review_mode;
    return typeof reviewMode === 'string'
        && REVIEW_MODES.includes(reviewMode as TaskReviewMode)
        ? reviewMode as TaskReviewMode
        : 'none';
};

const lineageReviewFloor = (
    assignments: AgentTaskAssignment[],
): TaskReviewMode => assignments.reduce<TaskReviewMode>((currentFloor, assignment) => {
    const assignmentFloor = assignmentLineageReviewFloor(assignment);
    return reviewModeMeets(assignmentFloor, currentFloor)
        ? assignmentFloor
        : currentFloor;
}, 'none');

const assessmentToDraft = (assessment: TaskRoutingAssessment): AssessmentDraft => ({
    axes: { ...assessment.axes },
    requiredSkillLevels: Object.fromEntries(
        Object.entries(assessment.required_skill_levels).map(([key, level]) => [
            key,
            level as TaskSkillLevel,
        ]),
    ),
    minimumReasoningTier: assessment.required_model.minimum_reasoning_tier,
    minimumContextTier: assessment.required_model.minimum_context_tier,
    modalityTags: assessment.required_model.modality_tags.join(', '),
    toolTags: assessment.required_model.tool_tags.join(', '),
    dataPolicyTags: assessment.required_model.data_policy_tags.join(', '),
    reviewMode: assessment.review_mode,
    confidence: assessment.confidence,
    reasonCodes: assessment.reason_codes.filter(
        (code): code is AssessmentReasonCode => (
            ASSESSMENT_REASON_CODES.includes(code as AssessmentReasonCode)
        ),
    ),
    rationale: assessment.rationale,
});

const reviewTranslationKey = (mode: TaskReviewMode) => (
    mode === 'specialist-independent' ? 'specialistIndependent' : mode
);

export const TaskRoutingPanel = ({ task, onAssigned }: TaskRoutingPanelProps) => {
    const { t } = useTranslation();
    const { hasAgentKey } = useAgentAccess();
    const queryClient = useQueryClient();
    const toast = useToast();
    const [draft, setDraft] = useState<AssessmentDraft>(DEFAULT_DRAFT);
    const [hydratedAssessmentKey, setHydratedAssessmentKey] = useState('');
    const [skillToAdd, setSkillToAdd] = useState('');
    const [purpose, setPurpose] = useState<AgentAssignmentPurpose>('execution');
    const [reviewerProfileId, setReviewerProfileId] = useState('');
    const [selectedCandidate, setSelectedCandidate] = useState<AgentRoutingCandidate | null>(null);
    const [dispatchReason, setDispatchReason] = useState('');
    const [selectionConfirmed, setSelectionConfirmed] = useState(false);
    const [conflictMessage, setConflictMessage] = useState<string | null>(null);
    const [clock, setClock] = useState(Date.now());

    // feedback-policy: query loading,error,retry,empty
    const capabilitiesQuery = useQuery({
        queryKey: ['agent-capabilities'],
        queryFn: agentService.getCapabilities,
        enabled: hasAgentKey,
        retry: protectedQueryRetry,
    });
    const routingStatus = capabilitiesQuery.data?.model_aware_routing;
    const configuredRoutingMode = routingStatus?.configured_mode ?? 'off';
    const effectiveRoutingMode = routingStatus?.effective_mode ?? 'off';
    const featureAdvertised = (
        routingStatus?.feature_advertised === true
        && capabilitiesQuery.data?.features.includes(MODEL_AWARE_ROUTING_FEATURE) === true
    );
    const previewAllowed = featureAdvertised
        && (effectiveRoutingMode === 'shadow' || effectiveRoutingMode === 'enforced');
    const enforcedDispatchAllowed = featureAdvertised
        && effectiveRoutingMode === 'enforced';
    const routingBlockerCodes = Array.from(new Set([
        ...(routingStatus?.blocker_codes ?? []),
        ...(routingStatus?.topology_readiness.blocker_codes ?? []),
    ]));
    const scopes = capabilitiesQuery.data?.scopes ?? [];
    const canReadSkillCatalog = scopes.some(scope => SKILL_CATALOG_READ_SCOPES.has(scope));
    const canReadTeamAssignments = scopes.some(
        scope => TEAM_ASSIGNMENT_READ_SCOPES.has(scope),
    );
    const canAssess = scopes.includes('planning:write') || scopes.includes('admin');
    const canDispatch = scopes.includes('assignments:write') || scopes.includes('admin');
    const needsPendingAssignmentEvidence = task.status === 'active';
    const activeExecutionRecovery = needsPendingAssignmentEvidence
        && purpose === 'execution';

    // feedback-policy: query loading,error,retry,empty
    const assessmentQuery = useQuery({
        queryKey: ['routing-assessment', task.id, task.version],
        queryFn: () => agentService.getTaskRoutingAssessment(task.id),
        enabled: hasAgentKey && previewAllowed,
        retry: protectedQueryRetry,
    });

    // feedback-policy: query loading,error,retry,empty
    const skillCatalogQuery = useQuery({
        queryKey: ['agent-profile-skill-catalog'],
        queryFn: agentService.getProfileSkillCatalog,
        enabled: hasAgentKey && previewAllowed && canReadSkillCatalog,
        retry: protectedQueryRetry,
    });

    // feedback-policy: query loading,error,retry,empty
    const rosterQuery = useQuery({
        queryKey: ['agent-actor-roster', true],
        queryFn: () => agentService.getActorRoster(true),
        enabled: hasAgentKey && previewAllowed,
        retry: protectedQueryRetry,
        refetchInterval: 30_000,
    });

    // feedback-policy: query loading,error,retry,empty
    const pendingAssignmentsQuery = useQuery({
        queryKey: [
            'agent-assignments',
            capabilitiesQuery.data?.actor.id,
            task.id,
            task.version,
            'execution',
            'queued',
        ],
        queryFn: () => agentService.listAssignments({
            taskId: task.id,
            purpose: 'execution',
            state: 'queued',
            limit: 500,
        }),
        enabled: hasAgentKey
            && previewAllowed
            && needsPendingAssignmentEvidence
            && canReadTeamAssignments,
        retry: protectedQueryRetry,
        refetchInterval: 30_000,
    });

    const clearPreview = () => {
        previewMutation.reset();
        setSelectedCandidate(null);
        setSelectionConfirmed(false);
        setDispatchReason('');
    };

    const invalidateRoutingEvidence = () => {
        void queryClient.invalidateQueries({ queryKey: ['routing-assessment', task.id] });
        void queryClient.invalidateQueries({ queryKey: ['agent-actor-roster'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-model-bindings'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-assignments'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-pipeline'] });
    };

    const handleConflict = (error: unknown, fallback: string) => {
        const normalized = normalizeApiError(error, fallback);
        if (normalized.status === 409) {
            setConflictMessage(normalized.message);
            clearPreview();
            invalidateRoutingEvidence();
            return;
        }
        toast.error(normalized.message);
    };

    // feedback-policy: mutation pending,toast
    const assessmentMutation = useMutation({
        mutationFn: (command: TaskRoutingAssessmentCommand) => (
            agentService.createTaskRoutingAssessment(
                task.id,
                command,
                createAgentCommandMetadata(command.rationale),
            )
        ),
        onSuccess: receipt => {
            clearPreview();
            setConflictMessage(null);
            void queryClient.invalidateQueries({ queryKey: ['routing-assessment', task.id] });
            toast.success(t('taskRouting.assessmentSaved'));
            setHydratedAssessmentKey(`assessment:${receipt.assessment.id}`);
        },
        onError: error => handleConflict(error, t('taskRouting.assessmentSaveFailed')),
    });

    // feedback-policy: mutation pending,toast
    const previewMutation = useMutation({
        mutationFn: () => {
            const assessmentState = assessmentQuery.data;
            const assessment = assessmentState?.assessment;
            if (!assessmentState || !assessment) {
                throw new Error(t('taskRouting.staleAssessmentEvidence'));
            }
            const parsedReviewerId = Number(reviewerProfileId);
            return agentService.previewTaskRouting(task.id, {
                purpose,
                assessment_id: assessment.id,
                expected_task_version: assessmentState.current_task_version,
                reviewer_profile_id: purpose === 'verification' && parsedReviewerId > 0
                    ? parsedReviewerId
                    : null,
            });
        },
        onSuccess: () => {
            setSelectedCandidate(null);
            setSelectionConfirmed(false);
            setDispatchReason('');
            setConflictMessage(null);
            setClock(Date.now());
        },
        onError: error => handleConflict(error, t('taskRouting.previewFailed')),
    });

    // feedback-policy: mutation pending,toast
    const assignmentMutation = useMutation({
        mutationFn: (candidate: AgentRoutingCandidate) => {
            const preview = previewMutation.data;
            const assessment = assessmentQuery.data?.assessment;
            if (!preview || !assessment) throw new Error(t('taskRouting.previewStale'));
            const metadata = createAgentCommandMetadata(dispatchReason);
            if (task.status === 'active' && preview.purpose === 'execution') {
                const pendingSelections = (pendingAssignmentsQuery.data ?? [])
                    .filter(isPendingExecutionSelection);
                if (pendingSelections.length !== 1) {
                    throw new Error(t('taskRouting.recoveryAssignmentMismatch', {
                        count: pendingSelections.length,
                    }));
                }
                const pendingAssignment = pendingSelections[0];
                const pendingActor = rosterQuery.data?.find(
                    actor => actor.id === pendingAssignment.actor_id,
                );
                if (
                    !pendingActor
                    || pendingAssignment.task_version !== preview.current_task_version
                ) {
                    throw new Error(t('taskRouting.recoveryAssignmentStale'));
                }
                return agentService.updateAssignment(
                    pendingAssignment.id,
                    {
                        expected_queue_revision: pendingActor.queue_revision,
                        assessment_id: preview.assessment_id,
                        model_binding_id: candidate.model_binding_id,
                        model_binding_revision: candidate.model_binding_revision,
                        routing_preview_id: preview.preview_id,
                        routing_preview_digest: preview.preview_digest,
                        actor_id: candidate.actor_id,
                        reviewer_profile_id: preview.reviewer_profile_id,
                        reason: dispatchReason.trim(),
                    },
                    metadata,
                );
            }
            return agentService.createAssignment({
                task_id: task.id,
                actor_id: candidate.actor_id,
                expected_task_version: preview.current_task_version,
                purpose: preview.purpose,
                assessment_id: preview.assessment_id,
                model_binding_id: candidate.model_binding_id,
                model_binding_revision: candidate.model_binding_revision,
                routing_preview_id: preview.preview_id,
                routing_preview_digest: preview.preview_digest,
                team_member_id: candidate.capacity_owner_id,
                reviewer_profile_id: preview.reviewer_profile_id,
                queue_class: 'normal',
                reason: dispatchReason.trim(),
            }, metadata);
        },
        onSuccess: () => {
            toast.success(t(
                task.status === 'active'
                    ? 'taskRouting.recoveryDispatchSuccess'
                    : 'taskRouting.dispatchSuccess',
            ));
            clearPreview();
            invalidateRoutingEvidence();
            onAssigned?.();
        },
        onError: error => handleConflict(error, t('taskRouting.dispatchFailed')),
    });

    const assessmentState = assessmentQuery.data;
    const assessment = assessmentState?.assessment ?? null;
    const hydrationKey = assessment
        ? `${task.id}:${assessment.id}:${assessmentState?.current_task_version}`
        : `${task.id}:none:${assessmentState?.current_task_version ?? task.version}`;

    useEffect(() => {
        if (!assessmentState || hydratedAssessmentKey === hydrationKey) return;
        setDraft(assessment ? assessmentToDraft(assessment) : {
            ...DEFAULT_DRAFT,
            axes: { ...DEFAULT_DRAFT.axes },
            requiredSkillLevels: {},
            reasonCodes: [],
        });
        setHydratedAssessmentKey(hydrationKey);
        clearPreview();
        // clearPreview is intentionally excluded: hydration is keyed to server evidence.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [assessment, assessmentState, hydratedAssessmentKey, hydrationKey]);

    useEffect(() => {
        const preview = previewMutation.data;
        if (!preview) return undefined;
        setClock(Date.now());
        const intervalId = window.setInterval(() => setClock(Date.now()), 1_000);
        return () => window.clearInterval(intervalId);
    }, [previewMutation.data]);

    const derivedBand = deriveDifficultyBand(draft.axes, draft.reasonCodes);
    const policyReviewMode = minimumReviewMode(draft.axes, draft.reasonCodes);
    const taskEvidenceStale = Boolean(
        assessmentState && assessmentState.current_task_version !== task.version,
    );
    const assessmentCurrent = assessmentState?.state === 'current'
        && Boolean(assessment?.is_current)
        && assessment?.task_version === assessmentState.current_task_version;
    const preview = previewMutation.data;
    const previewExpired = Boolean(preview && Date.parse(preview.expires_at) <= clock);
    const roster = useMemo(() => rosterQuery.data ?? [], [rosterQuery.data]);
    const pendingSelectionAssignments = useMemo(
        () => (pendingAssignmentsQuery.data ?? []).filter(isPendingExecutionSelection),
        [pendingAssignmentsQuery.data],
    );
    const pendingSelectionAssignment = pendingSelectionAssignments.length === 1
        ? pendingSelectionAssignments[0]
        : null;
    const recoveryReviewFloor = lineageReviewFloor(pendingSelectionAssignments);
    const requiredReviewMode = reviewModeMeets(recoveryReviewFloor, policyReviewMode)
        ? recoveryReviewFloor
        : policyReviewMode;
    const reviewValid = reviewModeMeets(draft.reviewMode, requiredReviewMode);
    const pendingSelectionActor = pendingSelectionAssignment
        ? roster.find(actor => actor.id === pendingSelectionAssignment.actor_id)
        : null;
    const recoveryAssignmentReady = !activeExecutionRecovery || Boolean(
        canReadTeamAssignments
        && pendingSelectionAssignment
        && pendingSelectionActor
        && pendingSelectionAssignment.task_version === task.version,
    );
    const selectedRosterActor = selectedCandidate
        ? roster.find(actor => actor.id === selectedCandidate.actor_id)
        : null;
    const selectedRosterBinding = selectedRosterActor && selectedCandidate
        ? selectedRosterActor.eligible_model_bindings.find(
            binding => binding.id === selectedCandidate.model_binding_id,
        )
        : null;
    const rosterOrBindingStale = Boolean(selectedCandidate && (
        !selectedRosterActor
        || !selectedRosterActor.enabled
        || selectedRosterActor.actor_revision !== selectedCandidate.actor_revision
        || selectedRosterActor.queue_revision !== selectedCandidate.actor_queue_revision
        || selectedRosterActor.profile_revision !== selectedCandidate.profile_revision
        || !selectedRosterBinding
        || selectedRosterBinding.revision !== selectedCandidate.model_binding_revision
        || selectedRosterBinding.model_catalog_id !== selectedCandidate.model_catalog_id
        || selectedRosterBinding.model_catalog?.revision !== selectedCandidate.model_catalog_revision
        || !selectedRosterBinding.selectable
    ));
    const previewEvidenceStale = Boolean(preview && (
        previewExpired
        || taskEvidenceStale
        || !assessmentCurrent
        || preview.assessment_id !== assessment?.id
        || preview.current_task_version !== assessmentState?.current_task_version
        || rosterOrBindingStale
    ));

    const updateAxis = (axis: keyof TaskDifficultyAxes, score: TaskDifficultyScore) => {
        setDraft(current => ({
            ...current,
            axes: { ...current.axes, [axis]: score },
        }));
        clearPreview();
    };

    const toggleReasonCode = (reasonCode: AssessmentReasonCode, checked: boolean) => {
        setDraft(current => ({
            ...current,
            reasonCodes: checked
                ? [...current.reasonCodes, reasonCode].sort()
                : current.reasonCodes.filter(code => code !== reasonCode),
        }));
        clearPreview();
    };

    const addRequiredSkill = () => {
        if (!skillToAdd || draft.requiredSkillLevels[skillToAdd]) return;
        setDraft(current => ({
            ...current,
            requiredSkillLevels: {
                ...current.requiredSkillLevels,
                [skillToAdd]: 3,
            },
        }));
        setSkillToAdd('');
        clearPreview();
    };

    const submitAssessment = (event: FormEvent) => {
        event.preventDefault();
        if (!assessmentState || !reviewValid) return;
        assessmentMutation.mutate({
            expected_task_version: assessmentState.current_task_version,
            band: derivedBand,
            axes: draft.axes,
            required_skill_levels: draft.requiredSkillLevels,
            required_model: {
                minimum_reasoning_tier: draft.minimumReasoningTier,
                minimum_context_tier: draft.minimumContextTier,
                modality_tags: parseRoutingTags(draft.modalityTags),
                tool_tags: parseRoutingTags(draft.toolTags),
                data_policy_tags: parseRoutingTags(draft.dataPolicyTags),
            },
            review_mode: draft.reviewMode,
            confidence: draft.confidence,
            reason_codes: draft.reasonCodes,
            rationale: draft.rationale.trim(),
        });
    };

    if (!hasAgentKey) {
        return (
            <section className="card space-y-3" aria-labelledby={`task-routing-${task.id}`}>
                <h3 id={`task-routing-${task.id}`} className="flex items-center gap-2 font-semibold text-content-primary">
                    <Route aria-hidden="true" className="h-4 w-4 text-action" />
                    {t('taskRouting.title')}
                </h3>
                <QueryEmptyState
                    title={t('taskRouting.accessRequired')}
                    description={t('taskRouting.description')}
                />
                <Link className="btn secondary w-fit" to="/settings?tab=models_agents">
                    {t('taskRouting.configureAccess')}
                </Link>
            </section>
        );
    }

    if (capabilitiesQuery.isPending) {
        return <QueryLoadingState message={t('taskRouting.loading')} />;
    }

    if (capabilitiesQuery.isError) {
        return (
            <QueryErrorState
                error={capabilitiesQuery.error}
                fallback={t('taskRouting.loadFailed')}
                onRetry={() => { void capabilitiesQuery.refetch(); }}
            />
        );
    }

    if (!previewAllowed) {
        return (
            <section className="card space-y-3" aria-labelledby={`task-routing-${task.id}`}>
                <h3 id={`task-routing-${task.id}`} className="flex items-center gap-2 font-semibold text-content-primary">
                    <Route aria-hidden="true" className="h-4 w-4 text-action" />
                    {t('taskRouting.title')}
                </h3>
                <p className="text-sm text-content-secondary">{t('taskRouting.description')}</p>
                <dl className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                        <dt className="text-content-tertiary">{t('taskRouting.configuredMode')}</dt>
                        <dd className="text-content-primary">
                            {t(`taskRouting.rolloutModes.${configuredRoutingMode}`)}
                        </dd>
                    </div>
                    <div>
                        <dt className="text-content-tertiary">{t('taskRouting.effectiveMode')}</dt>
                        <dd className="text-feedback-danger-foreground">
                            {t(`taskRouting.rolloutModes.${effectiveRoutingMode}`)}
                        </dd>
                    </div>
                    <div>
                        <dt className="text-content-tertiary">{t('taskRouting.topologyReadiness')}</dt>
                        <dd className="text-content-primary">
                            {t(`taskRouting.topologyStatuses.${routingStatus?.topology_readiness.status ?? 'unavailable'}`)}
                        </dd>
                    </div>
                </dl>
                <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                    {t('taskRouting.featureUnavailable')}
                </div>
                {routingBlockerCodes.length > 0 && (
                    <div>
                        <p className="text-xs font-semibold uppercase tracking-wide text-content-secondary">
                            {t('taskRouting.rolloutBlockers')}
                        </p>
                        <ul className="mt-1 list-disc space-y-1 pl-5 text-xs text-content-secondary">
                            {routingBlockerCodes.map(code => (
                                <li key={code}>{formatRoutingCode(code)}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </section>
        );
    }

    if (
        assessmentQuery.isPending
        || rosterQuery.isPending
        || (
            needsPendingAssignmentEvidence
            && canReadTeamAssignments
            && pendingAssignmentsQuery.isPending
        )
    ) {
        return <QueryLoadingState message={t('taskRouting.loading')} />;
    }

    const queryError = assessmentQuery.error
        || rosterQuery.error
        || (
            needsPendingAssignmentEvidence
            && canReadTeamAssignments
            && pendingAssignmentsQuery.error
        );
    if (queryError) {
        return (
            <QueryErrorState
                error={queryError}
                fallback={t('taskRouting.loadFailed')}
                onRetry={() => {
                    void capabilitiesQuery.refetch();
                    void assessmentQuery.refetch();
                    void rosterQuery.refetch();
                    if (needsPendingAssignmentEvidence && canReadTeamAssignments) {
                        void pendingAssignmentsQuery.refetch();
                    }
                }}
            />
        );
    }

    const skillCatalog = skillCatalogQuery.data ?? [];
    const parsedReviewerProfileId = Number(reviewerProfileId);
    const reviewerIdValid = reviewerProfileId.trim().length === 0
        || (Number.isInteger(parsedReviewerProfileId) && parsedReviewerProfileId > 0);
    const canSaveAssessment = previewAllowed
        && canAssess
        && !assessmentCurrent
        && !taskEvidenceStale
        && (!needsPendingAssignmentEvidence || canReadTeamAssignments)
        && reviewValid
        && draft.confidence >= 0.6
        && draft.confidence <= 1
        && draft.rationale.trim().length > 0;
    const canGeneratePreview = previewAllowed
        && assessmentCurrent
        && !taskEvidenceStale
        && reviewValid
        && recoveryAssignmentReady
        && reviewerIdValid
        && !previewMutation.isPending;
    const canSubmitAssignment = enforcedDispatchAllowed
        && canDispatch
        && Boolean(selectedCandidate)
        && Boolean(preview)
        && !previewEvidenceStale
        && reviewValid
        && recoveryAssignmentReady
        && selectionConfirmed
        && dispatchReason.trim().length > 0
        && !assignmentMutation.isPending;

    return (
        <section className="card space-y-4" aria-labelledby={`task-routing-${task.id}`}>
            <div>
                <h3 id={`task-routing-${task.id}`} className="flex items-center gap-2 font-semibold text-content-primary">
                    <Route aria-hidden="true" className="h-4 w-4 text-action" />
                    {t('taskRouting.title')}
                </h3>
                <p className="mt-1 text-sm text-content-secondary">{t('taskRouting.description')}</p>
            </div>

            <dl className="grid grid-cols-2 gap-2 text-xs">
                <div>
                    <dt className="text-content-tertiary">{t('taskRouting.configuredMode')}</dt>
                    <dd className="text-content-primary">
                        {t(`taskRouting.rolloutModes.${configuredRoutingMode}`)}
                    </dd>
                </div>
                <div>
                    <dt className="text-content-tertiary">{t('taskRouting.effectiveMode')}</dt>
                    <dd className={
                        effectiveRoutingMode === 'enforced'
                            ? 'text-feedback-success-foreground'
                            : 'text-feedback-warning-foreground'
                    }>
                        {t(`taskRouting.rolloutModes.${effectiveRoutingMode}`)}
                    </dd>
                </div>
                <div>
                    <dt className="text-content-tertiary">{t('taskRouting.topologyReadiness')}</dt>
                    <dd className="text-content-primary">
                        {t(`taskRouting.topologyStatuses.${routingStatus?.topology_readiness.status ?? 'unavailable'}`)}
                    </dd>
                </div>
                <div>
                    <dt className="text-content-tertiary">{t('taskRouting.policyVersion')}</dt>
                    <dd className="text-content-primary">{MODEL_AWARE_ROUTING_FEATURE}</dd>
                </div>
                <div>
                    <dt className="text-content-tertiary">{t('taskRouting.taskVersion')}</dt>
                    <dd className="text-content-primary tnum">{task.version} / {assessmentState?.current_task_version}</dd>
                </div>
                <div>
                    <dt className="text-content-tertiary">{t('taskRouting.assessmentState')}</dt>
                    <dd className="text-content-primary">{t(`taskRouting.assessmentStates.${assessmentState?.state ?? 'none'}`)}</dd>
                </div>
            </dl>

            {effectiveRoutingMode === 'shadow' && (
                <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="status">
                    {t('taskRouting.shadowNotice')}
                </div>
            )}
            {taskEvidenceStale && (
                <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="alert">
                    {t('taskRouting.staleTaskEvidence')}
                </div>
            )}
            {conflictMessage && (
                <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="alert">
                    <p className="font-semibold">{t('taskRouting.conflictTitle')}</p>
                    <p>{conflictMessage}</p>
                    <p className="mt-1">{t('taskRouting.conflictDescription')}</p>
                </div>
            )}

            <form onSubmit={submitAssessment} className="space-y-4">
                <fieldset
                    disabled={!canAssess || assessmentMutation.isPending || assessmentCurrent}
                    className="space-y-4"
                >
                    <legend className="text-sm font-semibold text-content-primary">{t('taskRouting.assessmentHeading')}</legend>
                    {assessmentCurrent && (
                        <div className="rounded-md border border-feedback-info-border bg-feedback-info-muted p-3 text-sm text-feedback-info-foreground" role="status">
                            {t('taskRouting.currentAssessmentImmutable')}
                        </div>
                    )}

                    <div>
                        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskRouting.difficultyAxes')}</p>
                        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                            {AXIS_KEYS.map(axis => (
                                <label key={axis} className="field">
                                    <span className="field-lbl">{t(`taskRouting.axes.${axis}`)}</span>
                                    <select
                                        className="input"
                                        value={draft.axes[axis]}
                                        onChange={event => updateAxis(axis, Number(event.target.value) as TaskDifficultyScore)}
                                    >
                                        {[1, 2, 3].map(score => (
                                            <option key={score} value={score}>{t('taskRouting.axisScore', { score })}</option>
                                        ))}
                                    </select>
                                </label>
                            ))}
                        </div>
                        <div className="mt-2 flex flex-wrap items-center gap-2">
                            <span className="text-sm text-content-secondary">{t('taskRouting.derivedBand')}:</span>
                            <span className="rounded-full border border-border bg-surface-muted px-2 py-0.5 text-xs font-semibold text-content-primary">
                                {t(`taskRouting.bands.${derivedBand}`)}
                            </span>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <p className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskRouting.requiredSkills')}</p>
                        {!canReadSkillCatalog && (
                            <div className="rounded-md border border-feedback-info-border bg-feedback-info-muted p-3 text-sm text-feedback-info-foreground" role="status">
                                {t('taskRouting.skillCatalogScopeUnavailable')}
                            </div>
                        )}
                        {canReadSkillCatalog && skillCatalogQuery.isPending && (
                            <p className="text-xs text-content-secondary" role="status">
                                {t('taskRouting.skillCatalogLoading')}
                            </p>
                        )}
                        {canReadSkillCatalog && skillCatalogQuery.isError && (
                            <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="alert">
                                <p>{t('taskRouting.skillCatalogLoadFailed')}</p>
                                <Button
                                    type="button"
                                    size="sm"
                                    variant="secondary"
                                    className="mt-2"
                                    onClick={() => { void skillCatalogQuery.refetch(); }}
                                >
                                    {t('taskRouting.retrySkillCatalog')}
                                </Button>
                            </div>
                        )}
                        {canReadSkillCatalog
                            && !skillCatalogQuery.isPending
                            && !skillCatalogQuery.isError && (
                            <div className="flex flex-col gap-2 sm:flex-row">
                                <select className="input" aria-label={t('taskRouting.selectSkill')} value={skillToAdd} onChange={event => setSkillToAdd(event.target.value)}>
                                    <option value="">{t('taskRouting.selectSkill')}</option>
                                    {skillCatalog
                                        .filter(skill => !draft.requiredSkillLevels[skill.skill_key])
                                        .map(skill => <option key={skill.skill_key} value={skill.skill_key}>{skill.skill_name}</option>)}
                                </select>
                                <Button type="button" size="sm" variant="secondary" onClick={addRequiredSkill} disabled={!skillToAdd}>
                                    <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                    {t('taskRouting.addSkill')}
                                </Button>
                            </div>
                        )}
                        {Object.keys(draft.requiredSkillLevels).length === 0 ? (
                            <p className="text-xs text-content-tertiary">{t('taskRouting.noRequiredSkills')}</p>
                        ) : (
                            <div className="space-y-2">
                                {Object.entries(draft.requiredSkillLevels).map(([skillKey, level]) => (
                                    <div key={skillKey} className="flex items-center gap-2 rounded-md border border-border bg-surface-muted p-2">
                                        <span className="min-w-0 flex-1 truncate text-sm text-content-primary">
                                            {skillCatalog.find(skill => skill.skill_key === skillKey)?.skill_name ?? formatRoutingCode(skillKey)}
                                        </span>
                                        <label className="flex items-center gap-1 text-xs text-content-secondary">
                                            {t('taskRouting.skillLevel')}
                                            <select
                                                className="input w-16"
                                                value={level}
                                                onChange={event => {
                                                    setDraft(current => ({
                                                        ...current,
                                                        requiredSkillLevels: {
                                                            ...current.requiredSkillLevels,
                                                            [skillKey]: Number(event.target.value) as TaskSkillLevel,
                                                        },
                                                    }));
                                                    clearPreview();
                                                }}
                                            >
                                                {[1, 2, 3, 4, 5].map(value => <option key={value} value={value}>{value}</option>)}
                                            </select>
                                        </label>
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant="ghost"
                                            aria-label={t('taskRouting.removeSkill', { skill: skillKey })}
                                            onClick={() => {
                                                setDraft(current => ({
                                                    ...current,
                                                    requiredSkillLevels: Object.fromEntries(
                                                        Object.entries(current.requiredSkillLevels).filter(([key]) => key !== skillKey),
                                                    ),
                                                }));
                                                clearPreview();
                                            }}
                                        >
                                            <Trash2 aria-hidden="true" className="h-4 w-4" />
                                        </Button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div className="space-y-2">
                        <p className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskRouting.modelEnvelope')}</p>
                        <div className="grid grid-cols-2 gap-2">
                            <label className="field">
                                <span className="field-lbl">{t('taskRouting.minimumReasoningTier')}</span>
                                <select className="input" value={draft.minimumReasoningTier} onChange={event => { setDraft({ ...draft, minimumReasoningTier: Number(event.target.value) as ModelReasoningTier }); clearPreview(); }}>
                                    <option value={1}>1</option><option value={2}>2</option><option value={3}>3</option>
                                </select>
                            </label>
                            <label className="field">
                                <span className="field-lbl">{t('taskRouting.minimumContextTier')}</span>
                                <select className="input" value={draft.minimumContextTier} onChange={event => { setDraft({ ...draft, minimumContextTier: event.target.value as ModelContextTier }); clearPreview(); }}>
                                    <option value="small">small</option><option value="medium">medium</option><option value="large">large</option>
                                </select>
                            </label>
                        </div>
                        <Input label={t('taskRouting.modalities')} value={draft.modalityTags} onChange={event => { setDraft({ ...draft, modalityTags: event.target.value }); clearPreview(); }} required />
                        <Input label={t('taskRouting.tools')} value={draft.toolTags} onChange={event => { setDraft({ ...draft, toolTags: event.target.value }); clearPreview(); }} />
                        <Input label={t('taskRouting.dataPolicy')} value={draft.dataPolicyTags} onChange={event => { setDraft({ ...draft, dataPolicyTags: event.target.value }); clearPreview(); }} />
                    </div>

                    <div className="space-y-2">
                        <label className="field">
                            <span className="field-lbl">{t('taskRouting.reviewMode')}</span>
                            <select className="input" value={draft.reviewMode} onChange={event => { setDraft({ ...draft, reviewMode: event.target.value as TaskReviewMode }); clearPreview(); }}>
                                {REVIEW_MODES.map(mode => (
                                    <option key={mode} value={mode}>{t(`taskRouting.reviewModes.${reviewTranslationKey(mode)}`)}</option>
                                ))}
                            </select>
                        </label>
                        <p className="text-xs text-content-secondary">
                            {t('taskRouting.minimumReview', {
                                mode: t(`taskRouting.reviewModes.${reviewTranslationKey(requiredReviewMode)}`),
                            })}
                        </p>
                        {(draft.axes.risk === 3 || requiredReviewMode === 'specialist-independent') && (
                            <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="status">
                                {t('taskRouting.highRiskReviewRequired')}
                            </div>
                        )}
                        {!reviewValid && (
                            <p className="text-sm text-feedback-danger-foreground" role="alert">{t('taskRouting.reviewBelowMinimum')}</p>
                        )}
                    </div>

                    <Input
                        label={t('taskRouting.confidence')}
                        type="number"
                        min="0.6"
                        max="1"
                        step="0.05"
                        value={draft.confidence}
                        onChange={event => { setDraft({ ...draft, confidence: Number(event.target.value) }); clearPreview(); }}
                    />

                    <fieldset className="space-y-2">
                        <legend className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskRouting.reasonCodes')}</legend>
                        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                            {ASSESSMENT_REASON_CODES.map(reasonCode => (
                                <Checkbox
                                    key={reasonCode}
                                    checked={draft.reasonCodes.includes(reasonCode)}
                                    onChange={checked => toggleReasonCode(reasonCode, checked)}
                                    label={formatRoutingCode(reasonCode)}
                                />
                            ))}
                        </div>
                    </fieldset>

                    <label className="field">
                        <span className="field-lbl">
                            {t('taskRouting.rationale')}
                            <RequiredIndicator />
                        </span>
                        <textarea
                            className="input min-h-24"
                            value={draft.rationale}
                            onChange={event => { setDraft({ ...draft, rationale: event.target.value }); clearPreview(); }}
                            placeholder={t('taskRouting.rationalePlaceholder')}
                            required
                        />
                    </label>

                    <Button type="submit" isLoading={assessmentMutation.isPending} disabled={!canSaveAssessment}>
                        {t('taskRouting.saveAssessment')}
                    </Button>
                </fieldset>
            </form>

            {!assessmentCurrent && (
                <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="status">
                    {t('taskRouting.staleAssessmentEvidence')}
                </div>
            )}

            <section className="space-y-3" aria-labelledby={`routing-preview-${task.id}`}>
                <h4 id={`routing-preview-${task.id}`} className="text-sm font-semibold text-content-primary">{t('taskRouting.previewHeading')}</h4>
                <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                    <label className="field">
                        <span className="field-lbl">{t('taskRouting.purpose')}</span>
                        <select className="input" value={purpose} onChange={event => { setPurpose(event.target.value as AgentAssignmentPurpose); clearPreview(); }}>
                            <option value="execution">{t('taskRouting.purposes.execution')}</option>
                            <option value="verification">{t('taskRouting.purposes.verification')}</option>
                        </select>
                    </label>
                    {purpose === 'verification' && (
                        <div>
                            <Input label={t('taskRouting.reviewerProfileId')} type="number" min="1" value={reviewerProfileId} onChange={event => { setReviewerProfileId(event.target.value); clearPreview(); }} />
                            <p className="mt-1 text-xs text-content-tertiary">{t('taskRouting.reviewerProfileHelp')}</p>
                        </div>
                    )}
                </div>
                {needsPendingAssignmentEvidence && !canReadTeamAssignments && (
                    <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                        {t('taskRouting.recoveryAssignmentReadRequired')}
                    </div>
                )}
                {activeExecutionRecovery
                    && canReadTeamAssignments
                    && pendingSelectionAssignments.length !== 1 && (
                    <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                        {t('taskRouting.recoveryAssignmentMismatch', {
                            count: pendingSelectionAssignments.length,
                        })}
                    </div>
                )}
                {activeExecutionRecovery
                    && canReadTeamAssignments
                    && pendingSelectionAssignment
                    && (
                        !pendingSelectionActor
                        || pendingSelectionAssignment.task_version !== task.version
                    ) && (
                    <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                        {t('taskRouting.recoveryAssignmentStale')}
                    </div>
                )}
                {activeExecutionRecovery && recoveryAssignmentReady && pendingSelectionAssignment && (
                    <div className="rounded-md border border-feedback-info-border bg-feedback-info-muted p-3 text-sm text-feedback-info-foreground" role="status">
                        {t('taskRouting.recoveryAssignmentReady', {
                            id: pendingSelectionAssignment.id,
                            queueClass: pendingSelectionAssignment.queue_class,
                        })}
                    </div>
                )}
                <Button type="button" variant="secondary" onClick={() => previewMutation.mutate()} isLoading={previewMutation.isPending} disabled={!canGeneratePreview}>
                    <RefreshCw aria-hidden="true" className="mr-2 h-4 w-4" />
                    {t('taskRouting.generatePreview')}
                </Button>

                {preview && (
                    <>
                        <dl className="grid grid-cols-2 gap-2 rounded-md border border-border bg-surface-muted p-3 text-xs">
                            <div><dt className="text-content-tertiary">{t('taskRouting.generatedAt')}</dt><dd className="text-content-primary">{formatDateTime(preview.generated_at)}</dd></div>
                            <div><dt className="text-content-tertiary">{t('taskRouting.expiresAt')}</dt><dd className="text-content-primary">{formatDateTime(preview.expires_at)}</dd></div>
                        </dl>
                        <p className="text-sm text-content-secondary" role="status" aria-live="polite">
                            {t('taskRouting.previewSummary', {
                                eligible: preview.eligible_candidates.length,
                                excluded: preview.exclusions.length,
                            })}
                        </p>
                        {preview.hard_blocker_codes.length > 0 && (
                            <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                                <p className="font-semibold">{t('taskRouting.previewHardBlockers')}</p>
                                <div className="mt-2 flex flex-wrap gap-1">
                                    {preview.hard_blocker_codes.map(blocker => (
                                        <span key={blocker} className="rounded-full border border-feedback-danger-border bg-surface-card px-2 py-0.5 text-xs">
                                            {formatRoutingCode(blocker)}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        )}
                        {previewEvidenceStale && (
                            <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground" role="alert">
                                {previewExpired ? t('taskRouting.previewExpired') : t('taskRouting.previewStale')}
                            </div>
                        )}
                        <RoutingCandidateComparison
                            preview={preview}
                            roster={roster}
                            selectedCandidateKey={selectedCandidate
                                ? `${selectedCandidate.actor_id}:${selectedCandidate.model_binding_id}`
                                : null}
                            onSelectCandidate={candidate => {
                                setSelectedCandidate(candidate);
                                setSelectionConfirmed(false);
                                setDispatchReason('');
                            }}
                            selectionDisabled={previewEvidenceStale}
                        />
                        {preview.eligible_candidates.length === 0 && (
                            <div className="rounded-md border border-feedback-warning-border bg-surface-muted p-4">
                                <h5 className="font-semibold text-content-primary">{t('taskRouting.recoveryHeading')}</h5>
                                <p className="mt-1 text-sm text-content-secondary">{t('taskRouting.recoveryDescription')}</p>
                                <div className="mt-3 flex flex-wrap gap-2">
                                    <Button type="button" size="sm" variant="secondary" onClick={() => clearPreview()}>{t('taskRouting.editAssessment')}</Button>
                                    <Button
                                        type="button"
                                        size="sm"
                                        variant="secondary"
                                        onClick={() => {
                                            clearPreview();
                                            void rosterQuery.refetch();
                                        }}
                                    >
                                        {t('taskRouting.refreshEvidence')}
                                    </Button>
                                    <Link className="btn secondary" to="/team">{t('taskRouting.openProfiles')}</Link>
                                    <Link className="btn secondary" to="/settings?tab=models_agents">{t('taskRouting.openModelAdministration')}</Link>
                                </div>
                            </div>
                        )}
                    </>
                )}
            </section>

            {preview && preview.eligible_candidates.length > 0 && (
                <section className="space-y-3 border-t border-border pt-4" aria-labelledby={`routing-dispatch-${task.id}`}>
                    <h4 id={`routing-dispatch-${task.id}`} className="text-sm font-semibold text-content-primary">{t('taskRouting.selectionHeading')}</h4>
                    {!selectedCandidate && <p className="text-sm text-content-secondary">{t('taskRouting.noDefaultSelection')}</p>}
                    <label className="field">
                        <span className="field-lbl">
                            {t('taskRouting.dispatchReason')}
                            <RequiredIndicator />
                        </span>
                        <textarea
                            className="input min-h-20"
                            value={dispatchReason}
                            onChange={event => setDispatchReason(event.target.value)}
                            placeholder={t('taskRouting.dispatchReasonPlaceholder')}
                            disabled={!selectedCandidate || previewEvidenceStale}
                            required
                        />
                    </label>
                    <Checkbox
                        checked={selectionConfirmed}
                        onChange={setSelectionConfirmed}
                        disabled={!selectedCandidate || previewEvidenceStale}
                        label={t('taskRouting.confirmSelection')}
                    />
                    <Button
                        type="button"
                        onClick={() => {
                            if (selectedCandidate) assignmentMutation.mutate(selectedCandidate);
                        }}
                        isLoading={assignmentMutation.isPending}
                        disabled={!canSubmitAssignment}
                    >
                        <CheckCircle2 aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('taskRouting.dispatch')}
                    </Button>
                    <p className="text-xs text-content-tertiary">{t('taskRouting.reportedTrustNote')}</p>
                </section>
            )}
        </section>
    );
};
