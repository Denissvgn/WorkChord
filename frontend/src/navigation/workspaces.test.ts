import { describe, expect, it } from 'vitest';
import { DESTINATIONS } from './destinations';
import { getWorkspaceForPath, WORKSPACES } from './workspaces';

describe('work areas for the current shell', () => {
    it.each([
        ['/', 'delivery'],
        ['/plan/master', 'planning'],
        ['/projects/42/releases/7', 'delivery'],
        ['/roadmap', 'planning'],
        ['/iterations', 'planning'],
        ['/calendar', 'planning'],
        ['/gantt', 'planning'],
        ['/agent-pipeline', 'delivery'],
        ['/agent-team/setup', 'resource'],
        ['/settings/email', 'resource'],
        ['/mobile/connect', 'delivery'],
    ] as const)('maps %s to the %s area', (pathname, workspace) => {
        expect(getWorkspaceForPath(pathname).key).toBe(workspace);
    });

    it('falls back to Delivery for an unmatched path', () => {
        expect(getWorkspaceForPath('/missing').key).toBe('delivery');
    });

    it('links every registry destination with its registry label and icon', () => {
        const items = WORKSPACES.flatMap(workspace => workspace.items);
        for (const destination of DESTINATIONS) {
            expect(items.filter(item => item.to === destination.path), destination.path).toEqual([{
                to: destination.path,
                labelKey: destination.labelKey,
                defaultLabel: destination.defaultLabel,
                icon: destination.icon,
            }]);
        }
    });
});
