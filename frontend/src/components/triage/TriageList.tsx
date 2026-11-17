import {
    Inbox,
    Plus
} from 'lucide-react';
import type {
    TriageItem
} from '../../types/triage';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { InlineEmptyState } from '../ui';
import { QuickCapture } from '../tasks/QuickCapture';

import { TriageRow } from './TriageRow';
import { t } from './triageUtils';
export const TriageList = ({ items, selectedId, projectsById, iterationsById, listErrorMessage, isLoading, activeFilterCount, onRetry, onSelect, onCreate, onReset }: {
    items: TriageItem[]; selectedId: number | null; projectsById: Record<number, string>; iterationsById: Record<number, string>;
    listErrorMessage: string | null; isLoading: boolean; activeFilterCount: number; onRetry: () => void;
    onSelect: (id: number) => void; onCreate: (title?: string) => void; onReset: () => void;
}) => (
    <div className="flex min-h-[320px] flex-col overflow-hidden rounded-lg lg:min-h-0 border border-border bg-surface-card">
        <QuickCapture listRow target={{ kind: 'triage' }} onExpand={onCreate} />
        {listErrorMessage ? (
            <QueryErrorState
                className="m-4"
                message={listErrorMessage}
                onRetry={() => void onRetry()}
            />
        ) : isLoading ? (
            <div className="flex h-full items-center justify-center p-8 text-content-secondary">{t('surfaces.triagePage.loadingIntake')}</div>
        ) : items.length === 0 ? (
            <div className="flex h-full items-center justify-center p-8">
                {activeFilterCount > 0 ? (
                    <InlineEmptyState
                        headingLevel={2}
                        icon={<Inbox className="h-5 w-5" />}
                        title={t('emptyStates.filtered.title')}
                        description={t('emptyStates.filtered.body')}
                        actions={<Button variant="secondary" onClick={onReset}>{t('emptyStates.filtered.clear')}</Button>}
                    />
                ) : (
                    <InlineEmptyState
                        headingLevel={2}
                        icon={<Inbox className="h-5 w-5" />}
                        title={t('emptyStates.triage.emptyTitle')}
                        description={t('emptyStates.triage.emptyBody')}
                        actions={(
                            <Button onClick={() => onCreate()}>
                                <Plus className="h-4 w-4" aria-hidden="true" />
                                {t('emptyStates.triage.action')}
                            </Button>
                        )}
                    />
                )}
            </div>
        ) : (
            <div className="min-h-0 flex-1 overflow-auto">
                <table className="min-w-[760px] w-full">
                    <thead className="sticky top-0 z-10 border-b border-border bg-surface-muted text-left text-xs font-semibold uppercase tracking-wide text-content-secondary">
                        <tr>
                            <th className="px-4 py-3">{t('surfaces.triagePage.item')}</th>
                            <th className="px-4 py-3">{t('surfaces.triagePage.status')}</th>
                            <th className="px-4 py-3">{t('surfaces.triagePage.priority')}</th>
                            <th className="px-4 py-3">{t('surfaces.triagePage.labels')}</th>
                            <th className="px-4 py-3">{t('surfaces.triagePage.hints')}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map(item => (
                            <TriageRow
                                key={item.id}
                                item={item}
                                isSelected={item.id === selectedId}
                                projectsById={projectsById}
                                iterationsById={iterationsById}
                                onSelect={onSelect}
                            />
                        ))}
                    </tbody>
                </table>
            </div>
        )}
    </div>

);
