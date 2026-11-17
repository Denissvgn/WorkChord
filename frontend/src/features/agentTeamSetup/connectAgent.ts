import axios from 'axios';
import type { AgentTeamMaster, AgentTeamMemberSpec, AgentTeamRole, AgentTeamStatus } from '../../types/agent';
import { assertAgentTeamMasterSecretFree } from './manifest';

export const AGENT_RUNTIMES = ['claude-code', 'codex', 'antigravity', 'pi', 'other'] as const;
export type AgentRuntime = (typeof AGENT_RUNTIMES)[number];
/** Product names are not translated; the other runtimes take their label from the catalog. */
export const RUNTIME_PRODUCT_NAMES: Partial<Record<AgentRuntime, string>> = { 'claude-code': 'Claude Code', codex: 'Codex', antigravity: 'Antigravity' };

/** Stored with the new member, so the record reads the same in every interface language. */
const runtimeRecordNames: Record<AgentRuntime, string> = {
    'claude-code': 'Claude Code', codex: 'Codex', antigravity: 'Antigravity', pi: 'Pi', other: 'Agent',
};
const roleRecordNames: Record<AgentTeamRole, string> = { pm: 'PM', worker: 'Worker', verifier: 'Reviewer' };

const teamMembers = (manifest: AgentTeamMaster) => [manifest.controller, ...manifest.workers, ...manifest.verifiers];

/** A declared member the server reports as not configured: kept in the manifest but never created. */
const isPending = (key: string, status: AgentTeamStatus) => status.members.some(item => item.actor_key === key && !item.configured);

/**
 * The manifest allows one PM, so PM is offered only while the team has none. A PM
 * that is declared but never configured (for example one a template declared) is
 * not a PM yet; connecting a PM replaces it.
 */
export const hasPM = (current: AgentTeamMaster | null, status: AgentTeamStatus) => Boolean(
    status.members.some(member => member.role === 'pm' && member.configured)
    || (current?.controller && !isPending(current.controller.actor_key, status)),
);

/** True when connecting a PM replaces a declared PM that was never configured. */
export const replacesPendingPM = (current: AgentTeamMaster | null, status: AgentTeamStatus) => Boolean(
    current?.controller && isPending(current.controller.actor_key, status),
);

/**
 * Builds the manifest the server would hold after adding one member: the current
 * topology unchanged plus the new member. A team without a topology starts from the
 * server template, whose members of the chosen role the new member replaces.
 *
 * `previousAttempt` is the member an earlier, unsuccessful connect sent. The server
 * keeps the manifest of a blocked apply, so that member can be declared but never
 * configured; it is dropped here instead of being left beside the new one.
 */
export function buildConnectedMember(
    points: { current: AgentTeamMaster | null; template: AgentTeamMaster },
    status: AgentTeamStatus, role: AgentTeamRole, runtime: AgentRuntime, model: string, previousAttempt?: string,
): { manifest: AgentTeamMaster; member: AgentTeamMemberSpec } {
    const manifest = structuredClone(points.current ?? points.template);
    const source = role === 'pm' ? points.template.controller
        : role === 'worker' ? points.template.workers[0] : points.template.verifiers[0];
    if (!source || (role === 'pm' && hasPM(points.current, status))) throw new Error('role_unavailable');
    if (!points.current) {
        if (role === 'worker') manifest.workers = [];
        if (role === 'verifier') manifest.verifiers = [];
    }
    const dropped = previousAttempt && isPending(previousAttempt, status) ? previousAttempt : null;
    if (dropped) {
        manifest.workers = manifest.workers.filter(item => item.actor_key !== dropped);
        manifest.verifiers = manifest.verifiers.filter(item => item.actor_key !== dropped);
    }
    const occupied = new Set([...teamMembers(manifest).map(member => member.actor_key), ...status.members.map(member => member.actor_key)]);
    if (dropped && !teamMembers(manifest).some(item => item.actor_key === dropped)) occupied.delete(dropped);
    let index = 1;
    while (occupied.has(`${runtime}-${role}-${index}`)) index += 1;
    const key = `${runtime}-${role}-${index}`;
    const member: AgentTeamMemberSpec = {
        ...structuredClone(source), role, actor_key: key, actor_name: `workchord-${key}`,
        display_name: `${runtimeRecordNames[runtime]} ${roleRecordNames[role]} ${index}`,
        runtime_ref: `runtime://${runtime}/${key}`, credential_ref: `${manifest.credential_sink_ref}/${key}`,
        model_binding_keys: [model], default_model_binding_key: model,
    };
    if (role === 'pm') manifest.controller = member;
    else if (role === 'worker') manifest.workers.push(member);
    else manifest.verifiers.push(member);
    assertAgentTeamMasterSecretFree(manifest);
    return { manifest, member };
}

/**
 * The name the server's filesystem credential sink gives this member's file:
 * the first 24 hex digits of SHA-256 over the public credential reference, then
 * the actor key. Only the public reference is hashed; no key is involved.
 */
export async function credentialFilename(member: AgentTeamMemberSpec): Promise<string> {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(member.credential_ref));
    return `${Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('').slice(0, 24)}-${member.actor_key}.json`;
}

const shellQuote = (value: string) => `'${value.replaceAll("'", "'\\''")}'`;

/** Shell setup for the runtime host: the key is read from the delivered file, never written here. */
export function runtimeSnippet(runtime: AgentRuntime, server: string, filename: string): string {
    const base = server.replace(/\/$/, '');
    const setup = [
        'set +x',
        `export WORKCHORD_BASE_URL=${shellQuote(base)}`,
        ': "${WORKCHORD_CREDENTIAL_DIR:?Set this to the private credential folder on the runtime host}"',
        `export AGENT_API_KEY="$(jq -er '.api_key' "$WORKCHORD_CREDENTIAL_DIR/${filename}")"`,
    ];
    if (runtime === 'codex') return [
        '# Add to ~/.codex/config.toml once:',
        '# [mcp_servers.workchord]',
        `# url = ${JSON.stringify(`${base}/api/mcp`)}`,
        '# bearer_token_env_var = "AGENT_API_KEY"',
        ...setup, 'codex',
    ].join('\n');
    if (runtime === 'claude-code') return [...setup, 'claude'].join('\n');
    if (runtime === 'pi') return [...setup, '# Start Pi with the local provider and model chosen above.', 'pi'].join('\n');
    return [
        ...setup,
        runtime === 'antigravity' ? '# Run this in the Antigravity agent terminal.' : "# Run this in the runtime's private terminal.",
        '# The installed role skill reads WORKCHORD_BASE_URL and AGENT_API_KEY.',
    ].join('\n');
}

/** Steps of the guided connection, in order. */
export const CONNECT_STEPS = ['role', 'runtime', 'model', 'review', 'connect'] as const;
export const STEP_INDEX = { role: 0, runtime: 1, model: 2, review: 3, connect: 4 } as const;

type ConnectIssueReason = 'role' | 'runtime' | 'model' | 'sink' | 'teamChanged' | 'unavailable' | 'other'
    | 'applyUnconfirmed' | 'deliveryUncertain';
export interface ConnectIssue { step: number; reason: ConnectIssueReason; code: string }

/** Places a server code beside the answer that caused it, with a plain-language reason. */
export function connectIssue(code: string, path = ''): ConnectIssue {
    const target = `${path} ${code}`;
    const safeCode = /^[a-zA-Z0-9_.-]{1,100}$/.test(code) ? code : 'request_failed';
    if (/credential|sink/.test(target)) return { step: STEP_INDEX.review, reason: 'sink', code: safeCode };
    if (/revision|stale_plan|digest|conflict/.test(target)) return { step: STEP_INDEX.review, reason: 'teamChanged', code: safeCode };
    if (/model|binding/.test(target)) return { step: STEP_INDEX.model, reason: 'model', code: safeCode };
    if (/runtime/.test(target)) return { step: STEP_INDEX.runtime, reason: 'runtime', code: safeCode };
    if (/role|profile|scope|package|assignment_mode/.test(target)) return { step: STEP_INDEX.role, reason: 'role', code: safeCode };
    return { step: STEP_INDEX.review, reason: 'other', code: safeCode };
}

/**
 * Whether a failed apply request may still have been carried out. Without a server
 * answer, on a timeout, a rate limit or a server error it may have run, so the same
 * request (same idempotency key) is retried to read its receipt. Any other 4xx answer
 * is a definite rejection: nothing was applied, and the change is reviewed again.
 */
export function applyOutcomeUnknown(error: unknown): boolean {
    const code = axios.isAxiosError(error) ? error.response?.status : undefined;
    return code === undefined || code === 408 || code === 429 || code >= 500;
}
