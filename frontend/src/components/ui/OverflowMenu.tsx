import { useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import clsx from 'clsx';
import { MoreHorizontal } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export type OverflowMenuItem = {
    label: ReactNode;
    icon?: ReactNode;
    onSelect: () => void;
    tone?: 'default' | 'danger';
    disabled?: boolean;
};

export const OverflowMenu = ({
    items,
    label,
    className,
}: {
    items: OverflowMenuItem[];
    label?: string;
    className?: string;
}) => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const accessibleLabel = label ?? t('actions.moreActions');

    useEffect(() => {
        if (!open) return;
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                setOpen(false);
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [open]);

    return (
        <div className={clsx('relative', className)}>
            <button
                type="button"
                onClick={() => setOpen(value => !value)}
                aria-label={accessibleLabel}
                aria-haspopup="menu"
                aria-expanded={open}
                className="btn"
                style={{ width: 30, padding: 0, justifyContent: 'center' }}
            >
                <MoreHorizontal className="h-4 w-4" />
            </button>
            {open && (
                <>
                    <div style={{ position: 'fixed', inset: 0, zIndex: 10 }} onClick={() => setOpen(false)} aria-hidden />
                    <div
                        role="menu"
                        style={{
                            position: 'absolute', right: 0, top: '100%', zIndex: 20, marginTop: 4, width: 208,
                            overflow: 'hidden', borderRadius: 'var(--r-md)', border: '1px solid var(--border-2)',
                            background: 'var(--panel)', padding: 4, boxShadow: 'var(--sh-pop)',
                        }}
                    >
                        {items.map((item, index) => (
                            <button
                                key={index}
                                role="menuitem"
                                type="button"
                                disabled={item.disabled}
                                className="ofm-item"
                                style={item.tone === 'danger' ? { color: 'var(--blocked)' } : undefined}
                                onClick={() => {
                                    setOpen(false);
                                    item.onSelect();
                                }}
                            >
                                {item.icon}
                                <span>{item.label}</span>
                            </button>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};
