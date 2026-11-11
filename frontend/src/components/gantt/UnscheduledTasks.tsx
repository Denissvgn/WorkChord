import { useTranslation } from 'react-i18next';
import type { UnscheduledTask } from '../../types/gantt';

/** The planned tasks a schedule run leaves without dates, each with what would get it scheduled. */
export const UnscheduledTasks = ({ items }: { items?: UnscheduledTask[] }) => {
    const { t } = useTranslation();
    if (!items?.length) return null;
    return (
        <details className="mt-2 text-sm">
            <summary className="cursor-pointer font-medium text-content-primary">
                {t('gantt.unscheduled.summary', { count: items.length })}
            </summary>
            <ul className="mt-1 space-y-1">
                {items.map(item => (
                    <li key={item.task_id}>
                        <span className="font-medium text-content-primary">#{item.task_id} {item.task_title}</span>
                        {' · '}
                        <span className="text-content-secondary">
                            {t(`gantt.unscheduled.reasons.${item.reason}`, { defaultValue: item.message })}
                        </span>
                    </li>
                ))}
            </ul>
        </details>
    );
};
