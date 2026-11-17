import { describe, expect, it } from 'vitest';
import i18n, { changeAppLanguage } from './i18n';
import { englishResources } from './resources.en';
import { russianResources } from './resources.ru';

const getCatalogValue = (
    catalog: Record<string, unknown>,
    key: string,
): unknown => key.split('.').reduce<unknown>((value, segment) => (
    value && typeof value === 'object'
        ? (value as Record<string, unknown>)[segment]
        : undefined
), catalog);

const placeholders = (value: string) => Array.from(
    value.matchAll(/{{\s*([^},\s]+)[^}]*}}/g),
    match => match[1],
).sort();

const agentStepIds = [
    'authority',
    'master',
    'controller',
    'workers',
    'bindings',
    'verifier',
    'review',
];

const dynamicMasterKeys = [
    ...agentStepIds.flatMap(id => [
        `agentTeamSetup.steps.${id}.title`,
        `agentTeamSetup.steps.${id}.description`,
        `agentTeamSetup.steps.${id}.action`,
    ]),
    ...['done', 'warn', 'blocked', 'todo'].map(
        state => `agentTeamSetup.stepStates.${state}`,
    ),
    ...[
        'createMember',
        'adoptMember',
        'updateMember',
        'noChange',
        'disableMember',
        'replaceMember',
        'blocked',
        'unmanaged',
    ].map(operation => `agentTeamSetup.operations.${operation}`),
    ...[
        'create',
        'safeUpdate',
        'noChange',
        'blockedConflict',
        'requiresReplacement',
        'proposeDisable',
        'unmanaged',
    ].map(kind => `agentTeamSetup.reconciliationClasses.${kind}`),
    ...['completed', 'partial', 'blocked'].map(
        status => `agentTeamSetup.applyStatuses.${status}`,
    ),
    ...['pending', 'applied', 'noChange', 'blocked'].map(
        status => `agentTeamSetup.actionStatuses.${status}`,
    ),
    'agentTeamSetup.actionHeadingFor',
    'agentTeamSetup.applyActionFor',
    'agentTeamSetup.checksComplete',
    'agentTeamSetup.confirmActionFor',
    'agentTeamSetup.currentCheckNamed',
    'agentTeamSetup.handoffFor',
    'agentTeamSetup.railProgress',
    'agentTeamSetup.readinessTitle',
    'agentTeamSetup.summaryProgress',
];

describe('lazy language resources', () => {
    it('loads the Russian catalog only when that language is selected', async () => {
        expect(i18n.hasResourceBundle('ru', 'translation')).toBe(false);

        await changeAppLanguage('ru');

        expect(i18n.hasResourceBundle('ru', 'translation')).toBe(true);
        expect(i18n.t('common.loading')).toBe('Загрузка…');
    });

    it('keeps dynamic workflow catalogs complete with matching placeholders', () => {
        const english = englishResources.translation as Record<string, unknown>;
        const russian = russianResources.translation as Record<string, unknown>;

        for (const key of dynamicMasterKeys) {
            const englishValue = getCatalogValue(english, key);
            const russianValue = getCatalogValue(russian, key);
            expect(englishValue, `missing English ${key}`).toEqual(expect.any(String));
            expect(russianValue, `missing Russian ${key}`).toEqual(expect.any(String));
            expect(placeholders(russianValue as string), `placeholder mismatch for ${key}`)
                .toEqual(placeholders(englishValue as string));
        }

        for (const [summaryKey, railKey] of [
            ['agentTeamSetup.summaryProgress', 'agentTeamSetup.railProgress'],
        ]) {
            expect(getCatalogValue(english, summaryKey))
                .not.toBe(getCatalogValue(english, railKey));
            expect(getCatalogValue(russian, summaryKey))
                .not.toBe(getCatalogValue(russian, railKey));
        }

        expect(getCatalogValue(english, 'agentTeamSetup.readinessTitle'))
            .toBe('Agent setup readiness');
        expect(getCatalogValue(english, 'agentTeamSetup.checksComplete'))
            .toBe('{{done}} of {{total}} setup checks complete');
        expect(getCatalogValue(russian, 'agentTeamSetup.readinessTitle'))
            .toBe('Готовность настройки агентов');
    });

    it('uses natural plurals for Overview counts in English and Russian', async () => {
        await changeAppLanguage('en');

        expect(i18n.t('overview.daysLeft', { count: 1 })).toBe('1 day left');
        expect(i18n.t('overview.daysLeft', { count: 2 })).toBe('2 days left');
        expect(i18n.t('overview.attention.overdueTitle', { count: 1 }))
            .toBe('1 overdue task');
        expect(i18n.t('overview.attention.overdueTitle', { count: 2 }))
            .toBe('2 overdue tasks');
        expect(i18n.t('overview.attention.unassignedTitle', { count: 1 }))
            .toBe('1 unassigned task');
        expect(i18n.t('overview.attention.unassignedTitle', { count: 2 }))
            .toBe('2 unassigned tasks');
        expect(i18n.t('overview.attention.intakeTitle', { count: 1 }))
            .toBe('1 request needs triage');
        expect(i18n.t('overview.attention.intakeTitle', { count: 2 }))
            .toBe('2 requests need triage');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 1 }))
            .toBe('Review 1 remaining exception');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 2 }))
            .toBe('Review 2 remaining exceptions');
        expect(i18n.t('overview.tasksShipped', {
            completed: 1,
            total: 1,
            count: 1,
        })).toBe('1 / 1 task implemented');
        expect(i18n.t('overview.focus.deliveryProgressValue', {
            percent: 50,
            completed: 1,
            total: 2,
            count: 2,
        })).toBe('50% implemented — 1 of 2 tasks implemented');
        expect(i18n.t('nav.counters.requestsWaiting', { count: 1 })).toBe('1 request waiting');
        expect(i18n.t('nav.counters.requestsWaiting', { count: 2 })).toBe('2 requests waiting');
        expect(i18n.t('nav.counters.planProgress', { done: 4, total: 6 }))
            .toBe('4 of 6 plan steps complete');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 1 }))
            .toBe('1 reconciliation action is still pending.');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 2 }))
            .toBe('2 reconciliation actions are still pending.');

        await changeAppLanguage('ru');

        expect(i18n.t('overview.daysLeft', { count: 1 })).toBe('Остался 1 день');
        expect(i18n.t('overview.daysLeft', { count: 2 })).toBe('Осталось 2 дня');
        expect(i18n.t('overview.daysLeft', { count: 5 })).toBe('Осталось 5 дней');
        expect(i18n.t('overview.attention.overdueTitle', { count: 1 }))
            .toBe('1 просроченная задача');
        expect(i18n.t('overview.attention.overdueTitle', { count: 2 }))
            .toBe('2 просроченные задачи');
        expect(i18n.t('overview.attention.overdueTitle', { count: 5 }))
            .toBe('5 просроченных задач');
        expect(i18n.t('overview.attention.unassignedTitle', { count: 1 }))
            .toBe('1 задача без исполнителя');
        expect(i18n.t('overview.attention.unassignedTitle', { count: 2 }))
            .toBe('2 задачи без исполнителя');
        expect(i18n.t('overview.attention.unassignedTitle', { count: 5 }))
            .toBe('5 задач без исполнителя');
        expect(i18n.t('overview.attention.intakeTitle', { count: 1 }))
            .toBe('1 входящий элемент требует разбора');
        expect(i18n.t('overview.attention.intakeTitle', { count: 2 }))
            .toBe('2 входящих элемента требуют разбора');
        expect(i18n.t('overview.attention.intakeTitle', { count: 5 }))
            .toBe('5 входящих элементов требуют разбора');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 1 }))
            .toBe('Проверить 1 оставшееся исключение');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 2 }))
            .toBe('Проверить 2 оставшихся исключения');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 5 }))
            .toBe('Проверить 5 оставшихся исключений');
        expect(i18n.t('overview.tasksShipped', {
            completed: 1,
            total: 1,
            count: 1,
        })).toBe('Реализовано 1 из 1 задачи');
        expect(i18n.t('overview.tasksShipped', {
            completed: 1,
            total: 2,
            count: 2,
        })).toBe('Реализовано 1 из 2 задач');
        expect(i18n.t('overview.tasksShipped', {
            completed: 3,
            total: 5,
            count: 5,
        })).toBe('Реализовано 3 из 5 задач');
        expect(i18n.t('overview.tasksShipped', {
            completed: 13,
            total: 21,
            count: 21,
        })).toBe('Реализовано 13 из 21 задачи');
        expect(i18n.t('nav.counters.requestsWaiting', { count: 1 })).toBe('1 запрос ждёт');
        expect(i18n.t('nav.counters.requestsWaiting', { count: 2 })).toBe('2 запроса ждут');
        expect(i18n.t('nav.counters.requestsWaiting', { count: 5 })).toBe('5 запросов ждут');
        expect(i18n.t('nav.counters.requestsWaiting', { count: 21 })).toBe('21 запрос ждёт');
        expect(i18n.t('nav.counters.planProgress', { done: 4, total: 6 }))
            .toBe('Шагов плана выполнено: 4 из 6');
        expect(i18n.t('overview.workNowRemaining', { count: 1 }))
            .toBe('На доске задач доступна ещё 1 открытая задача.');
        expect(i18n.t('overview.workNowRemaining', { count: 2 }))
            .toBe('На доске задач доступны ещё 2 открытые задачи.');
        expect(i18n.t('overview.workNowRemaining', { count: 5 }))
            .toBe('На доске задач доступны ещё 5 открытых задач.');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 1 }))
            .toBe('Осталось 1 действие согласования.');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 2 }))
            .toBe('Осталось 2 действия согласования.');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 5 }))
            .toBe('Осталось 5 действий согласования.');
    });

    it('ensures exhaustive parity and placeholder match across all keys in Russian catalog', () => {
        const flatten = (obj: Record<string, unknown>, prefix = ''): Record<string, string> => {
            const res: Record<string, string> = {};
            for (const [k, v] of Object.entries(obj)) {
                const nextKey = prefix ? `${prefix}.${k}` : k;
                if (v && typeof v === 'object' && !Array.isArray(v)) {
                    Object.assign(res, flatten(v as Record<string, unknown>, nextKey));
                } else if (typeof v === 'string') {
                    res[nextKey] = v;
                }
            }
            return res;
        };

        const en = flatten(englishResources.translation as Record<string, unknown>);
        const ru = flatten(russianResources.translation as Record<string, unknown>);

        const ruBaseKeys = new Set<string>();
        for (const k of Object.keys(ru)) {
            ruBaseKeys.add(k.replace(/_(zero|one|two|few|many|other)$/, ''));
        }

        const missingInRu: string[] = [];
        for (const k of Object.keys(en)) {
            const baseKey = k.replace(/_(zero|one|two|few|many|other)$/, '');
            if (!ru[k] && !ruBaseKeys.has(baseKey)) {
                missingInRu.push(k);
            }
        }
        expect(missingInRu, 'Keys present in English but missing in Russian').toEqual([]);

        const enBaseKeys = new Set<string>();
        for (const k of Object.keys(en)) {
            enBaseKeys.add(k.replace(/_(zero|one|two|few|many|other)$/, ''));
        }

        const missingInEn: string[] = [];
        for (const k of Object.keys(ru)) {
            const baseKey = k.replace(/_(zero|one|two|few|many|other)$/, '');
            if (!en[k] && !enBaseKeys.has(baseKey)) {
                missingInEn.push(k);
            }
        }
        expect(missingInEn, 'Keys present in Russian but missing in English').toEqual([]);

        const placeholderMismatches: Array<{ key: string; enPh: string[]; ruPh: string[] }> = [];
        for (const [k, valEn] of Object.entries(en)) {
            const valRu = ru[k] || ru[`${k}_other`] || ru[`${k}_one`];
            if (!valRu) continue;
            const enPh = placeholders(valEn);
            const ruPh = placeholders(valRu);
            if (enPh.join(',') !== ruPh.join(',')) {
                placeholderMismatches.push({ key: k, enPh, ruPh });
            }
        }
        expect(placeholderMismatches, 'Interpolation placeholder mismatches').toEqual([]);
    });
});

