import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AccessKeysSummary } from './AccessKeysSummary';
import { SettingsUnsavedBar } from './SettingsUnsavedBar';
import { SystemHealthPanel } from './SystemHealthPanel';
import { WithheldValuesNote } from './WithheldValuesNote';

const health = vi.hoisted(() => ({ check: vi.fn() }));
vi.mock('../../services/healthService', () => ({ healthService: health }));

describe('settings access, unsaved state, and About', () => {
    it('names both keys with what each unlocks and how to get it', () => {
        renderWithProviders(<AccessKeysSummary />);
        expect(screen.getByRole('heading', { name: 'Two keys' })).toBeInTheDocument();
        expect(screen.getByText('Admin key')).toBeInTheDocument();
        expect(screen.getByText('Agent key')).toBeInTheDocument();
        expect(screen.getByText(/WORKCHORD_ADMIN_API_KEY/)).toBeInTheDocument();
    });

    it('shows unsaved changes with Save and Discard, and nothing when clean', async () => {
        const onSave = vi.fn();
        const onDiscard = vi.fn();
        const { user, rerender } = renderWithProviders(<SettingsUnsavedBar dirty onSave={onSave} onDiscard={onDiscard} />);
        const bar = screen.getByRole('region', { name: 'Unsaved changes' });
        expect(bar).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await user.click(screen.getByRole('button', { name: 'Discard' }));
        expect(onSave).toHaveBeenCalledOnce();
        expect(onDiscard).toHaveBeenCalledOnce();
        rerender(<SettingsUnsavedBar dirty={false} onSave={onSave} />);
        expect(screen.queryByRole('region', { name: 'Unsaved changes' })).toBeNull();
    });

    it('names withheld values only when the server withheld some', () => {
        const { rerender } = renderWithProviders(<WithheldValuesNote fields={['smtp_host', 'unknown']} labels={{ smtp_host: 'mail server host' }} />);
        expect(screen.getByText('Hidden without the admin key: mail server host.')).toBeInTheDocument();
        rerender(<WithheldValuesNote fields={[]} labels={{ smtp_host: 'mail server host' }} />);
        expect(screen.queryByText(/Hidden without the admin key/)).toBeNull();
    });

    it('checks health when About opens and shows the version line', async () => {
        health.check.mockResolvedValue({ state: 'healthy' });
        renderWithProviders(<SystemHealthPanel />);
        expect(await screen.findByText('The application service is healthy.')).toBeInTheDocument();
        expect(health.check).toHaveBeenCalledOnce();
        expect(screen.getByText(/^WorkChord version/)).toBeInTheDocument();
    });
});
