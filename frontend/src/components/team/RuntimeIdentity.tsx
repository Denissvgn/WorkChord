import { useTranslation } from 'react-i18next';
import type { AgentTeamRuntimeIdentityStatus } from '../../types/agent';
import { formatDateTime } from '../../utils/formatDate';

const P = 'agentTeamSetup.runtimeIdentity';

/**
 * Which runtime instance acknowledged an agent's handoff. A change of identity, an acknowledgement under an
 * earlier identity and a refused identity are stated with the identities involved, so a second runtime taking
 * the same seat is never silent. A member that never acknowledged is labelled so, not as an unsent identity.
 */
export const RuntimeIdentity = ({ identity, acknowledgementState }: {
    identity: AgentTeamRuntimeIdentityStatus | undefined;
    acknowledgementState?: 'missing' | 'current' | 'stale';
}) => {
    const { t, i18n } = useTranslation();
    const state = identity?.state ?? 'unknown';
    const label = state === 'unknown' && acknowledgementState === 'missing' ? 'notAcknowledged' : state;
    return <div data-runtime-identity={state}>
        <dt className="text-content-secondary">{t(`${P}.title`)}</dt>
        <dd>
            {t(`${P}.states.${label}`)}
            {identity?.acknowledged_instance_id && <span className="block break-all font-mono text-xs">{identity.acknowledged_instance_id}</span>}
            {state === 'changed' && identity?.previous_instance_id && identity.changed_at && <span className="block break-all text-xs">
                {t(`${P}.changedFrom`, { id: identity.previous_instance_id, at: formatDateTime(identity.changed_at, i18n.language) })}
            </span>}
            {state === 'stale' && identity?.expected_instance_id && <span className="block break-all text-xs">
                {t(`${P}.staleExpected`, { id: identity.expected_instance_id })}
            </span>}
            {identity?.refused_instance_id && identity.refused_at && <span className="block break-all text-xs" data-runtime-refused>
                {t(`${P}.refused`, { id: identity.refused_instance_id, at: formatDateTime(identity.refused_at, i18n.language) })}
            </span>}
        </dd>
    </div>;
};
