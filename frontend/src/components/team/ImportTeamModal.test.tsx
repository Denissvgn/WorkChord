import { act, fireEvent, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import type { TeamMember } from '../../types/team';
import { ImportTeamModal } from './ImportTeamModal';

const teamServiceMock = vi.hoisted(() => ({
    importFromText: vi.fn(),
}));

vi.mock('../../services/teamService', () => ({
    teamService: teamServiceMock,
}));

const deferred = <T,>() => {
    let resolve!: (value: T) => void;
    const promise = new Promise<T>(next => {
        resolve = next;
    });
    return { promise, resolve };
};

class ControlledFileReader {
    static instances: ControlledFileReader[] = [];

    readyState = 0;
    result: string | ArrayBuffer | null = null;
    onload: (() => void) | null = null;
    onerror: (() => void) | null = null;
    onabort: (() => void) | null = null;

    constructor() {
        ControlledFileReader.instances.push(this);
    }

    readAsText() {
        this.readyState = 1;
    }

    abort() {
        this.readyState = 2;
        this.onabort?.();
    }

    succeed(value: string) {
        this.result = value;
        this.readyState = 2;
        this.onload?.();
    }

    fail() {
        this.readyState = 2;
        this.onerror?.();
    }
}

describe('ImportTeamModal', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        ControlledFileReader.instances = [];
        teamServiceMock.importFromText.mockResolvedValue({
            imported_count: 1,
            members: [],
        });
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    it('rejects empty, unrecognized, and oversized imports before mutation', async () => {
        const { user } = renderWithProviders(
            <ImportTeamModal iterationId={9} onClose={vi.fn()} />,
        );
        const importButton = screen.getByRole('button', { name: 'Import' });
        const textInput = screen.getByRole('textbox', { name: 'Team members to import' });

        await user.click(importButton);
        expect(screen.getByRole('alert')).toHaveTextContent('Enter text or upload a file');

        fireEvent.change(textInput, { target: { value: 'This is not an import row' } });
        await user.click(importButton);
        expect(screen.getByRole('alert')).toHaveTextContent(
            'No team rows were found. Each team row must start with --.',
        );

        fireEvent.change(textInput, {
            target: {
                value: Array.from(
                    { length: 501 },
                    (_, index) => `-- "Person ${index}" Developer 100 1.0 20`,
                ).join('\n'),
            },
        });
        await user.click(importButton);
        expect(screen.getByRole('alert')).toHaveTextContent(
            'Import up to 500 non-empty rows at a time.',
        );
        expect(teamServiceMock.importFromText).not.toHaveBeenCalled();
    });

    it('reports state, freezes every exit, and invalidates dependent data while importing', async () => {
        const importRequest = deferred<{ imported_count: number; members: TeamMember[] }>();
        teamServiceMock.importFromText.mockReturnValueOnce(importRequest.promise);
        const onClose = vi.fn();
        const onStateChange = vi.fn();
        let stateAtSuccess: { dirty: boolean; pending: boolean } | undefined;
        const onImportSuccess = vi.fn(() => {
            stateAtSuccess = onStateChange.mock.lastCall?.[0];
        });
        const queryClient = createTestQueryClient();
        const invalidateQueries = vi.spyOn(queryClient, 'invalidateQueries');
        const { user } = renderWithProviders(
            <ImportTeamModal
                iterationId={9}
                onClose={onClose}
                onSuccess={onImportSuccess}
                onStateChange={onStateChange}
            />,
            { queryClient },
        );
        const textInput = screen.getByRole('textbox', { name: 'Team members to import' });
        const validText = '-- "Ada Lovelace" Developer 100 1.0 20';

        await waitFor(() => {
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: false, pending: false });
        });
        await user.type(textInput, validText);
        await waitFor(() => {
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: true, pending: false });
        });

        await user.click(screen.getByRole('button', { name: 'Import' }));
        await waitFor(() => {
            expect(teamServiceMock.importFromText).toHaveBeenCalledWith(9, validText);
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: true, pending: true });
        });

        const closeButton = screen.getByRole('button', { name: 'Close' });
        const cancelButton = screen.getByRole('button', { name: 'Cancel' });
        expect(closeButton).toBeDisabled();
        expect(cancelButton).toBeDisabled();
        expect(textInput).toBeDisabled();
        expect(screen.getByLabelText('Team import file')).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Upload .txt file' })).toBeDisabled();
        await user.click(cancelButton);
        expect(onClose).not.toHaveBeenCalled();

        await act(async () => {
            importRequest.resolve({ imported_count: 1, members: [] });
        });

        await waitFor(() => {
            expect(invalidateQueries).toHaveBeenCalledWith({ queryKey: ['team', 9] });
            expect(invalidateQueries).toHaveBeenCalledWith({ queryKey: ['teamMemberProfiles'] });
            expect(invalidateQueries).toHaveBeenCalledWith({ queryKey: ['workload'] });
            expect(invalidateQueries).toHaveBeenCalledWith({ queryKey: ['gantt'] });
            expect(onImportSuccess).toHaveBeenCalledOnce();
        });
        expect(stateAtSuccess).toEqual({ dirty: true, pending: true });
        expect(onClose).not.toHaveBeenCalled();
        expect(screen.queryByText('Imported: 1 members')).not.toBeInTheDocument();
    });

    it('ignores stale file reads and exposes file failures without dropping prior text', async () => {
        vi.stubGlobal('FileReader', ControlledFileReader);
        renderWithProviders(
            <ImportTeamModal iterationId={9} onClose={vi.fn()} />,
        );
        const fileInput = screen.getByLabelText('Team import file');
        const textInput = screen.getByRole('textbox', { name: 'Team members to import' });

        fireEvent.change(fileInput, {
            target: { files: [new File(['first'], 'first.txt', { type: 'text/plain' })] },
        });
        const firstReader = ControlledFileReader.instances[0];
        fireEvent.change(fileInput, {
            target: { files: [new File(['second'], 'second.txt', { type: 'text/plain' })] },
        });
        const secondReader = ControlledFileReader.instances[1];

        firstReader.succeed('-- "Stale Person" Developer 100 1.0 20');
        secondReader.succeed('-- "Current Person" Developer 100 1.0 20');

        await waitFor(() => {
            expect(textInput).toHaveValue('-- "Current Person" Developer 100 1.0 20');
        });

        fireEvent.change(fileInput, {
            target: { files: [new File(['broken'], 'broken.txt', { type: 'text/plain' })] },
        });
        ControlledFileReader.instances[2].fail();

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'The selected file could not be read. Choose another file or paste its contents.',
        );
        expect(textInput).toHaveValue('-- "Current Person" Developer 100 1.0 20');
    });
});
