import { useTranslation } from 'react-i18next';
import type { AgentModelCatalogEntry } from '../../types/agent';
import { formatDateTime } from '../../utils/formatDate';
import { Button } from '../common/Button';

export function ModelCatalog({ entries, canAdminister, busy, onEdit, onToggle }: {
    entries: AgentModelCatalogEntry[]; canAdminister: boolean; busy: boolean;
    onEdit: (entry: AgentModelCatalogEntry) => void; onToggle: (entry: AgentModelCatalogEntry) => void;
}) {
    const { t } = useTranslation();
    return <div className="overflow-x-auto"><table className="w-full text-left text-sm">
        <thead><tr>{['configuredAlias', 'provider', 'reasoningTier', 'effort', 'contextTier', 'costTier', 'latencyTier', 'lastVerified'].map(key => <th className="p-2" key={key}>{t(`modelAdministration.${key}`)}</th>)}<th className="p-2">{t('taskEditor.status')}</th><th className="p-2">{t('actions.edit')}</th></tr></thead>
        <tbody>{entries.map(entry => <tr key={entry.id} className="border-t border-border">
            <td className="p-2">{entry.configured_model_alias}<div className="text-xs text-content-secondary">{entry.key}</div></td><td className="p-2">{entry.provider}</td><td className="p-2">{entry.reasoning_tier}</td><td className="p-2">{t(`modelAdministration.effort_${entry.effort}`)}</td><td className="p-2">{entry.context_tier}</td><td className="p-2">{entry.cost_tier}{entry.local_first && <div className="text-xs text-content-secondary">{t('modelAdministration.localFirst')}</div>}</td><td className="p-2">{entry.latency_tier}</td><td className="p-2">{entry.last_verified_at ? formatDateTime(entry.last_verified_at) : t('modelAdministration.neverVerified')}</td><td className="p-2">{entry.enabled ? t('common.enabled') : t('common.disabled')}</td>
            <td className="p-2">{canAdminister && <div className="flex gap-2"><Button size="sm" variant="secondary" disabled={busy} onClick={() => onEdit(entry)} aria-label={t('modelAdministration.editCatalogAction', { alias: entry.configured_model_alias })}>{t('actions.edit')}</Button><Button size="sm" variant="outline" disabled={busy} onClick={() => onToggle(entry)} aria-label={t(entry.enabled ? 'modelAdministration.disableCatalogAction' : 'modelAdministration.enableCatalogAction', { alias: entry.configured_model_alias })}>{t(entry.enabled ? 'common.disable' : 'common.enable')}</Button></div>}</td>
        </tr>)}</tbody>
    </table></div>;
}
