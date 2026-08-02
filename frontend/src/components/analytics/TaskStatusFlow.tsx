import React from 'react';
import type { TaskStatus, TaskStatusLog } from '../../types/task';
import { ArrowRight } from 'lucide-react';
import clsx from 'clsx';
import { useTranslation } from 'react-i18next';
import { STATUS_TONE, toneBorderClassName } from '../ui/tone';
import { formatDateTime } from '../../utils/formatDate';

interface TaskStatusFlowProps {
    logs: TaskStatusLog[];
}

export const TaskStatusFlow: React.FC<TaskStatusFlowProps> = ({ logs }) => {
    // 1. Sort logs by date ascending
    const sortedLogs = [...logs].sort((a, b) => new Date(a.changed_at).getTime() - new Date(b.changed_at).getTime());

    if (sortedLogs.length === 0) return null;

    return (
        <div className="flex items-center overflow-x-auto overflow-y-hidden pt-6 pb-14 px-2">
            {/* Initial State */}
            <StatusNode status={sortedLogs[0].from_status} />

            {sortedLogs.map((log, index) => (
                <React.Fragment key={log.id}>
                    {/* Transition Arrow */}
                    <div className="relative w-24 flex-shrink-0 flex items-center justify-center mx-[-4px] z-0">
                        {/* The Line */}
                        <div className="h-0.5 w-full bg-action relative">
                            {/* Arrow Head */}
                            <ArrowRight className="absolute -right-3 -top-[9px] w-5 h-5 text-action bg-surface-card rounded-full p-0.5" />
                        </div>

                        {/* Transition Metadata (Absolute positioned below) */}
                        <div className="absolute top-4 left-0 w-full text-center">
                            <div className="flex items-center justify-center gap-1 text-wc-micro text-content-secondary font-medium">
                                <span className="w-4 h-4 rounded-full bg-surface-subtle flex items-center justify-center text-xs text-content-primary">
                                    {(log.triggered_by || 'U').charAt(0).toUpperCase()}
                                </span>
                            </div>
                            <div className="text-wc-micro text-content-tertiary mt-0.5 whitespace-nowrap">
                                {formatDateTime(log.changed_at)}
                            </div>
                        </div>
                    </div>

                    {/* Target State */}
                    <StatusNode status={log.to_status} isLast={index === sortedLogs.length - 1} />
                </React.Fragment>
            ))}
        </div>
    );
};

const StatusNode = ({ status, isLast }: { status: TaskStatus, isLast?: boolean }) => {
    const { t } = useTranslation();
    return (
        <div className={clsx(
            "flex-shrink-0 w-28 h-8 flex items-center justify-center rounded-md text-xs font-semibold border shadow-sm z-10 bg-surface-card",
            toneBorderClassName[STATUS_TONE[status]],
            isLast && "ring-2 ring-offset-1 ring-focus border-action"
        )}>
            {t(`statuses.${status}`)}
        </div>
    );
};
