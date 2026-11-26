import { useTranslation } from 'react-i18next';
import type { AgentTeamRuntimeIdentityStatus } from '../../types/agent';
import { formatDateTime } from '../../utils/formatDate';

const P = 'agentTeamSetup.runtimeIdentity';

/**
 * Which runtime instance acknowledged an agent's handoff. A change of identity and a refused identity are
 * stated with the identities involved, so a second runtime taking the same seat is never silent.
 */
export const RuntimeIdentity = ({ identity, className }: { identity: AgentTeamRuntimeIdentityStatus | undefined; className?: string }) => {
    const { t, i18n } = useTranslation();
    const state = identity?.state ?? 'unknown';
    return <div className={className} data-runtime-identity={state}>
        <dt className="text-content-secondary">{t(`${P}.title`)}</dt>
        <dd>
            {t(`${P}.states.${state}`)}
            {identity?.acknowledged_instance_id && <span className="block break-all font-mono text-xs">{identity.acknowledged_instance_id}</span>}
            {state === 'changed' && identity?.previous_instance_id && identity.changed_at && <span className="block break-all text-xs">
                {t(`${P}.changedFrom`, { id: identity.previous_instance_id, at: formatDateTime(identity.changed_at, i18n.language) })}
            </span>}
            {state === 'refused' && identity?.refused_instance_id && identity.refused_at && <span className="block break-all text-xs">
                {t(`${P}.refused`, { id: identity.refused_instance_id, at: formatDateTime(identity.refused_at, i18n.language) })}
            </span>}
        </dd>
    </div>;
};
