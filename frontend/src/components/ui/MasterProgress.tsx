interface MasterProgressProps {
    className?: string;
    completed: number;
    label: string;
    total: number;
    valueText: string;
}

export const MasterProgress = ({
    className = '',
    completed,
    label,
    total,
    valueText,
}: MasterProgressProps) => {
    const boundedTotal = Number.isFinite(total) && total > 0
        ? total
        : 1;
    const boundedCompleted = Number.isFinite(completed)
        ? Math.min(boundedTotal, Math.max(0, completed))
        : 0;
    const completionRatio = boundedCompleted / boundedTotal;

    return (
        <div
            className={`master-progress${className ? ` ${className}` : ''}`}
            role="progressbar"
            aria-label={label}
            aria-valuemin={0}
            aria-valuemax={boundedTotal}
            aria-valuenow={boundedCompleted}
            aria-valuetext={valueText}
        >
            <span style={{ transform: `scaleX(${completionRatio})` }} />
        </div>
    );
};
