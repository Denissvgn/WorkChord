import { Bot, KeyRound } from 'lucide-react';
import { useTranslation } from 'react-i18next';

/** The two keys by the names used everywhere: what each unlocks and how to get it. */
export const AccessKeysSummary = () => {
    const { t } = useTranslation();
    const keys = [
        { id: 'admin', icon: KeyRound },
        { id: 'agent', icon: Bot },
    ] as const;
    return (
        <section className="card card-pad space-y-3" aria-labelledby="access-keys-title">
            <h3 id="access-keys-title" className="text-base font-semibold">{t('settingsPage.access.title')}</h3>
            <p className="text-sm text-content-secondary">{t('settingsPage.access.withoutKey')}</p>
            <dl className="grid gap-4 md:grid-cols-2">
                {keys.map(({ id, icon: Icon }) => (
                    <div key={id} className="space-y-1">
                        <dt className="flex items-center gap-2 font-semibold"><Icon aria-hidden="true" className="h-4 w-4" />{t(`settingsPage.access.${id}Name`)}</dt>
                        <dd className="m-0 text-sm">{t(`settingsPage.access.${id}Unlocks`)}</dd>
                        <dd className="m-0 text-sm text-content-secondary">{t(`settingsPage.access.${id}HowToGet`)}</dd>
                    </div>
                ))}
            </dl>
        </section>
    );
};
