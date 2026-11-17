import fs from 'node:fs';
import path from 'node:path';
import ts from 'typescript';

const srcRoot = path.resolve('src');
const scopes = process.argv.slice(2).filter((argument) => argument.startsWith('--scope='))
  .flatMap((argument) => argument.slice('--scope='.length).split(','));
const filesUnder = (directory) => fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
  const fullPath = path.join(directory, entry.name);
  if (entry.isDirectory()) return filesUnder(fullPath);
  return /\.tsx?$/.test(entry.name) && !/\.d\.ts$/.test(entry.name) ? [path.resolve(fullPath)] : [];
});
const sourceFiles = filesUnder(srcRoot);
const parsed = new Map(sourceFiles.map((file) => [file, ts.createSourceFile(file, fs.readFileSync(file, 'utf8'), ts.ScriptTarget.Latest, true)]));
const resolveModule = (file, moduleName) => {
  const base = path.resolve(path.dirname(file), moduleName);
  return [base, `${base}.ts`, `${base}.tsx`, path.join(base, 'index.ts'), path.join(base, 'index.tsx')]
    .find((candidate) => parsed.has(candidate));
};
const exports = new Map();
for (const [file, source] of parsed) {
  const names = new Set();
  for (const statement of source.statements) {
    if (ts.isExportDeclaration(statement)) {
      for (const element of statement.exportClause && ts.isNamedExports(statement.exportClause) ? statement.exportClause.elements : []) names.add(element.name.text);
    } else if (statement.modifiers?.some((modifier) => modifier.kind === ts.SyntaxKind.ExportKeyword)) {
      if (ts.isVariableStatement(statement)) {
        for (const declaration of statement.declarationList.declarations) if (ts.isIdentifier(declaration.name)) names.add(declaration.name.text);
      } else if ('name' in statement && statement.name && ts.isIdentifier(statement.name)) names.add(statement.name.text);
    }
  }
  if (names.size) exports.set(file, names);
}
const imported = new Map([...exports].map(([file, names]) => [file, new Map([...names].map((name) => [name, new Set()]))]));
for (const [file, source] of parsed) {
  if (/\.(test|spec)\.[jt]sx?$/.test(file)) continue;
  for (const statement of source.statements) {
    if (!ts.isImportDeclaration(statement) || !ts.isStringLiteral(statement.moduleSpecifier)) continue;
    const target = resolveModule(file, statement.moduleSpecifier.text);
    if (!target || !exports.has(target)) continue;
    const bindings = statement.importClause?.namedBindings;
    if (bindings && ts.isNamedImports(bindings)) {
      for (const element of bindings.elements) {
        imported.get(target)?.get((element.propertyName ?? element.name).text)?.add(file);
      }
    } else if (bindings && ts.isNamespaceImport(bindings)) {
      for (const importers of imported.get(target)?.values() ?? []) importers.add(file);
    }
  }
}
const selected = [...exports].flatMap(([file, names]) => [...names].flatMap((name) => {
  const relative = path.relative(srcRoot, file);
  if (scopes.length && !scopes.some((scope) => relative === scope || relative.startsWith(`${scope}/`))) return [];
  const importers = [...(imported.get(file)?.get(name) ?? [])];
  return importers.length ? [] : [{ file: relative, name }];
})).sort((a, b) => `${a.file}:${a.name}`.localeCompare(`${b.file}:${b.name}`));
console.log(`Named exports scanned: ${[...exports.values()].reduce((total, names) => total + names.size, 0)}`);
if (scopes.length) console.log(`Unused-export report scope: ${scopes.join(', ')}`);
console.log(`Unused named exports (no non-test source importer): ${selected.length}`);
console.log(selected.map(({ file, name }) => `${file}: ${name}`).join('\n'));
