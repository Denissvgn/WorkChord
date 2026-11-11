import type { ReactNode } from 'react';
import clsx from 'clsx';

export interface SegmentedOption<T extends string> {
    value: T;
    label: ReactNode;
    icon?: ReactNode;
}

/** One choice among a few, each a button with a pressed state, named as a group. */
export const SegmentedControl = <T extends string,>({ label, options, value, onChange, disabled, className }: {
    label: string;
    options: SegmentedOption<T>[];
    value: T;
    onChange: (value: T) => void;
    disabled?: boolean;
    className?: string;
}) => (
    <div role="group" aria-label={label} className={clsx('seg', className)}>
        {options.map(option => (
            <button key={option.value} type="button" aria-pressed={option.value === value} disabled={disabled}
                className="inline-flex items-center justify-center gap-1.5" onClick={() => onChange(option.value)}>
                {option.icon}{option.label}
            </button>
        ))}
    </div>
);
