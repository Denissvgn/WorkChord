import { expect, it } from 'vitest';
import { removeTaskDraft } from './taskDraftStorage';

it('discards scoped time drafts with the parent while retaining unrelated drafts', () => {
    sessionStorage.clear();
    for (const key of ['editor', 'editor:time', 'editor:time:[1,2,42]', 'editor:time:[1,2,43]', 'other:time:[1,2,42]']) {
        sessionStorage.setItem(key, 'draft');
    }
    removeTaskDraft('editor', true);
    expect(Object.keys(sessionStorage)).toEqual(['other:time:[1,2,42]']);
});
