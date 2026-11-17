/**
 * A page has at most one toolbar row. This rule reports a second `PageToolbar` in the same
 * JSX tree, so one render of a component cannot show two rows. Separate returns of one
 * component are separate trees, and a toolbar shown by a child component is counted at run
 * time by the page-chrome check, which this rule cannot see.
 */
const rule = {
    meta: {
        type: 'problem',
        schema: [],
        messages: {
            second: 'A page has at most one PageToolbar. Put search, filters, the view switch and view options in one toolbar.',
        },
    },
    create(context) {
        const counts = new Map();
        const treeRoot = node => {
            let root = node.parent;
            for (let current = node.parent; current; current = current.parent) {
                if (current.type === 'JSXElement' || current.type === 'JSXFragment') root = current;
                // A function boundary starts a new tree: render callbacks inside JSX are their own trees.
                else if (/Function/.test(current.type)) break;
            }
            return root;
        };
        return {
            JSXOpeningElement(node) {
                if (node.name.type !== 'JSXIdentifier' || node.name.name !== 'PageToolbar') return;
                const root = treeRoot(node);
                const seen = (counts.get(root) ?? 0) + 1;
                counts.set(root, seen);
                if (seen > 1) context.report({ node, messageId: 'second' });
            },
        };
    },
};

export default rule;
