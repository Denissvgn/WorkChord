import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { TFunction } from 'i18next';
import { Link } from 'react-router-dom';
import type { TaskStatusLog } from '../../types/task';
import { formatDateTime } from '../../utils/formatDate';
import { STATUS_TONE, toneVar } from '../ui/tone';

const HOUR = 3_600_000;

const spent = (t: TFunction, ms: number) => {
    if (ms < HOUR) return t('analytics.lifecycle.underAnHour');
    if (ms < 24 * HOUR) return t('analytics.lifecycle.hours', { count: Math.round(ms / HOUR) });
    return t('analytics.lifecycle.days', { count: Math.round(ms / (24 * HOUR)) });
};

/**
 * One task's states in order, with the time spent in each. The current state is
 * marked with weight and a "Current" tag, not a focus ring.
 */
export const TaskStatusFlow = ({ taskId, title, logs, nowMs }: { taskId: number; title: string; logs: TaskStatusLog[]; nowMs?: number }) => {
    const { t, i18n } = useTranslation();
    // "So far" is measured from when the list was first shown.
    const [shownAt] = useState(() => Date.now());
    const now = nowMs ?? shownAt;
    const sorted = [...logs].sort((a, b) => new Date(a.changed_at).getTime() - new Date(b.changed_at).getTime());
    if (sorted.length === 0) return null;
    const locale = i18n.resolvedLanguage ?? i18n.language;
    const states = [
        { status: sorted[0].from_status, enteredAt: null as string | null, by: null as string | null },
        ...sorted.map(log => ({ status: log.to_status, enteredAt: log.changed_at, by: log.triggered_by })),
    ];
    return (
        <section className="space-y-2" aria-labelledby={`lifecycle-${taskId}`}>
            <h4 id={`lifecycle-${taskId}`} className="font-medium">
                <Link to={`/tasks?task=${taskId}`} className="break-words text-action hover:underline">#{taskId} · {title}</Link>
            </h4>
            <ol className="space-y-1.5 border-l-2 border-border pl-4">
                {states.map((state, index) => {
                    const current = index === states.length - 1;
                    const start = state.enteredAt ? new Date(state.enteredAt).getTime() : null;
                    const end = current ? now : new Date(states[index + 1].enteredAt!).getTime();
                    return (
                        <li key={`${state.status}-${index}`} className="flex flex-wrap items-baseline gap-x-2 text-sm">
                            <span aria-hidden="true" className="relative -left-[1.4rem] -mr-3 h-2.5 w-2.5 rounded-full" style={{ background: toneVar[STATUS_TONE[state.status]] }} />
                            <span className={current ? 'font-semibold text-content-primary' : 'text-content-primary'}>{t(`statuses.${state.status}`)}</span>
                            {current && <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs font-medium">{t('analytics.lifecycle.current')}</span>}
                            <span className="text-content-secondary">
                                {start === null
                                    ? t('analytics.lifecycle.untilFirstChange', { at: formatDateTime(states[1].enteredAt!, locale) })
                                    : current ? t('analytics.lifecycle.forSoFar', { time: spent(t, end - start) }) : t('analytics.lifecycle.for', { time: spent(t, end - start) })}
                                {state.enteredAt && <> · {t('analytics.lifecycle.since', { at: formatDateTime(state.enteredAt, locale) })}</>}
                                {state.by && <> · {t(`analytics.lifecycle.by_${state.by}`, { defaultValue: t('analytics.lifecycle.byUnknown') })}</>}
                            </span>
                        </li>
                    );
                })}
            </ol>
        </section>
    );
};
