import { afterEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PageHeader } from './PageLayout';

describe('PageHeader', () => {
    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('renders one primary action and logs a development error when given two', () => {
        const error = vi.spyOn(console, 'error').mockImplementation(() => undefined);
        renderWithProviders(
            <PageHeader
                title="Projects"
                purpose="Plan work across iterations."
                primaryAction={[
                    <button key="a" type="button">Create project</button>,
                    <button key="b" type="button">Import project</button>,
                ]}
            />,
        );

        expect(screen.getByRole('button', { name: 'Create project' })).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Import project' })).not.toBeInTheDocument();
        expect(error).toHaveBeenCalledTimes(1);
        expect(error.mock.calls[0][0]).toContain('one primary action');
    });

    it('stays quiet for one primary action, two secondary actions and an overflow menu', () => {
        const error = vi.spyOn(console, 'error').mockImplementation(() => undefined);
        renderWithProviders(
            <PageHeader
                title="Projects"
                purpose="Plan work across iterations."
                primaryAction={<button type="button">Create project</button>}
                secondaryActions={[
                    <button key="a" type="button">Export</button>,
                    <button key="b" type="button">Share</button>,
                ]}
                overflowItems={[
                    { label: 'Archive', onSelect: vi.fn() },
                    { label: 'Delete', onSelect: vi.fn() },
                ]}
            />,
        );

        expect(screen.getByRole('heading', { level: 1, name: 'Projects' })).toBeInTheDocument();
        expect(screen.getByText('Plan work across iterations.')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Export' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Share' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'More actions' })).toBeInTheDocument();
        expect(error).not.toHaveBeenCalled();
    });

    it('logs a development error and drops the third secondary action', () => {
        const error = vi.spyOn(console, 'error').mockImplementation(() => undefined);
        renderWithProviders(
            <PageHeader
                title="Projects"
                secondaryActions={[
                    <button key="a" type="button">Export</button>,
                    <button key="b" type="button">Share</button>,
                    <button key="c" type="button">Print</button>,
                ]}
            />,
        );

        expect(screen.queryByRole('button', { name: 'Print' })).not.toBeInTheDocument();
        expect(error).toHaveBeenCalledTimes(1);
    });
});
