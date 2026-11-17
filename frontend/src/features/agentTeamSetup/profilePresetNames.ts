/**
 * Display names of the agent profile presets the server creates a profile from.
 * The preset read needs an agent key, which the operator does not have while
 * connecting the first agent, so Connect names the profile from this table.
 * A test compares it with the server's preset list.
 */
export const AGENT_PROFILE_PRESET_NAMES: Readonly<Record<string, string>> = {
    'pm-planning-agent': 'PM Planning Agent',
    'project-control-agent': 'Project Control Agent',
    'iteration-control-agent': 'Iteration Control Agent',
    'backend-implementation-agent': 'Backend Implementation Agent',
    'go-rust-agent-developer': 'Go And Rust Systems Agent',
    'frontend-implementation-agent': 'Frontend Implementation Agent',
    'qa-verification-agent': 'QA Verification Agent',
    'docs-wiki-agent': 'Documentation Agent',
    'release-ops-agent': 'Release And Operations Agent',
    'ux-ui-design-agent': 'UX/UI Design Agent',
    'delivery-forecast-agent': 'Delivery Forecast Agent',
    'security-scope-agent': 'Security And Scope Agent',
};
