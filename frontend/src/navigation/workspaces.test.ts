import { describe, expect, it } from 'vitest';
import { getWorkspaceForPath, getWorkspaceFromPath } from './workspaces';

describe('workspace routing', () => {
    it.each([
        ['/', 'delivery'],
        ['/plan/master', 'planning'],
        ['/projects/42/releases/7', 'delivery'],
        ['/roadmap', 'planning'],
        ['/gantt', 'planning'],
        ['/agent-team/setup', 'resource'],
        ['/settings/email', 'resource'],
    ] as const)('maps %s to the %s workspace', (pathname, workspace) => {
        expect(getWorkspaceFromPath(pathname)).toBe(workspace);
        expect(getWorkspaceForPath(pathname).key).toBe(workspace);
    });

    it('falls back to Delivery for an unmatched path', () => {
        expect(getWorkspaceFromPath('/missing')).toBe('delivery');
    });
});
