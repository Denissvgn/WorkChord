import { useId, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Trash2, ChevronDown, ChevronRight, GripVertical, Plus, X, ArrowUp, ArrowDown, Info } from 'lucide-react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import type { SchedulingPass, SortCriterion } from '../../types/schedulingRules';
import { TASK_FIELDS, FILTER_FIELDS, OPERATORS, FILTER_VALUES } from '../../types/schedulingRules';
import { schedulingPassDisplay } from '../../i18n/schedulingDisplay';

interface Props {
    pass: SchedulingPass;
    sortableId: string;
    onChange: (pass: SchedulingPass) => void;
    onRemove: () => void;
}

export const SchedulingPassCard = ({ pass, sortableId, onChange, onRemove }: Props) => {
    const { t } = useTranslation();
    const [expanded, setExpanded] = useState(false);
    const detailsId = useId();
    const display = schedulingPassDisplay(pass);

    // Sortable hook for drag-n-drop
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id: sortableId });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
        zIndex: isDragging ? 1000 : 'auto',
    };

    const handleToggleEnabled = (enabled: boolean) => {
        onChange({ ...pass, enabled });
    };

    // Filter conditions handlers
    const addCondition = () => {
        onChange({
            ...pass,
            filter: {
                all: [...pass.filter.all, 'task.is_deferred == false'],
            },
        });
    };

    const updateCondition = (index: number, value: string) => {
        onChange({
            ...pass,
            filter: {
                all: pass.filter.all.map((c, i) => i === index ? value : c),
            },
        });
    };

    const removeCondition = (index: number) => {
        onChange({
            ...pass,
            filter: {
                all: pass.filter.all.filter((_, i) => i !== index),
            },
        });
    };

    // Sort criteria handlers
    const addSortCriterion = () => {
        onChange({
            ...pass,
            sort: [...pass.sort, { field: 'priority', order: 'asc' }],
        });
    };

    const updateSortCriterion = (index: number, criterion: SortCriterion) => {
        onChange({
            ...pass,
            sort: pass.sort.map((s, i) => i === index ? criterion : s),
        });
    };

    const removeSortCriterion = (index: number) => {
        onChange({
            ...pass,
            sort: pass.sort.filter((_, i) => i !== index),
        });
    };

    const toggleSortOrder = (index: number) => {
        const criterion = pass.sort[index];
        updateSortCriterion(index, {
            ...criterion,
            order: criterion.order === 'asc' ? 'desc' : 'asc',
        });
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            className={`
                rounded-lg border bg-surface-card transition-all duration-200
                ${pass.enabled
                    ? 'border-action'
                    : 'border-border opacity-75'
                }
                ${isDragging ? 'shadow-lg' : ''}
            `}
        >
            {/* Header */}
            <div className="flex flex-wrap items-start gap-3 p-4 sm:flex-nowrap sm:items-center sm:gap-4">
                <button
                    type="button"
                    {...attributes}
                    {...listeners}
                    className="touch-none p-1 -m-1 cursor-grab active:cursor-grabbing"
                    aria-label={t('settingsScheduling.aria.dragToReorder')}
                >
                    <GripVertical className="w-4 h-4 text-content-tertiary hover:text-content-secondary" aria-hidden="true" />
                </button>

                <Checkbox
                    checked={pass.enabled}
                    onChange={handleToggleEnabled}
                    aria-label={t('settingsScheduling.aria.enablePass', { id: pass.id })}
                />

                <button
                    type="button"
                    onClick={() => setExpanded(!expanded)}
                    className="min-w-0 flex-1 text-left"
                    aria-expanded={expanded}
                    aria-controls={detailsId}
                >
                    <div className="flex items-center gap-2">
                        {expanded ? (
                            <ChevronDown className="w-4 h-4 shrink-0 text-content-tertiary" aria-hidden="true" />
                        ) : (
                            <ChevronRight className="w-4 h-4 shrink-0 text-content-tertiary" aria-hidden="true" />
                        )}
                        <span className="min-w-0 break-words">
                            <span className="font-medium text-content-primary">{display.name}</span>
                            {display.isBuiltIn && (
                                <code className="ms-2 break-all rounded bg-surface-subtle px-1.5 py-0.5 text-xs text-content-secondary">
                                    {display.technicalId}
                                </code>
                            )}
                        </span>
                    </div>
                    {display.description && (
                        <p className="ms-6 mt-0.5 break-words text-sm text-content-secondary">{display.description}</p>
                    )}
                </button>

                <button
                    type="button"
                    onClick={onRemove}
                    className="p-1 text-content-tertiary hover:text-feedback-danger-foreground transition-colors"
                    title={t('settingsScheduling.aria.removePass')}
                    aria-label={t('settingsScheduling.aria.removePass')}
                >
                    <Trash2 className="w-4 h-4" aria-hidden="true" />
                </button>
            </div>

            {/* Expanded Details */}
            {expanded && (
                <div id={detailsId} className="animate-in slide-in-from-top-2 space-y-6 border-t border-border-subtle px-4 pb-4 pt-2 duration-200">
                    {/* Basic Info */}
                    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                        <Input
                            label={t('settingsScheduling.fields.id')}
                            value={pass.id}
                            onChange={(e) => onChange({ ...pass, id: e.target.value })}
                        />
                        <Input
                            label={t('settingsScheduling.fields.description')}
                            value={pass.description}
                            onChange={(e) => onChange({ ...pass, description: e.target.value })}
                        />
                    </div>

                    {/* Filter Conditions */}
                    <div>
                        <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                            <h4 className="min-w-0 break-words text-sm font-medium text-content-primary">{t('settingsScheduling.fields.filterConditions')}</h4>
                            <button
                                type="button"
                                onClick={addCondition}
                                className="text-sm text-action hover:text-action flex items-center gap-1"
                            >
                                <Plus className="w-3 h-3" aria-hidden="true" />
                                {t('settingsScheduling.actions.add')}
                            </button>
                        </div>
                        {pass.filter.all.length === 0 ? (
                            <p className="text-sm text-content-secondary">{t('settingsScheduling.fields.noFilterConditions')}</p>
                        ) : (
                            <div className="space-y-2">
                                {pass.filter.all.map((condition, index) => {
                                    // Parse existing condition like "task.field == value"
                                    const parts = condition.match(/^([\w.]+)\s*(==|!=|<=?|>=?)\s*(.+)$/);
                                    const field = parts?.[1] || 'task.is_deferred';
                                    const operator = parts?.[2] || '==';
                                    const value = parts?.[3] || 'false';

                                    const handlePartChange = (newField: string, newOp: string, newValue: string) => {
                                        updateCondition(index, `${newField} ${newOp} ${newValue}`);
                                    };

                                    return (
                                        <div key={index} className="grid grid-cols-[auto_minmax(0,1fr)] items-center gap-2 md:flex">
                                            <span className="w-6 text-sm text-content-tertiary" aria-hidden="true">{index + 1}.</span>
                                            {/* Field dropdown */}
                                            <select
                                                value={field}
                                                onChange={(e) => handlePartChange(e.target.value, operator, value)}
                                                className="min-w-0 flex-1 rounded border border-border-strong px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                                aria-label={t('settingsScheduling.aria.conditionField', { index: index + 1 })}
                                            >
                                                {FILTER_FIELDS.map(f => (
                                                    <option key={f.value} value={f.value}>{t(f.labelKey)}</option>
                                                ))}
                                            </select>
                                            {/* Operator dropdown */}
                                            <select
                                                value={operator}
                                                onChange={(e) => handlePartChange(field, e.target.value, value)}
                                                className="col-start-2 w-full rounded border border-border-strong px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-focus md:w-24"
                                                aria-label={t('settingsScheduling.aria.conditionOperator', { index: index + 1 })}
                                            >
                                                {OPERATORS.map(op => (
                                                    <option key={op.value} value={op.value}>{t(op.labelKey)}</option>
                                                ))}
                                            </select>
                                            {/* Value dropdown/input */}
                                            <select
                                                value={FILTER_VALUES.some(v => v.value === value) ? value : '_custom_'}
                                                onChange={(e) => {
                                                    if (e.target.value !== '_custom_') {
                                                        handlePartChange(field, operator, e.target.value);
                                                    }
                                                }}
                                                className="col-start-2 w-full rounded border border-border-strong px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-focus md:w-28"
                                                aria-label={t('settingsScheduling.aria.conditionValue', { index: index + 1 })}
                                            >
                                                {FILTER_VALUES.map(v => (
                                                    <option key={v.value} value={v.value}>{t(v.labelKey)}</option>
                                                ))}
                                                <option value="_custom_">{t('settingsScheduling.options.filterValues.custom')}</option>
                                            </select>
                                            {/* Show custom input if value is not in predefined list */}
                                            {!FILTER_VALUES.some(v => v.value === value) && (
                                                <input
                                                    type="text"
                                                    value={value}
                                                    onChange={(e) => handlePartChange(field, operator, e.target.value)}
                                                    className="col-start-2 w-full rounded border border-border-strong bg-surface-muted px-2 py-1.5 font-mono text-sm focus:outline-none focus:ring-1 focus:ring-focus md:w-24"
                                                    placeholder={t('settingsScheduling.fields.value')}
                                                    aria-label={t('settingsScheduling.aria.customConditionValue', { index: index + 1 })}
                                                />
                                            )}
                                            <button
                                                type="button"
                                                onClick={() => removeCondition(index)}
                                                className="col-start-2 justify-self-end p-1 text-content-tertiary hover:text-feedback-danger-foreground"
                                                aria-label={t('settingsScheduling.aria.removeCondition')}
                                            >
                                                <X className="w-4 h-4" aria-hidden="true" />
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>

                    {/* Sort Criteria */}
                    <div>
                        <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                            <h4 className="min-w-0 break-words text-sm font-medium text-content-primary">{t('settingsScheduling.fields.sortCriteria')}</h4>
                            <button
                                type="button"
                                onClick={addSortCriterion}
                                className="text-sm text-action hover:text-action flex items-center gap-1"
                            >
                                <Plus className="w-3 h-3" aria-hidden="true" />
                                {t('settingsScheduling.actions.add')}
                            </button>
                        </div>
                        {pass.sort.length === 0 ? (
                            <p className="text-sm text-content-secondary">{t('settingsScheduling.fields.noSortCriteria')}</p>
                        ) : (
                            <div className="space-y-2">
                                {pass.sort.map((criterion, index) => (
                                    <div key={index} className="grid grid-cols-[auto_minmax(0,1fr)] items-center gap-2 md:flex">
                                        <span className="w-6 text-sm text-content-tertiary" aria-hidden="true">{index + 1}.</span>
                                        <select
                                            value={criterion.field}
                                            onChange={(e) => updateSortCriterion(index, { ...criterion, field: e.target.value })}
                                            className="min-w-0 flex-1 rounded border border-border-strong px-3 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-focus"
                                            aria-label={t('settingsScheduling.aria.sortField', { index: index + 1 })}
                                        >
                                            {TASK_FIELDS.map(f => (
                                                <option key={f.value} value={f.value}>{t(f.labelKey)}</option>
                                            ))}
                                        </select>
                                        <button
                                            type="button"
                                            onClick={() => toggleSortOrder(index)}
                                            className={`
                                                col-start-2 flex items-center justify-center gap-1 rounded border px-2 py-1.5 text-sm md:col-auto
                                                ${criterion.order === 'asc'
                                                    ? 'bg-action-muted border-action text-action'
                                                    : 'bg-feedback-warning-muted border-feedback-warning-border text-feedback-warning-foreground'
                                                }
                                            `}
                                            title={t(`settingsScheduling.options.sortOrder.${criterion.order}`)}
                                        >
                                            {criterion.order === 'asc' ? (
                                                <ArrowUp className="w-3 h-3" aria-hidden="true" />
                                            ) : (
                                                <ArrowDown className="w-3 h-3" aria-hidden="true" />
                                            )}
                                            {t(`settingsScheduling.options.sortOrder.${criterion.order}`)}
                                        </button>
                                        <button
                                            type="button"
                                            onClick={() => removeSortCriterion(index)}
                                            className="col-start-2 justify-self-end p-1 text-content-tertiary hover:text-feedback-danger-foreground"
                                            aria-label={t('settingsScheduling.aria.removeSortCriterion')}
                                        >
                                            <X className="w-4 h-4" aria-hidden="true" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Contextual Help */}
                    <div className="bg-action-muted border border-action rounded-md p-3 flex gap-3 text-sm text-action-muted-foreground mt-6">
                        <Info aria-hidden="true" className="w-5 h-5 text-action-muted-foreground shrink-0 mt-0.5" />
                        <div className="min-w-0">
                            <p className="font-medium mb-1">{t('settingsScheduling.fields.configurationGuide')}</p>
                            <ul className="list-disc list-inside space-y-1 text-xs">
                                <li><strong>{t('settingsScheduling.fields.filter')}</strong> {t('settingsScheduling.help.passes.filter')}</li>
                                <li><strong>{t('settingsScheduling.fields.sort')}</strong> {t('settingsScheduling.help.passes.sort')}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
