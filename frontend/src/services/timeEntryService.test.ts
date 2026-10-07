import { beforeEach, expect, it, vi } from 'vitest';
import { timeEntryService } from './timeEntryService';
const api = vi.hoisted(() => ({ get: vi.fn() }));
vi.mock('./api', () => ({ default: api }));
beforeEach(() => api.get.mockReset());
it('rejects mismatched scope, changed insertion bounds and unordered entry pages', async () => {
    const page = { items: [{ id: 4, project_id: 1, task_id: 2, version: 1 }], has_more: false, next_after_id: null, upper_id: 4 };
    api.get.mockResolvedValue({ data: page });
    await expect(timeEntryService.list({ project_id: 1 })).resolves.toEqual(page);
    await expect(timeEntryService.list({ project_id: 2 })).rejects.toThrow('scope');
    await expect(timeEntryService.list({ project_id: 1 }, 0, 3)).rejects.toThrow('bounded');
    api.get.mockResolvedValue({ data: { ...page, items: [page.items[0], page.items[0]] } });
    await expect(timeEntryService.list({ project_id: 1 })).rejects.toThrow('scope');
});
it('rejects history pages that repeat a version or omit a continuation cursor', async () => {
    api.get.mockResolvedValue({ data: { items: [{ version: 2 }], has_more: true, next_after_version: null } });
    await expect(timeEntryService.history(1, 1)).rejects.toThrow('history');
    api.get.mockResolvedValue({ data: { items: [{ version: 1 }], has_more: false, next_after_version: null } });
    await expect(timeEntryService.history(1, 1)).rejects.toThrow('history');
});
