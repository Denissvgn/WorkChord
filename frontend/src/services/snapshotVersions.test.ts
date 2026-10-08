import { expect, it, vi } from 'vitest';
import api from './api';
import { snapshotService } from './snapshotService';
vi.mock('./api', () => ({ default: { post: vi.fn().mockResolvedValue({ data: { success: true } }) } }));
it('restores with the confirmation-observed revision without fetching a replacement', async () => {
    await snapshotService.restore(7, 'snapshot_saved.json', 4);
    expect(api.post).toHaveBeenCalledWith('/iterations/7/snapshots/snapshot_saved.json/restore', { confirm: true, expected_revision: 4 });
});
