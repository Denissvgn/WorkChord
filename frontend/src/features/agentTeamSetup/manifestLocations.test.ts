import { describe, expect, it } from 'vitest';
import { fieldIssues, lineForPath, lineRange, manifestPathLines, pathIssue, syntaxIssue } from './manifestLocations';

const text = `{
  "schema_version": "agent-team-master-v1",
  "controller": {
    "role": "pm",
    "model_binding_keys": [
      "planning-default"
    ]
  },
  "workers": [
    {
      "role": "worker",
      "actor_key": "backend-worker"
    },
    {
      "role": "worker"
    }
  ]
}`;

describe('manifest locations', () => {
    it('maps keys, nested objects and array items to their lines', () => {
        const lines = manifestPathLines(text);
        expect(lines.get('schema_version')).toBe(2);
        expect(lines.get('controller.role')).toBe(4);
        expect(lines.get('controller.model_binding_keys[0]')).toBe(6);
        expect(lines.get('workers[0].actor_key')).toBe(12);
        expect(lines.get('workers[1].role')).toBe(15);
    });

    it('falls back to the nearest parent, and reads server field errors', () => {
        expect(lineForPath(text, 'workers[1].actor_key')).toBe(14);
        expect(fieldIssues(text, [{ loc: ['body', 'manifest', 'workers', 0, 'role'], msg: 'Input should be worker' }]))
            .toEqual([{ line: 11, path: 'workers[0].role', message: 'Input should be worker' }]);
        expect(pathIssue(text, 'Secret-bearing field is not allowed at $.workers[0].actor_key').line).toBe(12);
    });

    it('gives syntax errors a line and selects a line by offsets', () => {
        const broken = '{\n  "a": 1,\n  "b": \n}';
        let error: unknown;
        try { JSON.parse(broken); } catch (cause) { error = cause; }
        expect(syntaxIssue(broken, error)?.line).toBe(4);
        expect(lineRange('ab\ncd\nef', 2)).toEqual([3, 5]);
    });
});
