/**
 * A page has at most one toolbar row. For every value a component returns, this rule works out
 * which `PageToolbar` elements can be on screen together and reports the second one.
 *
 * - The two arms of one conditional (`a ? <PageToolbar /> : <PageToolbar />`) and separate
 *   returns of one function cannot render together, so they are accepted.
 * - Elements in one tree, in one fragment, in an array, on both sides of `&&`, `||` or `??`,
 *   or reached through variables, constants and local helper functions are counted together.
 * - A variable that is assigned more than once counts every assignment, because the rule does not
 *   follow control flow. Anything it cannot tell apart is rejected, not accepted.
 *
 * Toolbars inside a callback, a render prop or a child component are not seen here; the
 * page-chrome check counts them in the rendered page.
 */
const MESSAGE = 'A page has at most one PageToolbar. Put search, filters, the view switch and view options in one toolbar. This rule rejects two toolbars unless they are the two arms of one conditional or separate returns; it cannot prove that other combinations never render together.';

const isFunction = node => node && /^(FunctionDeclaration|FunctionExpression|ArrowFunctionExpression)$/.test(node.type);

const rule = {
    meta: {
        type: 'problem',
        schema: [],
        messages: { second: MESSAGE },
    },
    create(context) {
        const sourceCode = context.sourceCode ?? context.getSourceCode();
        const reported = new Set();

        const findVariable = (node, name) => {
            for (let scope = sourceCode.getScope(node); scope; scope = scope.upper) {
                const variable = scope.set.get(name);
                if (variable) return variable;
            }
            return null;
        };

        // The values a function can return: its expression body, or the argument of each of its returns.
        const returnsOf = fn => {
            if (fn.body.type !== 'BlockStatement') return [fn.body];
            const found = [];
            const visit = node => {
                if (!node || typeof node.type !== 'string') return;
                if (isFunction(node)) return;
                if (node.type === 'ReturnStatement') { if (node.argument) found.push(node.argument); return; }
                for (const key of sourceCode.visitorKeys[node.type] ?? []) {
                    const child = node[key];
                    if (Array.isArray(child)) child.forEach(visit); else visit(child);
                }
            };
            visit(fn.body);
            return found;
        };

        const functionsOf = (identifier) => {
            const variable = findVariable(identifier, identifier.name);
            if (!variable) return [];
            const found = [];
            for (const definition of variable.defs) {
                if (definition.node.type === 'FunctionDeclaration') found.push(definition.node);
            }
            for (const reference of variable.references) {
                if (reference.isWrite() && isFunction(reference.writeExpr)) found.push(reference.writeExpr);
            }
            return found;
        };

        // Longest list of toolbars that can be on screen together for the value of `node`.
        const longest = (lists) => lists.reduce((best, list) => (list.length > best.length ? list : best), []);
        const together = (nodes, visiting) => nodes.flatMap(child => toolbarsIn(child, visiting));

        const toolbarsIn = (node, visiting) => {
            if (!node) return [];
            switch (node.type) {
                case 'JSXElement': {
                    const name = node.openingElement.name;
                    const own = name.type === 'JSXIdentifier' && name.name === 'PageToolbar' ? [node.openingElement] : [];
                    const attributes = node.openingElement.attributes.map(attribute => (attribute.type === 'JSXSpreadAttribute' ? attribute.argument : attribute.value));
                    return [...own, ...together(attributes, visiting), ...together(node.children, visiting)];
                }
                case 'JSXFragment':
                    return together(node.children, visiting);
                case 'JSXExpressionContainer':
                    return node.expression.type === 'JSXEmptyExpression' ? [] : toolbarsIn(node.expression, visiting);
                case 'ConditionalExpression':
                    return [...toolbarsIn(node.test, visiting), ...longest([toolbarsIn(node.consequent, visiting), toolbarsIn(node.alternate, visiting)])];
                case 'LogicalExpression':
                    return together([node.left, node.right], visiting);
                case 'SequenceExpression':
                    return together(node.expressions, visiting);
                case 'ArrayExpression':
                    return together(node.elements, visiting);
                case 'SpreadElement':
                    return toolbarsIn(node.argument, visiting);
                case 'TSAsExpression':
                case 'TSNonNullExpression':
                case 'TSSatisfiesExpression':
                case 'TSTypeAssertion':
                    return toolbarsIn(node.expression, visiting);
                case 'Identifier': {
                    const variable = findVariable(node, node.name);
                    if (!variable || visiting.has(variable)) return [];
                    visiting.add(variable);
                    const values = variable.references.filter(reference => reference.isWrite() && reference.writeExpr).map(reference => reference.writeExpr);
                    const found = together(values, visiting);
                    visiting.delete(variable);
                    return found;
                }
                case 'CallExpression': {
                    const found = together(node.arguments.filter(argument => !isFunction(argument)), visiting);
                    if (node.callee.type !== 'Identifier') return found;
                    const variable = findVariable(node.callee, node.callee.name);
                    if (!variable || visiting.has(variable)) return found;
                    visiting.add(variable);
                    const helper = longest(functionsOf(node.callee).flatMap(fn => returnsOf(fn).map(value => toolbarsIn(value, visiting))));
                    visiting.delete(variable);
                    return [...found, ...helper];
                }
                default:
                    return [];
            }
        };

        const check = value => {
            const toolbars = toolbarsIn(value, new Set());
            for (const toolbar of toolbars.slice(1)) {
                if (reported.has(toolbar)) continue;
                reported.add(toolbar);
                context.report({ node: toolbar, messageId: 'second' });
            }
        };

        const checkFunction = fn => returnsOf(fn).forEach(check);

        return {
            FunctionDeclaration: checkFunction,
            FunctionExpression: checkFunction,
            ArrowFunctionExpression: checkFunction,
        };
    },
};

export default rule;
