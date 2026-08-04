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
    ...['done', 'needsAttention', 'blocked', 'notStarted', 'loadingStatus', 'unavailableStatus']
        .map(state => `plan.master.${state}`),
    'agentTeamSetup.actionHeadingFor',
    'agentTeamSetup.applyActionFor',
    'agentTeamSetup.checksComplete',
    'agentTeamSetup.confirmActionFor',
    'agentTeamSetup.currentCheckNamed',
    'agentTeamSetup.handoffFor',
    'agentTeamSetup.railProgress',
    'agentTeamSetup.readinessTitle',
    'agentTeamSetup.summaryProgress',
    'plan.master.checkpointOption',
    'plan.master.checkpointsComplete',
    'plan.master.railProgress',
    'plan.master.summaryProgress',
];

describe('lazy language resources', () => {
    it('loads the Russian catalog only when that language is selected', async () => {
        expect(i18n.hasResourceBundle('ru', 'translation')).toBe(false);

        await changeAppLanguage('ru');

        expect(i18n.hasResourceBundle('ru', 'translation')).toBe(true);
        expect(i18n.t('common.loading')).toBe('Загрузка...');
    });

    it('keeps dynamic master catalogs complete with matching placeholders', () => {
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
            ['plan.master.summaryProgress', 'plan.master.railProgress'],
        ]) {
            expect(getCatalogValue(english, summaryKey))
                .not.toBe(getCatalogValue(english, railKey));
            expect(getCatalogValue(russian, summaryKey))
                .not.toBe(getCatalogValue(russian, railKey));
        }

        expect(getCatalogValue(english, 'plan.master.checkpoints'))
            .toBe('Planning checkpoints');
        expect(getCatalogValue(english, 'plan.master.checkpointsComplete'))
            .toBe('{{done}} of {{total}} checkpoints complete');
        expect(getCatalogValue(english, 'agentTeamSetup.readinessTitle'))
            .toBe('Agent setup readiness');
        expect(getCatalogValue(english, 'agentTeamSetup.checksComplete'))
            .toBe('{{done}} of {{total}} setup checks complete');
        expect(getCatalogValue(russian, 'plan.master.checkpoints'))
            .toBe('Контрольные точки планирования');
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
            .toBe('1 intake item needs triage');
        expect(i18n.t('overview.attention.intakeTitle', { count: 2 }))
            .toBe('2 intake items need triage');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 1 }))
            .toBe('Review 1 remaining exception');
        expect(i18n.t('overview.focus.reviewRemainingExceptions', { count: 2 }))
            .toBe('Review 2 remaining exceptions');
        expect(i18n.t('overview.tasksShipped', {
            completed: 1,
            total: 1,
            count: 1,
        })).toBe('1 / 1 task complete');
        expect(i18n.t('overview.focus.deliveryProgressValue', {
            percent: 50,
            completed: 1,
            total: 2,
            count: 2,
        })).toBe('50% complete — 1 of 2 tasks complete');
        expect(i18n.t('nav.deliveryAttentionIntake', { count: 1 }))
            .toBe('Delivery Hub needs attention: 1 intake item awaits triage. Open Triage.');
        expect(i18n.t('nav.deliveryAttentionIntake', { count: 2 }))
            .toBe('Delivery Hub needs attention: 2 intake items await triage. Open Triage.');
        expect(i18n.t('nav.planningAttention', { count: 1 }))
            .toBe('Timeline & Planning needs attention: 1 Plan Work checkpoint remains.');
        expect(i18n.t('nav.planningAttention', { count: 5 }))
            .toBe('Timeline & Planning needs attention: 5 Plan Work checkpoints remain.');
        expect(i18n.t('plan.master.daysCount', { count: 1 })).toBe('1 day');
        expect(i18n.t('plan.master.daysCount', { count: 2 })).toBe('2 days');
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
        })).toBe('Завершено 1 из 1 задачи');
        expect(i18n.t('overview.tasksShipped', {
            completed: 1,
            total: 2,
            count: 2,
        })).toBe('Завершено 1 из 2 задач');
        expect(i18n.t('overview.tasksShipped', {
            completed: 3,
            total: 5,
            count: 5,
        })).toBe('Завершено 3 из 5 задач');
        expect(i18n.t('overview.tasksShipped', {
            completed: 13,
            total: 21,
            count: 21,
        })).toBe('Завершено 13 из 21 задачи');
        expect(i18n.t('nav.deliveryAttentionIntake', { count: 1 }))
            .toBe('Центр поставки требует внимания: 1 входящий элемент ожидает разбора. Откройте триаж.');
        expect(i18n.t('nav.deliveryAttentionIntake', { count: 2 }))
            .toBe('Центр поставки требует внимания: 2 входящих элемента ожидают разбора. Откройте триаж.');
        expect(i18n.t('nav.deliveryAttentionIntake', { count: 5 }))
            .toBe('Центр поставки требует внимания: 5 входящих элементов ожидают разбора. Откройте триаж.');
        expect(i18n.t('nav.planningAttention', { count: 1 }))
            .toBe('Таймлайн и планирование требуют внимания: осталась 1 контрольная точка планирования работы.');
        expect(i18n.t('nav.planningAttention', { count: 2 }))
            .toBe('Таймлайн и планирование требуют внимания: остались 2 контрольные точки планирования работы.');
        expect(i18n.t('nav.planningAttention', { count: 5 }))
            .toBe('Таймлайн и планирование требуют внимания: осталось 5 контрольных точек планирования работы.');
        expect(i18n.t('overview.workNowRemaining', { count: 1 }))
            .toBe('На доске задач доступна ещё 1 открытая задача.');
        expect(i18n.t('overview.workNowRemaining', { count: 2 }))
            .toBe('На доске задач доступны ещё 2 открытые задачи.');
        expect(i18n.t('overview.workNowRemaining', { count: 5 }))
            .toBe('На доске задач доступны ещё 5 открытых задач.');
        expect(i18n.t('plan.master.daysCount', { count: 1 })).toBe('1 день');
        expect(i18n.t('plan.master.daysCount', { count: 2 })).toBe('2 дня');
        expect(i18n.t('plan.master.daysCount', { count: 5 })).toBe('5 дней');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 1 }))
            .toBe('Осталось 1 действие согласования.');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 2 }))
            .toBe('Осталось 2 действия согласования.');
        expect(i18n.t('agentTeamSetup.pendingReconciliationActions', { count: 5 }))
            .toBe('Осталось 5 действий согласования.');
    });
});
