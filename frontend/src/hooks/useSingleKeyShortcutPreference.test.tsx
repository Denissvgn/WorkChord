import { act, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it } from 'vitest';
import { renderWithProviders } from '../test/renderWithProviders';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../utils/singleKeyShortcutPreference';
import { useSingleKeyShortcutPreference } from './useSingleKeyShortcutPreference';

const PreferenceProbe = () => {
    const { enabled, setEnabled } = useSingleKeyShortcutPreference();
    return (
        <>
            <output>{enabled ? 'enabled' : 'disabled'}</output>
            <button type="button" onClick={() => setEnabled(false)}>Disable</button>
        </>
    );
};

describe('useSingleKeyShortcutPreference', () => {
    beforeEach(() => {
        window.localStorage.clear();
    });

    it('defaults to enabled and persists an explicit opt-out', async () => {
        const { user } = renderWithProviders(<PreferenceProbe />);

        expect(screen.getByText('enabled')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Disable' }));

        expect(screen.getByText('disabled')).toBeVisible();
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('false');
    });

    it('synchronizes cross-tab changes and storage clearing', () => {
        renderWithProviders(<PreferenceProbe />);

        act(() => {
            window.dispatchEvent(new StorageEvent('storage', {
                key: SINGLE_KEY_SHORTCUTS_STORAGE_KEY,
                newValue: 'false',
            }));
        });
        expect(screen.getByText('disabled')).toBeVisible();

        // Cleared storage falls back to the default: on.
        act(() => {
            window.dispatchEvent(new StorageEvent('storage', {
                key: null,
                newValue: null,
            }));
        });
        expect(screen.getByText('enabled')).toBeVisible();
    });
});
