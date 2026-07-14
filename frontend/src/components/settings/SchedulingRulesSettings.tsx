import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Save, RotateCcw, ChevronDown, ChevronRight, Plus, Loader2 } from 'lucide-react';
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

export const SchedulingRulesSettings = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const [expandedSections, setExpandedSections] = useState<Set<SectionId>>(
        new Set(['modifiers', 'passes', 'constraints'])
    );
    const [localRules, setLocalRules] = useState<SchedulingRules | null>(null);
    const [hasChanges, setHasChanges] = useState(false);
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
    const { data, isLoading, error, refetch } = useQuery({
        queryKey: ['scheduling-rules'],
        queryFn: schedulingRulesService.getRules,
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
        staleTime: 5 * 60 * 1000, // 5 minutes
    });

    // Initialize local state when data loads
    if (data && !localRules && !hasChanges) {
        setLocalRules(data.rules);
    }

    // Save mutation
    const saveMutation = useMutation({
        mutationFn: schedulingRulesService.updateRules,
        onSuccess: (response) => {
            queryClient.invalidateQueries({ queryKey: ['scheduling-rules'] });
            setLocalRules(response.rules);
            setHasChanges(false);
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

    // Reset mutation
    const resetMutation = useMutation({
        mutationFn: schedulingRulesService.resetRules,
        onSuccess: (response) => {
            queryClient.invalidateQueries({ queryKey: ['scheduling-rules'] });
            setLocalRules(response.rules);
            setHasChanges(false);
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

    const updateRules = useCallback((updater: (rules: SchedulingRules) => SchedulingRules) => {
        setLocalRules(prev => {
            if (!prev) return prev;
            const updated = updater(prev);
            setHasChanges(true);
            return updated;
        });
    }, []);

    const handleSave = () => {
        if (localRules) {
            saveMutation.mutate(localRules);
        }
    };

    const handleReset = () => {
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

    // Effort Modifiers handlers
    const updateModifier = (index: number, modifier: EffortModifier) => {
        updateRules(rules => ({
            ...rules,
            effort_modifiers: rules.effort_modifiers.map((m, i) => i === index ? modifier : m),
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
            scheduling_passes: rules.scheduling_passes.map((p, i) => i === index ? pass : p),
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
        const { active, over } = event;
        if (!over || active.id === over.id) return;

        updateRules(rules => {
            const oldIndex = rules.scheduling_passes.findIndex(p => p.id === active.id);
            const newIndex = rules.scheduling_passes.findIndex(p => p.id === over.id);
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
        return null;
    }

    return (
        <div className="space-y-6 max-w-4xl">
            {/* Source indicator */}
            <div className="text-sm text-content-secondary">
                {t('settingsScheduling.sourceLabel')}{' '}
                <span className="font-medium">
                    {t(`settingsScheduling.sourceValues.${data?.source || 'unknown'}`)}
                </span>
            </div>

            {/* Effort Modifiers Section */}
            <div className="card">
                <button
                    onClick={() => toggleSection('modifiers')}
                    className="w-full flex items-center justify-between text-left"
                >
                    <h3 className="text-lg font-semibold text-content-primary flex items-center gap-2">
                        {expandedSections.has('modifiers') ? (
                            <ChevronDown className="w-5 h-5" />
                        ) : (
                            <ChevronRight className="w-5 h-5" />
                        )}
                        {t('settingsScheduling.sections.modifiers.title')}
                    </h3>
                    <span className="text-sm text-content-secondary">
                        {t('settingsScheduling.sections.modifiers.count', { count: localRules.effort_modifiers.length })}
                    </span>
                </button>

                {expandedSections.has('modifiers') && (
                    <div className="mt-4 space-y-4">
                        <p className="text-sm text-content-secondary">
                            {t('settingsScheduling.sections.modifiers.description')}
                        </p>
                        {localRules.effort_modifiers.map((modifier, index) => (
                            <EffortModifierCard
                                key={modifier.id}
                                modifier={modifier}
                                onChange={(m) => updateModifier(index, m)}
                                onRemove={() => removeModifier(index)}
                            />
                        ))}
                        <Button variant="outline" size="sm" onClick={addModifier}>
                            <Plus className="w-4 h-4 mr-2" />
                            {t('settingsScheduling.sections.modifiers.add')}
                        </Button>
                    </div>
                )}
            </div>

            {/* Scheduling Passes Section */}
            <div className="card">
                <button
                    onClick={() => toggleSection('passes')}
                    className="w-full flex items-center justify-between text-left"
                >
                    <h3 className="text-lg font-semibold text-content-primary flex items-center gap-2">
                        {expandedSections.has('passes') ? (
                            <ChevronDown className="w-5 h-5" />
                        ) : (
                            <ChevronRight className="w-5 h-5" />
                        )}
                        {t('settingsScheduling.sections.passes.title')}
                    </h3>
                    <span className="text-sm text-content-secondary">
                        {t('settingsScheduling.sections.passes.count', { count: localRules.scheduling_passes.length })}
                    </span>
                </button>

                {expandedSections.has('passes') && (
                    <div className="mt-4 space-y-4">
                        <p className="text-sm text-content-secondary">
                            {t('settingsScheduling.sections.passes.description')}
                        </p>
                        <DndContext
                            sensors={sensors}
                            collisionDetection={closestCenter}
                            onDragEnd={handlePassReorder}
                        >
                            <SortableContext
                                items={localRules.scheduling_passes.map(p => p.id)}
                                strategy={verticalListSortingStrategy}
                            >
                                {localRules.scheduling_passes.map((pass, index) => (
                                    <SchedulingPassCard
                                        key={pass.id}
                                        pass={pass}
                                        onChange={(p) => updatePass(index, p)}
                                        onRemove={() => removePass(index)}
                                    />
                                ))}
                            </SortableContext>
                        </DndContext>
                        <Button variant="outline" size="sm" onClick={addPass}>
                            <Plus className="w-4 h-4 mr-2" />
                            {t('settingsScheduling.sections.passes.add')}
                        </Button>
                    </div>
                )}
            </div>

            {/* Constraints Section */}
            <div className="card">
                <button
                    onClick={() => toggleSection('constraints')}
                    className="w-full flex items-center justify-between text-left"
                >
                    <h3 className="text-lg font-semibold text-content-primary flex items-center gap-2">
                        {expandedSections.has('constraints') ? (
                            <ChevronDown className="w-5 h-5" />
                        ) : (
                            <ChevronRight className="w-5 h-5" />
                        )}
                        {t('settingsScheduling.sections.constraints.title')}
                    </h3>
                </button>

                {expandedSections.has('constraints') && (
                    <div className="mt-4">
                        <p className="text-sm text-content-secondary mb-4">
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
            <div className="flex items-center justify-between pt-4 border-t border-border">
                <Button
                    variant="outline"
                    onClick={handleReset}
                    disabled={resetMutation.isPending}
                >
                    <RotateCcw className="w-4 h-4 mr-2" />
                    {t('settingsScheduling.actions.resetToDefaults')}
                </Button>
                <div className="flex items-center gap-3">
                    {hasChanges && (
                        <span className="text-sm text-feedback-warning-foreground">{t('settingsScheduling.unsavedChanges')}</span>
                    )}
                    <Button
                        onClick={handleSave}
                        disabled={!hasChanges || saveMutation.isPending}
                        isLoading={saveMutation.isPending}
                    >
                        <Save className="w-4 h-4 mr-2" />
                        {t('settingsScheduling.actions.saveChanges')}
                    </Button>
                </div>
            </div>
            {confirmationDialog}
        </div>
    );
};
