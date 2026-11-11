import { expect, it } from 'vitest';
import { canTransition } from './taskTransitions';

it('allows only the direct moves the server allows, so Undo is offered only where it can work', () => {
    expect(canTransition('planned', 'active')).toBe(true);
    expect(canTransition('active', 'planned')).toBe(false);
    expect(canTransition('resolved', 'active')).toBe(true);
    expect(canTransition('closed', 'resolved')).toBe(false);
});
