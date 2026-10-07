import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import type { FormEvent } from 'react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { TaskTimelinePanel } from './TaskTimelinePanel';

const taskServiceMock = vi.hoisted(() => ({
    getTimelinePage: vi.fn(),
    getExternalLinks: vi.fn(),
    createGitHubExternalLink: vi.fn(),
    deleteExternalLink: vi.fn(),
    refreshGitHubExternalLink: vi.fn(),
}));

vi.mock('../../services/taskService', () => ({
    taskService: taskServiceMock,
}));

vi.mock('../requestSources/RequestSourceLinksPanel', () => ({
    RequestSourceLinksPanel: () => <div>Request sources</div>,
}));

const task: Task = {
    id: 42,
    iteration_id: 1,
    project_id: null,
    title: 'Resolve launch blocker',
    priority: 1,
    effort_days: 2,
    effort_hours: 16,
    status: 'active',
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: 0,
    version: 1,
    request_count: 0,
    external_links: [],
    agent_readiness: {
        is_ready: false,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    children: [],
    dependencies: [],
};

describe('TaskTimelinePanel', () => {
    beforeEach(() => {
        taskServiceMock.getTimelinePage.mockReset();
        taskServiceMock.getTimelinePage.mockResolvedValue({ task_id: 42, items: [], has_more: false, next_cursor: null });
        taskServiceMock.getExternalLinks.mockReset();
        taskServiceMock.getExternalLinks.mockResolvedValue([]);
        taskServiceMock.createGitHubExternalLink.mockReset();
        taskServiceMock.createGitHubExternalLink.mockResolvedValue({});
        taskServiceMock.deleteExternalLink.mockReset();
        taskServiceMock.refreshGitHubExternalLink.mockReset();
    });

    it('hides cached private links when a later read fails', async () => {
        taskServiceMock.getExternalLinks.mockResolvedValue([{ id: 1, entity_type: 'task', entity_id: 42,
            provider: 'github', url: 'https://github.com/example/private/pull/1', title: 'Private source link',
            metadata_json: {}, is_legacy: false }]);
        const { queryClient } = renderWithProviders(<TaskTimelinePanel task={task} />);
        await screen.findByText('Private source link');
        taskServiceMock.getExternalLinks.mockRejectedValue(new Error('Permission revoked'));
        await act(async () => { await queryClient.invalidateQueries({ queryKey: ['task-external-links', 42] }); });
        await waitFor(() => expect(screen.queryByText('Private source link')).toBeNull());
        expect(screen.getByRole('alert')).toBeVisible();
        expect(screen.queryByRole('button', { name: /Delete.*Private source link/ })).toBeNull();
    });

    it('links GitHub work by keyboard without nesting or submitting the task form', async () => {
        const outerSubmit = vi.fn((event: FormEvent<HTMLFormElement>) => {
            event.preventDefault();
        });
        const { user, container } = renderWithProviders(
            <form aria-label="Task editor" onSubmit={outerSubmit}>
                <TaskTimelinePanel task={task} />
            </form>,
        );

        expect(container.querySelectorAll('form')).toHaveLength(1);

        await user.type(
            screen.getByRole('textbox'),
            'https://github.com/openai/workchord/pull/42{Enter}',
        );

        await waitFor(() => expect(
            taskServiceMock.createGitHubExternalLink,
        ).toHaveBeenCalledWith(
            42,
            { url: 'https://github.com/openai/workchord/pull/42' },
        ));
        expect(outerSubmit).not.toHaveBeenCalled();
    });
});
