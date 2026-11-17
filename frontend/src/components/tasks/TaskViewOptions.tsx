import { useEffect, useId, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { SlidersHorizontal } from 'lucide-react';
import { Select } from '../common/Select';
import type { SortKey } from './TaskList';

import { Button } from '../../components/common/Button';
/**
 * How the task list is arranged: grouping and order, in one popover next to the view switch. The trigger is an
 * icon button so the toolbar keeps one row; its name and tooltip are "View options".
 * Manual order is one list that is dragged, so it cannot be grouped.
 */
export const TaskViewOptions = ({ sortKey, onSortKeyChange, groupByStatus, onGroupByStatusChange }: {
    sortKey: SortKey;
    onSortKeyChange: (sortKey: SortKey) => void;
    groupByStatus: boolean;
    onGroupByStatusChange: (groupByStatus: boolean) => void;
}) => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    const triggerRef = useRef<HTMLButtonElement>(null);
    const panelId = useId();
    const manualOrder = sortKey === 'sort_order';

    useEffect(() => {
        if (!open) return;
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key !== 'Escape') return;
            event.preventDefault();
            setOpen(false);
            triggerRef.current?.focus();
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [open]);

    return (
        <div className="wc-filter-more">
            <Button
                data-page-chrome-control="button"
                ref={triggerRef}
                type="button"

                aria-label={t('tasks.viewOptions')}
                title={t('tasks.viewOptions')}
                aria-haspopup="dialog"
                aria-expanded={open}
                aria-controls={open ? panelId : undefined}
                onClick={() => setOpen(current => !current)}
             variant="secondary" iconOnly>
                <SlidersHorizontal aria-hidden="true" className="h-4 w-4" />
            </Button>
            {open && (
                <>
                    <div className="wc-filter-more-backdrop" onClick={() => setOpen(false)} aria-hidden />
                    <div id={panelId} role="dialog" aria-label={t('tasks.viewOptions')} className="wc-filter-more-panel tasks-view-options-panel">
                        <Select
                            label={t('tasks.groupBy')}
                            value={groupByStatus && !manualOrder ? 'status' : 'none'}
                            disabled={manualOrder}
                            help={manualOrder ? t('taskList.groupNeedsSort') : undefined}
                            onChange={event => onGroupByStatusChange(event.target.value === 'status')}
                        >
                            <option value="status">{t('tasks.groupByStatus')}</option>
                            <option value="none">{t('tasks.groupByNone')}</option>
                        </Select>
                        <Select
                            label={t('tasks.sortBy')}
                            value={sortKey}
                            help={manualOrder ? t('taskList.manualSortHint') : undefined}
                            onChange={event => onSortKeyChange(event.target.value as SortKey)}
                        >
                            <option value="priority">{t('taskList.sortPriority')}</option>
                            <option value="sort_order">{t('taskList.sortManual')}</option>
                            <option value="status">{t('taskList.sortStatus')}</option>
                            <option value="title">{t('taskList.sortTitle')}</option>
                        </Select>
                    </div>
                </>
            )}
        </div>
    );
};
