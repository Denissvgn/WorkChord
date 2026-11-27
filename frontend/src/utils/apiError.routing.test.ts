import { describe, expect, it } from 'vitest';
import { changeAppLanguage } from '../i18n/i18n';
import { getApiErrorMessage } from './apiError';

const refusal = { response: { status: 409, data: { detail: {
    code: 'routing_inconsistent', message: 'The task\'s routing conflicts with its assignee.',
    routing_check: { issues: [{ code: 'reviewer_shares_assignee_publisher', severity: 'conflict', message: 'Same publisher.' }, { code: 'reviewer_missing', severity: 'warning', message: 'No reviewer.' }] },
} } } };

describe('a refused reviewer conflict', () => {
    it.each([
        ['en', /same publisher as the new assignee.*Reassign to.*Routing section/],
        ['ru', /того же издателя.*Маршрутизация.*Переназначить на/],
    ])('is worded in %s with the conflict and where to resolve it', async (language, pattern) => {
        await changeAppLanguage(language);
        try {
            const message = getApiErrorMessage(refusal, 'fallback');
            expect(message).toMatch(pattern);
            expect(message).not.toContain('The task\'s routing conflicts');
            expect(message).not.toMatch(/No reviewer|не указан ревьюер/);
        } finally {
            await changeAppLanguage('en');
        }
    });
});
