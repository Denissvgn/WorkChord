import { screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import type {
    AgentActorRosterItem,
    AgentCapabilities,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRoutingPreviewResponse,
    AgentTaskAssignment,
    TaskRoutingAssessment,
    TaskRoutingAssessmentState,
} from '../../types/agent';
import type { Task } from '../../types/task';
import {
    modelAwareRoutingPreview,
    modelAwareRoutingRoster,
} from '../../test/fixtures/modelAwareRouting';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskRoutingPanel } from './TaskRoutingPanel';

const agentServiceMock = vi.hoisted(() => ({
    getCapabilities: vi.fn(),
    getTaskRoutingAssessment: vi.fn(),
    getProfileSkillCatalog: vi.fn(),
    getActorRoster: vi.fn(),
    createTaskRoutingAssessment: vi.fn(),
    previewTaskRouting: vi.fn(),
    createAssignment: vi.fn(),
    updateAssignment: vi.fn(),
    listAssignments: vi.fn(),
}));

const useAgentAccessMock = vi.hoisted(() => vi.fn());

vi.mock('../../services/agentService', () => ({
    agentService: agentServiceMock,
}));

vi.mock('../../hooks/useAgentAccess', () => ({
    useAgentAccess: useAgentAccessMock,
}));

const taskFixture: Task = {
    id: 42,
    iteration_id: 9,
    project_id: 3,
    title: 'Route model-aware work',
    description: 'Exercise governed routing.',
    priority: 2,
    effort_days: 2,
    effort_hours: 16,
    status: 'planned',
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: 1,
    external_links: [],
    request_count: 0,
    agent_readiness: {
        is_ready: true,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 7,
    children: [],
    dependencies: [],
};

const currentAssessment: TaskRoutingAssessment = {
    id: 91,
    task_id: taskFixture.id,
    task_version: taskFixture.version,
    policy_version: 'model-aware-routing-v1',
    band: 'standard',
    axes: {
        reasoning: 2,
        ambiguity: 2,
        context_breadth: 2,
        risk: 2,
        verification_burden: 2,
    },
    required_skill_levels: {
        'frontend-react': 4,
    },
    required_model: {
        minimum_reasoning_tier: 2,
        minimum_context_tier: 'medium',
        modality_tags: ['text'],
        tool_tags: ['repository'],
        data_policy_tags: ['private-source'],
    },
    review_mode: 'standard',
    confidence: 0.85,
    reason_codes: [],
    rationale: 'The current assessment is ready for candidate preview.',
    assessor: 'planner',
    assessor_actor_id: 1,
    created_at: '2026-07-28T00:00:00Z',
    policy_conformant: true,
    is_current: true,
};

const currentAssessmentState: TaskRoutingAssessmentState = {
    task_id: taskFixture.id,
    current_task_version: taskFixture.version,
    state: 'current',
    assessment: currentAssessment,
};

const modelCatalog: AgentModelCatalogEntry = {
    id: 21,
    key: 'provider-reasoner',
    provider: 'configured-provider',
    configured_model_alias: 'reasoner',
    reasoning_tier: 3,
    context_tier: 'large',
    modality_tags: ['text'],
    cost_tier: 'medium',
    latency_tier: 'balanced',
    enabled: true,
    revision: 5,
    last_verified_at: '2026-07-28T00:00:00Z',
    created_at: '2026-07-01T00:00:00Z',
    updated_at: '2026-07-28T00:00:00Z',
};

const modelBinding: AgentModelBinding = {
    id: 31,
    actor_id: 11,
    model_catalog_id: modelCatalog.id,
    is_default: true,
    enabled: true,
    tool_tags: ['repository'],
    data_policy_tags: ['private-source'],
    revision: 4,
    model_catalog_key: modelCatalog.key,
    selectable: true,
    model_catalog: modelCatalog,
    live_assignment_count: 0,
    historical_assignment_count: 0,
    run_reference_count: 0,
    created_at: '2026-07-01T00:00:00Z',
    updated_at: '2026-07-28T00:00:00Z',
};

const dispatchableRoster: AgentActorRosterItem[] = modelAwareRoutingRoster.map(actor => ({
    ...actor,
    eligible_model_bindings: [modelBinding],
}));

const pendingRecoveryAssignment: AgentTaskAssignment = {
    id: 71,
    task_id: taskFixture.id,
    actor_id: 11,
    team_member_id: null,
    purpose: 'execution',
    queue_class: 'rework',
    state: 'queued',
    queue_rank: 1000,
    not_before: null,
    assigned_by_actor_id: 1,
    reviewer_profile_id: null,
    task_version: taskFixture.version,
    model_binding_id: null,
    model_binding_revision: null,
    model_binding_status: 'not_selected',
    model_binding_stale_reasons: [],
    routing_snapshot: {
        schema_version: 'routing-lineage-snapshot-v1',
        selection_pending: true,
    },
    reason: 'Select a governed rework candidate.',
    created_at: '2026-07-28T00:00:00Z',
    updated_at: '2026-07-28T00:00:00Z',
};

const capabilities: AgentCapabilities = {
    server_version: '1.6.2',
    api_contract: 'workchord-agent/v1',
    actor: {
        id: 1,
        name: 'routing-planner',
        display_name: 'Routing Planner',
        scopes: ['planning:write', 'assignments:write'],
        enabled: true,
        role: 'pm',
        profile_id: null,
        work_policy: 'assigned_only',
        max_parallel_work: 1,
        queue_revision: 1,
        created_at: '2026-07-01T00:00:00Z',
        last_seen_at: null,
    },
    scopes: ['planning:write', 'assignments:write'],
    lease_limits: {},
    features: ['model-aware-routing-v1'],
    recommended_skills: {},
    lifecycle_actions: [],
    skill_catalog_version: null,
    skill_catalog_url: null,
    skill_discovery_url: null,
};

const previewFixture = (
    overrides: Partial<AgentRoutingPreviewResponse> = {},
): AgentRoutingPreviewResponse => {
    const expiresAt = overrides.expires_at
        ?? new Date(Date.now() + 60_000).toISOString();
    const generatedAt = overrides.generated_at
        ?? new Date(Date.parse(expiresAt) - 300_000).toISOString();
    return {
        ...modelAwareRoutingPreview,
        generated_at: generatedAt,
        expires_at: expiresAt,
        ...overrides,
    };
};

const renderPanel = () => renderWithProviders(
    <TaskRoutingPanel task={taskFixture} />,
);

const generatePreview = async (
    user: ReturnType<typeof renderPanel>['user'],
    expectedCallCount = 1,
) => {
    const button = await screen.findByRole('button', {
        name: i18n.t('taskRouting.generatePreview'),
    });
    expect(button).toBeEnabled();
    await user.click(button);
    await waitFor(() => {
        expect(agentServiceMock.previewTaskRouting).toHaveBeenCalledTimes(expectedCallCount);
    });
};

describe('TaskRoutingPanel routing gates', () => {
    beforeEach(() => {
        useAgentAccessMock.mockReset();
        useAgentAccessMock.mockReturnValue({ hasAgentKey: true });

        agentServiceMock.getCapabilities.mockReset();
        agentServiceMock.getTaskRoutingAssessment.mockReset();
        agentServiceMock.getProfileSkillCatalog.mockReset();
        agentServiceMock.getActorRoster.mockReset();
        agentServiceMock.createTaskRoutingAssessment.mockReset();
        agentServiceMock.previewTaskRouting.mockReset();
        agentServiceMock.createAssignment.mockReset();
        agentServiceMock.updateAssignment.mockReset();
        agentServiceMock.listAssignments.mockReset();

        agentServiceMock.getCapabilities.mockResolvedValue(capabilities);
        agentServiceMock.getTaskRoutingAssessment.mockResolvedValue(currentAssessmentState);
        agentServiceMock.getProfileSkillCatalog.mockResolvedValue([]);
        agentServiceMock.getActorRoster.mockResolvedValue(dispatchableRoster);
        agentServiceMock.createAssignment.mockResolvedValue({});
        agentServiceMock.updateAssignment.mockResolvedValue({});
        agentServiceMock.listAssignments.mockResolvedValue([]);
    });

    it('keeps a recommended candidate unselected until reason and confirmation are explicit', async () => {
        const onAssigned = vi.fn();
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture());
        const { user } = renderWithProviders(
            <TaskRoutingPanel task={taskFixture} onAssigned={onAssigned} />,
        );

        await generatePreview(user);
        expect(await screen.findByText(i18n.t('taskRouting.noDefaultSelection'))).toBeVisible();

        const radio = screen.getByRole('radio');
        const reason = screen.getByRole('textbox', {
            name: i18n.t('taskRouting.dispatchReason'),
        });
        const confirmation = screen.getByRole('checkbox', {
            name: i18n.t('taskRouting.confirmSelection'),
        });
        const dispatch = screen.getByRole('button', {
            name: i18n.t('taskRouting.dispatch'),
        });

        expect(radio).not.toBeChecked();
        expect(reason).toBeDisabled();
        expect(confirmation).toBeDisabled();
        expect(dispatch).toBeDisabled();
        expect(agentServiceMock.createAssignment).not.toHaveBeenCalled();

        await user.click(radio);
        expect(reason).toBeEnabled();
        expect(confirmation).toBeEnabled();
        expect(dispatch).toBeDisabled();

        await user.type(
            reason,
            'Current skills,{Enter}capacity, and binding are appropriate.',
        );
        expect(reason).toHaveValue(
            'Current skills,\ncapacity, and binding are appropriate.',
        );
        expect(dispatch).toBeDisabled();

        await user.click(confirmation);
        expect(dispatch).toBeEnabled();
        await user.click(dispatch);

        await waitFor(() => {
            expect(agentServiceMock.createAssignment).toHaveBeenCalledOnce();
        });
        expect(agentServiceMock.createAssignment).toHaveBeenCalledWith(
            expect.objectContaining({
                task_id: taskFixture.id,
                actor_id: 11,
                routing_preview_id: 'preview-42',
                reason: 'Current skills,\ncapacity, and binding are appropriate.',
            }),
            expect.objectContaining({
                rationale: 'Current skills, capacity, and binding are appropriate.',
            }),
        );
        expect(onAssigned).toHaveBeenCalledOnce();
    });

    it('accepts only a positive integer reviewer profile filter', async () => {
        const { user } = renderPanel();

        await user.selectOptions(
            await screen.findByRole('combobox', {
                name: i18n.t('taskRouting.purpose'),
            }),
            'verification',
        );
        const reviewerFilter = screen.getByRole('spinbutton', {
            name: i18n.t('taskRouting.reviewerProfileId'),
        });
        const previewButton = screen.getByRole('button', {
            name: i18n.t('taskRouting.generatePreview'),
        });

        await user.type(reviewerFilter, '1.5');
        expect(previewButton).toBeDisabled();

        await user.clear(reviewerFilter);
        await user.type(reviewerFilter, '23');
        expect(previewButton).toBeEnabled();
    });

    it('creates a normal verification assignment for resolved work', async () => {
        const resolvedTask: Task = {
            ...taskFixture,
            status: 'resolved',
        };
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture({
            purpose: 'verification',
        }));
        const { user } = renderWithProviders(
            <TaskRoutingPanel task={resolvedTask} />,
        );

        await user.selectOptions(
            await screen.findByRole('combobox', {
                name: i18n.t('taskRouting.purpose'),
            }),
            'verification',
        );
        await generatePreview(user);
        await user.click(screen.getByRole('radio'));
        await user.type(
            screen.getByRole('textbox', {
                name: i18n.t('taskRouting.dispatchReason'),
            }),
            'Use an independent verifier for the resolved task.',
        );
        await user.click(screen.getByRole('checkbox', {
            name: i18n.t('taskRouting.confirmSelection'),
        }));
        await user.click(screen.getByRole('button', {
            name: i18n.t('taskRouting.dispatch'),
        }));

        await waitFor(() => {
            expect(agentServiceMock.createAssignment).toHaveBeenCalledOnce();
        });
        expect(agentServiceMock.createAssignment).toHaveBeenCalledWith(
            expect.objectContaining({
                task_id: resolvedTask.id,
                purpose: 'verification',
                queue_class: 'normal',
            }),
            expect.objectContaining({
                rationale: 'Use an independent verifier for the resolved task.',
            }),
        );
        expect(agentServiceMock.updateAssignment).not.toHaveBeenCalled();
        expect(agentServiceMock.listAssignments).not.toHaveBeenCalled();
    });

    it('offers explicit recovery actions when no candidate is eligible', async () => {
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture({
            recommended_candidate: null,
            eligible_candidates: [],
            hard_blocker_codes: [
                'task_status_incompatible',
                'no_eligible_candidate',
            ],
        }));
        const { user } = renderPanel();

        await generatePreview(user);
        expect(screen.getByText(i18n.t('taskRouting.previewHardBlockers'))).toBeVisible();
        expect(screen.getByText('Task Status Incompatible')).toBeVisible();
        expect(await screen.findByText(i18n.t('taskRouting.recoveryHeading'))).toBeVisible();
        expect(screen.getByText(i18n.t('taskRouting.recoveryDescription'))).toBeVisible();
        expect(screen.getByRole('link', {
            name: i18n.t('taskRouting.openProfiles'),
        })).toHaveAttribute('href', '/team');

        await user.click(screen.getByRole('button', {
            name: i18n.t('taskRouting.editAssessment'),
        }));
        await waitFor(() => {
            expect(screen.queryByText(i18n.t('taskRouting.recoveryHeading'))).not.toBeInTheDocument();
        });

        await generatePreview(user, 2);
        await user.click(screen.getByRole('button', {
            name: i18n.t('taskRouting.refreshEvidence'),
        }));
        await waitFor(() => {
            expect(agentServiceMock.getActorRoster).toHaveBeenCalledTimes(2);
            expect(screen.queryByText(i18n.t('taskRouting.recoveryHeading'))).not.toBeInTheDocument();
        });
    });

    it('degrades only the skill picker when the actor lacks catalog read scope', async () => {
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture());
        const { user } = renderPanel();

        expect(await screen.findByText(
            i18n.t('taskRouting.skillCatalogScopeUnavailable'),
        )).toBeVisible();
        expect(agentServiceMock.getProfileSkillCatalog).not.toHaveBeenCalled();

        await generatePreview(user);
        expect(agentServiceMock.previewTaskRouting).toHaveBeenCalledOnce();
    });

    it('keeps routing available when the optional skill catalog request fails', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [...capabilities.actor.scopes, 'planning:read'],
            },
            scopes: [...capabilities.scopes, 'planning:read'],
        });
        agentServiceMock.getProfileSkillCatalog.mockRejectedValue({
            response: { status: 403 },
        });
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture());
        const { user } = renderPanel();

        expect(await screen.findByText(
            i18n.t('taskRouting.skillCatalogLoadFailed'),
        )).toBeVisible();
        await generatePreview(user);
        expect(agentServiceMock.previewTaskRouting).toHaveBeenCalledOnce();
    });

    it('updates the single queued selection-pending recovery assignment', async () => {
        const activeTask: Task = {
            ...taskFixture,
            status: 'active',
        };
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [...capabilities.actor.scopes, 'planning:read'],
            },
            scopes: [...capabilities.scopes, 'planning:read'],
        });
        agentServiceMock.listAssignments.mockResolvedValue([
            pendingRecoveryAssignment,
        ]);
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture());
        const { user } = renderWithProviders(
            <TaskRoutingPanel task={activeTask} />,
        );

        expect(await screen.findByText(i18n.t(
            'taskRouting.recoveryAssignmentReady',
            {
                id: pendingRecoveryAssignment.id,
                queueClass: pendingRecoveryAssignment.queue_class,
            },
        ))).toBeVisible();
        await generatePreview(user);
        await user.click(screen.getByRole('radio'));
        await user.type(
            screen.getByRole('textbox', {
                name: i18n.t('taskRouting.dispatchReason'),
            }),
            'Use the current governed rework candidate.',
        );
        await user.click(screen.getByRole('checkbox', {
            name: i18n.t('taskRouting.confirmSelection'),
        }));
        await user.click(screen.getByRole('button', {
            name: i18n.t('taskRouting.dispatch'),
        }));

        await waitFor(() => {
            expect(agentServiceMock.updateAssignment).toHaveBeenCalledOnce();
        });
        expect(agentServiceMock.updateAssignment).toHaveBeenCalledWith(
            pendingRecoveryAssignment.id,
            expect.objectContaining({
                expected_queue_revision: 7,
                assessment_id: currentAssessment.id,
                actor_id: 11,
                model_binding_id: modelBinding.id,
                model_binding_revision: modelBinding.revision,
                routing_preview_id: 'preview-42',
                reviewer_profile_id: null,
                reason: 'Use the current governed rework candidate.',
            }),
            expect.objectContaining({
                rationale: 'Use the current governed rework candidate.',
            }),
        );
        expect(agentServiceMock.createAssignment).not.toHaveBeenCalled();
    });

    it('requires planning read authority to discover team recovery assignments', async () => {
        const activeTask: Task = {
            ...taskFixture,
            status: 'active',
        };
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [
                    ...capabilities.actor.scopes,
                    'assignments:read',
                ],
            },
            scopes: [
                ...capabilities.scopes,
                'assignments:read',
            ],
        });

        renderWithProviders(<TaskRoutingPanel task={activeTask} />);

        expect(await screen.findByText(
            i18n.t('taskRouting.recoveryAssignmentReadRequired'),
        )).toBeVisible();
        expect(agentServiceMock.listAssignments).not.toHaveBeenCalled();
        expect(screen.getByRole('button', {
            name: i18n.t('taskRouting.generatePreview'),
        })).toBeDisabled();
    });

    it('reloads pending recovery evidence when the task version changes', async () => {
        const activeTask: Task = {
            ...taskFixture,
            status: 'active',
        };
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [...capabilities.actor.scopes, 'planning:read'],
            },
            scopes: [...capabilities.scopes, 'planning:read'],
        });
        agentServiceMock.listAssignments.mockResolvedValue([
            pendingRecoveryAssignment,
        ]);
        const { rerender } = renderWithProviders(
            <TaskRoutingPanel task={activeTask} />,
        );

        await waitFor(() => {
            expect(agentServiceMock.listAssignments).toHaveBeenCalledOnce();
        });

        rerender(
            <TaskRoutingPanel
                task={{ ...activeTask, version: activeTask.version + 1 }}
            />,
        );

        await waitFor(() => {
            expect(agentServiceMock.listAssignments).toHaveBeenCalledTimes(2);
        });
    });

    it('preserves the strictest pending lineage review floor', async () => {
        const activeTask: Task = {
            ...taskFixture,
            status: 'active',
        };
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [...capabilities.actor.scopes, 'planning:read'],
            },
            scopes: [...capabilities.scopes, 'planning:read'],
        });
        agentServiceMock.getTaskRoutingAssessment.mockResolvedValue({
            ...currentAssessmentState,
            state: 'stale',
            assessment: {
                ...currentAssessment,
                task_version: taskFixture.version - 1,
                is_current: false,
            },
        });
        agentServiceMock.listAssignments.mockResolvedValue([
            {
                ...pendingRecoveryAssignment,
                routing_snapshot: {
                    ...pendingRecoveryAssignment.routing_snapshot,
                    review_floor: {
                        review_mode: 'specialist-independent',
                        reviewer_profile_ids: [23],
                        independence_must_be_revalidated: true,
                    },
                },
            },
        ]);
        const { user } = renderWithProviders(
            <TaskRoutingPanel task={activeTask} />,
        );

        const reviewMode = await screen.findByRole('combobox', {
            name: i18n.t('taskRouting.reviewMode'),
        });
        const save = screen.getByRole('button', {
            name: i18n.t('taskRouting.saveAssessment'),
        });

        expect(screen.getByText(i18n.t('taskRouting.minimumReview', {
            mode: i18n.t('taskRouting.reviewModes.specialistIndependent'),
        }))).toBeVisible();
        expect(screen.getByText(i18n.t('taskRouting.reviewBelowMinimum'))).toBeVisible();
        expect(save).toBeDisabled();

        await user.selectOptions(reviewMode, 'specialist-independent');

        expect(screen.queryByText(
            i18n.t('taskRouting.reviewBelowMinimum'),
        )).not.toBeInTheDocument();
        expect(save).toBeEnabled();
    });

    it('cannot preview from an immutable assessment below the lineage review floor', async () => {
        const activeTask: Task = {
            ...taskFixture,
            status: 'active',
        };
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [...capabilities.actor.scopes, 'planning:read'],
            },
            scopes: [...capabilities.scopes, 'planning:read'],
        });
        agentServiceMock.listAssignments.mockResolvedValue([
            {
                ...pendingRecoveryAssignment,
                routing_snapshot: {
                    ...pendingRecoveryAssignment.routing_snapshot,
                    review_floor: {
                        review_mode: 'specialist-independent',
                        reviewer_profile_ids: [23],
                        independence_must_be_revalidated: true,
                    },
                },
            },
        ]);

        renderWithProviders(<TaskRoutingPanel task={activeTask} />);

        expect(await screen.findByText(
            i18n.t('taskRouting.currentAssessmentImmutable'),
        )).toBeVisible();
        expect(screen.getByText(
            i18n.t('taskRouting.reviewBelowMinimum'),
        )).toBeVisible();
        expect(screen.getByRole('button', {
            name: i18n.t('taskRouting.generatePreview'),
        })).toBeDisabled();
        expect(agentServiceMock.previewTaskRouting).not.toHaveBeenCalled();
    });

    it('blocks active recovery unless exactly one queued selection is pending', async () => {
        const activeTask: Task = {
            ...taskFixture,
            status: 'active',
        };
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            actor: {
                ...capabilities.actor,
                scopes: [...capabilities.actor.scopes, 'planning:read'],
            },
            scopes: [...capabilities.scopes, 'planning:read'],
        });
        agentServiceMock.listAssignments.mockResolvedValue([]);
        renderWithProviders(<TaskRoutingPanel task={activeTask} />);

        expect(await screen.findByText(i18n.t(
            'taskRouting.recoveryAssignmentMismatch',
            { count: 0 },
        ))).toBeVisible();
        expect(screen.getByRole('button', {
            name: i18n.t('taskRouting.generatePreview'),
        })).toBeDisabled();
        expect(agentServiceMock.previewTaskRouting).not.toHaveBeenCalled();
    });

    it('enforces independent review when the risk axis is high', async () => {
        agentServiceMock.getTaskRoutingAssessment.mockResolvedValue({
            ...currentAssessmentState,
            state: 'stale',
            assessment: {
                ...currentAssessment,
                task_version: taskFixture.version - 1,
                is_current: false,
            },
        });
        const { user } = renderPanel();

        const risk = await screen.findByRole('combobox', {
            name: i18n.t('taskRouting.axes.risk'),
        });
        const reviewMode = screen.getByRole('combobox', {
            name: i18n.t('taskRouting.reviewMode'),
        });
        const save = screen.getByRole('button', {
            name: i18n.t('taskRouting.saveAssessment'),
        });

        expect(reviewMode).toHaveValue('standard');
        await user.selectOptions(risk, '3');

        expect(screen.getByText(i18n.t('taskRouting.highRiskReviewRequired'))).toBeVisible();
        expect(screen.getByText(i18n.t('taskRouting.reviewBelowMinimum'))).toBeVisible();
        expect(save).toBeDisabled();

        await user.selectOptions(reviewMode, 'independent');
        expect(screen.queryByText(i18n.t('taskRouting.reviewBelowMinimum'))).not.toBeInTheDocument();
        expect(save).toBeEnabled();
    });

    it('keeps a current task-version assessment immutable in the UI', async () => {
        renderPanel();

        expect(await screen.findByText(
            i18n.t('taskRouting.currentAssessmentImmutable'),
        )).toBeVisible();
        expect(screen.getByRole('combobox', {
            name: i18n.t('taskRouting.axes.risk'),
        })).toBeDisabled();
        expect(screen.getByRole('button', {
            name: i18n.t('taskRouting.saveAssessment'),
        })).toBeDisabled();
    });

    it('stops at the capability handshake when routing is not advertised', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue({
            ...capabilities,
            features: [],
        });
        renderPanel();

        expect(await screen.findByText(i18n.t('taskRouting.featureUnavailable'))).toBeVisible();
        expect(agentServiceMock.getTaskRoutingAssessment).not.toHaveBeenCalled();
        expect(agentServiceMock.getProfileSkillCatalog).not.toHaveBeenCalled();
        expect(agentServiceMock.getActorRoster).not.toHaveBeenCalled();
    });

    it('disables a dispatch that becomes expired after selection', async () => {
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture({
            expires_at: new Date(Date.now() + 900).toISOString(),
        }));
        const { user } = renderPanel();

        await generatePreview(user);
        await user.click(screen.getByRole('radio'));

        const reason = screen.getByRole('textbox', {
            name: i18n.t('taskRouting.dispatchReason'),
        });
        const confirmation = screen.getByRole('checkbox', {
            name: i18n.t('taskRouting.confirmSelection'),
        });
        const dispatch = screen.getByRole('button', {
            name: i18n.t('taskRouting.dispatch'),
        });

        await user.type(reason, 'Use the current candidate.');
        await user.click(confirmation);
        expect(dispatch).toBeEnabled();

        expect(await screen.findByText(
            i18n.t('taskRouting.previewExpired'),
            {},
            { timeout: 1_800 },
        )).toBeVisible();
        expect(screen.getByRole('radio')).toBeDisabled();
        expect(reason).toBeDisabled();
        expect(confirmation).toBeDisabled();
        expect(dispatch).toBeDisabled();
        expect(agentServiceMock.createAssignment).not.toHaveBeenCalled();
    });

    it('clears dispatch controls and reloads evidence after an assignment conflict', async () => {
        const conflictMessage = 'Authoritative routing evidence changed.';
        agentServiceMock.previewTaskRouting.mockResolvedValue(previewFixture());
        agentServiceMock.createAssignment.mockRejectedValue({
            response: {
                status: 409,
                data: {
                    detail: {
                        code: 'routing_preview_stale',
                        message: conflictMessage,
                    },
                },
            },
        });
        const { user } = renderPanel();

        await generatePreview(user);
        await user.click(screen.getByRole('radio'));
        await user.type(
            screen.getByRole('textbox', {
                name: i18n.t('taskRouting.dispatchReason'),
            }),
            'Dispatch from current evidence.',
        );
        await user.click(screen.getByRole('checkbox', {
            name: i18n.t('taskRouting.confirmSelection'),
        }));
        await user.click(screen.getByRole('button', {
            name: i18n.t('taskRouting.dispatch'),
        }));

        expect(await screen.findByText(i18n.t('taskRouting.conflictTitle'))).toBeVisible();
        expect(screen.getByText(conflictMessage)).toBeVisible();
        await waitFor(() => {
            expect(screen.queryByRole('button', {
                name: i18n.t('taskRouting.dispatch'),
            })).not.toBeInTheDocument();
        });
        expect(screen.queryByRole('radio')).not.toBeInTheDocument();
        expect(agentServiceMock.getTaskRoutingAssessment.mock.calls.length).toBeGreaterThan(1);
        expect(agentServiceMock.getActorRoster.mock.calls.length).toBeGreaterThan(1);
    });
});
