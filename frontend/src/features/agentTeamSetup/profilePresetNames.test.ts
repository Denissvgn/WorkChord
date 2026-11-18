import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { AGENT_PROFILE_PRESET_NAMES } from './profilePresetNames';

describe('agent profile preset names', () => {
    it('match the server preset list', () => {
        const source = readFileSync(resolve(process.cwd(), '../backend/app/services/agent_profile_catalog_service.py'), 'utf8');
        const agents = source.slice(source.indexOf('PROFILE_PRESETS: list'), source.indexOf('HUMAN_PROFILE_PRESETS: list'));
        const pairs = [...agents.matchAll(/"key": "([^"]+)",\s+"display_name": "([^"]+)"/g)].map(match => [match[1], match[2]]);
        expect(pairs.length).toBeGreaterThan(0);
        expect(AGENT_PROFILE_PRESET_NAMES).toEqual(Object.fromEntries(pairs));
    });
});
