import { beforeEach, expect, it, vi } from 'vitest';
import api from './api';
import { planningInputService } from './planningInputService';

vi.mock('./api', () => ({ default: { get: vi.fn() } }));
beforeEach(() => vi.clearAllMocks());

it('returns the resource and complete revisions from one initial observation', async () => {
    const observed = { kind: 'calendar', resource_id: 7, resource: { id: 7, name: 'Working calendar' }, expected_revisions: { 12: 4 }, complete: true };
    vi.mocked(api.get).mockResolvedValueOnce({ data: observed });
    const draft = await planningInputService.readInitial<{ name: string }>('calendar', 7);
    expect(draft).toEqual(observed);
    expect(api.get).toHaveBeenCalledExactlyOnceWith('/tasks/planning-inputs/calendar/7/context', { params: { creating_member: false } });
    expect(draft.expected_revisions).toEqual({ 12: 4 });
});

it('observes the target iteration before a new allocation draft and propagates incomplete-scope failures', async () => {
    vi.mocked(api.get).mockRejectedValueOnce({ response: { status: 403 } });
    await expect(planningInputService.readInitial('member', 9, true)).rejects.toEqual({ response: { status: 403 } });
    expect(api.get).toHaveBeenCalledExactlyOnceWith('/tasks/planning-inputs/member/9/context', { params: { creating_member: true } });
});


it.each([
    { complete: false }, { resource_id: 8 }, { expected_revisions: { 1: 0 } },
    { expected_revisions: { 1: true } }, { expected_revisions: { '-1': 4 } }, { resource: { id: 8 } },
])('rejects malformed or partial observations before opening a draft: %j', async invalid => {
    vi.mocked(api.get).mockResolvedValueOnce({ data: { kind: 'calendar', resource_id: 7, resource: { id: 7 }, complete: true, expected_revisions: {}, ...invalid } });
    await expect(planningInputService.readInitial('calendar', 7)).rejects.toThrow(/initial planning/i);
});
