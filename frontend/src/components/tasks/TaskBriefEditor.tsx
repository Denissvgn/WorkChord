import { useId } from 'react';
import { ArrowDown, ArrowUp, Plus, Trash2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { TaskBrief } from '../../types/task';
import { Button } from '../common/Button';

import { newCriterion } from './taskEditorContract';

export const TaskBriefEditor = ({ value, onChange, disabled = false, hideContext = false }: {
    value: TaskBrief; onChange: (value: TaskBrief) => void; disabled?: boolean; hideContext?: boolean;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const move = (index: number, offset: number) => {
        const criteria = [...value.acceptance_criteria];
        [criteria[index], criteria[index + offset]] = [criteria[index + offset], criteria[index]];
        onChange({ ...value, acceptance_criteria: criteria });
    };
    return <fieldset disabled={disabled} className="space-y-4 min-w-0">
        <legend className="mb-3 text-base font-semibold text-content-primary">{t('domain.brief')}</legend>
        {(['goal', 'context', 'scope', 'exclusions'] as const).filter(field => !hideContext || field !== 'context').map(field => <div key={field}>
            <label className="field-lbl" htmlFor={`${id}-${field}`}>{t(`domain.${field}`)}</label>
            <textarea id={`${id}-${field}`} className="input min-h-20 w-full" value={value[field]}
                maxLength={field === 'goal' ? 8000 : field === 'context' ? 20000 : 12000}
                onChange={event => onChange({ ...value, [field]: event.target.value })} />
        </div>)}
        <div className="space-y-3 border-t border-border pt-4">
            <h3 className="font-semibold text-content-primary">{t('domain.criteria')}</h3>
            <p className="text-sm text-content-secondary">{t('domain.criteriaHelp')}</p>
            {value.acceptance_criteria.length === 0 && <p className="text-sm text-content-secondary">{t('domain.noCriteria')}</p>}
            {value.acceptance_criteria.map((criterion, index) => <div key={criterion.id} className="space-y-2 border-b border-border pb-3">
                <div className="flex items-center justify-between gap-2">
                    <label className="field-lbl mb-0" htmlFor={`${id}-${criterion.id}`}>{t('domain.criterion', { number: index + 1 })}</label>
                    <div className="flex gap-1">
                        <Button type="button" size="sm" variant="ghost" disabled={index === 0} aria-label={t('domain.moveCriterionUp', { number: index + 1 })} onClick={() => move(index, -1)}><ArrowUp className="h-4 w-4" aria-hidden="true" /></Button>
                        <Button type="button" size="sm" variant="ghost" disabled={index === value.acceptance_criteria.length - 1} aria-label={t('domain.moveCriterionDown', { number: index + 1 })} onClick={() => move(index, 1)}><ArrowDown className="h-4 w-4" aria-hidden="true" /></Button>
                        <Button type="button" size="sm" variant="ghost" aria-label={t('domain.removeCriterion', { number: index + 1 })} onClick={() => onChange({ ...value, acceptance_criteria: value.acceptance_criteria.filter(item => item.id !== criterion.id) })}><Trash2 className="h-4 w-4" aria-hidden="true" /></Button>
                    </div>
                </div>
                <textarea id={`${id}-${criterion.id}`} className="input min-h-16 w-full" value={criterion.text} required maxLength={4000}
                    onChange={event => onChange({ ...value, acceptance_criteria: value.acceptance_criteria.map(item => item.id === criterion.id ? { ...item, text: event.target.value } : item) })} />
                <label className="field-lbl" htmlFor={`${id}-${criterion.id}-verify`}>{t('domain.criterionVerification')}</label>
                <textarea id={`${id}-${criterion.id}-verify`} className="input min-h-16 w-full" value={criterion.verification} maxLength={4000}
                    onChange={event => onChange({ ...value, acceptance_criteria: value.acceptance_criteria.map(item => item.id === criterion.id ? { ...item, verification: event.target.value } : item) })} />
            </div>)}
            <Button type="button" variant="secondary" size="sm" disabled={value.acceptance_criteria.length >= 100}
                onClick={() => onChange({ ...value, acceptance_criteria: [...value.acceptance_criteria, newCriterion()] })}>
                <Plus className="mr-1 h-4 w-4" aria-hidden="true" />{t('domain.addCriterion')}
            </Button>
        </div>
        {(['verification', 'artifact_expectations'] as const).map(field => <div key={field}>
            <label className="field-lbl" htmlFor={`${id}-${field}`}>{t(`domain.${field}`)}</label>
            <textarea id={`${id}-${field}`} className="input min-h-20 w-full" value={value[field]} maxLength={12000}
                onChange={event => onChange({ ...value, [field]: event.target.value })} />
        </div>)}
    </fieldset>;
};
