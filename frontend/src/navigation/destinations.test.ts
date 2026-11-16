/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { englishResources } from '../i18n/resources.en';
import { russianResources } from '../i18n/resources.ru';
import {
    DESTINATION_GROUPS,
    DESTINATIONS,
    destinationsOwningPath,
    formatDestinationCounter,
    getCounterSource,
    getDestination,
    getDestinationForPath,
} from './destinations';
import { metadataForPath, routeMetadata } from './routeModules';

type Vocabulary = { destinations: Array<{ id: string; name: { en: string; ru: string } }> };

const vocabulary = JSON.parse(
    readFileSync(resolve(process.cwd(), '../config/workflow-vocabulary.json'), 'utf8'),
) as Vocabulary;

const catalogs = { en: englishResources.translation, ru: russianResources.translation } as const;

const lookup = (language: keyof typeof catalogs, key: string): unknown => key.split('.').reduce<unknown>(
    (value, segment) => (value && typeof value === 'object'
        ? (value as Record<string, unknown>)[segment]
        : undefined),
    catalogs[language],
);

// A concrete path for a route pattern, so `/projects/:projectId` is checked as `/projects/1`.
const samplePath = (pattern: string) => pattern.replace(/:[^/]+/g, '1');

describe('navigation registry', () => {
    it('holds ten destinations in four groups in the order of the navigation rule', () => {
        expect(DESTINATION_GROUPS.map(group => ({
            group: group.id,
            destinations: group.destinations.map(destination => destination.id),
        }))).toEqual([
            { group: 'start', destinations: ['overview', 'my_work', 'triage'] },
            { group: 'plan', destinations: ['projects', 'plan', 'gantt'] },
            { group: 'deliver', destinations: ['tasks', 'analytics'] },
            { group: 'setup', destinations: ['team', 'settings'] },
        ]);
        expect(DESTINATIONS).toHaveLength(10);
        expect(new Set(DESTINATIONS.map(destination => destination.path)).size).toBe(10);
    });

    it('names the groups Plan, Deliver and Setup and leaves the first group without a heading', () => {
        expect(DESTINATION_GROUPS.map(group => (group.labelKey ? lookup('en', group.labelKey) : null)))
            .toEqual([null, 'Plan', 'Deliver', 'Setup']);
        expect(DESTINATION_GROUPS.map(group => group.defaultLabel ?? null))
            .toEqual([null, 'Plan', 'Deliver', 'Setup']);
        for (const group of DESTINATION_GROUPS.filter(candidate => candidate.labelKey)) {
            expect(typeof lookup('ru', group.labelKey!), group.id).toBe('string');
        }
    });

    it('uses the vocabulary destinations, in their order and with their names', () => {
        expect(DESTINATIONS.map(destination => destination.id))
            .toEqual(vocabulary.destinations.map(destination => destination.id));
        for (const destination of DESTINATIONS) {
            const entry = vocabulary.destinations.find(candidate => candidate.id === destination.id);
            for (const language of ['en', 'ru'] as const) {
                expect(lookup(language, destination.labelKey), `${language} ${destination.id}`)
                    .toBe(entry?.name[language]);
            }
            expect(destination.defaultLabel).toBe(entry?.name.en);
        }
    });

    it('opens each destination at a path it owns', () => {
        for (const destination of DESTINATIONS) {
            expect(getDestinationForPath(destination.path)?.id, destination.path).toBe(destination.id);
        }
    });
});

describe('route ownership', () => {
    it.each(routeMetadata.map(route => [route.path, route.key] as const))(
        'route %s (%s) resolves to exactly one destination',
        pattern => {
            expect(destinationsOwningPath(samplePath(pattern)).map(destination => destination.id))
                .toHaveLength(1);
        },
    );

    it.each([
        ['/', 'overview'],
        ['/welcome', 'overview'],
        ['/my-work', 'my_work'],
        ['/mobile/connect', 'my_work'],
        ['/triage', 'triage'],
        ['/projects', 'projects'],
        ['/projects/42', 'projects'],
        ['/projects/42/releases/7', 'projects'],
        ['/roadmap', 'projects'],
        ['/plan', 'plan'],
        ['/plan/master', 'plan'],
        ['/plan/share/abc123', 'plan'],
        ['/iterations', 'plan'],
        ['/gantt', 'gantt'],
        ['/tasks', 'tasks'],
        ['/agent-pipeline', 'tasks'],
        ['/analytics', 'analytics'],
        ['/team', 'team'],
        ['/agent-team/setup', 'team'],
        ['/settings', 'settings'],
        ['/settings/email', 'settings'],
        ['/calendar', 'settings'],
    ] as const)('%s belongs to %s', (pathname, id) => {
        expect(destinationsOwningPath(pathname).map(destination => destination.id)).toEqual([id]);
    });

    it('claims no unknown path', () => {
        expect(getDestinationForPath('/missing')).toBeUndefined();
        expect(getDestinationForPath('/plans')).toBeUndefined();
    });

    it('claims only paths that the router serves', () => {
        const routePaths = new Set(routeMetadata.map(route => route.path));
        const claimed = DESTINATIONS.flatMap(destination => destination.owns);
        expect(claimed.filter(pattern => !routePaths.has(pattern))).toEqual([]);
        expect(new Set(claimed).size).toBe(claimed.length);
    });

    it('lists every route the app declares', () => {
        const appSource = readFileSync(resolve(process.cwd(), 'src/App.tsx'), 'utf8');
        const appPaths = [...appSource.matchAll(/<Route path="([^"]+)"/g)]
            .map(match => match[1])
            .filter(path => path !== '*');
        expect([...appPaths].sort()).toEqual(routeMetadata.map(route => route.path).sort());
    });
});

describe('document titles', () => {
    it('title each destination page with its sidebar name', () => {
        for (const destination of DESTINATIONS) {
            expect(metadataForPath(destination.path).titleKey, destination.path).toBe(destination.labelKey);
        }
    });

    it('title the old plan page with the Plan name', () => {
        expect(metadataForPath('/plan/master').titleKey).toBe(getDestination('plan').labelKey);
    });
});

describe('destination counters', () => {
    it('counts only on Triage and Plan', () => {
        expect(DESTINATIONS.filter(destination => getCounterSource(destination) !== 'none')
            .map(destination => [destination.id, getCounterSource(destination)]))
            .toEqual([['triage', 'requestsWaiting'], ['plan', 'planProgress']]);
        expect(getCounterSource(getDestination('tasks'))).toBe('none');
    });

    it('shows the number of requests waiting on Triage, and nothing when there are none', () => {
        const triage = getDestination('triage');
        expect(formatDestinationCounter(triage, { requestsWaiting: 4 })).toBe('4');
        expect(formatDestinationCounter(triage, { requestsWaiting: 0 })).toBeNull();
        expect(formatDestinationCounter(triage, {})).toBeNull();
    });

    it('shows Plan progress as n/6 only while the plan is incomplete', () => {
        const plan = getDestination('plan');
        expect(formatDestinationCounter(plan, { planProgress: { done: 0, total: 6 } })).toBe('0/6');
        expect(formatDestinationCounter(plan, { planProgress: { done: 4, total: 6 } })).toBe('4/6');
        expect(formatDestinationCounter(plan, { planProgress: { done: 6, total: 6 } })).toBeNull();
        expect(formatDestinationCounter(plan, {})).toBeNull();
    });

    it('shows no counter on Tasks, even with requests waiting', () => {
        expect(formatDestinationCounter(getDestination('tasks'), {
            requestsWaiting: 4,
            planProgress: { done: 2, total: 6 },
        })).toBeNull();
    });
});
