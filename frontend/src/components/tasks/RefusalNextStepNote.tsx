import type { TFunction } from 'i18next';
import { useTranslation } from 'react-i18next';
import type { RefusalNextStep } from '../../types/task';

/** The next step as one sentence in the person's language; the server's English sentence when this kind has no translation. */
const nextStepText = (t: TFunction, step: RefusalNextStep) => t(`domain.nextStepKinds.${step.kind}`, { defaultValue: step.message });

/**
 * What a person may do about a refusal, set beside the refusal. The sentence says what to do; the commands name the
 * routes and tools an agent or script uses for the same step. The form that takes the step, when this page has one,
 * is shown by the caller next to this note.
 */
export const RefusalNextStepNote = ({ step, className }: { step: RefusalNextStep; className?: string }) => {
    const { t } = useTranslation();
    const commands = Object.values(step.commands);
    return <div className={className ?? 'space-y-1 text-sm text-content-secondary'} data-testid="refusal-next-step">
        <p><span className="font-medium text-content-primary">{t('domain.nextStep')}</span> {nextStepText(t, step)}</p>
        {commands.length > 0 && <p>{t('domain.nextStepCommands')} {commands.map((command, index) => <span key={command}>
            {index > 0 && ', '}<code className="rounded bg-surface-muted px-1 py-0.5 text-xs">{command}</code></span>)}</p>}
    </div>;
};
