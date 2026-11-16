import { render, screen } from '@testing-library/react';
import { createMemoryRouter, RouterProvider, useLocation } from 'react-router-dom';
import { it, expect } from 'vitest';
import { LegacyRedirect } from './LegacyRedirect';

it('opens the work calendar section from the legacy calendar path', async () => {
    const Destination = () => { const location = useLocation(); return <div>{location.pathname + location.search}</div>; };
    const router = createMemoryRouter([
        { path: '/calendar', element: <LegacyRedirect><div>Old calendar</div></LegacyRedirect> },
        { path: '/settings', element: <Destination /> },
    ], { initialEntries: ['/calendar?year=2026'] });
    render(<RouterProvider router={router} />);
    expect(await screen.findByText('/settings?year=2026&tab=calendar')).toBeInTheDocument();
});
