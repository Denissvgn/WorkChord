import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus, X } from 'lucide-react';
import { Button } from '../common/Button';
import { useTranslation } from 'react-i18next';
import { labelService } from '../../services/labelService';
import type { Label } from '../../types/label';
import { labelDisplay, labelGroupDisplay } from '../../i18n/seedDisplay';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

interface LabelSelectorProps {
    value: string[];
    onChange: (labels: string[]) => void;
    label?: string;
    placeholder?: string;
    allowCustom?: boolean;
    className?: string;
}

type LabelOption = Label & {
    groupName: string;
};

const flattenLabels = (groups: Awaited<ReturnType<typeof labelService.getGroups>>): LabelOption[] => (
    groups.flatMap(group => group.labels.map(label => ({
        ...label,
        name: labelDisplay(label).name,
        groupName: labelGroupDisplay(group).name,
    })))
);

const mergeLabels = (current: string[], incoming: string) => {
    const trimmed = incoming.trim();
    if (!trimmed) return current;
    const existing = new Set(current.map(label => label.toLowerCase()));
    if (existing.has(trimmed.toLowerCase())) return current;
    return [...current, trimmed];
};

export const LabelSelector = ({
    value,
    onChange,
    label,
    placeholder,
    allowCustom = true,
    className,
}: LabelSelectorProps) => {
    const { t } = useTranslation();
    const resolvedLabel = label ?? t('surfaces.labelSelector.labels');
    const resolvedPlaceholder = placeholder ?? t('surfaces.labelSelector.addCustomLabel');
    const [selectedSuggestion, setSelectedSuggestion] = useState('');
    const [customLabel, setCustomLabel] = useState('');

    const activeGroupsQuery = useQuery({
        queryKey: ['label-groups', { includeInactive: false }],
        queryFn: () => labelService.getGroups(),
    });

    const allGroupsQuery = useQuery({
        queryKey: ['label-groups', { includeInactive: true }],
        queryFn: () => labelService.getGroups({ include_inactive: true }),
    });

    const activeGroups = useMemo(() => activeGroupsQuery.data ?? [], [activeGroupsQuery.data]);
    const allGroups = useMemo(() => allGroupsQuery.data ?? [], [allGroupsQuery.data]);
    const optionError = activeGroupsQuery.error ?? allGroupsQuery.error;
    const optionsLoading = activeGroupsQuery.isLoading || allGroupsQuery.isLoading;

    const activeLabels = useMemo(() => flattenLabels(activeGroups), [activeGroups]);
    const labelsBySlug = useMemo(() => {
        const map = new Map<string, LabelOption>();
        flattenLabels(allGroups).forEach(option => {
            map.set(option.slug, option);
        });
        return map;
    }, [allGroups]);

    const selectedValues = value ?? [];
    const availableLabels = activeLabels.filter(option => !selectedValues.includes(option.slug));

    const addLabel = (slug: string) => {
        onChange(mergeLabels(selectedValues, slug));
        setSelectedSuggestion('');
    };

    const addCustomLabel = () => {
        const next = mergeLabels(selectedValues, customLabel);
        onChange(next);
        setCustomLabel('');
    };

    const removeLabel = (slug: string) => {
        onChange(selectedValues.filter(labelSlug => labelSlug !== slug));
    };

    return (
        <div className={className}>
            {resolvedLabel && (
                <label className="block text-sm font-medium text-content-primary mb-1">
                    {resolvedLabel}
                </label>
            )}

            {optionsLoading && <QueryLoadingState className="mb-2 min-h-16 py-3" />}
            {optionError && (
                <QueryErrorState
                    className="mb-2"
                    error={optionError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => {
                        void activeGroupsQuery.refetch();
                        void allGroupsQuery.refetch();
                    }}
                />
            )}

            {selectedValues.length > 0 && (
                <div className="mb-2 flex flex-wrap gap-2">
                    {selectedValues.map(slug => {
                        const option = labelsBySlug.get(slug);
                        const isArchived = option ? !option.is_active || option.group?.is_active === false : false;
                        return (
                            <span
                                key={slug}
                                className="inline-flex items-center gap-1 rounded-full border px-2 py-1 text-sm"
                                style={option ? {
                                    color: option.color,
                                    backgroundColor: `${option.color}1A`,
                                    borderColor: `${option.color}66`,
                                } : undefined}
                            >
                                <span>{option ? labelDisplay(option).name : slug}</span>
                                {option && option.slug !== option.name && (
                                    <span className="text-xs">{option.slug}</span>
                                )}
                                {isArchived && (
                                    <span className="rounded-full bg-surface-subtle px-1.5 py-0.5 text-wc-micro font-medium text-content-secondary">
                                        {t('surfaces.labelSelector.archived')}
                                    </span>
                                )}
                                <button
                                    type="button"
                                    onClick={() => removeLabel(slug)}
                                    className="rounded-full p-0.5 text-content-secondary hover:bg-surface-card/70 hover:text-content-primary"
                                    aria-label={t('surfaces.labelSelector.removeLabel', { label: option ? labelDisplay(option).name : slug })}
                                >
                                    <X className="h-3 w-3" aria-hidden="true" />
                                </button>
                            </span>
                        );
                    })}
                </div>
            )}

            <div className="grid grid-cols-1 gap-2 sm:grid-cols-[minmax(0,1fr)_auto]">
                <select
                    disabled={optionsLoading || Boolean(optionError)}
                    value={selectedSuggestion}
                    onChange={event => {
                        const slug = event.target.value;
                        if (slug) addLabel(slug);
                    }}
                    className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('surfaces.labelSelector.addGovernedLabel')}</option>
                    {availableLabels.map(option => (
                        <option key={option.slug} value={option.slug}>
                            {option.name} · {option.groupName}
                        </option>
                    ))}
                </select>

                {allowCustom && (
                    <div className="flex min-w-0 gap-2">
                        <input
                            type="text"
                            value={customLabel}
                            onChange={event => setCustomLabel(event.target.value)}
                            onKeyDown={event => {
                                if (event.key === 'Enter') {
                                    event.preventDefault();
                                    addCustomLabel();
                                }
                            }}
                            placeholder={resolvedPlaceholder}
                            className="min-w-0 flex-1 rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        />
                        <Button
                            type="button"
                            variant="secondary"
                            onClick={addCustomLabel}
                            disabled={!customLabel.trim()}
                            aria-label={t('surfaces.labelSelector.addCustomLabel')}
                        >
                            <Plus className="h-4 w-4" aria-hidden="true" />
                        </Button>
                    </div>
                )}
            </div>
        </div>
    );
};
