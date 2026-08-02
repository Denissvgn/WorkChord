import { useEffect, useId, useRef, useState } from 'react';
import type { KeyboardEvent as ReactKeyboardEvent, ReactNode } from 'react';
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
    const triggerRef = useRef<HTMLButtonElement>(null);
    const menuItemRefs = useRef<Array<HTMLButtonElement | null>>([]);
    const menuId = useId();
    const accessibleLabel = label ?? t('actions.moreActions');

    const closeMenu = (restoreFocus = true) => {
        setOpen(false);
        if (restoreFocus) {
            triggerRef.current?.focus();
        }
    };

    useEffect(() => {
        if (!open) return;
        const handleKeyDown = (event: globalThis.KeyboardEvent) => {
            if (event.key === 'Escape') {
                event.preventDefault();
                setOpen(false);
                triggerRef.current?.focus();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        const firstEnabledItem = menuItemRefs.current.find(item => item && !item.disabled);
        firstEnabledItem?.focus();
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [open]);

    const handleMenuItemKeyDown = (event: ReactKeyboardEvent<HTMLButtonElement>, index: number) => {
        const enabledIndexes = items.reduce<number[]>((indexes, item, itemIndex) => {
            if (!item.disabled) indexes.push(itemIndex);
            return indexes;
        }, []);
        const currentPosition = enabledIndexes.indexOf(index);
        if (currentPosition < 0) return;

        let nextIndex: number | null = null;
        if (event.key === 'ArrowDown') {
            nextIndex = enabledIndexes[(currentPosition + 1) % enabledIndexes.length];
        } else if (event.key === 'ArrowUp') {
            nextIndex = enabledIndexes[(currentPosition - 1 + enabledIndexes.length) % enabledIndexes.length];
        } else if (event.key === 'Home') {
            nextIndex = enabledIndexes[0];
        } else if (event.key === 'End') {
            nextIndex = enabledIndexes[enabledIndexes.length - 1];
        } else if (event.key === 'Tab') {
            closeMenu(false);
            return;
        } else {
            return;
        }

        event.preventDefault();
        menuItemRefs.current[nextIndex]?.focus();
    };

    return (
        <div className={clsx('relative', className)}>
            <button
                ref={triggerRef}
                type="button"
                onClick={() => open ? closeMenu() : setOpen(true)}
                aria-label={accessibleLabel}
                aria-haspopup="menu"
                aria-expanded={open}
                aria-controls={open ? menuId : undefined}
                className="btn icon"
            >
                <MoreHorizontal className="h-4 w-4" />
            </button>
            {open && (
                <>
                    <div style={{ position: 'fixed', inset: 0, zIndex: 10 }} onClick={() => closeMenu()} aria-hidden />
                    <div
                        id={menuId}
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
                                ref={node => { menuItemRefs.current[index] = node; }}
                                role="menuitem"
                                type="button"
                                disabled={item.disabled}
                                className="ofm-item"
                                style={item.tone === 'danger' ? { color: 'var(--blocked)' } : undefined}
                                onClick={() => {
                                    closeMenu();
                                    item.onSelect();
                                }}
                                onKeyDown={event => handleMenuItemKeyDown(event, index)}
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
