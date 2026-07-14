import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import clsx from 'clsx';

interface CollapsibleSectionProps {
    title: string;
    defaultOpen?: boolean;
    children: React.ReactNode;
}

export const CollapsibleSection = ({ title, defaultOpen = false, children }: CollapsibleSectionProps) => {
    const [isOpen, setIsOpen] = useState(defaultOpen);

    return (
        <div className="border border-border rounded-lg overflow-hidden">
            <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between px-4 py-3 bg-surface-muted hover:bg-surface-subtle transition-colors"
            >
                <span className="font-medium text-content-primary">{title}</span>
                <ChevronDown
                    className={clsx(
                        "w-4 h-4 text-content-secondary transition-transform duration-200",
                        isOpen ? "rotate-0" : "-rotate-90"
                    )}
                />
            </button>
            {isOpen && (
                <div className="p-4 space-y-4 bg-surface-card border-t border-border">
                    {children}
                </div>
            )}
        </div>
    );
};