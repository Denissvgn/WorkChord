import { useMemo } from 'react';
import { useTranslation } from 'react-i18next';

type Member = Record<string, unknown> & { skill_package?: { name?: string; version?: string } };

const asMembers = (value: unknown): Member[] => Array.isArray(value) ? value.filter((item): item is Member => Boolean(item) && typeof item === 'object') : [];

/** What the JSON describes, read beside it: the controller, workers and verifiers, and what each is missing. */
export const AgentTeamManifestPreview = ({ text }: { text: string }) => {
    const { t } = useTranslation();
    const parsed = useMemo(() => {
        try { return JSON.parse(text) as Record<string, unknown>; } catch { return null; }
    }, [text]);
    if (!parsed || typeof parsed !== 'object') {
        return <p className="text-sm text-content-secondary">{t('agentTeamSetup.preview.unreadable')}</p>;
    }
    const controller = parsed.controller && typeof parsed.controller === 'object' ? [parsed.controller as Member] : [];
    const groups = [
        ['controller', controller], ['workers', asMembers(parsed.workers)], ['verifiers', asMembers(parsed.verifiers)],
    ] as const;
    const required = ['actor_key', 'profile_key', 'runtime_ref', 'credential_ref', 'default_model_binding_key'];
    return (
        <section className="space-y-3" aria-labelledby="manifest-preview-title">
            <h4 id="manifest-preview-title" className="text-sm font-semibold">{t('agentTeamSetup.preview.title')}</h4>
            <p className="text-xs text-content-secondary">
                {t('agentTeamSetup.preview.topology', { key: String(parsed.topology_key ?? t('agentTeamSetup.preview.missing')) })}
            </p>
            {groups.map(([group, members]) => (
                <div key={group} className="space-y-1">
                    <h5 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">
                        {t(`agentTeamSetup.preview.${group}`, { count: members.length })}
                    </h5>
                    {members.length === 0
                        ? <p className="text-sm text-feedback-warning-foreground">{t('agentTeamSetup.preview.none')}</p>
                        : <ul className="space-y-1">{members.map((member, index) => {
                            const missing = required.filter(key => !member[key]);
                            return <li key={`${group}-${index}`} className="rounded-md border border-border px-2 py-1.5 text-sm">
                                <span className="font-medium">{String(member.display_name ?? member.actor_key ?? t('agentTeamSetup.preview.unnamed'))}</span>
                                <span className="block text-xs text-content-secondary">
                                    {[member.actor_key, member.skill_package?.name && `${member.skill_package.name} ${member.skill_package.version ?? ''}`.trim(), member.default_model_binding_key]
                                        .filter(Boolean).map(String).join(' · ')}
                                </span>
                                {missing.length > 0 && <span className="block text-xs text-feedback-warning-foreground">{t('agentTeamSetup.preview.missingFields', { fields: missing.join(', ') })}</span>}
                            </li>;
                        })}</ul>}
                </div>
            ))}
        </section>
    );
};
