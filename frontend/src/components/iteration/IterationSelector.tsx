import { useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';
import { useIterationStore } from '../../store/iterationStore';
import { iterationService } from '../../services/iterationService';
import type { Iteration } from '../../types/iteration';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

interface IterationSelectorProps {
    className?: string;
    onChange?: (iterationId: number) => void;
    showLabel?: boolean;
    disabled?: boolean;
}

export const IterationSelector = ({
    className,
    onChange,
    showLabel = false,
    disabled = false,
}: IterationSelectorProps) => {
    const { t } = useTranslation();
    const { selectedIterationId, isBacklog, setSelectedIterationId, chooseDefaultIteration } = useIterationStore();

    const { data: iterations, isLoading, error, refetch } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    // Choose the default iteration when none is chosen; Backlog is a choice and is kept.
    useEffect(() => {
        if (iterations && iterations.length > 0) chooseDefaultIteration(iterations);
    }, [iterations, selectedIterationId, isBacklog, chooseDefaultIteration]);

    if (isLoading) return <QueryLoadingState className={className} />;
    if (error) return <QueryErrorState className={className} error={error} onRetry={() => void refetch()} />;

    // The parent route owns the no-iterations empty state.
    if (!iterations || iterations.length === 0) {
        return null;
    }

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const newId = parseInt(e.target.value);
        setSelectedIterationId(newId);
        onChange?.(newId);
    };

    const formatIterationOption = (iteration: Iteration) => (
        iteration.project?.name
            ? `${iteration.name} - ${iteration.project.name}`
            : `${iteration.name} - ${t('iterations.unscopedShort')}`
    );

    return (
        <div className={clsx("flex min-w-0 items-center gap-2", className)}>
            {showLabel && (
                <span className="shrink-0 text-sm font-medium text-content-secondary">
                    {t('iterationIndicator.currentIteration')}:
                </span>
            )}
            <select
                aria-label={t('iterationIndicator.selectIteration')}
                value={selectedIterationId}
                onChange={handleChange}
                disabled={disabled}
                className="min-w-0 max-w-full truncate rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
            >
                {isBacklog && <option value={0}>{t('teamwork.backlog')}</option>}
                {iterations.map(iter => (
                    <option key={iter.id} value={iter.id}>{formatIterationOption(iter)}</option>
                ))}
            </select>
        </div>
    );
};
