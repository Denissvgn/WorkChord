import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';
import ts from 'typescript';

// Reviewed FE-08 inventory. Any count change requires reviewing the file's
// loading/error/retry/empty or pending/failure policy and updating this record.
export const REVIEWED_HOOK_COUNTS = {
    'src/features/timeEntries/useTimeEntries.ts': [1, 0],
    'src/components/tasks/TimeEntriesPanel.tsx': [3, 2],
    'src/components/projects/TimeEntriesReport.tsx': [1, 1],
    'src/components/tasks/PagedTaskBrowser.tsx': [1, 0],
    'src/pages/MyWorkPage.tsx': [4, 2],
    'src/components/tasks/TaskSearch.tsx': [1, 0],
    'src/components/tasks/TaskDiscussion.tsx': [4, 2],
    'src/components/tasks/PersonCapacity.tsx': [3, 2],
    'src/components/tasks/DeliveryDependencies.tsx': [4, 1],
    'src/components/tasks/BacklogPanel.tsx': [2, 0],
    'src/components/layout/CommandMenu.tsx': [1, 0],
    'src/components/dashboard/SavedViewDashboardCards.tsx': [1, 0],
    'src/components/gantt/GanttChart.tsx': [0, 2],
    'src/components/gantt/TaskEditModal.tsx': [2, 0],
    'src/components/iteration/IterationForm.tsx': [1, 3],
    'src/components/iteration/IterationList.tsx': [1, 1],
    'src/components/iteration/IterationSelector.tsx': [1, 0],
    'src/components/labels/LabelSelector.tsx': [2, 0],
    'src/components/notifications/NotificationsPanel.tsx': [2, 0],
    'src/components/projects/InitiativeForm.tsx': [1, 2],
    'src/components/projects/ProjectForm.tsx': [3, 2],
    'src/components/projects/ProjectIterationsSection.tsx': [1, 2],
    'src/components/releases/ReleaseForm.tsx': [1, 2],
    'src/components/requestSources/RequestSourceLinksPanel.tsx': [2, 3],
    'src/components/settings/EmailSettingsPanel.tsx': [1, 2],
    'src/components/settings/GitHubSettingsPanel.tsx': [1, 4],
    'src/components/settings/InterfaceLanguageSettings.tsx': [1, 1],
    'src/components/settings/OutboundWebhooksPanel.tsx': [2, 6],
    'src/components/settings/RuntimeConfigSettings.tsx': [1, 4],
    'src/components/settings/SchedulingRulesSettings.tsx': [1, 2],
    'src/components/settings/SystemHealthPanel.tsx': [1, 0],
    'src/components/settings/TemplateLabelSettings.tsx': [2, 9],
    'src/components/tasks/ImportTasksModal.tsx': [1, 1],
    'src/components/tasks/KanbanBoard/KanbanBoard.tsx': [3, 1],
    'src/components/tasks/SavedViewsControl.tsx': [2, 4],
    'src/components/tasks/StatusChangeControl.tsx': [0, 1],
    'src/components/tasks/TaskBulkOperationsPanel.tsx': [4, 1],
    'src/components/tasks/TaskDependencySelector.tsx': [1, 0],
    'src/components/tasks/TaskFiltersBar.tsx': [3, 0],
    'src/components/tasks/TaskForm.tsx': [6, 4],
    'src/components/tasks/TaskList.tsx': [3, 4],
    'src/components/tasks/TaskTextEditorModal.tsx': [1, 1],
    'src/components/tasks/TaskTimelinePanel.tsx': [2, 3],
    'src/components/team/AssigneeRecommendationsPanel.tsx': [1, 0],
    'src/components/team/ImportTeamModal.tsx': [0, 1],
    'src/components/team/TeamForm.tsx': [1, 2],
    'src/components/team/TeamList.tsx': [3, 1],
    'src/components/team/TeamProfileManager.tsx': [1, 6],
    'src/components/team/VacationManager.tsx': [0, 3],
    'src/i18n/SystemLanguageProvider.tsx': [1, 0],
    'src/components/layout/AppSidebar.tsx': [1, 0],
    'src/components/layout/AppTopNav.tsx': [1, 0],
    'src/features/planningMasters/usePlanningNavigationSummary.ts': [2, 0],
    'src/features/planningMasters/usePlanningReadiness.ts': [5, 0],
    'src/pages/AgentPipelinePage.tsx': [3, 0],
    'src/pages/AnalyticsPage.tsx': [2, 0],
    'src/pages/CalendarPage.tsx': [3, 8],
    'src/pages/GanttPage.tsx': [4, 3],
    'src/pages/OverviewPage.tsx': [2, 0],
    'src/pages/PlanMasterPage.tsx': [1, 2],
    'src/pages/PlanSharePage.tsx': [1, 0],
    'src/pages/ProjectDetailPage.tsx': [7, 6],
    'src/pages/ProjectReleaseDetailPage.tsx': [2, 1],
    'src/pages/ProjectsPage.tsx': [4, 1],
    'src/pages/RoadmapPage.tsx': [3, 0],
    'src/pages/TasksPage.tsx': [3, 0],
    'src/pages/TeamPage.tsx': [2, 0],
    'src/pages/TriagePage.tsx': [11, 5],
};

const HOOK_KINDS = new Map([
    ['useQuery', 'query'],
    ['useQueries', 'query'],
    ['useInfiniteQuery', 'query'],
    ['useLiveWindow', 'query'],
    ['useMutation', 'mutation'],
]);

// Full normalized hook-call fingerprints complement the counts above. This
// prevents an unreviewed hook from replacing a reviewed hook in the same file
// while leaving Q/M totals unchanged.
export const REVIEWED_HOOK_FINGERPRINTS = {
    'src/features/timeEntries/useTimeEntries.ts': 'b689ed77e0980dbd',
    'src/components/tasks/TimeEntriesPanel.tsx': 'ec418c8617746822',
    'src/components/projects/TimeEntriesReport.tsx': 'e713a6d28f0867fa',
    'src/components/tasks/PagedTaskBrowser.tsx': '5e20eeaf74bec28f',
    'src/pages/MyWorkPage.tsx': 'e4703dc32c60b546',
    'src/components/tasks/TaskSearch.tsx': '1c836716acf30699',
    'src/components/tasks/TaskDiscussion.tsx': 'e8fb35323106d619',
    'src/components/tasks/PersonCapacity.tsx': '9ed055ec8adb42aa',
    'src/components/tasks/DeliveryDependencies.tsx': '0606dde61002be81',
    'src/components/tasks/BacklogPanel.tsx': 'b9aed1daacb99f0a',
    'src/components/layout/CommandMenu.tsx': '000910e369219b88',
    'src/components/dashboard/SavedViewDashboardCards.tsx': 'a850ee02012738f3',
    'src/components/gantt/GanttChart.tsx': 'ba83b7289529c7f1',
    'src/components/gantt/TaskEditModal.tsx': 'c2e5fc8906c57e4b',
    'src/components/iteration/IterationForm.tsx': '64499bf5dc9cf46c',
    'src/components/iteration/IterationList.tsx': 'ce187652dfa1be79',
    'src/components/iteration/IterationSelector.tsx': '0dc573bb0877300b',
    'src/components/labels/LabelSelector.tsx': 'b27bfa83465539dd',
    'src/components/notifications/NotificationsPanel.tsx': '6d48fbf5a238b163',
    'src/components/projects/InitiativeForm.tsx': '3059422f748cb121',
    'src/components/projects/ProjectForm.tsx': 'a78994f73e2a48c2',
    'src/components/projects/ProjectIterationsSection.tsx': '487f6ba0d0dbabd5',
    'src/components/releases/ReleaseForm.tsx': '1732e55f12cc0848',
    'src/components/requestSources/RequestSourceLinksPanel.tsx': '93987503489c3a23',
    'src/components/settings/EmailSettingsPanel.tsx': '09a7b416183054f3',
    'src/components/settings/GitHubSettingsPanel.tsx': '45df5a73c267ad6e',
    'src/components/settings/InterfaceLanguageSettings.tsx': '37833eab286e1764',
    'src/components/settings/OutboundWebhooksPanel.tsx': '32f533ef4df7a02a',
    'src/components/settings/RuntimeConfigSettings.tsx': '5ff4edebc64ec10f',
    'src/components/settings/SchedulingRulesSettings.tsx': '27a425d0ace18683',
    'src/components/settings/SystemHealthPanel.tsx': '60dfa7ef98b40373',
    'src/components/settings/TemplateLabelSettings.tsx': 'ac7e0eb3f564698d',
    'src/components/tasks/ImportTasksModal.tsx': '4f2bd662789ead7b',
    'src/components/tasks/KanbanBoard/KanbanBoard.tsx': '1fa0ebc6ef0f6a7c',
    'src/components/tasks/SavedViewsControl.tsx': '1bbeb39ebaf10ee3',
    'src/components/tasks/StatusChangeControl.tsx': '729d6a0213d9e7b2',
    'src/components/tasks/TaskBulkOperationsPanel.tsx': 'da3ed54d577ce8a2',
    'src/components/tasks/TaskDependencySelector.tsx': 'a95773dee19beda4',
    'src/components/tasks/TaskFiltersBar.tsx': 'baf74934c27cea16',
    'src/components/tasks/TaskForm.tsx': '25d4d439cc45725b',
    'src/components/tasks/TaskList.tsx': '644c5a4adff141b7',
    'src/components/tasks/TaskTextEditorModal.tsx': '1a455f699d3e28df',
    'src/components/tasks/TaskTimelinePanel.tsx': 'd6c1a837cced1865',
    'src/components/team/AssigneeRecommendationsPanel.tsx': '8450676dbd07de86',
    'src/components/team/ImportTeamModal.tsx': '12bf6d2f5ae17a79',
    'src/components/team/TeamForm.tsx': '3b33d610019f1ad8',
    'src/components/team/TeamList.tsx': '23628a820b3557ec',
    'src/components/team/TeamProfileManager.tsx': '34c0d99ccebfa900',
    'src/components/team/VacationManager.tsx': 'c59125d77b1edefe',
    'src/i18n/SystemLanguageProvider.tsx': '52087c287c3e9315',
    'src/components/layout/AppSidebar.tsx': '9b6e6b003295400b',
    'src/components/layout/AppTopNav.tsx': '78ebdb449b4d7743',
    'src/features/planningMasters/usePlanningNavigationSummary.ts': 'a3c7904176ba9f46',
    'src/features/planningMasters/usePlanningReadiness.ts': '83544c1613ceb53d',
    'src/pages/AgentPipelinePage.tsx': '200e7928fa9ecf11',
    'src/pages/AnalyticsPage.tsx': 'd0ccdf0dc14dee0f',
    'src/pages/CalendarPage.tsx': 'a6437ae02b4232aa',
    'src/pages/GanttPage.tsx': '0ea68b05fd1e3f43',
    'src/pages/OverviewPage.tsx': 'e54b146286e95b83',
    'src/pages/PlanMasterPage.tsx': '099fb2eef2f3f843',
    'src/pages/PlanSharePage.tsx': '9e333df62efb5575',
    'src/pages/ProjectDetailPage.tsx': '9dab38fcac41fd04',
    'src/pages/ProjectReleaseDetailPage.tsx': '9145592c7cadb869',
    'src/pages/ProjectsPage.tsx': '4fd72b0f96d3e263',
    'src/pages/RoadmapPage.tsx': '8cf2879f1873fa25',
    'src/pages/TasksPage.tsx': '13b6684eab5a4b87',
    'src/pages/TeamPage.tsx': '1b061fa3a8dd4c25',
    'src/pages/TriagePage.tsx': 'c0c3648f5ab135a5',
};

const walkAst = (node, visit) => {
    visit(node);
    ts.forEachChild(node, child => walkAst(child, visit));
};

const unwrapExpression = expression => {
    let current = expression;
    while (
        ts.isParenthesizedExpression(current)
        || ts.isAsExpression(current)
        || ts.isTypeAssertionExpression(current)
        || ts.isNonNullExpression(current)
    ) {
        current = current.expression;
    }
    return current;
};

/**
 * Locate React Query hooks through the TypeScript AST so generics, multiline
 * calls, import aliases, and simple variable aliases cannot bypass review.
 */
export const findHookCalls = (source, fileName = 'source.tsx') => {
    const sourceFile = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
    const aliases = new Map(HOOK_KINDS);
    const namespaces = new Set();

    for (const statement of sourceFile.statements) {
        if (!ts.isImportDeclaration(statement)
            || !ts.isStringLiteral(statement.moduleSpecifier)
            || statement.moduleSpecifier.text !== '@tanstack/react-query') continue;

        const clause = statement.importClause;
        const bindings = clause?.namedBindings;
        if (bindings && ts.isNamespaceImport(bindings)) namespaces.add(bindings.name.text);
        if (bindings && ts.isNamedImports(bindings)) {
            for (const element of bindings.elements) {
                const importedName = (element.propertyName ?? element.name).text;
                const kind = HOOK_KINDS.get(importedName);
                if (kind) aliases.set(element.name.text, kind);
            }
        }
    }

    const expressionKind = expression => {
        const candidate = unwrapExpression(expression);
        if (ts.isIdentifier(candidate)) return aliases.get(candidate.text);
        if (ts.isPropertyAccessExpression(candidate)
            && ts.isIdentifier(candidate.expression)
            && namespaces.has(candidate.expression.text)) {
            return HOOK_KINDS.get(candidate.name.text);
        }
        if (ts.isElementAccessExpression(candidate)
            && ts.isIdentifier(candidate.expression)
            && namespaces.has(candidate.expression.text)
            && ts.isStringLiteral(candidate.argumentExpression)) {
            return HOOK_KINDS.get(candidate.argumentExpression.text);
        }
        return undefined;
    };

    // Resolve chains such as `const queryHook = importedUseQuery;` before
    // locating calls. A bounded fixed point also covers aliases of aliases.
    for (let pass = 0; pass < 8; pass += 1) {
        let changed = false;
        walkAst(sourceFile, node => {
            if (ts.isVariableDeclaration(node) && ts.isIdentifier(node.name) && node.initializer) {
                const kind = expressionKind(node.initializer);
                if (kind && aliases.get(node.name.text) !== kind) {
                    aliases.set(node.name.text, kind);
                    changed = true;
                }
            }
            if (ts.isVariableDeclaration(node)
                && ts.isObjectBindingPattern(node.name)
                && node.initializer
                && ts.isIdentifier(unwrapExpression(node.initializer))
                && namespaces.has(unwrapExpression(node.initializer).text)) {
                for (const element of node.name.elements) {
                    if (!ts.isIdentifier(element.name)) continue;
                    const importedName = element.propertyName && ts.isIdentifier(element.propertyName)
                        ? element.propertyName.text
                        : element.name.text;
                    const kind = HOOK_KINDS.get(importedName);
                    if (kind && aliases.get(element.name.text) !== kind) {
                        aliases.set(element.name.text, kind);
                        changed = true;
                    }
                }
            }
        });
        if (!changed) break;
    }

    const calls = [];
    walkAst(sourceFile, node => {
        if (!ts.isCallExpression(node)) return;
        const kind = expressionKind(node.expression);
        if (!kind) return;
        const { line } = sourceFile.getLineAndCharacterOfPosition(node.getStart(sourceFile));
        const normalizedSource = node.getText(sourceFile).replace(/\s+/g, ' ').trim();
        const signature = crypto
            .createHash('sha256')
            .update(`${kind}:${normalizedSource}`)
            .digest('hex')
            .slice(0, 16);
        calls.push({ kind, line: line + 1, signature });
    });
    return calls;
};

const hookCounts = (source, fileName) => {
    const calls = findHookCalls(source, fileName);
    return [
        calls.filter(call => call.kind === 'query').length,
        calls.filter(call => call.kind === 'mutation').length,
    ];
};

export const hookInventoryFingerprint = (source, fileName = 'source.tsx') => crypto
    .createHash('sha256')
    .update(findHookCalls(source, fileName).map(call => call.signature).join('|'))
    .digest('hex')
    .slice(0, 16);

const walk = directory => fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const target = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(target) : [target];
});

export const validateNewHookAnnotations = source => {
    const lines = source.split(/\r?\n/);
    const errors = [];
    findHookCalls(source).forEach(({ kind, line }) => {
        const index = line - 1;
        const context = lines.slice(Math.max(0, index - 3), index + 1).join('\n');
        const expected = kind === 'query'
            ? /feedback-policy:\s*query\s+loading,error,retry,empty/
            : /feedback-policy:\s*mutation\s+pending,(field|inline|toast)/;
        if (!expected.test(context)) errors.push(`line ${index + 1}: missing reviewed ${kind} feedback-policy annotation`);
    });
    return errors;
};

export const checkQueryFeedback = root => {
    const sourceRoot = path.join(root, 'src');
    const errors = [];
    const seen = new Set();
    for (const absolutePath of walk(sourceRoot).filter(file => /\.(ts|tsx)$/.test(file) && !/\.test\./.test(file))) {
        const relativePath = path.relative(root, absolutePath).replaceAll(path.sep, '/');
        const source = fs.readFileSync(absolutePath, 'utf8');
        const actual = hookCounts(source, relativePath);
        if (actual[0] + actual[1] === 0) continue;
        seen.add(relativePath);
        const reviewed = REVIEWED_HOOK_COUNTS[relativePath];
        if (!reviewed) {
            errors.push(...validateNewHookAnnotations(source).map(error => `${relativePath}:${error}`));
            continue;
        }
        if (actual[0] !== reviewed[0] || actual[1] !== reviewed[1]) {
            errors.push(`${relativePath}: hook inventory changed from Q${reviewed[0]}/M${reviewed[1]} to Q${actual[0]}/M${actual[1]}; review feedback policy and update baseline`);
        }
        const actualFingerprint = hookInventoryFingerprint(source, relativePath);
        const reviewedFingerprint = REVIEWED_HOOK_FINGERPRINTS[relativePath];
        if (!reviewedFingerprint) {
            errors.push(`${relativePath}: reviewed hook fingerprint is missing`);
        } else if (actualFingerprint !== reviewedFingerprint) {
            errors.push(`${relativePath}: hook implementation fingerprint changed; review loading/error/retry/empty and pending/failure policy before updating the baseline`);
        }
    }
    for (const reviewedPath of Object.keys(REVIEWED_HOOK_COUNTS)) {
        if (!seen.has(reviewedPath)) errors.push(`${reviewedPath}: reviewed hook file is missing or no longer contains hooks`);
    }
    return errors;
};

const isMain = process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;
if (isMain) {
    const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
    const errors = checkQueryFeedback(root);
    if (errors.length > 0) {
        console.error(errors.join('\n'));
        process.exitCode = 1;
    } else {
        console.log(`Query feedback guard passed (${Object.keys(REVIEWED_HOOK_COUNTS).length} reviewed files).`);
    }
}
