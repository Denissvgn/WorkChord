import i18n from './i18n';
import type { GitHubStatusAutomationRule } from '../types/github';
import type { Label, LabelGroup } from '../types/label';
import type { SavedView, SavedViewDashboardCard } from '../types/savedView';
import type { WorkTemplate } from '../types/template';

interface TemplateSeedBaseline {
    name: string;
    description: string;
    default_title: string;
    default_description: string;
    default_checklist: string[];
}

const templateBaselines: Record<string, TemplateSeedBaseline> = {
    task_feature: {
        name: 'Feature',
        description: 'Default template for new product capability work.',
        default_title: 'Implement feature',
        default_description: 'Define the user-facing behavior, implement the feature, and verify the outcome.',
        default_checklist: ['Confirm acceptance criteria', 'Implement the scoped behavior', 'Add or update tests'],
    },
    task_bug: {
        name: 'Bug',
        description: 'Default template for defect investigation and fixes.',
        default_title: 'Fix bug',
        default_description: 'Reproduce the defect, identify the cause, implement the fix, and verify the regression path.',
        default_checklist: ['Reproduce', 'Fix', 'Verify'],
    },
    task_technical_task: {
        name: 'Technical task',
        description: 'Default template for maintenance, refactoring, or internal engineering work.',
        default_title: 'Complete technical task',
        default_description: 'Make the internal change while preserving existing behavior and tests.',
        default_checklist: ['Confirm scope', 'Make the change', 'Run relevant checks'],
    },
    task_risk_blocker: {
        name: 'Risk / blocker',
        description: 'Default template for urgent work that blocks delivery or reduces major risk.',
        default_title: 'Resolve blocker',
        default_description: 'Describe the blocked outcome, current impact, mitigation plan, and owner.',
        default_checklist: ['Identify impacted work', 'Choose mitigation', 'Confirm unblock criteria'],
    },
    task_release_task: {
        name: 'Release task',
        description: 'Default template for release preparation and verification.',
        default_title: 'Prepare release task',
        default_description: 'Complete the release step and verify the release criteria before handoff.',
        default_checklist: ['Confirm release scope', 'Complete release step', 'Verify outcome'],
    },
    task_agent_ready: {
        name: 'Agent-ready task',
        description: 'Default template for scoped work that an agent can execute safely.',
        default_title: 'Agent-ready task',
        default_description: 'Provide exact scope, constraints, expected files or modules, and verification commands.',
        default_checklist: ['State the implementation boundary', 'List required checks', 'Document expected output'],
    },
    triage_customer_request: {
        name: 'Customer request',
        description: 'Default template for customer-originated intake.',
        default_title: 'Customer request',
        default_description: 'Capture the customer need, source context, impact, and expected outcome.',
        default_checklist: ['Link source conversation', 'Identify affected customer', 'Clarify expected outcome'],
    },
};

const labelGroupBaselines: Record<string, { name: string; description: string }> = {
    group_type: { name: 'Type', description: 'Work classification labels.' },
    group_area: { name: 'Area', description: 'Product or engineering area labels.' },
    group_risk: { name: 'Risk', description: 'Delivery risk and review labels.' },
    group_source: { name: 'Source', description: 'Intake origin labels.' },
    group_capability: { name: 'Capability', description: 'Agent capability labels.' },
};

const labelBaselines: Record<string, string> = {
    label_feature: 'Feature',
    label_bug: 'Bug',
    label_chore: 'Chore',
    label_incident: 'Incident',
    label_research: 'Research',
    label_release: 'Release',
    label_request: 'Request',
    label_backend: 'Backend',
    label_frontend: 'Frontend',
    label_scheduling: 'Scheduling',
    label_analytics: 'Analytics',
    label_integrations: 'Integrations',
    label_blocked: 'Blocked',
    label_risky: 'Risky',
    label_needs_review: 'Needs review',
    label_customer: 'Customer',
    label_internal: 'Internal',
    label_agent: 'Agent',
    label_import: 'Import',
    label_cap_docs: 'Docs',
    label_cap_code: 'Code',
    label_cap_test: 'Test',
    label_cap_research: 'Research',
};

const savedViewBaselines: Record<string, { name: string; description: string }> = {
    triage_needs_triage: { name: 'Needs triage', description: 'New intake items that need review.' },
    tasks_unassigned: { name: 'Unassigned', description: 'Tasks without an assigned owner.' },
    tasks_blocked: { name: 'Blocked', description: 'Tasks tagged as blocked.' },
    tasks_overdue: { name: 'Overdue', description: 'Tasks currently marked as overdue.' },
    tasks_high_priority: { name: 'High priority', description: 'Priority 1 tasks.' },
    tasks_ready_for_agent: { name: 'Ready for agent', description: 'Tasks that satisfy explicit agent-readiness criteria.' },
    tasks_active_this_iteration: { name: 'Active this iteration', description: 'Active tasks in the selected iteration.' },
    projects_at_risk: { name: 'At risk projects', description: 'Projects with at-risk health.' },
};

const githubRuleBaselines = [
    {
        seedKey: 'pr_opened_starts_work',
        name: 'PR opened starts work',
        description: 'When a linked pull request opens, move a planned task to active.',
        github_event_type: 'github_pr_opened',
        from_status: 'planned',
        target_status: 'active',
        reason_template: 'GitHub automation: {github_event_type} for {repo} PR #{pr_number}',
    },
    {
        seedKey: 'pr_merged_resolves_work',
        name: 'PR merged resolves work',
        description: 'When a linked pull request is merged, move an active task to resolved.',
        github_event_type: 'github_pr_merged',
        from_status: 'active',
        target_status: 'resolved',
        reason_template: 'GitHub automation: {github_event_type} for {repo} PR #{pr_number}',
    },
];

const seedText = (key: string, fallback: string) => (
    i18n.t(`seedDisplay.${key}`, { defaultValue: fallback })
);

const localizeIfBaseline = (value: string | null | undefined, baseline?: string, key?: string) => (
    value && baseline && key && value === baseline ? seedText(key, value) : value
);

export const labelGroupDisplay = (group: LabelGroup | { seed_key?: string | null; name: string; description?: string | null }) => {
    const baseline = group.seed_key ? labelGroupBaselines[group.seed_key] : undefined;
    return {
        name: localizeIfBaseline(group.name, baseline?.name, `labelGroups.${group.seed_key}.name`) ?? group.name,
        description: localizeIfBaseline(group.description, baseline?.description, `labelGroups.${group.seed_key}.description`) ?? group.description,
    };
};

export const labelDisplay = (label: Label | { seed_key?: string | null; name: string; description?: string | null }) => {
    const baseline = label.seed_key ? labelBaselines[label.seed_key] : undefined;
    return {
        name: localizeIfBaseline(label.name, baseline, `labels.${label.seed_key}.name`) ?? label.name,
        description: label.description,
    };
};

export const templateDisplay = (template: WorkTemplate) => {
    const baseline = template.seed_key ? templateBaselines[template.seed_key] : undefined;
    return {
        name: localizeIfBaseline(template.name, baseline?.name, `templates.${template.seed_key}.name`) ?? template.name,
        description: localizeIfBaseline(template.description, baseline?.description, `templates.${template.seed_key}.description`) ?? template.description,
        default_title: localizeIfBaseline(template.default_title, baseline?.default_title, `templates.${template.seed_key}.default_title`) ?? template.default_title,
        default_description: localizeIfBaseline(template.default_description, baseline?.default_description, `templates.${template.seed_key}.default_description`) ?? template.default_description,
        default_checklist: template.default_checklist.map((item, index) => (
            baseline?.default_checklist[index] === item
                ? seedText(`templates.${template.seed_key}.default_checklist.${index}`, item)
                : item
        )),
    };
};

export const savedViewDisplay = (view: SavedView | SavedViewDashboardCard) => {
    const baseline = view.seed_key ? savedViewBaselines[view.seed_key] : undefined;
    return {
        name: localizeIfBaseline(view.name, baseline?.name, `savedViews.${view.seed_key}.name`) ?? view.name,
        description: localizeIfBaseline(view.description, baseline?.description, `savedViews.${view.seed_key}.description`) ?? view.description,
    };
};

export const githubRuleDisplay = (rule: GitHubStatusAutomationRule) => {
    const baseline = githubRuleBaselines.find(candidate => (
        rule.name === candidate.name &&
        rule.description === candidate.description &&
        rule.github_event_type === candidate.github_event_type &&
        rule.from_status === candidate.from_status &&
        rule.target_status === candidate.target_status &&
        rule.reason_template === candidate.reason_template
    ));
    return {
        name: localizeIfBaseline(rule.name, baseline?.name, `githubRules.${baseline?.seedKey}.name`) ?? rule.name,
        description: localizeIfBaseline(rule.description, baseline?.description, `githubRules.${baseline?.seedKey}.description`) ?? rule.description,
        reason_template: localizeIfBaseline(rule.reason_template, baseline?.reason_template, `githubRules.${baseline?.seedKey}.reason_template`) ?? rule.reason_template,
    };
};
