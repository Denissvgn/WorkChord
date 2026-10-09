import { expect, it, vi } from 'vitest';
import api from './api';
import { taskService } from './taskService';
vi.mock('./api', () => ({ default: { post: vi.fn().mockResolvedValue({ data: {} }), delete: vi.fn().mockResolvedValue({ data: {} }) } }));
it('sends the caller-observed task version for both dependency directions', async () => {
    await taskService.addDependency(4, 8, 3);
    expect(api.post).toHaveBeenCalledWith('/tasks/4/dependencies', { depends_on_id: 8, expected_version: 3 });
    await taskService.removeDependency(4, 8, 3);
    expect(api.delete).toHaveBeenCalledWith('/tasks/4/dependencies/8', { params: { expected_version: 3 } });
});
