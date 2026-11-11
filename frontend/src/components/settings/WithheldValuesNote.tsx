import { EyeOff } from 'lucide-react';
import { useTranslation } from 'react-i18next';

/** Names the values the server left out because this browser has no admin key. */
export const WithheldValuesNote = ({ fields, labels }: { fields: string[] | undefined; labels: Record<string, string> }) => {
    const { t } = useTranslation();
    const names = [...new Set((fields ?? []).map(field => labels[field]).filter(Boolean))];
    if (names.length === 0) return null;
    return (
        <p className="flex items-start gap-2 rounded-md border border-border bg-surface-muted px-3 py-2 text-sm text-content-secondary">
            <EyeOff aria-hidden="true" className="mt-0.5 h-4 w-4 shrink-0" />
            <span>{t('settings.withheldValues', { names: names.join(', ') })}</span>
        </p>
    );
};
