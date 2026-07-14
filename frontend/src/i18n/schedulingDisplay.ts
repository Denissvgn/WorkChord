import i18n from './i18n';
import type { EffortModifier, SchedulingPass, SortCriterion } from '../types/schedulingRules';

const defaultEffortModifiers = [
    {
        key: 'professionalism',
        id: 'professionalism',
        formula: 'effort / assignee.professionalism_coefficient',
        operation: null,
        fallback: 'effort',
        min_value: null,
    },
    {
        key: 'operationalOverhead',
        id: 'operational_overhead',
        formula: 'effort / (1 - assignee.operational_utilization / 100)',
        operation: null,
        fallback: 'effort',
        min_value: null,
    },
    {
        key: 'roundUp',
        id: 'round_up',
        formula: null,
        operation: 'ceil',
        fallback: 'effort',
        min_value: 1,
    },
] as const;

const defaultSchedulingPasses = [
    {
        key: 'criticalDeadline',
        id: 'critical_deadline',
        description: '\u0417\u0430\u0434\u0430\u0447\u0438 \u0441 \u0434\u0435\u0434\u043b\u0430\u0439\u043d\u043e\u043c \u2014 \u0431\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0439 \u0441\u0440\u043e\u043a \u0440\u0430\u043d\u044c\u0448\u0435',
        filter: ['task.max_finish_date != null', 'task.is_deferred == false'],
        sort: [
            { field: 'max_finish_date', order: 'asc' },
            { field: 'priority', order: 'asc' },
        ],
    },
    {
        key: 'beforeVacation',
        id: 'before_vacation',
        description: '\u0417\u0430\u0434\u0430\u0447\u0438 \u0434\u043e \u043e\u0442\u043f\u0443\u0441\u043a\u0430',
        filter: ['task.fits_before_vacation == true', 'task.is_deferred == false'],
        sort: [
            { field: 'is_optional', order: 'asc' },
            { field: 'priority', order: 'asc' },
            { field: 'adjusted_effort', order: 'asc' },
        ],
    },
    {
        key: 'afterVacation',
        id: 'after_vacation',
        description: '\u0417\u0430\u0434\u0430\u0447\u0438 \u043f\u043e\u0441\u043b\u0435 \u043e\u0442\u043f\u0443\u0441\u043a\u0430',
        filter: ['task.fits_before_vacation == false', 'task.is_deferred == false'],
        sort: [
            { field: 'is_optional', order: 'asc' },
            { field: 'priority', order: 'asc' },
            { field: 'adjusted_effort', order: 'desc' },
        ],
    },
] as const;

const nullableTextMatches = (
    value: string | null | undefined,
    expected: string | null,
) => (value ?? null) === expected;

const nullableNumberMatches = (
    value: number | null | undefined,
    expected: number | null,
) => (value ?? null) === expected;

const sortMatches = (
    actual: SortCriterion[],
    expected: readonly { field: string; order: 'asc' | 'desc' }[],
) => (
    actual.length === expected.length &&
    actual.every((item, index) => (
        item.field === expected[index].field && item.order === expected[index].order
    ))
);

const filterMatches = (actual: string[], expected: readonly string[]) => (
    actual.length === expected.length &&
    actual.every((item, index) => item === expected[index])
);

const displayText = (key: string, fallback: string) => (
    i18n.t(key, { defaultValue: fallback })
);

export const effortModifierDisplay = (modifier: EffortModifier) => {
    const baseline = defaultEffortModifiers.find(candidate => (
        modifier.id === candidate.id &&
        nullableTextMatches(modifier.formula, candidate.formula) &&
        nullableTextMatches(modifier.operation, candidate.operation) &&
        modifier.fallback === candidate.fallback &&
        nullableNumberMatches(modifier.min_value, candidate.min_value)
    ));

    if (!baseline) {
        return {
            name: modifier.id,
            technicalId: modifier.id,
            isBuiltIn: false,
        };
    }

    return {
        name: displayText(
            `settingsScheduling.defaults.effortModifiers.${baseline.key}.name`,
            modifier.id,
        ),
        technicalId: modifier.id,
        isBuiltIn: true,
    };
};

export const schedulingPassDisplay = (pass: SchedulingPass) => {
    const baseline = defaultSchedulingPasses.find(candidate => (
        pass.id === candidate.id &&
        pass.description === candidate.description &&
        filterMatches(pass.filter.all, candidate.filter) &&
        sortMatches(pass.sort, candidate.sort)
    ));

    if (!baseline) {
        return {
            name: pass.id,
            description: pass.description,
            technicalId: pass.id,
            isBuiltIn: false,
        };
    }

    return {
        name: displayText(
            `settingsScheduling.defaults.schedulingPasses.${baseline.key}.name`,
            pass.id,
        ),
        description: displayText(
            `settingsScheduling.defaults.schedulingPasses.${baseline.key}.description`,
            pass.description,
        ),
        technicalId: pass.id,
        isBuiltIn: true,
    };
};
