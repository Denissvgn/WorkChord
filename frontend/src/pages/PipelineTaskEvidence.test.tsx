import { screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../i18n/i18n';
import type {
    AgentRun,
    TaskTimelineResponse,
} from '../types/agent';
import type { Task } from '../types/task';
import { renderWithProviders } from '../test/renderWithProviders';
import { PipelineTaskEvidence } from '../components/tasks/PipelineTaskEvidence';

const agentServiceMock = vi.hoisted(() => ({
    getPipeline: vi.fn(),
    getTaskTimeline: vi.fn(),
    getRunDetail: vi.fn(),
}));

const useAdminAccessMock = vi.hoisted(() => vi.fn());
const useAgentAccessMock = vi.hoisted(() => vi.fn());

vi.mock('../services/agentService', () => ({
    agentService: agentServiceMock,
}));

const useKeylessReaderMock = vi.hoisted(() => vi.fn(() => ({ settings: false, workViews: false })));

vi.mock('../hooks/useAdminAccess', () => ({
    useAdminAccess: useAdminAccessMock,
    useKeylessReader: useKeylessReaderMock,
}));

vi.mock('../hooks/useAgentAccess', () => ({
    useAgentAccess: useAgentAccessMock,
}));

vi.mock('../components/agent/TaskRoutingPanel', () => ({
    TaskRoutingPanel: () => null,
}));

const sensitive = {
    timelineTitle: 'secret-timeline-title',
    timelineReason: 'secret-timeline-reason',
    timelineSummary: 'secret-timeline-summary',
    configuredModel: 'secret-configured-model-alias',
    legacyModel: 'secret-legacy-model',
    resolvedModel: 'secret-resolved-provider-model',
    toolName: 'secret-provider-tool-input',
    metadataPrompt: 'secret-raw-provider-prompt',
    artifactToken: 'secret-artifact-url-token',
    commitToken: 'secret-commit-url-token',
    pullRequestToken: 'secret-pr-url-token',
    eventType: 'secret-event-type',
    eventMessage: 'secret-private-log-message',
    eventPayload: 'secret-event-payload',
    traceId: 'secret-trace-id',
    correlationId: 'secret-correlation-id',
    idempotencyKey: 'secret-idempotency-key',
    runError: 'secret-private-runtime-error',
    runSummary: 'secret-private-provider-output',
};

const taskFixture: Task = {
    id: 42,
    iteration_id: 9,
    project_id: 3,
    title: 'Bounded run evidence',
    description: 'Inspect the safe execution status.',
    priority: 2,
    effort_days: 2,
    effort_hours: 16,
    status: 'active',
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
        is_ready: false,
        blockers: ['Definition evidence is incomplete.'],
        warnings: [],
        criteria: [],
    },
    version: 7,
    children: [],
    dependencies: [],
};

const timelineFixture: TaskTimelineResponse = {
    task_id: taskFixture.id,
    items: [
        {
            item_type: 'agent_run',
            timestamp: '2026-07-28T00:00:00Z',
            title: sensitive.timelineTitle,
            payload: {
                run_id: 501,
                reason: sensitive.timelineReason,
                summary: sensitive.timelineSummary,
            },
        },
        {
            item_type: 'agent_run_event',
            timestamp: '2026-07-28T00:01:00Z',
            title: sensitive.eventMessage,
            payload: {
                prompt: sensitive.metadataPrompt,
            },
        },
    ],
};

const runFixture = (status: AgentRun['status']): AgentRun => ({
    id: 501,
    task_id: taskFixture.id,
    actor_id: 11,
    assignment_id: 31,
    claim_generation: 2,
    status,
    trace_id: sensitive.traceId,
    model_binding_id: 31,
    model_binding_revision: 4,
    configured_model_alias: sensitive.configuredModel,
    resolved_model_id: sensitive.resolvedModel,
    model_trust_state: 'matched',
    model_match_basis: 'configured_alias',
    model: sensitive.legacyModel,
    tool_name: sensitive.toolName,
    metadata: {
        prompt: sensitive.metadataPrompt,
    },
    artifact_links: [
        `https://artifacts.example/private?token=${sensitive.artifactToken}`,
    ],
    commit_url: `https://github.com/example/private/commit/abc?token=${sensitive.commitToken}`,
    pr_url: `https://github.com/example/private/pull/7?token=${sensitive.pullRequestToken}`,
    summary: sensitive.runSummary,
    error: sensitive.runError,
    started_at: '2026-07-28T00:00:00Z',
    heartbeat_at: '2026-07-28T00:02:00Z',
    events: [{
        id: 601,
        run_id: 501,
        event_type: sensitive.eventType,
        message: sensitive.eventMessage,
        payload: {
            private_log: sensitive.eventPayload,
            provider_prompt: sensitive.metadataPrompt,
        },
        trace_id: sensitive.traceId,
        correlation_id: sensitive.correlationId,
        idempotency_key: sensitive.idempotencyKey,
        created_at: '2026-07-28T00:01:00Z',
    }],
});

const openRunConsole = async () => {
    const { user } = renderWithProviders(<PipelineTaskEvidence task={taskFixture} />);
    await user.click(screen.getByText(i18n.t('agentPipeline.consoleTitle'), { selector: 'summary' }));
    await screen.findByText(i18n.t('agentPipeline.consoleTitle'), { selector: 'summary' });
    await waitFor(() => {
        expect(agentServiceMock.getRunDetail).toHaveBeenCalledWith(501);
    });
};

const expectSensitiveValuesWithheld = () => {
    const renderedMarkup = document.documentElement.innerHTML;
    for (const value of Object.values(sensitive)) {
        expect(renderedMarkup).not.toContain(value);
    }
};

describe('Pipeline task bounded run evidence', () => {
    beforeEach(() => {
        useAdminAccessMock.mockReset();
        useAgentAccessMock.mockReset();
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        useAgentAccessMock.mockReturnValue({ hasAgentKey: true });

        agentServiceMock.getPipeline.mockReset();
        agentServiceMock.getTaskTimeline.mockReset();
        agentServiceMock.getRunDetail.mockReset();
        agentServiceMock.getTaskTimeline.mockResolvedValue(timelineFixture);
    });

    it.each([
        ['failed', 'failureDetailsWithheld'],
        ['succeeded', 'successDetailsWithheld'],
    ] as const)('withholds raw fields from a %s run', async (status, outcomeKey) => {
        agentServiceMock.getRunDetail.mockResolvedValue(runFixture(status));

        await openRunConsole();

        expect(await screen.findByText(
            i18n.t(`agentPipeline.${outcomeKey}`),
        )).toBeVisible();
        expect(screen.getByText(i18n.t('agentPipeline.sensitiveRunFieldsWithheld'))).toBeVisible();
        expect(screen.getByText(i18n.t('agentPipeline.runEventDetailsWithheld'))).toBeVisible();
        expect(screen.getAllByText(i18n.t('agentPipeline.timelineDetailsWithheld'))).toHaveLength(2);
        expect(screen.getByText(
            i18n.t('agentPipeline.modelBindingEvidenceValue', {
                id: 31,
                revision: 4,
            }),
        )).toBeVisible();
        expect(screen.getByText(
            i18n.t('agentPipeline.externalReferencesWithheld', { count: 3 }),
        )).toBeVisible();
        expectSensitiveValuesWithheld();
    });

    it('maps unsupported status and trust values to closed fallback labels', async () => {
        const statusSentinel = 'secret-unsupported-run-status';
        const trustSentinel = 'secret-unsupported-trust-state';
        agentServiceMock.getRunDetail.mockResolvedValue({
            ...runFixture('running'),
            status: statusSentinel,
            model_trust_state: trustSentinel,
        } as unknown as AgentRun);

        await openRunConsole();

        expect(await screen.findByText(i18n.t('agentPipeline.runStatuses.unknown'))).toBeVisible();
        expect(screen.getByText(i18n.t('agentPipeline.modelTrustStates.unknown'))).toBeVisible();
        expect(document.documentElement.innerHTML).not.toContain(statusSentinel);
        expect(document.documentElement.innerHTML).not.toContain(trustSentinel);
        expectSensitiveValuesWithheld();
    });

    it('does not expose raw API error details when run evidence fails', async () => {
        const errorSentinel = 'secret-upstream-run-error';
        agentServiceMock.getRunDetail.mockRejectedValue({
            response: {
                status: 503,
                data: {
                    detail: errorSentinel,
                },
            },
        });

        await openRunConsole();

        expect(await screen.findByText(i18n.t('agentPipeline.runUnavailable'))).toBeVisible();
        expect(document.documentElement.innerHTML).not.toContain(errorSentinel);
        expect(document.documentElement.innerHTML).not.toContain(sensitive.timelineTitle);
        expect(document.documentElement.innerHTML).not.toContain(sensitive.timelineReason);
        expect(document.documentElement.innerHTML).not.toContain(sensitive.timelineSummary);
    });

    it('keeps run evidence behind the key for a keyless reader', () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        useAgentAccessMock.mockReturnValue({ hasAgentKey: false });
        renderWithProviders(<PipelineTaskEvidence task={taskFixture} />);
        expect(screen.queryByText(i18n.t('agentPipeline.consoleTitle'))).not.toBeInTheDocument();
        expect(agentServiceMock.getTaskTimeline).not.toHaveBeenCalled();
        expect(agentServiceMock.getRunDetail).not.toHaveBeenCalled();
    });

    it.each(['task-timeline', 'agent-run-detail'])('hides cached evidence when %s authorization expires', async queryKey => {
        agentServiceMock.getRunDetail.mockResolvedValue(runFixture('succeeded'));
        const { user, queryClient } = renderWithProviders(<PipelineTaskEvidence task={taskFixture} />);
        await user.click(screen.getByText(i18n.t('agentPipeline.consoleTitle'), { selector: 'summary' }));
        const binding = i18n.t('agentPipeline.modelBindingEvidenceValue', { id: 31, revision: 4 });
        expect(await screen.findByText(binding)).toBeVisible();
        const service = queryKey === 'task-timeline' ? agentServiceMock.getTaskTimeline : agentServiceMock.getRunDetail;
        service.mockRejectedValue({ response: { status: 403, data: { detail: 'private authorization detail' } } });
        await queryClient.invalidateQueries({ queryKey: [queryKey] });
        await waitFor(() => expect(screen.queryByText(binding)).not.toBeInTheDocument());
        expect(screen.queryByText(i18n.t('agentPipeline.outcomeSuccess'))).not.toBeInTheDocument();
        expect(document.documentElement.innerHTML).not.toContain('private authorization detail');
        expectSensitiveValuesWithheld();
    });
});
