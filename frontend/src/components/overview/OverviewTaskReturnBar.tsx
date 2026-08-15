import { ArrowLeft, Waypoints } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import type { RefObject } from 'react';
import { overviewTaskReturnFocusId } from '../../features/overview/overviewTaskThread';

export const OverviewTaskReturnBar = ({
    active,
    taskId,
    taskTitle,
    returnActionRef,
}: {
    active: boolean;
    taskId: number | null;
    taskTitle?: string | null;
    returnActionRef?: RefObject<HTMLAnchorElement | null>;
}) => {
    const { t } = useTranslation();

    if (!active) return null;

    return (
        <aside
            className="overview-thread-return"
            aria-label={t('overview.thread.returnContext')}
        >
            <span className="overview-thread-return-icon">
                <Waypoints aria-hidden="true" />
            </span>
            <div className="overview-thread-return-copy">
                <strong>{t('overview.thread.returnContext')}</strong>
                <span>
                    {taskId && taskTitle
                        ? t('overview.thread.returnTask', {
                            id: taskId,
                            title: taskTitle,
                        })
                        : t('overview.thread.returnBody')}
                </span>
            </div>
            <Link
                ref={returnActionRef}
                className="btn secondary sm"
                to="/"
                state={taskId
                    ? { returnFocusId: overviewTaskReturnFocusId(taskId) }
                    : undefined}
            >
                <ArrowLeft aria-hidden="true" size={13} />
                {t('overview.thread.returnAction')}
            </Link>
        </aside>
    );
};
