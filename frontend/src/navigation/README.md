# Navigation helper checks
Signatures (pure, no imports): `mapLegacyPath(pathname: string, search: string): string | null` in `legacyPaths.ts`.
`parseScope(search: string): { project?: number | 'all'; iteration?: number | 'backlog' }` and `formatScope(scope: { project: number | 'all'; iteration: number | 'backlog' }, search: string): string` in `scopeParams.ts`.
Search strings may include a leading '?'; non-empty results always start with '?'.
Legacy query order: the caller's pairs first, then mapped pairs whose key the caller did not set.
Run from `frontend/`: `node --test src/navigation/legacyPaths.check.test.ts src/navigation/scopeParams.check.test.ts`.
The implementer must not edit `legacyPaths.check.test.ts` or `scopeParams.check.test.ts`; a failing case means the helper is wrong.
Each case has its own name and assertion message, so a failure names the input and the expected output.
The checks import only `node:test`, `node:assert` and the helper under test.
Both files run with `npm run test:navigation`, which `npm run test:run` includes; vitest skips them because they use Node's runner.
