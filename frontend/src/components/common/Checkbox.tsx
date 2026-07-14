import { forwardRef } from 'react';
import { Check } from 'lucide-react';
import clsx from 'clsx';
import { twMerge } from 'tailwind-merge';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
    label?: string;
    onChange?: (checked: boolean) => void;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
    ({ className, label, checked, onChange, disabled, ...props }, ref) => {
        return (
            <label className={clsx(
                "inline-flex items-center gap-2 cursor-pointer group select-none",
                disabled && "cursor-not-allowed opacity-50",
                className
            )}>
                <div className="relative flex items-center">
                    <input
                        type="checkbox"
                        ref={ref}
                        className="peer sr-only"
                        checked={checked}
                        onChange={(e) => onChange?.(e.target.checked)}
                        disabled={disabled}
                        {...props}
                    />
                    <div className={twMerge(
                        "w-5 h-5 border rounded transition-all duration-200 flex items-center justify-center",
                        "border-border-strong bg-surface-card group-hover:border-border-strong peer-focus:ring-2 peer-focus:ring-focus/20",
                        checked && "bg-action border-action group-hover:border-action-hover",
                        disabled && "bg-surface-subtle border-border"
                    )}>
                        <Check
                            className={clsx(
                                "w-3.5 h-3.5 text-action-foreground transition-all duration-200",
                                checked ? "opacity-100 scale-100" : "opacity-0 scale-75"
                            )}
                            strokeWidth={3}
                        />
                    </div>
                </div>
                {label && (
                    <span className="text-sm font-medium text-content-primary group-hover:text-content-primary transition-colors">
                        {label}
                    </span>
                )}
            </label>
        );
    }
);

Checkbox.displayName = 'Checkbox';
