import { useState, useCallback, useMemo } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { AlertTriangle, Save, RotateCcw, ChevronDown, ChevronRight, Plus, Loader2 } from 'lucide-react';
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
} from '@dnd-kit/core';
import type { DragEndEvent } from '@dnd-kit/core';
import {
    arrayMove,
    SortableContext,
    sortableKeyboardCoordinates,
    verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { Button } from '../common/Button';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { schedulingRulesService } from '../../services/schedulingRulesService';
import type { SchedulingRules, EffortModifier, SchedulingPass, Constraints } from '../../types/schedulingRules';
import { EffortModifierCard } from './EffortModifierCard';
import { SchedulingPassCard } from './SchedulingPassCard';
import { ConstraintsPanel } from './ConstraintsPanel';
import { getAdminAccessErrorMessage } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { protectedQueryRetry } from '../../utils/protectedQueries';

type SectionId = 'modifiers' | 'passes' | 'constraints';

const SETTINGS_ROW_ID = Symbol('settings-row-id');
type SettingsRowIdentity = { [SETTINGS_ROW_ID]: string };
type EditableEffortModifier = EffortModifier & SettingsRowIdentity;
type EditableSchedulingPass = SchedulingPass & SettingsRowIdentity;
type EditableSchedulingRules = Omit<SchedulingRules, 'effort_modifiers' | 'scheduling_passes'> & {
    effort_modifiers: EditableEffortModifier[];
    scheduling_passes: EditableSchedulingPass[];
};

let settingsRowSequence = 0;
const createSettingsRowId = (kind: 'modifier' | 'pass') => (
    `${kind}-${++settingsRowSequence}`
);

const literalEffortDivisor = (formula: string | null | undefined) => {
    if (!formula) return null;
    const directDivision = formula.match(
        /^\s*effort\s*\/\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)\s*$/i,
    );
    if (directDivision) return Number(directDivision[1]);

    const inversePercentage = formula.match(
        /^\s*effort\s*\/\s*\(\s*1\s*-\s*assignee\.[A-Za-z_]\w*\s*\/\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?)\s*\)\s*$/i,
    );
    return inversePercentage ? Number(inversePercentage[1]) : null;
};

const withSettingsRowIds = (rules: SchedulingRules): EditableSchedulingRules => ({
    ...rules,
    effort_modifiers: rules.effort_modifiers.map(modifier => ({
        ...modifier,
        [SETTINGS_ROW_ID]: createSettingsRowId('modifier'),
    })),
    scheduling_passes: rules.scheduling_passes.map(pass => ({
        ...pass,
        [SETTINGS_ROW_ID]: createSettingsRowId('pass'),
    })),
});

export const SchedulingRulesSettings = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const [expandedSections, setExpandedSections] = useState<Set<SectionId>>(
        new Set(['modifiers', 'passes', 'constraints'])
    );
    const [draftRules, setDraftRules] = useState<EditableSchedulingRules | null>(null);
    const [hasChanges, setHasChanges] = useState(false);
    const [validationErrors, setValidationErrors] = useState<string[]>([]);
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    // DnD sensors for keyboard and pointer
    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8, // Require 8px movement to start drag
            },
        }),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    // Fetch current rules
    // feedback-policy: query loading,error,retry,empty
    const { data, isLoading, error, refetch } = useQuery({
        queryKey: ['scheduling-rules'],
        queryFn: schedulingRulesService.getRules,
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
        staleTime: 5 * 60 * 1000, // 5 minutes
    });

    const serverRules = useMemo(
        () => data?.rules ? withSettingsRowIds(data.rules) : null,
        [data],
    );
    const localRules = hasChanges ? draftRules : serverRules;

    // feedback-policy: mutation pending,toast
    const saveMutation = useMutation({
        mutationFn: schedulingRulesService.updateRules,
        onSuccess: (response) => {
            queryClient.setQueryData(['scheduling-rules'], response);
            setDraftRules(null);
            setHasChanges(false);
            setValidationErrors([]);
            toast.success(t('settingsScheduling.saveSuccess'));
        },
        onError: (error: unknown) => {
            toast.error(getAdminAccessErrorMessage(error, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsScheduling.saveFailed'),
            }));
        },
    });

    // feedback-policy: mutation pending,toast
    const resetMutation = useMutation({
        mutationFn: schedulingRulesService.resetRules,
        onSuccess: (response) => {
            queryClient.setQueryData(['scheduling-rules'], response);
            setDraftRules(null);
            setHasChanges(false);
            setValidationErrors([]);
            toast.success(t('settingsScheduling.resetSuccess'));
        },
        onError: (error: unknown) => {
            toast.error(getAdminAccessErrorMessage(error, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsScheduling.resetFailed'),
            }));
        },
    });

    const isMutating = saveMutation.isPending || resetMutation.isPending;

    const toggleSection = (section: SectionId) => {
        setExpandedSections(prev => {
            const newSet = new Set(prev);
            if (newSet.has(section)) {
                newSet.delete(section);
            } else {
                newSet.add(section);
            }
            return newSet;
        });
    };

    const updateRules = useCallback((
        updater: (rules: EditableSchedulingRules) => EditableSchedulingRules,
    ) => {
        const currentRules = draftRules ?? serverRules;
        if (!currentRules) return;
        setDraftRules(updater(currentRules));
        setHasChanges(true);
        setValidationErrors([]);
    }, [draftRules, serverRules]);

    const validateRules = (rules: SchedulingRules) => {
        const issues: string[] = [];
        const modifierIds = new Set<string>();
        rules.effort_modifiers.forEach((modifier, index) => {
            const id = modifier.id.trim();
            if (!id) {
                issues.push(t('settingsScheduling.validation.modifierIdRequired', { index: index + 1 }));
            } else if (modifierIds.has(id)) {
                issues.push(t('settingsScheduling.validation.duplicateModifierId', { id }));
            }
            modifierIds.add(id);

            if (
                modifier.min_value != null
                && (!Number.isFinite(modifier.min_value) || modifier.min_value < 0)
            ) {
                issues.push(t('settingsScheduling.validation.modifierMinValue', { id: id || index + 1 }));
            }

            const divisor = literalEffortDivisor(modifier.formula);
            if (divisor != null && (!Number.isFinite(divisor) || divisor <= 0)) {
                issues.push(t('settingsScheduling.validation.modifierDivisorPositive', {
                    id: id || index + 1,
                }));
            }
        });

        const passIds = new Set<string>();
        rules.scheduling_passes.forEach((pass, index) => {
            const id = pass.id.trim();
            if (!id) {
                issues.push(t('settingsScheduling.validation.passIdRequired', { index: index + 1 }));
            } else if (passIds.has(id)) {
                issues.push(t('settingsScheduling.validation.duplicatePassId', { id }));
            }
            passIds.add(id);

            if (pass.filter.all.some(condition => !condition.trim())) {
                issues.push(t('settingsScheduling.validation.emptyCondition', { id: id || index + 1 }));
            }
        });

        const maxOverload = rules.constraints.balance_workload?.max_overload_percent;
        if (
            maxOverload != null
            && (!Number.isFinite(maxOverload) || maxOverload < 0 || maxOverload > 100)
        ) {
            issues.push(t('settingsScheduling.validation.maxOverload'));
        }

        return Array.from(new Set(issues));
    };

    const handleSave = () => {
        if (!localRules || isMutating) return;
        const issues = validateRules(localRules);
        setValidationErrors(issues);
        if (issues.length > 0) return;
        saveMutation.mutate(localRules);
    };

    const handleReset = () => {
        if (isMutating) return;
        requestConfirmation({
            title: t('settingsScheduling.actions.resetToDefaults'),
            description: t('settingsScheduling.resetConfirm'),
            confirmLabel: t('settingsScheduling.actions.resetToDefaults'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'warning',
            onConfirm: () => resetMutation.mutateAsync(),
        });
    };

    const handleDiscard = () => {
        if (!data || isMutating) return;
        setDraftRules(null);
        setHasChanges(false);
        setValidationErrors([]);
    };

    // Effort Modifiers handlers
    const updateModifier = (index: number, modifier: EffortModifier) => {
        updateRules(rules => ({
            ...rules,
            effort_modifiers: rules.effort_modifiers.map((current, i) => (
                i === index
                    ? { ...modifier, [SETTINGS_ROW_ID]: current[SETTINGS_ROW_ID] }
                    : current
            )),
        }));
    };

    const addModifier = () => {
        updateRules(rules => ({
            ...rules,
            effort_modifiers: [
                ...rules.effort_modifiers,
                {
                    id: `modifier_${Date.now()}`,
                    enabled: true,
                    formula: 'effort',
                    fallback: 'effort',
                    [SETTINGS_ROW_ID]: createSettingsRowId('modifier'),
                },
            ],
        }));
    };

    const removeModifier = (index: number) => {
        updateRules(rules => ({
            ...rules,
            effort_modifiers: rules.effort_modifiers.filter((_, i) => i !== index),
        }));
    };

    // Scheduling Passes handlers
    const updatePass = (index: number, pass: SchedulingPass) => {
        updateRules(rules => ({
            ...rules,
            scheduling_passes: rules.scheduling_passes.map((current, i) => (
                i === index
                    ? { ...pass, [SETTINGS_ROW_ID]: current[SETTINGS_ROW_ID] }
                    : current
            )),
        }));
    };

    const addPass = () => {
        updateRules(rules => ({
            ...rules,
            scheduling_passes: [
                ...rules.scheduling_passes,
                {
                    id: `pass_${Date.now()}`,
                    description: t('settingsScheduling.newPassDescription'),
                    enabled: true,
                    filter: { all: [] },
                    sort: [],
                    [SETTINGS_ROW_ID]: createSettingsRowId('pass'),
                },
            ],
        }));
    };

    const removePass = (index: number) => {
        updateRules(rules => ({
            ...rules,
            scheduling_passes: rules.scheduling_passes.filter((_, i) => i !== index),
        }));
    };

    // Drag-n-drop reorder handler for scheduling passes
    const handlePassReorder = (event: DragEndEvent) => {
        if (isMutating) return;
        const { active, over } = event;
        if (!over || active.id === over.id) return;

        updateRules(rules => {
            const oldIndex = rules.scheduling_passes.findIndex(
                pass => pass[SETTINGS_ROW_ID] === active.id,
            );
            const newIndex = rules.scheduling_passes.findIndex(
                pass => pass[SETTINGS_ROW_ID] === over.id,
            );
            if (oldIndex === -1 || newIndex === -1) return rules;
            return {
                ...rules,
                scheduling_passes: arrayMove(rules.scheduling_passes, oldIndex, newIndex),
            };
        });
    };

    // Constraints handler
    const updateConstraints = (constraints: Constraints) => {
        updateRules(rules => ({
            ...rules,
            constraints,
        }));
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-action" />
                <span className="ml-3 text-content-secondary">{t('settingsScheduling.loadingRules')}</span>
            </div>
        );
    }

    if (error) {
        const message = getAdminAccessErrorMessage(error, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settingsScheduling.loadFailed'),
        });
        return <QueryErrorState message={message} onRetry={() => void refetch()} />;
    }

    if (!localRules) {
        return (
            <QueryErrorState
                message={t('settingsScheduling.rulesUnavailable')}
                onRetry={() => void refetch()}
            />
        );
    }

    return (
        <div className="max-w-4xl space-y-6">
            {/* Source indicator */}
            <div className="text-sm text-content-secondary">
                {t('settingsScheduling.sourceLabel')}{' '}
                <span className="font-medium">
                    {t(`settingsScheduling.sourceValues.${data?.source || 'unknown'}`)}
                </span>
            </div>

            {validationErrors.length > 0 && (
                <div className="rounded-lg border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground" role="alert">
                    <div className="flex items-start gap-3">
                        <AlertTriangle aria-hidden="true" className="mt-0.5 h-5 w-5 shrink-0" />
                        <div className="min-w-0">
                            <p className="font-semibold">{t('settingsScheduling.validation.title')}</p>
                            <ul className="mt-1 list-disc space-y-1 ps-5 text-sm">
                                {validationErrors.map(issue => <li key={issue}>{issue}</li>)}
                            </ul>
                        </div>
                    </div>
                </div>
            )}

            <fieldset className="contents" disabled={isMutating} aria-busy={isMutating}>
                {/* Effort Modifiers Section */}
                <div className="card">
                    <button
                        type="button"
                        onClick={() => toggleSection('modifiers')}
                        className="flex w-full items-center justify-between text-left"
                        aria-expanded={expandedSections.has('modifiers')}
                        aria-controls="scheduling-modifiers-panel"
                    >
                        <h3 className="flex min-w-0 items-center gap-2 text-lg font-semibold text-content-primary">
                            {expandedSections.has('modifiers') ? (
                                <ChevronDown aria-hidden="true" className="h-5 w-5 shrink-0" />
                            ) : (
                                <ChevronRight aria-hidden="true" className="h-5 w-5 shrink-0" />
                            )}
                            <span className="break-words">{t('settingsScheduling.sections.modifiers.title')}</span>
                        </h3>
                        <span className="shrink-0 text-sm text-content-secondary">
                            {t('settingsScheduling.sections.modifiers.count', { count: localRules.effort_modifiers.length })}
                        </span>
                    </button>

                    {expandedSections.has('modifiers') && (
                        <div id="scheduling-modifiers-panel" className="mt-4 space-y-4">
                            <p className="text-sm text-content-secondary">
                                {t('settingsScheduling.sections.modifiers.description')}
                            </p>
                            {localRules.effort_modifiers.map((modifier, index) => (
                                <EffortModifierCard
                                    key={modifier[SETTINGS_ROW_ID]}
                                    modifier={modifier}
                                    onChange={(m) => updateModifier(index, m)}
                                    onRemove={() => removeModifier(index)}
                                />
                            ))}
                            <Button variant="outline" size="sm" onClick={addModifier}>
                                <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                {t('settingsScheduling.sections.modifiers.add')}
                            </Button>
                        </div>
                    )}
                </div>

                {/* Scheduling Passes Section */}
                <div className="card">
                    <button
                        type="button"
                        onClick={() => toggleSection('passes')}
                        className="flex w-full items-center justify-between text-left"
                        aria-expanded={expandedSections.has('passes')}
                        aria-controls="scheduling-passes-panel"
                    >
                        <h3 className="flex min-w-0 items-center gap-2 text-lg font-semibold text-content-primary">
                            {expandedSections.has('passes') ? (
                                <ChevronDown aria-hidden="true" className="h-5 w-5 shrink-0" />
                            ) : (
                                <ChevronRight aria-hidden="true" className="h-5 w-5 shrink-0" />
                            )}
                            <span className="break-words">{t('settingsScheduling.sections.passes.title')}</span>
                        </h3>
                        <span className="shrink-0 text-sm text-content-secondary">
                            {t('settingsScheduling.sections.passes.count', { count: localRules.scheduling_passes.length })}
                        </span>
                    </button>

                    {expandedSections.has('passes') && (
                        <div id="scheduling-passes-panel" className="mt-4 space-y-4">
                            <p className="text-sm text-content-secondary">
                                {t('settingsScheduling.sections.passes.description')}
                            </p>
                            <DndContext
                                sensors={sensors}
                                collisionDetection={closestCenter}
                                onDragEnd={handlePassReorder}
                            >
                                <SortableContext
                                    items={localRules.scheduling_passes.map(pass => pass[SETTINGS_ROW_ID])}
                                    strategy={verticalListSortingStrategy}
                                >
                                    {localRules.scheduling_passes.map((pass, index) => (
                                        <SchedulingPassCard
                                            key={pass[SETTINGS_ROW_ID]}
                                            pass={pass}
                                            sortableId={pass[SETTINGS_ROW_ID]}
                                            onChange={(p) => updatePass(index, p)}
                                            onRemove={() => removePass(index)}
                                        />
                                    ))}
                                </SortableContext>
                            </DndContext>
                            <Button variant="outline" size="sm" onClick={addPass}>
                                <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                {t('settingsScheduling.sections.passes.add')}
                            </Button>
                        </div>
                    )}
                </div>

                {/* Constraints Section */}
                <div className="card">
                    <button
                        type="button"
                        onClick={() => toggleSection('constraints')}
                        className="flex w-full items-center justify-between text-left"
                        aria-expanded={expandedSections.has('constraints')}
                        aria-controls="scheduling-constraints-panel"
                    >
                        <h3 className="flex min-w-0 items-center gap-2 text-lg font-semibold text-content-primary">
                            {expandedSections.has('constraints') ? (
                                <ChevronDown aria-hidden="true" className="h-5 w-5 shrink-0" />
                            ) : (
                                <ChevronRight aria-hidden="true" className="h-5 w-5 shrink-0" />
                            )}
                            <span className="break-words">{t('settingsScheduling.sections.constraints.title')}</span>
                        </h3>
                    </button>

                    {expandedSections.has('constraints') && (
                        <div id="scheduling-constraints-panel" className="mt-4">
                            <p className="mb-4 text-sm text-content-secondary">
                                {t('settingsScheduling.sections.constraints.description')}
                            </p>
                            <ConstraintsPanel
                                constraints={localRules.constraints}
                                onChange={updateConstraints}
                            />
                        </div>
                    )}
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col gap-3 border-t border-border pt-4 sm:flex-row sm:items-center sm:justify-between">
                    <Button
                        variant="outline"
                        onClick={handleReset}
                        disabled={isMutating}
                        isLoading={resetMutation.isPending}
                    >
                        <RotateCcw aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('settingsScheduling.actions.resetToDefaults')}
                    </Button>
                    <div className="flex flex-col gap-3 sm:items-end">
                        {hasChanges && (
                            <span className="text-sm text-feedback-warning-foreground">{t('settingsScheduling.unsavedChanges')}</span>
                        )}
                        <div className="flex flex-wrap gap-2 sm:justify-end">
                            <Button
                                type="button"
                                variant="secondary"
                                onClick={handleDiscard}
                                disabled={!hasChanges || isMutating}
                            >
                                {t('actions.discard')}
                            </Button>
                            <Button
                                onClick={handleSave}
                                disabled={!hasChanges || isMutating}
                                isLoading={saveMutation.isPending}
                            >
                                <Save aria-hidden="true" className="mr-2 h-4 w-4" />
                                {t('settingsScheduling.actions.saveChanges')}
                            </Button>
                        </div>
                    </div>
                </div>
            </fieldset>
            {confirmationDialog}
        </div>
    );
};
