import { useRef } from 'react';
import type { KeyboardEvent, ReactNode } from 'react';
import clsx from 'clsx';

export interface SegmentedOption<T extends string> {
    value: T;
    label: ReactNode;
    icon?: ReactNode;
}

/**
 * One choice among a few, each a button with a pressed state, named as a group.
 *
 * With `arrowKeys`, only the pressed button is in the tab order and the arrow,
 * Home and End keys move to another option and choose it. Without it every
 * button is a tab stop, as before.
 */
export const SegmentedControl = <T extends string,>({ label, options, value, onChange, disabled, className, arrowKeys = false }: {
    label: string;
    options: SegmentedOption<T>[];
    value: T;
    onChange: (value: T) => void;
    disabled?: boolean;
    className?: string;
    arrowKeys?: boolean;
}) => {
    const groupRef = useRef<HTMLDivElement>(null);

    const handleKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
        if (!arrowKeys || disabled) return;
        let next: number;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % options.length;
        else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + options.length) % options.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = options.length - 1;
        else return;
        event.preventDefault();
        groupRef.current?.querySelectorAll<HTMLButtonElement>('button')[next]?.focus();
        onChange(options[next].value);
    };

    // The pressed option is the one tab stop; when nothing matches, the first option is.
    const stopIndex = Math.max(0, options.findIndex(option => option.value === value));

    return (
        <div ref={groupRef} role="group" aria-label={label} className={clsx('seg', className)}>
            {options.map((option, index) => (
                <button data-page-chrome-control="button" key={option.value} type="button" aria-pressed={option.value === value} disabled={disabled}
                    tabIndex={arrowKeys && index !== stopIndex ? -1 : undefined}
                    className="inline-flex items-center justify-center gap-1.5"
                    onClick={() => onChange(option.value)}
                    onKeyDown={event => handleKeyDown(event, index)}>
                    {option.icon}{option.label}
                </button>
            ))}
        </div>
    );
};
