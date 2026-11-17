import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';

const srcRoot = path.resolve('src');
const resourceFiles = new Set([
  path.resolve('src/i18n/resources.en.ts'),
  path.resolve('src/i18n/resources.ru.ts'),
]);
const filesUnder = (directory) => fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
  const fullPath = path.join(directory, entry.name);
  if (entry.isDirectory()) return filesUnder(fullPath);
  return /\.tsx?$/.test(entry.name) ? [path.resolve(fullPath)] : [];
});
const sourceFiles = filesUnder(srcRoot);
const parsed = new Map(sourceFiles.map((file) => [file, ts.createSourceFile(file, fs.readFileSync(file, 'utf8'), ts.ScriptTarget.Latest, true)]));
const importMaps = new Map();
for (const [file, source] of parsed) {
  const bindings = new Map();
  for (const statement of source.statements) {
    if (!ts.isImportDeclaration(statement) || !ts.isStringLiteral(statement.moduleSpecifier)) continue;
    const resolvedBase = path.resolve(path.dirname(file), statement.moduleSpecifier.text);
    const target = [resolvedBase, `${resolvedBase}.ts`, `${resolvedBase}.tsx`, path.join(resolvedBase, 'index.ts')].find((candidate) => parsed.has(candidate));
    if (!target || !statement.importClause?.namedBindings || !ts.isNamedImports(statement.importClause.namedBindings)) continue;
    for (const element of statement.importClause.namedBindings.elements) bindings.set(element.name.text, { file: target, name: (element.propertyName ?? element.name).text });
  }
  importMaps.set(file, bindings);
}
const localConst = (file, name) => {
  const source = parsed.get(file);
  for (const statement of source?.statements ?? []) {
    if (!ts.isVariableStatement(statement)) continue;
    for (const declaration of statement.declarationList.declarations) {
      if (ts.isIdentifier(declaration.name) && declaration.name.text === name && declaration.initializer) return declaration.initializer;
    }
  }
  return null;
};
const propertyName = (node) => {
  if (ts.isIdentifier(node) || ts.isStringLiteral(node) || ts.isNumericLiteral(node)) return node.text;
  return null;
};
const resolveObject = (node, file, seen = new Set()) => {
  if (ts.isParenthesizedExpression(node)) return resolveObject(node.expression, file, seen);
  if (ts.isAsExpression(node) || ts.isSatisfiesExpression(node) || ts.isTypeAssertionExpression(node)) return resolveObject(node.expression, file, seen);
  if (ts.isIdentifier(node)) {
    const key = `${file}:${node.text}`;
    if (seen.has(key)) return null;
    const nextSeen = new Set(seen).add(key);
    const imported = importMaps.get(file)?.get(node.text);
    if (imported) return resolveObject(localConst(imported.file, imported.name), imported.file, nextSeen);
    return resolveObject(localConst(file, node.text), file, nextSeen);
  }
  return ts.isObjectLiteralExpression(node) ? node : null;
};
const resolveObjectInfo = (node, file, seen = new Set()) => {
  if (!node) return null;
  if (ts.isParenthesizedExpression(node)) return resolveObjectInfo(node.expression, file, seen);
  if (ts.isAsExpression(node) || ts.isSatisfiesExpression(node) || ts.isTypeAssertionExpression(node)) return resolveObjectInfo(node.expression, file, seen);
  if (ts.isIdentifier(node)) {
    const key = `${file}:${node.text}`;
    if (seen.has(key)) return null;
    const nextSeen = new Set(seen).add(key);
    const imported = importMaps.get(file)?.get(node.text);
    if (imported) return resolveObjectInfo(localConst(imported.file, imported.name), imported.file, nextSeen);
    return resolveObjectInfo(localConst(file, node.text), file, nextSeen);
  }
  return ts.isObjectLiteralExpression(node) ? { object: node, file } : null;
};
const english = parsed.get(path.resolve('src/i18n/resources.en.ts'));
const exportedInitializer = (name) => {
  for (const statement of english.statements) {
    if (!ts.isVariableStatement(statement)) continue;
    const declaration = statement.declarationList.declarations.find((item) => ts.isIdentifier(item.name) && item.name.text === name);
    if (declaration?.initializer) return declaration.initializer;
  }
  return null;
};
const englishObject = resolveObject(exportedInitializer('englishResources'), path.resolve('src/i18n/resources.en.ts'));
if (!englishObject) throw new Error('Could not resolve englishResources');
const translationProperty = englishObject.properties.find((item) => ts.isPropertyAssignment(item) && propertyName(item.name) === 'translation');
const translationObject = translationProperty ? resolveObject(translationProperty.initializer, path.resolve('src/i18n/resources.en.ts')) : null;
if (!translationObject) throw new Error('Could not resolve English translation bundle');
const fullKeys = new Set();
const keyLocations = new Map();
const subtreeKeys = new Map();
// Resolve nested resource constants from the English root and keep each key as a full dotted path.
const flattenResolved = (object, file, prefix = '') => {
  for (const property of object.properties) {
    if (!ts.isPropertyAssignment(property)) continue;
    const key = propertyName(property.name);
    if (key == null) continue;
    const full = prefix ? `${prefix}.${key}` : key;
    const child = resolveObjectInfo(property.initializer, file);
    if (child) {
      const before = fullKeys.size;
      flattenResolved(child.object, child.file, full);
      if (fullKeys.size > before) {
        subtreeKeys.set(full, [...fullKeys].filter((entry) => entry.startsWith(`${full}.`)));
      }
    } else {
      fullKeys.add(full);
      keyLocations.set(full, { file, property });
    }
  }
};
flattenResolved(translationObject, path.resolve('src/i18n/resources.en.ts'));

const usedLiterals = new Set();
const dynamicPrefixes = new Set();
const usedSubtrees = new Set();
const staticValue = (node, file, seen = new Set()) => {
  if (ts.isParenthesizedExpression(node)) return staticValue(node.expression, file, seen);
  if (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node)) return node.text;
  if (ts.isIdentifier(node)) {
    if (seen.has(node.text)) return null;
    const initializer = localConst(file, node.text);
    return initializer ? staticValue(initializer, file, new Set(seen).add(node.text)) : null;
  }
  return null;
};
const staticPrefix = (node, file) => {
  if (ts.isParenthesizedExpression(node)) return staticPrefix(node.expression, file);
  const value = staticValue(node, file);
  if (value !== null) return value;
  if (ts.isTemplateExpression(node)) {
    let prefix = node.head.text;
    for (const span of node.templateSpans) {
      const expressionValue = staticValue(span.expression, file);
      if (expressionValue === null) break;
      prefix += expressionValue + span.literal.text;
    }
    return prefix;
  }
  if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.PlusToken) {
    const left = staticValue(node.left, file);
    return left === null ? staticPrefix(node.left, file) : left;
  }
  return '';
};
const stringValue = (node) => ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node) ? node.text : null;
const pluralBase = (key) => key.replace(/_(zero|one|two|few|many|other)$/, '');
const isTranslationCall = (node) => ts.isCallExpression(node) && (
  (ts.isIdentifier(node.expression) && ['t', 'i18nT'].includes(node.expression.text)) ||
  (ts.isPropertyAccessExpression(node.expression) && ['t', 'getFixedT'].includes(node.expression.name.text))
);
for (const [file, source] of parsed) {
  if (resourceFiles.has(file)) continue;
  const visit = (node) => {
    if (isTranslationCall(node) && node.arguments.length) {
      const first = node.arguments[0];
      const literal = stringValue(first);
      if (literal !== null) usedLiterals.add(literal);
      else {
        const prefix = staticPrefix(first, file);
        if (prefix) dynamicPrefixes.add(prefix);
      }
      if (node.arguments.slice(1).some((argument) => ts.isObjectLiteralExpression(argument) && argument.properties.some((property) => ts.isPropertyAssignment(property) && propertyName(property.name) === 'returnObjects' && property.initializer.kind === ts.SyntaxKind.TrueKeyword))) {
        if (literal !== null) usedSubtrees.add(literal);
      }
    }
    if (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node)) usedLiterals.add(node.text);
    if (ts.isTemplateExpression(node) || (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.PlusToken)) {
      const prefix = staticPrefix(node, file);
      if (prefix) dynamicPrefixes.add(prefix);
    }
    ts.forEachChild(node, visit);
  };
  visit(source);
}
const isUsed = (key) => {
  const base = pluralBase(key);
  return usedLiterals.has(key)
    || usedLiterals.has(base)
    || relevantDynamicPrefixes.some((prefix) => key.startsWith(prefix))
    || [...usedSubtrees].some((prefix) => key.startsWith(`${prefix}.`));
};
const relevantDynamicPrefixes = [...dynamicPrefixes].filter((prefix) => prefix.length >= 4 && [...fullKeys].some((key) => key.startsWith(prefix))).sort();
const unmatched = [...fullKeys].filter((key) => !isUsed(key));
unmatched.sort();
const retiredPatterns = [/^plan\.master\./, /^plan\.hub\./, /^plan\.steps\./, /^surfaces\.(roadmapPage|ganttChart|projectsPage|triagePage)\./, /^overview\.(dataStatus|focus|attention)\./, /^analytics\.onTrack\./, /^agentTeamSetup\./, /^calendar\./, /^iterations\./];
const retiredUnread = unmatched.filter((key) => retiredPatterns.some((pattern) => pattern.test(key)));
console.log(`English translation keys: ${fullKeys.size}`);
console.log(`Exact literal keys matched: ${[...usedLiterals].filter((key) => fullKeys.has(key)).length}`);
console.log(`Dynamic prefixes matching catalog keys: ${relevantDynamicPrefixes.length}`);
console.log(`Dynamic prefix list: ${relevantDynamicPrefixes.join(', ')}`);
console.log(`Whole subtrees: ${usedSubtrees.size}`);
console.log(`Unread keys: ${unmatched.length}`);
console.log(`Unread retired-area keys: ${retiredUnread.length}`);
console.log('--- UNREAD KEYS ---');
console.log(unmatched.join('\n'));

if (process.argv.includes('--delete')) {
  const bundleFor = (language) => {
    const file = path.resolve(`src/i18n/resources.${language}.ts`);
    const source = parsed.get(file);
    const exportName = language === 'en' ? 'englishResources' : 'russianResources';
    const declaration = source.statements.flatMap((statement) => ts.isVariableStatement(statement) ? [...statement.declarationList.declarations] : []).find((item) => ts.isIdentifier(item.name) && item.name.text === exportName);
    const root = resolveObjectInfo(declaration?.initializer, file);
    const translation = root?.object.properties.find((item) => ts.isPropertyAssignment(item) && propertyName(item.name) === 'translation');
    return translation ? resolveObjectInfo(translation.initializer, root.file) : null;
  };
  const ruInfo = bundleFor('ru');
  if (!ruInfo) throw new Error('Could not resolve Russian translation bundle');
  const ruLocations = new Map();
  const collectRu = (object, file, prefix = '') => {
    for (const property of object.properties) {
      if (!ts.isPropertyAssignment(property)) continue;
      const key = propertyName(property.name);
      if (key == null) continue;
      const full = prefix ? `${prefix}.${key}` : key;
      const child = resolveObjectInfo(property.initializer, file);
      if (child) collectRu(child.object, child.file, full);
      else ruLocations.set(full, { file, property });
    }
  };
  collectRu(ruInfo.object, ruInfo.file);
  const editGroups = new Map();
  const russianHandled = new Set();
  for (const key of unmatched) {
    const englishLocation = keyLocations.get(key);
    if (!englishLocation) throw new Error(`Missing English translation for ${key}`);
    const family = pluralBase(key);
    const familyStillUsed = [...fullKeys].some((candidate) => pluralBase(candidate) === family && !unmatched.includes(candidate));
    if (!ruLocations.has(key) && !ruLocations.has(family)) throw new Error(`Missing Russian translation for ${key}`);
    const removeLocations = [[englishLocation.file, englishLocation.property]];
    if (!familyStillUsed && !russianHandled.has(family)) {
      const russianFamily = [...ruLocations.entries()].filter(([candidate]) => candidate === family || pluralBase(candidate) === family);
      if (!russianFamily.length) throw new Error(`Missing Russian translation family for ${key}`);
      removeLocations.push(...russianFamily.map(([, location]) => [location.file, location.property]));
      russianHandled.add(family);
    }
    for (const [file, property] of removeLocations) {
      const siblings = property.parent.properties;
      const index = siblings.indexOf(property);
      let start = property.getFullStart();
      let end = property.getEnd();
      if (index < siblings.length - 1) {
        end = siblings[index + 1].getFullStart();
      } else if (index > 0) {
        const previousEnd = siblings[index - 1].getEnd();
        const between = fs.readFileSync(file, 'utf8').slice(previousEnd, property.getStart());
        const comma = between.lastIndexOf(',');
        if (comma < 0) throw new Error(`Missing sibling comma for ${key}`);
        start = previousEnd + comma;
      } else {
        const content = fs.readFileSync(file, 'utf8');
        let after = property.getEnd();
        while (/\s/.test(content[after] ?? '')) after += 1;
        if (content[after] === ',') end = after + 1;
      }
      if (!editGroups.has(file)) editGroups.set(file, []);
      editGroups.get(file).push({ start, end });
    }
  }
  for (const [file, edits] of editGroups) {
    let content = fs.readFileSync(file, 'utf8');
    edits.sort((a, b) => b.start - a.start);
    for (const edit of edits) content = content.slice(0, edit.start) + content.slice(edit.end);
    fs.writeFileSync(file, content);
  }
  console.log(`Deleted ${unmatched.length} unread keys from both languages.`);
}
