import { render, screen, waitFor } from '@testing-library/react';
import { createMemoryRouter, RouterProvider, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import { LegacyRedirect } from './LegacyRedirect';

vi.mock('./legacySwitches', () => ({ legacySwitches: { '/plan/master': true, '/iterations': false } }));
function Location() {
    const location = useLocation();
    return <div>{location.pathname + location.search + location.hash}</div>;
}
function setup(path: string) {
    const router = createMemoryRouter([
        { path: '/before', element: <div>Previous page</div> },
        { path: '/plan/master', element: <LegacyRedirect><div>Old master</div></LegacyRedirect> },
        { path: '/iterations', element: <LegacyRedirect><div>Old iterations</div></LegacyRedirect> },
        { path: '/plan', element: <Location /> },
    ], { initialEntries: ['/before', path], initialIndex: 1 });
    render(<RouterProvider router={router} />);
    return router;
}
describe('legacy redirects', () => {
    it('replaces an enabled legacy location while preserving query and hash', async () => {
        const router = setup('/plan/master?scope=team&scope=mine#details');
        expect(await screen.findByText('/plan?scope=team&scope=mine#details')).toBeInTheDocument();
        await router.navigate(-1);
        await waitFor(() => expect(screen.getByText('Previous page')).toBeInTheDocument());
    });
    it('renders the old page when its switch is off', async () => {
        const router = setup('/iterations?scope=team#details');
        expect(await screen.findByText('Old iterations')).toBeInTheDocument();
        expect(router.state.location.pathname + router.state.location.search + router.state.location.hash).toBe('/iterations?scope=team#details');
    });
});
