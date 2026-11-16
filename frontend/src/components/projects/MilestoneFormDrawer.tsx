import clsx from 'clsx';
import type { FormEvent } from 'react';
import { Button } from '../common/Button';
import { RequiredIndicator } from '../common/Input';

import {
    SlideOverDrawer
} from '../ui';
import type {
    ProjectMilestoneStatus
} from '../../types/project';

import { type MilestoneFormState, milestoneStatusLabelKeys, t, textareaClassName } from './projectDetailShared';
export const MilestoneFormDrawer = ({
    mode,
    form,
    error,
    isSaving,
    onChange,
    onSubmit,
    onCancel,
}: {
    mode: 'create' | 'edit';
    form: MilestoneFormState;
    error: string | null;
    isSaving: boolean;
    onChange: <K extends keyof MilestoneFormState>(field: K, value: MilestoneFormState[K]) => void;
    onSubmit: (event: FormEvent<HTMLFormElement>) => void;
    onCancel: () => void;
}) => (
    <SlideOverDrawer
        open
        title={mode === 'create' ? t('surfaces.projectDetail.createMilestone') : t('surfaces.projectDetail.editMilestone')}
        closeLabel={t('actions.close')}
        onClose={onCancel}
    >
        <form className="space-y-4 p-5" onSubmit={onSubmit}>
            {error && (
                <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-name">
                    {t('surfaces.projectDetail.milestoneName')}
                    <RequiredIndicator />
                    <input
                        id="milestone-name"
                        value={form.name}
                        onChange={event => onChange('name', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                        maxLength={255}
                        required
                    />
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-status">
                    {t('surfaces.projectDetail.status')}
                    <select
                        id="milestone-status"
                        value={form.status}
                        onChange={event => onChange('status', event.target.value as ProjectMilestoneStatus)}
                        className="mt-1 w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    >
                        {Object.entries(milestoneStatusLabelKeys).map(([value, labelKey]) => (
                            <option key={value} value={value}>{t(labelKey)}</option>
                        ))}
                    </select>
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-target-date">
                    {t('surfaces.projectDetail.targetDate')}
                    <input
                        id="milestone-target-date"
                        type="date"
                        value={form.target_date}
                        onChange={event => onChange('target_date', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-completed-at">
                    {t('surfaces.projectDetail.completedAt')}
                    <input
                        id="milestone-completed-at"
                        type="datetime-local"
                        value={form.completed_at}
                        onChange={event => onChange('completed_at', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-sort-order">
                    {t('surfaces.projectDetail.sortOrder')}
                    <input
                        id="milestone-sort-order"
                        type="number"
                        value={form.sort_order}
                        onChange={event => onChange('sort_order', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </label>
            </div>

            <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-description">
                {t('surfaces.projectDetail.description')}
                <textarea
                    id="milestone-description"
                    value={form.description}
                    onChange={event => onChange('description', event.target.value)}
                    className={clsx('mt-1', textareaClassName)}
                    rows={3}
                />
            </label>

            <div className="flex justify-end gap-3">
                <Button type="button" variant="secondary" onClick={onCancel}>{t('surfaces.projectDetail.cancel')}</Button>
                <Button type="submit" isLoading={isSaving} disabled={!form.name.trim()}>
                    {mode === 'create' ? t('surfaces.projectDetail.createMilestone') : t('surfaces.projectDetail.saveMilestone')}
                </Button>
            </div>
        </form>
    </SlideOverDrawer>
);

