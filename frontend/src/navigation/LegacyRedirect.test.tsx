import { render, screen, waitFor } from '@testing-library/react';
import { createMemoryRouter, RouterProvider, useLocation } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { LegacyRedirect } from './LegacyRedirect';

function Location() {
    const location = useLocation();
    return <div>{location.pathname + location.search + location.hash}</div>;
}
function setup(path: string) {
    const router = createMemoryRouter([
        { path: '/before', element: <div>Previous page</div> },
        ...['/plan/master', '/iterations', '/roadmap', '/agent-pipeline', '/agent-team/setup', '/calendar']
            .map(route => ({ path: route, element: <LegacyRedirect /> })),
        { path: '/plan', element: <Location /> },
        { path: '*', element: <Location /> },
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
    it.each([
        ['/plan/master', '/plan'],
        ['/iterations', '/plan?panel=iterations'],
        ['/roadmap', '/projects?view=roadmap'],
        ['/agent-pipeline', '/tasks?layout=pipeline'],
        ['/agent-team/setup', '/team?tab=connect'],
        ['/calendar', '/settings?tab=calendar'],
    ])('redirects %s to its current destination and keeps caller parameters', async (legacy, destination) => {
        const query = destination.includes('?')
            ? `?scope=team&${destination.split('?')[1]}`
            : '?scope=team';
        const target = `${destination.split('?')[0]}${query}#details`;
        const router = setup(`${legacy}?scope=team#details`);
        await waitFor(() => expect(router.state.location.pathname + router.state.location.search + router.state.location.hash)
            .toBe(target));
        expect(await screen.findByText(target)).toBeInTheDocument();
    });
});
