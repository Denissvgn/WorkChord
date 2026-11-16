import type { AgentTeamMaster, AgentTeamMemberSpec, AgentTeamRole, AgentTeamStatus } from '../../types/agent';
import { assertAgentTeamMasterSecretFree } from './manifest';

export type AgentRuntime = 'claude-code' | 'codex' | 'antigravity' | 'pi' | 'other';
export const runtimeNames: Record<AgentRuntime, string> = {
    'claude-code': 'Claude Code', codex: 'Codex', antigravity: 'Antigravity', pi: 'Pi with a local model', other: 'Other',
};
export const roleNames: Record<AgentTeamRole, string> = { pm: 'PM', worker: 'Worker', verifier: 'Reviewer' };
export const teamMembers = (manifest: AgentTeamMaster) => [manifest.controller, ...manifest.workers, ...manifest.verifiers];
export const hasPM = (current: AgentTeamMaster | null, status: AgentTeamStatus) => Boolean(
    current?.controller || status.members.some(member => member.role === 'pm' && member.configured),
);

export function buildConnectedMember(
    points: { current: AgentTeamMaster | null; template: AgentTeamMaster },
    status: AgentTeamStatus, role: AgentTeamRole, runtime: AgentRuntime, model: string,
): { manifest: AgentTeamMaster; member: AgentTeamMemberSpec } {
    const manifest = structuredClone(points.current ?? points.template);
    const source = role === 'pm' ? points.template.controller
        : role === 'worker' ? points.template.workers[0] : points.template.verifiers[0];
    if (!source || (role === 'pm' && hasPM(points.current, status))) throw new Error('role_unavailable');
    const occupied = new Set([...teamMembers(manifest).map(member => member.actor_key), ...status.members.map(member => member.actor_key)]);
    let index = 1;
    while (occupied.has(`${runtime}-${role}-${index}`)) index += 1;
    const key = `${runtime}-${role}-${index}`;
    const member: AgentTeamMemberSpec = {
        ...structuredClone(source), actor_key: key, actor_name: `workchord-${key}`,
        display_name: `${runtimeNames[runtime]} ${roleNames[role]} ${index}`,
        runtime_ref: `runtime://${runtime}/${key}`, credential_ref: `${manifest.credential_sink_ref}/${key}`,
        model_binding_keys: [model], default_model_binding_key: model,
    };
    if (role === 'pm') manifest.controller = member;
    else if (role === 'worker') manifest.workers.push(member);
    else manifest.verifiers.push(member);
    assertAgentTeamMasterSecretFree(manifest);
    return { manifest, member };
}

// Matches the existing filesystem apply sink; this hashes a public reference, never a key.
export async function credentialFilename(member: AgentTeamMemberSpec): Promise<string> {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(member.credential_ref));
    return `${Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('').slice(0, 24)}-${member.actor_key}.json`;
}

const shellQuote = (value: string) => `'${value.replaceAll("'", "'\\''")}'`;
export function runtimeSnippet(runtime: AgentRuntime, server: string, filename: string): string {
    const setup = [
        'set +x',
        `export WORKCHORD_BASE_URL=${shellQuote(server)}`,
        `: "\${WORKCHORD_CREDENTIAL_DIR:?Set this to the private credential folder on the runtime host}"`,
        `export AGENT_API_KEY="$(jq -er '.api_key' "$WORKCHORD_CREDENTIAL_DIR/${filename}")"`,
    ].join('\n');
    if (runtime === 'codex') return `${setup}\nexport WORKCHORD_AGENT_KEY="$AGENT_API_KEY"\ncodex\n\n# Add to ~/.codex/config.toml before starting Codex:\n# [mcp_servers.workchord]\n# url = ${JSON.stringify(`${server.replace(/\/$/, '')}/api/mcp`)}\n# bearer_token_env_var = "WORKCHORD_AGENT_KEY"`;
    if (runtime === 'claude-code') return `${setup}\nclaude`;
    if (runtime === 'pi') return `${setup}\n# Start Pi with your configured local provider and selected model.\npi`;
    return `${setup}\n# Run this in ${runtime === 'antigravity' ? "Antigravity’s agent terminal" : "your runtime’s private terminal"}.\n# The installed role skill uses WORKCHORD_BASE_URL and AGENT_API_KEY for REST.`;
}

export interface ConnectIssue { step: number; message: string; code: string }
export function connectIssue(code: string, path = ''): ConnectIssue {
    const target = `${path} ${code}`;
    const step = /model|binding/.test(target) ? 2 : /runtime|credential|sink|server_url/.test(target) ? 1
        : /role|profile|scope|package|assignment_mode/.test(target) ? 0 : 3;
    const message = /credential_sink/.test(code) ? 'The server credential folder is unavailable. Ask the operator to configure it, then review again.'
        : /revision|stale|digest/.test(code) ? 'The team changed. Review again to get the current plan.'
        : step === 2 ? 'This model cannot be used. Choose an enabled catalog model, then review again.'
        : step === 1 ? 'This runtime setup cannot be used. Check the runtime and server configuration, then review again.'
        : step === 0 ? 'This role configuration is unavailable. Choose another role or check its profile and skill package in Advanced.'
        : 'The server could not approve this change. Review again, or inspect the team in Advanced.';
    return { step, message, code: /^[a-zA-Z0-9_.-]{1,100}$/.test(code) ? code : 'request_failed' };
}
