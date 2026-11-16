import { describe, expect, it } from 'vitest';
import i18n, { ensureLanguageResources } from './i18n';

describe('Plan work count wording', () => {
    it.each([
        { count: 0, task: 'tasks', day: 'days' },
        { count: 1, task: 'task', day: 'day' },
        { count: 2, task: 'tasks', day: 'days' },
        { count: 5, task: 'tasks', day: 'days' },
    ])('uses grammatical English for $count tasks and days', ({ count, task, day }) => {
        const expected = {
            total: `${count} ${task} · 8 h total effort`,
            taskCount: `${count} ${task}`,
            addSelected: `Add ${count} ${task}`,
            addFailed: `${count} ${task} added. The remaining selections were not added.`,
            needsAssignee: `Needs an assignee · ${count}`,
            needsEffort: `Needs effort · ${count}`,
            assign: `Assign ${count} ${task}`,
            assigned: `${count} ${task} assigned.`,
            assignFailed: `${count} ${task} assigned. Assignment stopped; review the remaining tasks before retrying.`,
            days: `${count} ${day} at 8 h/day`,
        };
        for (const [key, text] of Object.entries(expected)) {
            expect(i18n.t(`planWork.${key}`, { lng: 'en', count, days: count, hours: 8 })).toBe(text);
        }
    });

    it.each([
        { count: 0, task: 'задач', object: 'задач', added: 'Добавлено', assigned: 'Назначено', day: 'дней' },
        { count: 1, task: 'задача', object: 'задачу', added: 'Добавлена', assigned: 'Назначена', day: 'день' },
        { count: 2, task: 'задачи', object: 'задачи', added: 'Добавлены', assigned: 'Назначены', day: 'дня' },
        { count: 5, task: 'задач', object: 'задач', added: 'Добавлено', assigned: 'Назначено', day: 'дней' },
    ])('uses grammatical Russian for $count tasks and days', async ({ count, task, object, added, assigned, day }) => {
        await ensureLanguageResources('ru');
        const expected = {
            total: `${count} ${task} · 8 ч общих трудозатрат`,
            taskCount: `${count} ${task}`,
            addSelected: `Добавить ${count} ${object}`,
            addFailed: `${added} ${count} ${task}. Остальные выбранные задачи не добавлены.`,
            needsAssignee: `Нужен исполнитель · ${count}`,
            needsEffort: `Нужны трудозатраты · ${count}`,
            assign: `Назначить ${count} ${object}`,
            assigned: `${assigned} ${count} ${task}.`,
            assignFailed: `${assigned} ${count} ${task}. Назначение остановлено; проверьте оставшиеся задачи перед повтором.`,
            days: `${count} ${day} при 8 ч/день`,
        };
        for (const [key, text] of Object.entries(expected)) {
            expect(i18n.t(`planWork.${key}`, { lng: 'ru', count, days: count, hours: 8 })).toBe(text);
        }
    });

    it('uses the fractional day form with a localized decimal', async () => {
        await ensureLanguageResources('ru');
        expect(i18n.t('planWork.days', { lng: 'ru', count: 1.5, days: '1,5', hours: 8 })).toBe('1,5 дня при 8 ч/день');
        expect(i18n.t('planWork.days', { lng: 'en', count: 1.5, days: '1.5', hours: 8 })).toBe('1.5 days at 8 h/day');
    });
});
