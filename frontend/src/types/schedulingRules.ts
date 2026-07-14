/**
 * Scheduling Rules Types
 * Mirrors backend SchedulingRulesSchema structure
 */

export interface SortCriterion {
    field: string;
    order: 'asc' | 'desc';
}

export interface FilterConfig {
    all: string[];
}

export interface SchedulingPass {
    id: string;
    description: string;
    enabled: boolean;
    filter: FilterConfig;
    sort: SortCriterion[];
}

export interface EffortModifier {
    id: string;
    enabled: boolean;
    formula?: string | null;
    operation?: 'ceil' | 'floor' | 'round' | null;
    fallback: string;
    min_value?: number | null;
}

export interface BalanceWorkload {
    enabled: boolean;
    max_overload_percent: number;
}

export interface Constraints {
    sequential_per_assignee: boolean;
    respect_dependencies: boolean;
    min_start_date: boolean;
    max_finish_date: boolean;
    prefer_uninterrupted: boolean;
    balance_workload?: BalanceWorkload | null;
}

export interface SchedulingRules {
    schema_version: string;
    effort_modifiers: EffortModifier[];
    scheduling_passes: SchedulingPass[];
    constraints: Constraints;
}

export interface SchedulingRulesResponse {
    rules: SchedulingRules;
    source: 'yaml' | 'database' | 'defaults';
}

// Available fields for form dropdowns
export const TASK_FIELDS = [
    { value: 'priority', labelKey: 'settingsScheduling.options.taskFields.priority' },
    { value: 'effort_days', labelKey: 'settingsScheduling.options.taskFields.effortDays' },
    { value: 'adjusted_effort', labelKey: 'settingsScheduling.options.taskFields.adjustedEffort' },
    { value: 'is_optional', labelKey: 'settingsScheduling.options.taskFields.isOptional' },
    { value: 'is_deferred', labelKey: 'settingsScheduling.options.taskFields.isDeferred' },
    { value: 'max_finish_date', labelKey: 'settingsScheduling.options.taskFields.maxFinishDate' },
    { value: 'min_start_date', labelKey: 'settingsScheduling.options.taskFields.minStartDate' },
    { value: 'fits_before_vacation', labelKey: 'settingsScheduling.options.taskFields.fitsBeforeVacation' },
] as const;

export const ASSIGNEE_FIELDS = [
    { value: 'assignee.professionalism_coefficient', labelKey: 'settingsScheduling.options.assigneeFields.professionalismCoefficient' },
    { value: 'assignee.operational_utilization', labelKey: 'settingsScheduling.options.assigneeFields.operationalUtilization' },
    { value: 'assignee.days_before_vacation', labelKey: 'settingsScheduling.options.assigneeFields.daysBeforeVacation' },
] as const;

export const OPERATORS = [
    { value: '==', labelKey: 'settingsScheduling.options.operators.equals' },
    { value: '!=', labelKey: 'settingsScheduling.options.operators.notEquals' },
    { value: '<', labelKey: 'settingsScheduling.options.operators.lessThan' },
    { value: '<=', labelKey: 'settingsScheduling.options.operators.lessOrEqual' },
    { value: '>', labelKey: 'settingsScheduling.options.operators.greaterThan' },
    { value: '>=', labelKey: 'settingsScheduling.options.operators.greaterOrEqual' },
] as const;

export const MATH_OPERATIONS = [
    { value: 'ceil', labelKey: 'settingsScheduling.options.mathOperations.ceil' },
    { value: 'floor', labelKey: 'settingsScheduling.options.mathOperations.floor' },
    { value: 'round', labelKey: 'settingsScheduling.options.mathOperations.round' },
] as const;

// Fields available for filter conditions (with task. prefix for clarity)
export const FILTER_FIELDS = [
    { value: 'task.max_finish_date', labelKey: 'settingsScheduling.options.filterFields.maxFinishDate' },
    { value: 'task.min_start_date', labelKey: 'settingsScheduling.options.filterFields.minStartDate' },
    { value: 'task.is_deferred', labelKey: 'settingsScheduling.options.filterFields.isDeferred' },
    { value: 'task.is_optional', labelKey: 'settingsScheduling.options.filterFields.isOptional' },
    { value: 'task.fits_before_vacation', labelKey: 'settingsScheduling.options.filterFields.fitsBeforeVacation' },
    { value: 'task.priority', labelKey: 'settingsScheduling.options.filterFields.priority' },
    { value: 'task.effort_days', labelKey: 'settingsScheduling.options.filterFields.effortDays' },
    { value: 'task.adjusted_effort', labelKey: 'settingsScheduling.options.filterFields.adjustedEffort' },
    { value: 'task.status', labelKey: 'settingsScheduling.options.filterFields.status' },
] as const;

// Common values for filter comparisons
export const FILTER_VALUES = [
    { value: 'null', labelKey: 'settingsScheduling.options.filterValues.empty' },
    { value: 'true', labelKey: 'settingsScheduling.options.filterValues.true' },
    { value: 'false', labelKey: 'settingsScheduling.options.filterValues.false' },
] as const;

// Formula templates for effort modifiers
export const FORMULA_TEMPLATES = [
    {
        id: 'divide_by_field',
        labelKey: 'settingsScheduling.options.formulaTemplates.divideByField',
        helpKey: 'settingsScheduling.help.modifiers.formulaTemplates.divideByField',
        build: (field: string) => `effort / assignee.${field}`,
        match: /^effort\s*\/\s*assignee\.(\w+)$/,
    },
    {
        id: 'inverse_percentage',
        labelKey: 'settingsScheduling.options.formulaTemplates.inversePercentage',
        helpKey: 'settingsScheduling.help.modifiers.formulaTemplates.inversePercentage',
        build: (field: string, divisor: number = 100) => `effort / (1 - assignee.${field} / ${divisor})`,
        match: /^effort\s*\/\s*\(1\s*-\s*assignee\.(\w+)\s*\/\s*(\d+)\)$/,
    },
    {
        id: 'multiply',
        labelKey: 'settingsScheduling.options.formulaTemplates.multiply',
        helpKey: 'settingsScheduling.help.modifiers.formulaTemplates.multiply',
        build: (_: string, multiplier: number = 1) => `effort * ${multiplier}`,
        match: /^effort\s*\*\s*([\d.]+)$/,
    },
    {
        id: 'divide_constant',
        labelKey: 'settingsScheduling.options.formulaTemplates.divideConstant',
        helpKey: 'settingsScheduling.help.modifiers.formulaTemplates.divideConstant',
        build: (_: string, divisor: number = 1) => `effort / ${divisor}`,
        match: /^effort\s*\/\s*([\d.]+)$/,
    },
    {
        id: 'add_buffer',
        labelKey: 'settingsScheduling.options.formulaTemplates.addBuffer',
        helpKey: 'settingsScheduling.help.modifiers.formulaTemplates.addBuffer',
        build: (_: string, buffer: number = 1) => `effort + ${buffer}`,
        match: /^effort\s*\+\s*([\d.]+)$/,
    },
    {
        id: 'custom',
        labelKey: 'settingsScheduling.options.formulaTemplates.custom',
        helpKey: 'settingsScheduling.help.modifiers.type',
        build: () => 'effort',
        match: null,
    },
] as const;

// Assignee fields available for formulas
export const FORMULA_ASSIGNEE_FIELDS = [
    { value: 'professionalism_coefficient', labelKey: 'settingsScheduling.options.formulaAssigneeFields.professionalismCoefficient' },
    { value: 'operational_utilization', labelKey: 'settingsScheduling.options.formulaAssigneeFields.operationalUtilization' },
    { value: 'days_before_vacation', labelKey: 'settingsScheduling.options.formulaAssigneeFields.daysBeforeVacation' },
    { value: 'experience_years', labelKey: 'settingsScheduling.options.formulaAssigneeFields.experienceYears' },
] as const;
