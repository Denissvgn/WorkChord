import { beforeEach, describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { useScopeStore } from '../../features/scope/scopeStore';
import { BareLayout } from './BareLayout';

const homeLink = () => screen.getAllByRole('link').find(link => link.classList.contains('brand'));

describe('BareLayout', () => {
    beforeEach(() => {
        useScopeStore.setState({ project: null, iteration: null });
    });

    it('keeps the scope in the URL on the home link over the remembered scope', () => {
        useScopeStore.getState().remember({ project: 1, iteration: 12 });

        renderWithProviders(<BareLayout><p>Shared plan</p></BareLayout>, {
            initialEntries: ['/plan/share/abc?project=2&iteration=backlog'],
        });

        expect(homeLink()).toHaveAttribute('href', '/?project=2&iteration=backlog');
    });

    it('carries the remembered scope on the home link when the URL has none', () => {
        useScopeStore.getState().remember({ project: 'all', iteration: 12 });

        renderWithProviders(<BareLayout><p>Connect</p></BareLayout>, { initialEntries: ['/mobile/connect'] });

        expect(homeLink()).toHaveAttribute('href', '/?project=all&iteration=12');
    });

    it('links home without parameters before any scope is known', () => {
        renderWithProviders(<BareLayout><p>Connect</p></BareLayout>, { initialEntries: ['/mobile/connect'] });

        expect(homeLink()).toHaveAttribute('href', '/');
    });
});
