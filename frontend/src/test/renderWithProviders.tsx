import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, type RenderOptions } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import type { ReactElement, ReactNode } from 'react';
import { ToastProvider } from '../components/feedback/ToastProvider';
import '../i18n/i18n';

export const createTestQueryClient = () => new QueryClient({
    defaultOptions: {
        queries: {
            retry: false,
        },
        mutations: {
            retry: false,
        },
    },
});

interface RenderWithProvidersOptions extends Omit<RenderOptions, 'wrapper'> {
    initialEntries?: string[];
    queryClient?: QueryClient;
}

export const renderWithProviders = (
    ui: ReactElement,
    {
        initialEntries = ['/'],
        queryClient = createTestQueryClient(),
        ...renderOptions
    }: RenderWithProvidersOptions = {},
) => {
    const Wrapper = ({ children }: { children: ReactNode }) => (
        <QueryClientProvider client={queryClient}>
            <MemoryRouter initialEntries={initialEntries}>
                <ToastProvider>{children}</ToastProvider>
            </MemoryRouter>
        </QueryClientProvider>
    );

    return {
        queryClient,
        user: userEvent.setup(),
        ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    };
};
