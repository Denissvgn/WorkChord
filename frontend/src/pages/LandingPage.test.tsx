import { expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import LandingPage from './LandingPage';

it('renders the landing copy from the catalog', () => {
    renderWithProviders(<LandingPage />);
    expect(screen.getByRole('heading', { level: 1, name: 'Plan work that holds.' })).toBeInTheDocument();
    expect(screen.getByRole('list', { name: 'Coordinate surfaces' })).toHaveTextContent('Agent pipeline');
    expect(screen.getByText('Result — Less intent is lost between intake and planning.')).toBeInTheDocument();
    expect(document.body.textContent).not.toMatch(/landing\.\w+/);
});
