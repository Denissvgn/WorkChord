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
            <button type="button" onClick={() => setEnabled(true)}>Enable</button>
        </>
    );
};

describe('useSingleKeyShortcutPreference', () => {
    beforeEach(() => {
        window.localStorage.clear();
    });

    it('defaults to disabled and persists explicit opt-in', async () => {
        const { user } = renderWithProviders(<PreferenceProbe />);

        expect(screen.getByText('disabled')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Enable' }));

        expect(screen.getByText('enabled')).toBeVisible();
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('true');
    });

    it('synchronizes cross-tab changes and storage clearing', () => {
        renderWithProviders(<PreferenceProbe />);

        act(() => {
            window.dispatchEvent(new StorageEvent('storage', {
                key: SINGLE_KEY_SHORTCUTS_STORAGE_KEY,
                newValue: 'true',
            }));
        });
        expect(screen.getByText('enabled')).toBeVisible();

        act(() => {
            window.dispatchEvent(new StorageEvent('storage', {
                key: null,
                newValue: null,
            }));
        });
        expect(screen.getByText('disabled')).toBeVisible();
    });
});
