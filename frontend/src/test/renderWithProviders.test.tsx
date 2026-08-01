import { useQueryClient } from '@tanstack/react-query';
import { screen } from '@testing-library/react';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { useToast } from '../components/feedback/toast';
import { renderWithProviders } from './renderWithProviders';

const ProviderProbe = () => {
    const queryClient = useQueryClient();
    const location = useLocation();
    const { i18n } = useTranslation();
    const toast = useToast();

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
    });
});
