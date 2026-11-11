import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import type { FormEvent } from 'react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { RequestSourceLinksPanel } from './RequestSourceLinksPanel';

const requestSourceServiceMock = vi.hoisted(() => ({
    getLinks: vi.fn(),
    search: vi.fn(),
    createLink: vi.fn(),
    deleteLink: vi.fn(),
}));

vi.mock('../../services/requestSourceService', () => ({
    requestSourceService: requestSourceServiceMock,
}));

describe('RequestSourceLinksPanel', () => {
    beforeEach(() => {
        requestSourceServiceMock.getLinks.mockReset();
        requestSourceServiceMock.getLinks.mockResolvedValue([]);
        requestSourceServiceMock.search.mockReset();
        requestSourceServiceMock.search.mockResolvedValue([]);
        requestSourceServiceMock.createLink.mockReset();
        requestSourceServiceMock.createLink.mockResolvedValue({});
        requestSourceServiceMock.deleteLink.mockReset();
    });

    it('adds a request source by keyboard without nesting or submitting the task form', async () => {
        const outerSubmit = vi.fn((event: FormEvent<HTMLFormElement>) => {
            event.preventDefault();
        });
        const { user, container } = renderWithProviders(
            <form aria-label="Task editor" onSubmit={outerSubmit}>
                <RequestSourceLinksPanel
                    targetType="task"
                    targetId={42}
                    compact
                />
            </form>,
        );

        expect(container.querySelectorAll('form')).toHaveLength(1);

        // The form waits behind "Link request" and has real labels.
        expect(screen.queryByRole('textbox', { name: 'Request title' })).toBeNull();
        await user.click(screen.getByRole('button', { name: 'Link request' }));
        const requestTitle = screen.getByRole('textbox', { name: 'Request title' });
        expect(screen.getByRole('textbox', { name: 'Source name' })).toBeInTheDocument();
        await user.type(requestTitle, 'Customer escalation{Enter}');

        await waitFor(() => expect(requestSourceServiceMock.createLink).toHaveBeenCalledWith(
            expect.objectContaining({
                target_type: 'task',
                target_id: 42,
                request_source: expect.objectContaining({
                    title: 'Customer escalation',
                }),
            }),
        ));
        expect(outerSubmit).not.toHaveBeenCalled();
        await waitFor(() => expect(screen.queryByRole('textbox', { name: 'Request title' })).toBeNull());
    });
});
