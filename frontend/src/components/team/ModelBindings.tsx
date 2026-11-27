import { useTranslation } from 'react-i18next';
import type { AgentModelBinding, AgentModelCatalogEntry } from '../../types/agent';
import { Button } from '../common/Button';

export function ModelBindings({ bindings, actorNames, catalog, canAdminister, busy, onEdit, onToggle }: {
    bindings: AgentModelBinding[]; actorNames: Map<number, string>; catalog: Map<number, AgentModelCatalogEntry>;
    canAdminister: boolean; busy: boolean; onEdit: (binding: AgentModelBinding) => void; onToggle: (binding: AgentModelBinding) => void;
}) {
    const { t } = useTranslation();
    return <div className="overflow-x-auto"><table className="w-full text-left text-sm">
        <thead><tr>{['actor', 'catalogEntry', 'tools', 'dataPolicy', 'default'].map(key => <th className="p-2" key={key}>{t(`modelAdministration.${key}`)}</th>)}<th className="p-2">{t('taskEditor.status')}</th><th className="p-2">{t('actions.edit')}</th></tr></thead>
        <tbody>{bindings.map(binding => {
            const actor = actorNames.get(binding.actor_id) ?? String(binding.actor_id);
            const model = binding.model_catalog?.configured_model_alias ?? catalog.get(binding.model_catalog_id)?.configured_model_alias ?? binding.model_catalog_key ?? String(binding.model_catalog_id);
            const effort = binding.model_catalog?.effort ?? catalog.get(binding.model_catalog_id)?.effort;
            return <tr key={binding.id} className="border-t border-border"><td className="p-2">{actor}</td><td className="p-2">{model}{effort && <div className="text-xs text-content-secondary">{t('modelAdministration.effort')}: {t(`modelAdministration.effort_${effort}`)}</div>}</td><td className="p-2">{binding.tool_tags.join(', ') || t('common.none')}</td><td className="p-2">{binding.data_policy_tags.join(', ') || t('common.none')}</td><td className="p-2">{t(binding.is_default ? 'common.yes' : 'common.no')}</td><td className="p-2">{t(binding.enabled ? 'common.enabled' : 'common.disabled')}</td><td className="p-2">{canAdminister && <div className="flex gap-2"><Button size="sm" variant="secondary" disabled={busy} onClick={() => onEdit(binding)} aria-label={t('modelAdministration.editBindingAction', { actor, model })}>{t('actions.edit')}</Button><Button size="sm" variant="outline" disabled={busy} onClick={() => onToggle(binding)} aria-label={t(binding.enabled ? 'modelAdministration.disableBindingAction' : 'modelAdministration.enableBindingAction', { actor, model })}>{t(binding.enabled ? 'common.disable' : 'common.enable')}</Button></div>}</td></tr>;
        })}</tbody>
    </table></div>;
}
