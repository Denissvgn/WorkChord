import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { AgentTeamMaster, AgentTeamMemberSpec, AgentTeamMemberStatus } from '../../types/agent';
import { RUNTIME_PRODUCT_NAMES, credentialFilename, runtimeOfMember, runtimeSnippet } from '../../features/agentTeamSetup/connectAgent';
import { Button } from '../common/Button';
import { RuntimeIdentity } from './RuntimeIdentity';

const P = 'agentTeamSetup.connect';

/** The credential file name for a member, from its public reference; null until the digest is ready. */
const useCredentialFilename = (member: AgentTeamMemberSpec) => {
    const { credential_ref: ref, actor_key: key } = member;
    const [named, setNamed] = useState<{ ref: string; key: string; filename: string } | null>(null);
    useEffect(() => {
        let live = true;
        void credentialFilename({ credential_ref: ref, actor_key: key }).then(filename => { if (live) setNamed({ ref, key, filename }); });
        return () => { live = false; };
    }, [ref, key]);
    // A name computed for another member is never shown for this one.
    return named && named.ref === ref && named.key === key ? named.filename : null;
};

/**
 * What the Connect steps show once a member exists: the credential file, the skill package, the runtime
 * snippet, the handoff and the acknowledgement state. Connect and the agent's drawer render this same view.
 */
export const ConnectionSteps = ({ manifest, member, memberStatus, connected, checking = false, onCheck }: {
    manifest: AgentTeamMaster;
    member: AgentTeamMemberSpec;
    memberStatus: AgentTeamMemberStatus | undefined;
    connected: boolean;
    checking?: boolean;
    onCheck: () => void;
}) => {
    const { t } = useTranslation();
    const runtime = runtimeOfMember(member);
    const runtimeName = RUNTIME_PRODUCT_NAMES[runtime] ?? t(`${P}.runtimes.${runtime}`);
    const filename = useCredentialFilename(member);

    return <>
        <p role="status" className="font-medium">{connected ? t(`${P}.connected`) : t(`${P}.waiting`)}</p>
        <dl className="space-y-3 text-sm">
            <div><dt className="text-content-secondary">{t(`${P}.sinkRef`)}</dt><dd className="break-all font-mono">{manifest.credential_sink_ref}</dd></div>
            <div><dt className="text-content-secondary">{t(`${P}.sinkFile`)}</dt><dd className="break-all font-mono">{filename ?? ''}</dd></div>
            <div>
                <dt className="text-content-secondary">{t(`${P}.packageToInstall`)}</dt>
                <dd>{t(`${P}.packageName`, { name: member.skill_package.name, version: member.skill_package.version })}</dd>
                <dd className="break-all font-mono text-xs">{t(`${P}.packageDigest`, { digest: member.skill_package.sha256 })}</dd>
            </div>
            {memberStatus?.configured && <RuntimeIdentity identity={memberStatus.runtime_identity} />}
        </dl>
        <p className="text-sm text-content-secondary">{t(`${P}.hostNote`)}</p>
        <pre aria-label={t(`${P}.snippetLabel`, { runtime: runtimeName })} className="overflow-x-auto rounded-md border border-border bg-surface-muted p-4 text-xs">
            <code>{filename ? runtimeSnippet(runtime, manifest.server_url, filename) : ''}</code>
        </pre>
        <p className="text-sm">{t(`${P}.installNote`)}</p>
        {memberStatus?.handoff && <details>
            <summary className="cursor-pointer text-sm">{t(`${P}.handoff`)}</summary>
            <pre className="mt-2 overflow-x-auto rounded-md border border-border p-3 text-xs">{JSON.stringify(memberStatus.handoff, null, 2)}</pre>
        </details>}
        {!connected && <Button variant="secondary" disabled={checking} onClick={onCheck}>{t(`${P}.checkConnection`)}</Button>}
    </>;
};
