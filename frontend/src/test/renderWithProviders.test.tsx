import { useQueryClient } from '@tanstack/react-query';
import { screen } from '@testing-library/react';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { useToast } from '../components/feedback/toast';
import { renderWithProviders } from './renderWithProviders';

const ProviderProbe = () => {
    const queryClient = useQueryClient();
    const location = useLocation();
    const { i18n } = useTranslation();
    const toast = useToast();
    const [restored, setRestored] = useState(false);

    return (
        <>
            <output
                aria-label="Provider state"
                data-language={i18n.language}
                data-query-client={String(Boolean(queryClient))}
            >
                {location.pathname}
            </output>
            <button type="button" onClick={() => toast.info('Harness ready', { durationMs: 0 })}>
                Notify
            </button>
            <button
                type="button"
                onClick={() => toast.success('Change saved', {
                    actionLabel: 'Undo',
                    durationMs: 0,
                    onAction: () => setRestored(true),
                })}
            >
                Notify with undo
            </button>
            <output aria-label="Undo state">{restored ? 'Restored' : 'Changed'}</output>
        </>
    );
};

describe('renderWithProviders', () => {
    it('provides query, router, i18n, toast, and user-event support', async () => {
        const { user } = renderWithProviders(<ProviderProbe />, {
            initialEntries: ['/routing'],
        });

        const state = screen.getByLabelText('Provider state');
        expect(state).toHaveTextContent('/routing');
        expect(state).toHaveAttribute('data-language', 'en');
        expect(state).toHaveAttribute('data-query-client', 'true');

        await user.click(screen.getByRole('button', { name: 'Notify' }));
        expect(screen.getByText('Harness ready')).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Notify with undo' }));
        await user.click(screen.getByRole('button', { name: 'Undo' }));
        expect(screen.getByLabelText('Undo state')).toHaveTextContent('Restored');
        expect(screen.queryByText('Change saved')).not.toBeInTheDocument();
    });
});
