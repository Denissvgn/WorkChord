import { expect, it } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import LandingPage from './LandingPage';

it('renders one heading, one paragraph, the four workflow stages and one workspace button', () => {
    renderWithProviders(<LandingPage />);
    expect(screen.getByRole('heading', { level: 1, name: 'Plan and deliver work with people and agents.' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    expect(screen.queryAllByRole('heading')).toHaveLength(1);

    const stages = within(screen.getByRole('list', { name: 'Workflow' })).getAllByRole('listitem');
    expect(stages.map(stage => stage.querySelector('.landing-stage__term')?.textContent)).toEqual(['Capture', 'Plan and assign', 'Do', 'Review']);

    const actions = screen.getAllByRole('link', { name: 'Open the workspace' });
    expect(actions).toHaveLength(1);
    expect(actions[0]).toHaveAttribute('href', '/');
    expect(screen.queryAllByRole('button')).toHaveLength(0);
});

it('uses the shared destination names and none of the retired copy', () => {
    renderWithProviders(<LandingPage />);
    const text = document.body.textContent ?? '';
    expect(text).toContain('Triage');
    expect(text).toContain('My Work');
    expect(text).toContain('Analytics');
    expect(text).not.toMatch(/landing\.\w+/);
    expect(text).not.toMatch(/agent PM|Roadmap|Gantt|Dependencies|Coordinate|Shape/);
});
