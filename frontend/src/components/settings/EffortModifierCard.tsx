import { useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { Trash2, ChevronDown, ChevronRight, Info } from 'lucide-react';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import type { EffortModifier } from '../../types/schedulingRules';
import { MATH_OPERATIONS, FORMULA_TEMPLATES, FORMULA_ASSIGNEE_FIELDS } from '../../types/schedulingRules';
import { effortModifierDisplay } from '../../i18n/schedulingDisplay';

interface Props {
    modifier: EffortModifier;
    onChange: (modifier: EffortModifier) => void;
    onRemove: () => void;
}

// Parse formula to identify template and extract values
function parseFormula(formula: string | null | undefined): {
    templateId: string;
    field: string;
    constant: number;
} {
    if (!formula) {
        return { templateId: 'custom', field: 'professionalism_coefficient', constant: 100 };
    }

    // Try each template's pattern
    for (const template of FORMULA_TEMPLATES) {
        if (template.match) {
            const match = formula.match(template.match);
            if (match) {
                return {
                    templateId: template.id,
                    field: match[1] || 'professionalism_coefficient',
                    constant: parseFloat(match[2] || match[1]) || 100,
                };
            }
        }
    }

    return { templateId: 'custom', field: 'professionalism_coefficient', constant: 100 };
}

export const EffortModifierCard = ({ modifier, onChange, onRemove }: Props) => {
    const { t } = useTranslation();
    const [expanded, setExpanded] = useState(false);

    // Parse current formula to identify template
    const parsedFormula = useMemo(() => parseFormula(modifier.formula), [modifier.formula]);
    const display = effortModifierDisplay(modifier);
    const [selectedField, setSelectedField] = useState(parsedFormula.field);
    const [constantValue, setConstantValue] = useState(parsedFormula.constant);

    const handleToggleEnabled = (enabled: boolean) => {
        onChange({ ...modifier, enabled });
    };

    const handleOperationChange = (operation: string) => {
        onChange({
            ...modifier,
            operation: operation as 'ceil' | 'floor' | 'round' | null,
            formula: operation ? null : modifier.formula, // Clear formula if operation is set
        });
    };

    const handleFallbackChange = (fallback: string) => {
        onChange({ ...modifier, fallback });
    };

    const handleMinValueChange = (value: string) => {
        const numValue = value ? parseFloat(value) : null;
        onChange({ ...modifier, min_value: numValue });
    };

    // Template-based formula construction
    const handleTemplateChange = (templateId: string) => {
        const template = FORMULA_TEMPLATES.find(t => t.id === templateId);
        if (!template) return;

        if (templateId === 'custom') {
            // Keep current formula when switching to custom
            return;
        }

        const newFormula = template.build(selectedField, constantValue);
        onChange({ ...modifier, formula: newFormula });
    };

    const handleFieldChange = (field: string) => {
        setSelectedField(field);
        const template = FORMULA_TEMPLATES.find(t => t.id === parsedFormula.templateId);
        if (template && template.id !== 'custom') {
            const newFormula = template.build(field, constantValue);
            onChange({ ...modifier, formula: newFormula });
        }
    };

    const handleConstantChange = (value: number) => {
        setConstantValue(value);
        const template = FORMULA_TEMPLATES.find(t => t.id === parsedFormula.templateId);
        if (template && template.id !== 'custom') {
            const newFormula = template.build(selectedField, value);
            onChange({ ...modifier, formula: newFormula });
        }
    };

    const handleCustomFormulaChange = (formula: string) => {
        onChange({ ...modifier, formula: formula || null });
    };

    // Check if current template needs field/constant inputs
    const needsFieldInput = ['divide_by_field', 'inverse_percentage'].includes(parsedFormula.templateId);
    const needsConstantInput = ['inverse_percentage', 'multiply', 'divide_constant', 'add_buffer'].includes(parsedFormula.templateId);
    const selectedTemplate = FORMULA_TEMPLATES.find(template => template.id === parsedFormula.templateId);
    const constantLabelKey = parsedFormula.templateId === 'inverse_percentage'
        ? 'settingsScheduling.fields.divisor'
        : parsedFormula.templateId === 'multiply'
            ? 'settingsScheduling.fields.multiplier'
            : parsedFormula.templateId === 'add_buffer'
                ? 'settingsScheduling.fields.bufferDays'
                : 'settingsScheduling.fields.constant';

    return (
        <div
            className={`
                rounded-lg border bg-surface-card transition-all duration-200
                ${modifier.enabled
                    ? 'border-l-4 border-l-action border-border'
                    : 'border-l-4 border-l-border-strong border-border opacity-75'
                }
            `}
        >
            {/* Header */}
            <div className="flex items-center gap-4 p-4">
                <Checkbox
                    checked={modifier.enabled}
                    onChange={handleToggleEnabled}
                    aria-label={t('settingsScheduling.aria.enableModifier', { id: modifier.id })}
                />

                <button
                    onClick={() => setExpanded(!expanded)}
                    className="flex-1 flex items-center gap-2 text-left"
                >
                    {expanded ? (
                        <ChevronDown className="w-4 h-4 text-content-tertiary" />
                    ) : (
                        <ChevronRight className="w-4 h-4 text-content-tertiary" />
                    )}
                    <span className="min-w-0">
                        <span className="font-medium text-content-primary">{display.name}</span>
                        {display.isBuiltIn && (
                            <code className="ml-2 rounded bg-surface-subtle px-1.5 py-0.5 text-xs text-content-secondary">
                                {display.technicalId}
                            </code>
                        )}
                    </span>
                </button>

                {/* Preview */}
                {!expanded && (
                    <div className="text-sm text-content-secondary font-mono truncate max-w-xs">
                        {modifier.formula || modifier.operation || '—'}
                    </div>
                )}

                <button
                    onClick={onRemove}
                    className="p-1 text-content-tertiary hover:text-feedback-danger-foreground transition-colors"
                    title={t('settingsScheduling.aria.removeModifier')}
                    aria-label={t('settingsScheduling.aria.removeModifier')}
                >
                    <Trash2 className="w-4 h-4" aria-hidden="true" />
                </button>
            </div>

            {/* Expanded Details */}
            {expanded && (
                <div className="px-4 pb-4 pt-2 border-t border-border-subtle space-y-4 animate-in slide-in-from-top-2 duration-200">
                    <div className="grid grid-cols-2 gap-4">
                        <Input
                            label={t('settingsScheduling.fields.id')}
                            value={modifier.id}
                            onChange={(e) => onChange({ ...modifier, id: e.target.value })}
                            placeholder="modifier_id"
                        />
                        <div>
                            <label className="block text-sm font-medium text-content-primary mb-1">
                                {t('settingsScheduling.fields.type')}
                            </label>
                            <select
                                value={modifier.operation ? '_operation_' : parsedFormula.templateId}
                                onChange={(e) => {
                                    if (e.target.value === '_operation_') {
                                        handleOperationChange('ceil');
                                    } else {
                                        handleOperationChange('');
                                        handleTemplateChange(e.target.value);
                                    }
                                }}
                                className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                <optgroup label={t('settingsScheduling.groups.formulaBased')}>
                                    {FORMULA_TEMPLATES.map(template => (
                                        <option key={template.id} value={template.id}>{t(template.labelKey)}</option>
                                    ))}
                                </optgroup>
                                <optgroup label={t('settingsScheduling.groups.mathOperation')}>
                                    <option value="_operation_">{t('settingsScheduling.groups.roundResult')}</option>
                                </optgroup>
                            </select>
                        </div>
                    </div>

                    {/* Show operation dropdown if operation type selected */}
                    {modifier.operation && (
                        <div>
                            <label className="block text-sm font-medium text-content-primary mb-1">
                                {t('settingsScheduling.fields.roundingOperation')}
                            </label>
                            <select
                                value={modifier.operation || 'ceil'}
                                onChange={(e) => handleOperationChange(e.target.value)}
                                className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                {MATH_OPERATIONS.map(op => (
                                    <option key={op.value} value={op.value}>{t(op.labelKey)}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    {/* Formula constructor UI */}
                    {!modifier.operation && (
                        <div className="space-y-3">
                            {/* Field selector for templates that need it */}
                            {needsFieldInput && (
                                <div>
                                    <label className="block text-sm font-medium text-content-primary mb-1">
                                        {t('settingsScheduling.fields.assigneeField')}
                                    </label>
                                    <select
                                        value={selectedField}
                                        onChange={(e) => handleFieldChange(e.target.value)}
                                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                    >
                                        {FORMULA_ASSIGNEE_FIELDS.map(f => (
                                            <option key={f.value} value={f.value}>{t(f.labelKey)}</option>
                                        ))}
                                    </select>
                                </div>
                            )}

                            {/* Constant input for templates that need it */}
                            {needsConstantInput && (
                                <div>
                                    <label className="block text-sm font-medium text-content-primary mb-1">
                                        {t(constantLabelKey)}
                                    </label>
                                    <input
                                        type="number"
                                        value={constantValue}
                                        onChange={(e) => handleConstantChange(parseFloat(e.target.value) || 1)}
                                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                        step="0.1"
                                        min="0"
                                    />
                                </div>
                            )}

                            {/* Custom formula input */}
                            {parsedFormula.templateId === 'custom' && (
                                <div>
                                    <label className="block text-sm font-medium text-content-primary mb-1">
                                        {t('settingsScheduling.fields.customFormula')}
                                    </label>
                                    <input
                                        type="text"
                                        value={modifier.formula || ''}
                                        onChange={(e) => handleCustomFormulaChange(e.target.value)}
                                        placeholder="effort / assignee.professionalism_coefficient"
                                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm font-mono text-sm bg-surface-muted focus:outline-none focus:ring-1 focus:ring-focus"
                                    />
                                    <p className="mt-1 text-xs text-content-secondary">
                                        {t('settingsScheduling.fields.variables')}{' '}
                                        <code>effort</code>, <code>assignee.professionalism_coefficient</code>, <code>assignee.operational_utilization</code>
                                    </p>
                                </div>
                            )}

                            {/* Generated formula preview */}
                            {parsedFormula.templateId !== 'custom' && modifier.formula && (
                                <div className="bg-surface-muted rounded-md p-3">
                                    <p className="text-xs text-content-secondary mb-1">{t('settingsScheduling.fields.generatedFormula')}</p>
                                    <code className="text-sm font-mono text-content-primary">{modifier.formula}</code>
                                </div>
                            )}
                        </div>
                    )}

                    <div className="grid grid-cols-2 gap-4">
                        <Input
                            label={t('settingsScheduling.fields.fallback')}
                            value={modifier.fallback}
                            onChange={(e) => handleFallbackChange(e.target.value)}
                            placeholder="effort"
                        />
                        <Input
                            type="number"
                            label={t('settingsScheduling.fields.minValue')}
                            value={modifier.min_value?.toString() || ''}
                            onChange={(e) => handleMinValueChange(e.target.value)}
                            placeholder={t('settingsScheduling.fields.optional')}
                            min={0}
                        />
                    </div>

                    {/* Contextual Help */}
                    <div className="bg-action-muted border border-action rounded-md p-3 flex gap-3 text-sm text-action-muted-foreground mt-4">
                        <Info className="w-5 h-5 text-action-muted-foreground shrink-0 mt-0.5" />
                        <div>
                            <p className="font-medium mb-1">{t('settingsScheduling.fields.howThisWorks')}</p>
                            <p className="mb-2">
                                {modifier.operation
                                    ? t('settingsScheduling.help.modifiers.rounding')
                                    : t(selectedTemplate?.helpKey || 'settingsScheduling.help.modifiers.type')
                                }
                            </p>
                            <ul className="list-disc list-inside space-y-1 text-xs">
                                <li><strong>{t('settingsScheduling.fields.fallbackLabel')}</strong> {t('settingsScheduling.help.modifiers.fallback')}</li>
                                <li><strong>{t('settingsScheduling.fields.minValueLabel')}</strong> {t('settingsScheduling.help.modifiers.minValue')}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
