import { useId, useState } from 'react';
import { ChevronDown } from 'lucide-react';
import clsx from 'clsx';

interface CollapsibleSectionProps {
    title: string;
    defaultOpen?: boolean;
    /** Controls the section from outside; pair it with `onOpenChange`. */
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
    children: React.ReactNode;
}

export const CollapsibleSection = ({ title, defaultOpen = false, open, onOpenChange, children }: CollapsibleSectionProps) => {
    const [ownOpen, setOwnOpen] = useState(defaultOpen);
    const isOpen = open ?? ownOpen;
    const setIsOpen = (next: boolean) => {
        setOwnOpen(next);
        onOpenChange?.(next);
    };
    const contentId = useId();

    return (
        <div className="border border-border rounded-lg overflow-hidden">
            <button
                type="button"
                aria-expanded={isOpen}
                aria-controls={contentId}
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex items-center justify-between px-4 py-3 bg-surface-muted hover:bg-surface-subtle transition-colors"
            >
                <span className="font-medium text-content-primary">{title}</span>
                <ChevronDown
                    aria-hidden="true"
                    className={clsx(
                        "w-4 h-4 text-content-secondary transition-transform duration-200",
                        isOpen ? "rotate-0" : "-rotate-90"
                    )}
                />
            </button>
            <div id={contentId} hidden={!isOpen}>
                {isOpen && <div className="p-4 space-y-4 bg-surface-card border-t border-border">
                    {children}
                </div>}
            </div>
        </div>
    );
};
