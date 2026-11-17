/**
 * A page has at most one toolbar row. For every value a function returns, this rule works out
 * which `PageToolbar` elements can be on screen together and reports every one after the first.
 *
 * Which component is the toolbar is decided by its binding, not by the name written in JSX:
 * a named import with or without an alias, a default import, a namespace import (`ui.PageToolbar`),
 * a name the imported local module re-exports for it, and constants or wrappers that hold it.
 *
 * Where a toolbar element can be held, the rule follows it: JSX trees and fragments, attributes and
 * render props, variables (every assignment counts, because the rule does not follow control flow),
 * destructuring, object properties, array elements, values added later (`rows.a = …`, `push`),
 * local helper functions and their return values, local components rendered as JSX, and callbacks
 * passed to calls (a `map` or `flatMap` callback renders once per item, so its toolbar counts twice).
 *
 * Only two things are accepted as exclusive: the two arms of one conditional expression, and
 * separate return statements. One member read with a computed key (`views[mode]`) reads one value,
 * so it counts like a conditional over the values it can read. Everything else that the rule cannot
 * prove exclusive is reported, and the message says so.
 *
 * Toolbars inside a component imported from another file are not seen here; the page-chrome check
 * counts them in the rendered page.
 */
import { existsSync, readFileSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const MESSAGE = 'A page has at most one PageToolbar. Put search, filters, the view switch and view options in one toolbar. This rule accepts two toolbars only when they are the two arms of one conditional expression or in separate return statements; it cannot prove that any other combination never renders together, so it reports it.';

const TOOLBAR = 'PageToolbar';
// Path segments: a property name, or one of these markers.
const CALL = Symbol('call'); // the value returned by calling
const DYNAMIC = Symbol('dynamic'); // one value read with a key the rule cannot compute
const ALL = Symbol('all'); // every value of the container at once (array rest, spreads)

const isFunction = node => Boolean(node) && /^(FunctionDeclaration|FunctionExpression|ArrowFunctionExpression)$/.test(node.type);
const WRAPPERS = new Set(['TSAsExpression', 'TSNonNullExpression', 'TSSatisfiesExpression', 'TSTypeAssertion', 'ChainExpression', 'AwaitExpression', 'ParenthesizedExpression']);
const ELEMENT_FACTORIES = new Set(['createElement', 'jsx', 'jsxs', 'jsxDEV']);
const MUTATING_METHODS = new Set(['push', 'unshift', 'splice', 'fill', 'set', 'add']);
const PER_ITEM_METHODS = new Set(['map', 'flatMap']);
const MODULE_EXTENSIONS = ['', '.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js', '/index.jsx'];
const TOOLBAR_MODULE = /(^|\/)PageToolbar(\.[jt]sx?)?$/;

// Names under which a module exports the toolbar, read from its re-export statements.
const exportCache = new Map();
const resolveModule = (fromFile, source) => {
    if (!source.startsWith('.')) return null;
    const base = resolve(dirname(fromFile), source);
    for (const extension of MODULE_EXTENSIONS) {
        const candidate = base + extension;
        try {
            if (existsSync(candidate) && statSync(candidate).isFile()) return candidate;
        } catch {
            // An unreadable candidate is not the module.
        }
    }
    return null;
};
const specifiersOf = list => list.split(',').map(part => part.trim().replace(/^type\s+/, '')).filter(Boolean).map(part => {
    const [local, exported] = part.split(/\s+as\s+/);
    return { local: local.trim(), exported: (exported ?? local).trim() };
});
const toolbarExportNames = (fromFile, source, depth = 0) => {
    const names = new Set([TOOLBAR]);
    if (TOOLBAR_MODULE.test(source)) names.add('default');
    const file = fromFile && resolveModule(fromFile, source);
    if (!file || depth > 4) return names;
    let mtime = 0;
    try { mtime = statSync(file).mtimeMs; } catch { return names; }
    const cached = exportCache.get(file);
    if (cached && cached.mtime === mtime) return cached.names;
    exportCache.set(file, { mtime, names }); // guards against re-export cycles while reading
    let text = '';
    try { text = readFileSync(file, 'utf8'); } catch { return names; }
    for (const match of text.matchAll(/export\s*\*\s*from\s*['"]([^'"]+)['"]/g)) {
        for (const name of toolbarExportNames(file, match[1], depth + 1)) if (name !== 'default') names.add(name);
    }
    for (const match of text.matchAll(/export\s+(?:type\s+)?\{([^}]*)\}\s*from\s*['"]([^'"]+)['"]/g)) {
        const inner = toolbarExportNames(file, match[2], depth + 1);
        for (const { local, exported } of specifiersOf(match[1])) if (inner.has(local)) names.add(exported);
    }
    const imported = new Set([TOOLBAR]);
    for (const match of text.matchAll(/import\s*\{([^}]*)\}\s*from\s*['"]([^'"]+)['"]/g)) {
        const inner = toolbarExportNames(file, match[2], depth + 1);
        for (const { local, exported } of specifiersOf(match[1])) if (inner.has(local)) imported.add(exported);
    }
    for (const match of text.matchAll(/export\s*\{([^}]*)\}(?!\s*from)/g)) {
        for (const { local, exported } of specifiersOf(match[1])) if (imported.has(local)) names.add(exported);
    }
    for (const match of text.matchAll(/export\s+default\s+([A-Za-z_$][\w$]*)\s*;?/g)) if (imported.has(match[1])) names.add('default');
    return names;
};

const keyOfMember = node => {
    if (!node.computed) return node.property.type === 'Identifier' || node.property.type === 'PrivateIdentifier' ? node.property.name : DYNAMIC;
    if (node.property.type === 'Literal') return String(node.property.value);
    if (node.property.type === 'TemplateLiteral' && node.property.expressions.length === 0) return node.property.quasis[0].value.cooked;
    return DYNAMIC;
};
const keyOfProperty = node => {
    if (!node.computed) return node.key.type === 'Identifier' ? node.key.name : String(node.key.value);
    if (node.key.type === 'Literal') return String(node.key.value);
    return DYNAMIC;
};

const longest = lists => lists.reduce((best, list) => (list.length > best.length ? list : best), []);

const rule = {
    meta: {
        type: 'problem',
        schema: [],
        messages: { second: MESSAGE },
    },
    create(context) {
        const sourceCode = context.sourceCode ?? context.getSourceCode();
        const filename = context.physicalFilename ?? context.filename ?? context.getFilename();
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

        // For an identifier that is written by a declaration or an assignment, the written value and
        // the path from that value to the identifier through destructuring, plus any default values.
        const destructuringPath = identifier => {
            const path = [];
            const defaults = [];
            let node = identifier;
            for (;;) {
                const parent = node.parent;
                if (!parent) return { path, defaults };
                if (parent.type === 'Property' && parent.value === node && parent.parent.type === 'ObjectPattern') {
                    path.unshift(keyOfProperty(parent));
                    node = parent.parent;
                } else if (parent.type === 'ArrayPattern') {
                    path.unshift(String(parent.elements.indexOf(node)));
                    node = parent;
                } else if (parent.type === 'AssignmentPattern' && parent.left === node) {
                    defaults.push({ value: parent.right, path: [] });
                    node = parent;
                } else if (parent.type === 'RestElement') {
                    if (parent.parent.type === 'ArrayPattern') path.unshift(ALL);
                    node = parent.parent;
                } else {
                    return { path, defaults };
                }
            }
        };

        // Every value written to a variable, each with the path that leads from it to the variable.
        const assignmentsOf = variable => {
            const found = [];
            for (const definition of variable.defs) {
                if (definition.node.type === 'FunctionDeclaration' || definition.node.type === 'ClassDeclaration') found.push({ value: definition.node, path: [] });
            }
            for (const reference of variable.references) {
                if (!reference.isWrite() || !reference.writeExpr) continue;
                const { path, defaults } = destructuringPath(reference.identifier);
                found.push({ value: reference.writeExpr, path }, ...defaults);
            }
            return found;
        };

        // Values put into a variable's container after it was written: `rows.a = …`, `rows.push(…)`,
        // `Object.assign(rows, …)`. `key` is the property being read, when known.
        const additionsTo = (variable, key) => {
            const found = [];
            for (const reference of variable.references) {
                const identifier = reference.identifier;
                const parent = identifier.parent;
                if (parent?.type === 'MemberExpression' && parent.object === identifier) {
                    const grand = parent.parent;
                    if (grand?.type === 'AssignmentExpression' && grand.left === parent) {
                        const written = keyOfMember(parent);
                        if (typeof key === 'string' && typeof written === 'string' && written !== key) continue;
                        found.push(grand.right);
                    } else if (grand?.type === 'CallExpression' && grand.callee === parent && MUTATING_METHODS.has(keyOfMember(parent))) {
                        found.push(...grand.arguments);
                    }
                } else if (parent?.type === 'CallExpression' && parent.arguments[0] === identifier
                    && parent.callee.type === 'MemberExpression' && keyOfMember(parent.callee) === 'assign'
                    && parent.callee.object.type === 'Identifier' && parent.callee.object.name === 'Object') {
                    found.push(...parent.arguments.slice(1));
                }
            }
            return found;
        };

        // Whether the component that `node` (followed by `path`) names is the toolbar.
        const isToolbarVariable = (variable, path, seen) => {
            if (seen.has(variable)) return false;
            seen.add(variable);
            try {
                if (path.length === 0 && variable.name === TOOLBAR) return true;
                for (const definition of variable.defs) {
                    if (definition.type !== 'ImportBinding') continue;
                    const specifier = definition.node;
                    const names = toolbarExportNames(filename, definition.parent.source.value);
                    if (specifier.type === 'ImportSpecifier') {
                        const imported = specifier.imported.type === 'Identifier' ? specifier.imported.name : String(specifier.imported.value);
                        if (path.length === 0 && names.has(imported)) return true;
                    } else if (specifier.type === 'ImportDefaultSpecifier') {
                        if (path.length === 0 && names.has('default')) return true;
                    } else if (specifier.type === 'ImportNamespaceSpecifier') {
                        if (path.length === 1 && (names.has(path[0]) || path[0] === TOOLBAR)) return true;
                    }
                }
                return assignmentsOf(variable).some(({ value, path: prefix }) => isToolbarAt(value, [...prefix, ...path], seen));
            } finally {
                seen.delete(variable);
            }
        };

        const isToolbarAt = (node, path, seen) => {
            if (!node) return false;
            if (WRAPPERS.has(node.type)) return isToolbarAt(node.expression ?? node.argument, path, seen);
            switch (node.type) {
                case 'Identifier': {
                    const variable = findVariable(node, node.name);
                    return variable ? isToolbarVariable(variable, path, seen) : path.length === 0 && node.name === TOOLBAR;
                }
                case 'MemberExpression': {
                    const key = keyOfMember(node);
                    if (path.length === 0 && key === TOOLBAR) return true;
                    return isToolbarAt(node.object, [key, ...path], seen);
                }
                case 'ObjectExpression': {
                    if (path.length === 0) return false;
                    const [key, ...rest] = path;
                    return node.properties.some(property => (property.type === 'SpreadElement'
                        ? isToolbarAt(property.argument, path, seen)
                        : (key === DYNAMIC || keyOfProperty(property) === DYNAMIC || keyOfProperty(property) === key) && isToolbarAt(property.value, rest, seen)));
                }
                case 'ConditionalExpression':
                    return isToolbarAt(node.consequent, path, seen) || isToolbarAt(node.alternate, path, seen);
                case 'LogicalExpression':
                    return isToolbarAt(node.left, path, seen) || isToolbarAt(node.right, path, seen);
                case 'AssignmentExpression':
                    return isToolbarAt(node.right, path, seen);
                case 'CallExpression':
                    // A wrapper such as memo(PageToolbar) or forwardRef is still the toolbar.
                    return path.length === 0 && node.arguments.some(argument => isToolbarAt(argument, [], seen));
                default:
                    return false;
            }
        };

        const jsxNameParts = name => {
            const path = [];
            let node = name;
            while (node.type === 'JSXMemberExpression') {
                path.unshift(node.property.name);
                node = node.object;
            }
            return node.type === 'JSXIdentifier' ? { root: node, path } : null;
        };

        const isToolbarName = name => {
            const parts = jsxNameParts(name);
            if (!parts) return false;
            const { root, path } = parts;
            if (path.length === 0 && /^[a-z]/.test(root.name)) return false;
            if (path.length > 0 && path[path.length - 1] === TOOLBAR) return true;
            const variable = findVariable(root, root.name);
            if (!variable) return path.length === 0 && root.name === TOOLBAR;
            return isToolbarVariable(variable, path, new Set());
        };

        // Toolbars that can be on screen together for the value of `node` followed by `path`.
        const together = (items, visiting) => items.flatMap(([node, path]) => toolbarsAt(node, path, visiting));

        const variableToolbars = (variable, path, visiting) => {
            if (!variable || visiting.has(variable)) return [];
            visiting.add(variable);
            const found = [
                ...together(assignmentsOf(variable).map(({ value, path: prefix }) => [value, [...prefix, ...path]]), visiting),
                ...together(additionsTo(variable, path[0]).map(value => [value, []]), visiting),
            ];
            visiting.delete(variable);
            return found;
        };

        const functionToolbars = (fn, path, visiting) => {
            if (visiting.has(fn)) return [];
            const rest = path[0] === CALL ? path.slice(1) : path.length === 0 ? [] : null;
            if (rest === null) return [];
            visiting.add(fn);
            const found = longest(returnsOf(fn).map(value => toolbarsAt(value, rest, visiting)));
            visiting.delete(fn);
            return found;
        };

        const containerToolbars = (entries, spreads, path, visiting, matches) => {
            const [key, ...rest] = path;
            if (key === CALL) return [];
            if (key === ALL) return together([...entries.map(entry => [entry.value, rest]), ...spreads.map(spread => [spread, path])], visiting);
            if (key === DYNAMIC) return longest([...entries.map(entry => toolbarsAt(entry.value, rest, visiting)), ...spreads.map(spread => toolbarsAt(spread, path, visiting))]);
            return together([...entries.filter(entry => matches(entry, key)).map(entry => [entry.value, rest]), ...spreads.map(spread => [spread, path])], visiting);
        };

        const toolbarsAt = (node, path, visiting) => {
            if (!node) return [];
            if (WRAPPERS.has(node.type)) return toolbarsAt(node.expression ?? node.argument, path, visiting);
            if (isFunction(node)) return functionToolbars(node, path, visiting);
            switch (node.type) {
                case 'JSXElement': {
                    if (path.length > 0) return toolbarsAt(node, [], visiting);
                    const opening = node.openingElement;
                    const attributes = opening.attributes.map(attribute => [attribute.type === 'JSXSpreadAttribute' ? attribute.argument : attribute.value, []]);
                    const inside = together([...attributes, ...node.children.map(child => [child, []])], visiting);
                    if (isToolbarName(opening.name)) return [opening, ...inside];
                    // A component defined in this file renders its own returns here.
                    const parts = jsxNameParts(opening.name);
                    const isComponent = parts && (parts.path.length > 0 || /^[A-Z]/.test(parts.root.name));
                    const local = isComponent ? variableToolbars(findVariable(parts.root, parts.root.name), [...parts.path, CALL], visiting) : [];
                    return [...local, ...inside];
                }
                case 'JSXFragment':
                    return together(node.children.map(child => [child, []]), visiting);
                case 'JSXExpressionContainer':
                case 'JSXSpreadChild':
                    return node.expression.type === 'JSXEmptyExpression' ? [] : toolbarsAt(node.expression, path, visiting);
                case 'ConditionalExpression':
                    return [...toolbarsAt(node.test, [], visiting), ...longest([toolbarsAt(node.consequent, path, visiting), toolbarsAt(node.alternate, path, visiting)])];
                case 'LogicalExpression':
                    return together([[node.left, path], [node.right, path]], visiting);
                case 'SequenceExpression':
                    return together(node.expressions.map((expression, index) => [expression, index === node.expressions.length - 1 ? path : []]), visiting);
                case 'AssignmentExpression':
                    return toolbarsAt(node.right, path, visiting);
                case 'SpreadElement':
                    return toolbarsAt(node.argument, path, visiting);
                case 'ArrayExpression': {
                    const elements = node.elements.filter(Boolean);
                    if (path.length === 0) return together(elements.map(element => [element, []]), visiting);
                    const [key, ...rest] = path;
                    if (key === 'length') return [];
                    const hasSpread = elements.some(element => element.type === 'SpreadElement');
                    if (typeof key === 'string' && /^\d+$/.test(key) && !hasSpread) return toolbarsAt(node.elements[Number(key)], rest, visiting);
                    if (typeof key === 'string' && !/^\d+$/.test(key)) return together(elements.map(element => [element, []]), visiting); // a method such as filter or concat
                    const entries = elements.filter(element => element.type !== 'SpreadElement').map(value => ({ value }));
                    const spreads = elements.filter(element => element.type === 'SpreadElement').map(element => element.argument);
                    return containerToolbars(entries, spreads, typeof key === 'string' ? [DYNAMIC, ...rest] : path, visiting, () => true);
                }
                case 'ObjectExpression': {
                    const entries = node.properties.filter(property => property.type === 'Property').map(property => ({ key: keyOfProperty(property), value: property.value }));
                    const spreads = node.properties.filter(property => property.type === 'SpreadElement').map(property => property.argument);
                    if (path.length === 0) return together([...entries.map(entry => [entry.value, []]), ...spreads.map(spread => [spread, []])], visiting);
                    return containerToolbars(entries, spreads, path, visiting, (entry, key) => entry.key === key || entry.key === DYNAMIC);
                }
                case 'Identifier':
                    return variableToolbars(findVariable(node, node.name), path, visiting);
                case 'MemberExpression':
                    return toolbarsAt(node.object, [keyOfMember(node), ...path], visiting);
                case 'CallExpression':
                case 'NewExpression': {
                    const callee = node.callee;
                    const method = callee.type === 'MemberExpression' ? keyOfMember(callee) : callee.type === 'Identifier' ? callee.name : null;
                    const own = path.length === 0 && ELEMENT_FACTORIES.has(method) && isToolbarAt(node.arguments[0], [], new Set()) ? [node] : [];
                    const perItem = callee.type === 'MemberExpression' && PER_ITEM_METHODS.has(method);
                    const fromArguments = node.arguments.flatMap(argument => {
                        if (!isFunction(argument)) return toolbarsAt(argument, [], visiting);
                        const returned = functionToolbars(argument, [CALL, ...path], visiting);
                        return perItem ? [...returned, ...returned] : returned;
                    });
                    const fromCallee = node.type === 'CallExpression' && callee.type !== 'Super' ? toolbarsAt(callee, [CALL, ...path], visiting) : [];
                    return [...own, ...fromArguments, ...fromCallee];
                }
                case 'TaggedTemplateExpression':
                    return toolbarsAt(node.tag, [CALL, ...path], visiting);
                default:
                    return [];
            }
        };

        const check = value => {
            const toolbars = toolbarsAt(value, [], new Set());
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
