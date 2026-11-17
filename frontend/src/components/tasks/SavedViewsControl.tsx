import i18n from '../../i18n/i18n';
import { useEffect, useId, useRef, useState } from 'react';
import type { KeyboardEvent as ReactKeyboardEvent, ReactNode } from 'react';
import { Check, ChevronDown, Copy, RotateCcw, Save, Trash2 } from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../common/Button';
import type { SavedViewScope } from '../../types/savedView';
import { savedViewDisplay } from '../../i18n/seedDisplay';
import type { SavedViewManager } from './useSavedViewManager';

const t = i18n.t.bind(i18n);

const sortScopeLabel = (scope: SavedViewScope) => {
    if (scope === 'personal') return t('surfaces.savedViews.personal');
    if (scope === 'shared') return t('surfaces.savedViews.shared');
    return t('surfaces.savedViews.system');
};

type PickerItem =
    | { kind: 'view'; key: string; label: ReactNode; checked: boolean; disabled?: boolean; onSelect: () => void }
    | { kind: 'action'; key: string; label: ReactNode; icon: ReactNode; disabled?: boolean; tone?: 'danger'; onSelect: () => void };

/**
 * The page title of Tasks: the name of the view shown, opening a menu with every saved view and
 * the actions on the current one. Put it in PageHeader's `title`.
 */
export const SavedViewPicker = ({ manager, label }: { manager: SavedViewManager; label: string }) => {
    const [open, setOpen] = useState(false);
    const triggerRef = useRef<HTMLButtonElement>(null);
    const itemRefs = useRef<Array<HTMLButtonElement | null>>([]);
    const menuId = useId();
    const { selectedView, savedViews, modified, canMutateSelected } = manager;

    const closeMenu = (restoreFocus = true) => {
        setOpen(false);
        if (restoreFocus) triggerRef.current?.focus();
    };

    useEffect(() => {
        if (!open) return;
        const handleKeyDown = (event: globalThis.KeyboardEvent) => {
            if (event.key !== 'Escape') return;
            event.preventDefault();
            setOpen(false);
            triggerRef.current?.focus();
        };
        window.addEventListener('keydown', handleKeyDown);
        (itemRefs.current.find(item => item?.getAttribute('aria-checked') === 'true') ?? itemRefs.current.find(Boolean))?.focus();
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [open]);

    const items: PickerItem[] = [
        { kind: 'view', key: 'all', label: t('tasks.allTasks'), checked: !selectedView, onSelect: () => manager.chooseView(null) },
        ...savedViews.map(view => ({
            kind: 'view' as const,
            key: `view-${view.id}`,
            label: (
                <>
                    <span className="min-w-0 flex-1 truncate">{savedViewDisplay(view).name}</span>
                    <span className="text-xs text-content-secondary">
                        {sortScopeLabel(view.scope)}{view.is_valid ? '' : ` · ${t('surfaces.savedViews.invalid')}`}
                    </span>
                </>
            ),
            checked: view.id === selectedView?.id,
            disabled: !view.is_valid,
            onSelect: () => manager.chooseView(view.id),
        })),
        { kind: 'action', key: 'save-as', label: t('teamwork.saveAs'), icon: <Save aria-hidden="true" className="h-4 w-4" />, onSelect: manager.openSaveAs },
        {
            kind: 'action', key: 'save', label: t('teamwork.saveChanges'), icon: <Check aria-hidden="true" className="h-4 w-4" />,
            disabled: !canMutateSelected || !modified || manager.isSaving, onSelect: () => void manager.saveChanges(),
        },
        ...(selectedView && modified ? [{
            kind: 'action' as const, key: 'reset', label: t('teamwork.resetView'), icon: <RotateCcw aria-hidden="true" className="h-4 w-4" />,
            onSelect: manager.resetView,
        }] : []),
        {
            kind: 'action', key: 'duplicate', label: t('surfaces.savedViews.duplicate'), icon: <Copy aria-hidden="true" className="h-4 w-4" />,
            disabled: !selectedView || !selectedView.is_valid, onSelect: manager.openDuplicate,
        },
        {
            kind: 'action', key: 'delete', label: t('surfaces.savedViews.delete'), icon: <Trash2 aria-hidden="true" className="h-4 w-4" />,
            tone: 'danger', disabled: !canMutateSelected || manager.isDeleting, onSelect: manager.requestDelete,
        },
    ];

    const handleItemKeyDown = (event: ReactKeyboardEvent<HTMLButtonElement>, index: number) => {
        let next: number | null = null;
        if (event.key === 'ArrowDown') next = (index + 1) % items.length;
        else if (event.key === 'ArrowUp') next = (index - 1 + items.length) % items.length;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = items.length - 1;
        else if (event.key === 'Tab') { closeMenu(false); return; }
        else return;
        event.preventDefault();
        itemRefs.current[next]?.focus();
    };

    const firstActionIndex = items.findIndex(item => item.kind === 'action');

    return (
        <span className="tasks-view-picker">
            <Button
                data-page-chrome-control="button"
                ref={triggerRef}
                type="button"
                className="tasks-view-picker-trigger h-[30px]"
                aria-haspopup="menu"
                aria-expanded={open}
                aria-controls={open ? menuId : undefined}
                onClick={() => (open ? closeMenu() : setOpen(true))}
             variant="secondary">
                <span>{label}</span>
                <ChevronDown aria-hidden="true" className="h-4 w-4 shrink-0" />
            </Button>
            {open && (
                <>
                    <span className="tasks-view-picker-backdrop" onClick={() => closeMenu()} aria-hidden />
                    <span id={menuId} role="menu" aria-label={t('surfaces.savedViews.savedViews')} className="tasks-view-picker-menu">
                        {manager.isLoading && <span role="status" className="block px-2.5 py-1.5 text-sm text-content-secondary">{t('tasks.loadingSavedView')}</span>}
                        {manager.loadError && (
                            <span role="alert" className="block px-2.5 py-1.5 text-sm text-feedback-danger-foreground">
                                {t('tasks.savedViewsLoadFailed')}
                            </span>
                        )}
                        {items.map((item, index) => (
                            <span key={item.key} className={clsx('block', index === firstActionIndex && 'tasks-view-picker-divider')}>
                                <Button
                                    data-page-chrome-control="button"
                                    ref={node => { itemRefs.current[index] = node; }}
                                    type="button"
                                    role={item.kind === 'view' ? 'menuitemradio' : 'menuitem'}
                                    aria-checked={item.kind === 'view' ? item.checked : undefined}
                                    aria-disabled={item.disabled || undefined}
                                    className={clsx('ofm-item', item.disabled && 'cursor-not-allowed opacity-60', item.kind === 'action' && item.tone === 'danger' && 'text-feedback-danger-foreground')}
                                    onClick={() => {
                                        if (item.disabled) return;
                                        closeMenu();
                                        item.onSelect();
                                    }}
                                    onKeyDown={event => handleItemKeyDown(event, index)}
                                 variant="secondary">
                                    {item.kind === 'view'
                                        ? <Check aria-hidden="true" className={clsx('h-4 w-4 shrink-0', !item.checked && 'invisible')} />
                                        : item.icon}
                                    {item.label}
                                </Button>
                            </span>
                        ))}
                        {manager.loadError && (
                            <span className="block px-1 pt-1">
                                <Button variant="ghost" size="sm" onClick={manager.retryLoad}>{t('queryFeedback.retry')}</Button>
                            </span>
                        )}
                    </span>
                </>
            )}
        </span>
    );
};
