import {
    AlertCircle,
    Plus
} from 'lucide-react';
import type {
    TriageTaskDraftResponse
} from '../../types/triage';
import { Button } from '../common/Button';
import { newCriterion } from '../tasks/taskEditorContract';

import type { Dispatch, SetStateAction } from 'react';
import type { TaskBrief } from '../../types/task';
import { t } from './triageUtils';
export const TriageDraftPreview = ({ draftPreview, applyDraft, setBrief, description, setDescription, title, setTitle, draftErrorMessage }: {
    draftPreview: TriageTaskDraftResponse | null; applyDraft: () => void; setBrief: Dispatch<SetStateAction<TaskBrief>>;
    description: string; setDescription: (value: string | ((previous: string) => string)) => void;
    title: string; setTitle: (value: string) => void; draftErrorMessage: string | null;
}) => {
    if (!draftPreview && !draftErrorMessage) return null;
    return (<>
    {draftPreview && (
        <div className="space-y-3 rounded-lg border border-border bg-surface-muted p-4 text-sm text-content-primary shadow-xs">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border/50 pb-2">
                <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold uppercase tracking-wide text-content-primary">{t('surfaces.triagePage.aiDraftPreview')}</span>
                    <span className="rounded-full border border-border bg-surface-card px-2 py-0.5 text-xs text-content-primary">
                        {draftPreview.is_fallback ? t('surfaces.triagePage.fallbackDraft') : 'AI'}
                    </span>
                    {draftPreview.provider && (
                        <span className="rounded-full border border-border bg-surface-card px-2 py-0.5 text-xs text-content-primary">
                            {draftPreview.provider}
                        </span>
                    )}
                </div>
                <Button type="button" variant="secondary" size="sm" onClick={applyDraft}>
                    {t('surfaces.triagePage.applyDraft')}
                </Button>
            </div>

            {draftPreview.warnings && draftPreview.warnings.length > 0 && (
                <div className="rounded border border-feedback-warning-border bg-feedback-warning-muted p-2 text-xs text-feedback-warning-foreground">
                    <div className="font-semibold flex items-center gap-1 mb-1">
                        <AlertCircle className="h-3.5 w-3.5 text-feedback-warning" />
                        <span>{t('surfaces.triagePage.warnings')}</span>
                    </div>
                    <ul className="list-disc pl-4 space-y-0.5">
                        {draftPreview.warnings.map((w, idx) => (
                            <li key={idx}>{w}</li>
                        ))}
                    </ul>
                </div>
            )}

            <div>
                <p className="font-semibold text-content-primary">{draftPreview.suggested_title}</p>
                <p className="mt-1 whitespace-pre-wrap text-xs text-content-primary leading-relaxed">{draftPreview.suggested_description}</p>
            </div>

            {/* Granular interactive suggestion options */}
            <div className="grid grid-cols-1 gap-3 border-t border-border/50 pt-3">
                {draftPreview.acceptance_criteria.length > 0 && (
                    <div>
                        <div className="flex items-center justify-between text-xs font-semibold text-content-primary mb-1">
                            <span>{t('surfaces.triagePage.acceptanceCriteria')}</span>
                            <Button variant="ghost" size="sm"
                                type="button"
                                onClick={() => setBrief(previous => ({ ...previous, acceptance_criteria: [...previous.acceptance_criteria, ...draftPreview.acceptance_criteria.map(text => newCriterion(text))] }))}
                                className="text-content-primary hover:text-content-primary font-semibold underline shrink-0 ml-2"
                            >
                                <Plus aria-hidden="true" className="mr-0.5 inline h-3 w-3" />{t('surfaces.triagePage.appendToDescription')}
                            </Button>
                        </div>
                        <ul className="list-disc pl-4 text-xs text-content-secondary space-y-0.5">
                            {draftPreview.acceptance_criteria.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </div>
                )}
                {draftPreview.suggested_checklist.length > 0 && (
                    <div>
                        <div className="flex items-center justify-between text-xs font-semibold text-content-primary mb-1">
                            <span>{t('surfaces.triagePage.suggestedChecklist')}</span>
                            <Button variant="ghost" size="sm"
                                type="button"
                                onClick={() => setDescription(prev => prev + (prev ? '\n\n' : '') + `${t('surfaces.triagePage.checklist')}:\n${draftPreview.suggested_checklist.map(item => `- ${item}`).join('\n')}`)}
                                className="text-content-primary hover:text-content-primary font-semibold underline shrink-0 ml-2"
                            >
                                <Plus aria-hidden="true" className="mr-0.5 inline h-3 w-3" />{t('surfaces.triagePage.appendToDescription')}
                            </Button>
                        </div>
                        <ul className="list-disc pl-4 text-xs text-content-secondary space-y-0.5">
                            {draftPreview.suggested_checklist.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </div>
                )}
                {draftPreview.risks.length > 0 && (
                    <div>
                        <div className="flex items-center justify-between text-xs font-semibold text-content-primary mb-1">
                            <span>{t('surfaces.triagePage.risks')}</span>
                            <Button variant="ghost" size="sm"
                                type="button"
                                onClick={() => setDescription(prev => prev + (prev ? '\n\n' : '') + `${t('surfaces.triagePage.risks')}:\n${draftPreview.risks.map(item => `- ${item}`).join('\n')}`)}
                                className="text-content-primary hover:text-content-primary font-semibold underline shrink-0 ml-2"
                            >
                                <Plus aria-hidden="true" className="mr-0.5 inline h-3 w-3" />{t('surfaces.triagePage.appendToDescription')}
                            </Button>
                        </div>
                        <ul className="list-disc pl-4 text-xs text-content-secondary space-y-0.5">
                            {draftPreview.risks.map((item, index) => (
                                <li key={index}>{item}</li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    )}

    {draftErrorMessage && (
        <div className="flex items-start gap-2 rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
            <span>{draftErrorMessage}</span>
        </div>
    )}

    <div>
        {draftPreview && draftPreview.suggested_title !== title && (
            <div className="mt-1 flex items-center justify-between rounded-md bg-surface-muted border border-border/50 px-2 py-1 text-xs text-content-primary">
                <span className="truncate">{t('surfaces.triagePage.suggested')}<strong>{draftPreview.suggested_title}</strong></span>
                <Button variant="ghost" size="sm"
                    type="button"
                    onClick={() => setTitle(draftPreview.suggested_title)}
                    className="text-content-primary hover:text-content-primary font-semibold underline shrink-0 ml-2"
                >
                    {t('surfaces.triagePage.applySuggestedTitle')}
                </Button>
            </div>
        )}
    </div>

    <div>
        {draftPreview && draftPreview.suggested_description !== description && (
            <div className="mt-1 flex flex-col gap-1 rounded-md bg-surface-muted border border-border/50 px-2 py-1 text-xs text-content-primary">
                <div className="flex items-center justify-between">
                    <span>{t('surfaces.triagePage.suggestedDescriptionPreview')}</span>
                    <Button variant="ghost" size="sm"
                        type="button"
                        onClick={() => setDescription(draftPreview.suggested_description)}
                        className="text-content-primary hover:text-content-primary font-semibold underline shrink-0 ml-2"
                    >
                        {t('surfaces.triagePage.applySuggestedDescription')}
                    </Button>
                </div>
                <pre className="max-h-24 overflow-y-auto whitespace-pre-wrap rounded bg-surface-card p-1.5 border border-border font-mono text-wc-micro text-content-primary leading-snug">
                    {draftPreview.suggested_description}
                </pre>
            </div>
        )}
    </div>


</>);
};
