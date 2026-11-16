import clsx from 'clsx';
import {
    AlertTriangle,
    Send
} from 'lucide-react';
import type { FormEvent } from 'react';
import { Button } from '../common/Button';
import { DisabledReason } from '../common/DisabledReason';
import { RequiredIndicator } from '../common/Input';

import {
    SlideOverDrawer
} from '../ui';
import type {
    ProjectHealth
} from '../../types/project';

import { healthDotClass, healthLabelKeys, healthToTone, type ProjectUpdateFormState, t, textareaClassName } from './projectDetailShared';
export const PostUpdateDrawer = ({
    open,
    onClose,
    form,
    error,
    isPending,
    setField,
    onSubmit,
    onDismissError,
    summaryIsBlank,
    projectName,
}: {
    open: boolean;
    onClose: () => void;
    form: ProjectUpdateFormState;
    error: string | null;
    isPending: boolean;
    setField: <K extends keyof ProjectUpdateFormState>(field: K, value: ProjectUpdateFormState[K]) => void;
    onSubmit: (event: FormEvent<HTMLFormElement>) => void;
    onDismissError: () => void;
    summaryIsBlank: boolean;
    projectName: string;
}) => {
    return (
        <SlideOverDrawer
            open={open}
            onClose={onClose}
            ariaLabel={t('surfaces.projectDetail.postStatusUpdate')}
            title={t('surfaces.projectDetail.postStatusUpdate')}
            subtitle={(
                <>
                    {t('surfaces.projectDetail.visibleToSubscribersOf')} <span className="font-medium text-content-primary">{projectName}</span>
                </>
            )}
            icon={<Send className="h-4 w-4" />}
        >
            <form className="flex min-h-full flex-col overflow-hidden" onSubmit={onSubmit}>
                <div className="flex-1 space-y-4 overflow-y-auto p-5">
                    {error && (
                        <div className="flex items-start justify-between gap-3 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                            <div className="flex gap-2">
                                <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                                <span>{error}</span>
                            </div>
                            <button
                                type="button"
                                className="bg-transparent p-0 text-xs font-medium text-feedback-danger-foreground hover:underline"
                                onClick={onDismissError}
                            >
                                {t('surfaces.projectDetail.dismiss')}
                            </button>
                        </div>
                    )}

                    <div>
                        <span id="drawer-health-label" className="mb-1.5 block text-xs font-semibold text-content-primary">
                            {t('surfaces.projectDetail.health')}
                        </span>
                        <div role="radiogroup" aria-labelledby="drawer-health-label" className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                            {(Object.entries(healthLabelKeys) as [ProjectHealth, string][]).map(([value, labelKey]) => {
                                const active = form.health === value;
                                const tone = healthToTone(value);
                                const dot = healthDotClass(value);
                                const activeCls: Record<string, string> = {
                                    green: 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground',
                                    yellow: 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground',
                                    red: 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground',
                                    gray: 'border-border bg-surface-muted text-content-primary',
                                };
                                return (
                                    <button
                                        key={value}
                                        type="button"
                                        role="radio"
                                        aria-checked={active}
                                        onClick={() => setField('health', value)}
                                        className={clsx(
                                            'inline-flex h-9 items-center gap-2 rounded-md border px-3 text-sm transition-colors',
                                            active ? clsx(activeCls[tone], 'font-semibold') : 'border-border bg-surface-card text-content-primary hover:bg-surface-muted',
                                        )}
                                    >
                                        <span className={clsx('h-2 w-2 rounded-full', dot)} />
                                        {t(labelKey)}
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    <div>
                        <div className="mb-1.5 flex items-baseline justify-between">
                            <label className="text-xs font-semibold text-content-primary" htmlFor="drawer-summary">{t('surfaces.projectDetail.summary')} <RequiredIndicator /></label>
                            <span className="text-wc-micro text-content-tertiary">{t('surfaces.projectDetail.oneLineStakeholdersWillSkim')}</span>
                        </div>
                        <input
                            id="drawer-summary"
                            required
                            aria-required="true"
                            value={form.summary}
                            onChange={event => setField('summary', event.target.value)}
                            placeholder={t('surfaces.projectDetail.eGSpecLandedEngKickoffTuesday')}
                            className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            maxLength={500}
                        />
                    </div>

                    <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-progress">{t('surfaces.projectDetail.progress')}</label>
                            <textarea
                                id="drawer-progress"
                                value={form.progress_text}
                                onChange={event => setField('progress_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.whatMovedThisWeek')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-risks">{t('surfaces.projectDetail.risks')}</label>
                            <textarea
                                id="drawer-risks"
                                value={form.risks_text}
                                onChange={event => setField('risks_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.whatMightSlip')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-decisions">{t('surfaces.projectDetail.decisions')}</label>
                            <textarea
                                id="drawer-decisions"
                                value={form.decisions_text}
                                onChange={event => setField('decisions_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.anythingNewLockedIn')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-next">{t('surfaces.projectDetail.nextSteps')}</label>
                            <textarea
                                id="drawer-next"
                                value={form.next_steps_text}
                                onChange={event => setField('next_steps_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.whatSNext')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                    </div>
                </div>

                <footer className="flex flex-wrap items-center justify-end gap-2 border-t border-border-subtle p-4">
                    <DisabledReason reason={summaryIsBlank && t('disabledReasons.summaryRequired')} className="mr-auto" />
                    <Button type="button" variant="secondary" onClick={onClose}>{t('surfaces.projectDetail.cancel')}</Button>
                    <Button type="submit" isLoading={isPending} disabled={summaryIsBlank}>
                        {!isPending && <Send className="mr-2 h-4 w-4" />}
                        {t('surfaces.projectDetail.postUpdate')}
                    </Button>
                </footer>
            </form>
        </SlideOverDrawer>
    );
};
