import { beforeEach, describe, expect, it, vi } from 'vitest';
import type {
    AgentCommandMetadata,
    AgentModelCatalogCreate,
    AgentTeamMaster,
    AgentTeamPlan,
    ModelAwareAgentTaskAssignmentCreate,
    TaskRoutingAssessmentCommand,
} from '../types/agent';
import api from './api';
import { agentService } from './agentService';

vi.mock('./api', () => ({
    default: {
        get: vi.fn(),
        post: vi.fn(),
        patch: vi.fn(),
    },
}));

const mockedApi = vi.mocked(api);

const metadata: AgentCommandMetadata = {
    idempotencyKey: 'idem-wave-5',
    rationale: 'Route this task using the approved model policy.',
    correlationId: 'corr-wave-5',
};

const expectedCommandConfig = {
    headers: {
        'Idempotency-Key': 'idem-wave-5',
        'X-Agent-Rationale': 'Route this task using the approved model policy.',
        'X-Correlation-ID': 'corr-wave-5',
    },
};

const catalogCommand: AgentModelCatalogCreate = {
    key: 'provider-reasoner',
    provider: 'configured-provider',
    configured_model_alias: 'reasoner',
    reasoning_tier: 3,
    context_tier: 'large',
    modality_tags: ['text'],
    cost_tier: 'medium',
    latency_tier: 'balanced',
};

const assessmentCommand: TaskRoutingAssessmentCommand = {
    expected_task_version: 7,
    band: 'advanced',
    axes: {
        reasoning: 3,
        ambiguity: 2,
        context_breadth: 2,
        risk: 3,
        verification_burden: 2,
    },
    required_skill_levels: {
        'frontend-react': 4,
    },
    required_model: {
        minimum_reasoning_tier: 3,
        minimum_context_tier: 'large',
        modality_tags: ['text'],
        tool_tags: ['repository'],
        data_policy_tags: ['private-source'],
    },
    review_mode: 'independent',
    confidence: 0.92,
    reason_codes: ['security'],
    rationale: 'Security-sensitive architecture work requires independent review.',
};

const assignmentCommand: ModelAwareAgentTaskAssignmentCreate = {
    task_id: 42,
    actor_id: 11,
    expected_task_version: 7,
    purpose: 'execution',
    assessment_id: 91,
    model_binding_id: 31,
    model_binding_revision: 4,
    routing_preview_id: 'preview-42',
    routing_preview_digest: 'a'.repeat(64),
    queue_class: 'normal',
    reason: 'Selected from the current routing preview.',
};

const agentTeamMaster = {
    schema_version: 'agent-team-master-v1',
    topology_key: 'delivery-team',
    server_url: 'https://workchord.invalid',
    credential_sink_ref: 'agent-team-secure-sink',
    required_server_features: ['agent-team-master-v1'],
    controller: {},
    workers: [{}],
    verifiers: [],
    readiness_policy: {
        minimum_execution_workers: 1,
        require_independent_verifier_when_assessed: false,
        maximum_runtime_staleness_seconds: 300,
    },
} as unknown as AgentTeamMaster;

const agentTeamPlan = {
    expected_topology_revision: 3,
    plan_digest: 'c'.repeat(64),
} as AgentTeamPlan;

describe('agentService model-aware routing requests', () => {
    beforeEach(() => {
        mockedApi.get.mockReset();
        mockedApi.post.mockReset();
        mockedApi.patch.mockReset();
        mockedApi.get.mockResolvedValue({ data: [] } as never);
        mockedApi.post.mockResolvedValue({ data: {} } as never);
        mockedApi.patch.mockResolvedValue({ data: {} } as never);
    });

    it('maps include-disabled list filters to the backend parameter name', async () => {
        await agentService.getActorRoster(true);
        await agentService.getModelCatalog(false);
        await agentService.getModelBindings({
            actorId: 11,
            includeDisabled: true,
        });

        expect(mockedApi.get).toHaveBeenNthCalledWith(
            1,
            '/agent/actors',
            { params: { include_disabled: true } },
        );
        expect(mockedApi.get).toHaveBeenNthCalledWith(
            2,
            '/agent/model-catalog',
            { params: { include_disabled: false } },
        );
        expect(mockedApi.get).toHaveBeenNthCalledWith(
            3,
            '/agent/model-bindings',
            {
                params: {
                    actor_id: 11,
                    include_disabled: true,
                },
            },
        );
    });

    it('sends exact command headers for catalog mutations', async () => {
        await agentService.createModelCatalogEntry(catalogCommand, metadata);

        expect(mockedApi.post).toHaveBeenCalledWith(
            '/agent/model-catalog',
            catalogCommand,
            expectedCommandConfig,
        );
    });

    it('sends exact command headers for routing assessments', async () => {
        await agentService.createTaskRoutingAssessment(
            42,
            assessmentCommand,
            metadata,
        );

        expect(mockedApi.post).toHaveBeenCalledWith(
            '/agent/planning/tasks/42/routing-assessment',
            assessmentCommand,
            expectedCommandConfig,
        );
    });

    it('sends exact command headers for assignment mutations', async () => {
        await agentService.createAssignment(assignmentCommand, metadata);

        expect(mockedApi.post).toHaveBeenCalledWith(
            '/agent/assignments',
            assignmentCommand,
            expectedCommandConfig,
        );
    });

    it('uses the setup status, validate, plan, and single-action apply contracts', async () => {
        await agentService.getAgentTeamStatus('delivery-team');
        await agentService.validateAgentTeamMaster(agentTeamMaster);
        await agentService.planAgentTeamMaster(agentTeamMaster, 3);
        await agentService.applyAgentTeamAction(
            agentTeamMaster,
            agentTeamPlan,
            'safe-update-worker',
            true,
            metadata,
        );

        expect(mockedApi.get).toHaveBeenCalledWith(
            '/agent/team-setup/status',
            { params: { topology_key: 'delivery-team' } },
        );
        expect(mockedApi.post).toHaveBeenNthCalledWith(
            1,
            '/agent/team-setup/validate',
            { manifest: agentTeamMaster },
        );
        expect(mockedApi.post).toHaveBeenNthCalledWith(
            2,
            '/agent/team-setup/plan',
            {
                manifest: agentTeamMaster,
                expected_topology_revision: 3,
            },
        );
        expect(mockedApi.post).toHaveBeenNthCalledWith(
            3,
            '/agent/team-setup/apply',
            {
                manifest: agentTeamMaster,
                expected_topology_revision: 3,
                plan_digest: agentTeamPlan.plan_digest,
                approved_action_ids: ['safe-update-worker'],
                confirmed_action_ids: ['safe-update-worker'],
            },
            expectedCommandConfig,
        );
    });
});
