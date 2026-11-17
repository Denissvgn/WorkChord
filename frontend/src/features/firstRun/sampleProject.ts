import { projectService } from '../../services/projectService';
import { iterationService } from '../../services/iterationService';
import { teamService } from '../../services/teamService';
import { taskService } from '../../services/taskService';
import { ganttService } from '../../services/ganttService';
import { planningInputService } from '../../services/planningInputService';
import type { WorkProfile } from '../identity/identityService';
import { sampleProjectFixture } from './sampleProject.fixture';

export type SampleKind = 'project' | 'milestone' | 'iteration' | 'profile' | 'member' | 'task';
export interface SampleRecord { kind: SampleKind; id: number; name: string; parentId?: number }
export interface SampleManifest { owner: string; records: SampleRecord[]; complete: boolean }
export type SaveSample = (manifest: SampleManifest) => void;
const revisions = async (kind: 'project' | 'iteration' | 'profile' | 'member', id: number) =>
    (await planningInputService.readInitial(kind, id)).expected_revisions;

const availableFixture = async (profileId: number, language: string) => {
    const now = new Date();
    const initial = sampleProjectFixture(language, now);
    const end = new Date(`${initial.start}T12:00:00`);
    end.setDate(end.getDate() + 365);
    const endDate = `${end.getFullYear()}-${String(end.getMonth() + 1).padStart(2, '0')}-${String(end.getDate()).padStart(2, '0')}`;
    const capacity = await teamService.getProfileCapacity(profileId, initial.start, endDate);
    const days = new Map(capacity.days.map(day => [day.date, day]));
    // Keep the whole example together and reserve no time already allocated to other work.
    for (let offset = 0; offset + 25 <= 365; offset += 7) {
        const candidate = new Date(now);
        candidate.setDate(candidate.getDate() + offset);
        const fixture = sampleProjectFixture(language, candidate);
        if (capacity.calendar_year != null && (Number(fixture.start.slice(0, 4)) !== capacity.calendar_year
            || Number(fixture.end.slice(0, 4)) !== capacity.calendar_year)) continue;
        const window = capacity.days.filter(day => day.date >= fixture.start && day.date <= fixture.end);
        if (window.length === 26 && days.has(fixture.start) && days.has(fixture.end)
            && window.every(day => day.allocated_hours === 0 && day.committed_effort_hours === 0)) return fixture;
    }
    throw new Error('No unallocated date window is available for the sample.');
};

/** Keep the receipt after each successful call, including before any subsequent call can fail. */
export const loadSampleProject = async (manifest: SampleManifest, person: WorkProfile, language: string, save: SaveSample) => {
    const fixture = await availableFixture(person.id, language);
    const remember = (record: SampleRecord) => {
        manifest.records.push(record);
        save({ ...manifest, records: [...manifest.records] });
        return record.id;
    };
    const project = await projectService.create({ name: fixture.project, start_date: fixture.start, target_date: fixture.end,
        status: 'planned', health: 'unknown', sort_order: 0, owner_profile_id: person.id });
    remember({ kind: 'project', id: project.id, name: project.name });
    const milestones: number[] = [];
    for (const data of fixture.milestones) {
        const milestone = await projectService.createMilestone(project.id, data);
        milestones.push(remember({ kind: 'milestone', id: milestone.id, name: milestone.name, parentId: project.id }));
    }
    const iteration = await iterationService.create({ name: fixture.iteration, project_id: project.id, start_date: fixture.start, end_date: fixture.end });
    remember({ kind: 'iteration', id: iteration.id, name: iteration.name, parentId: project.id });
    const agent = await teamService.createProfile({ display_name: 'Sample agent', automation_enabled: false,
        profile_kind: 'agent', assignment_modes: ['ownership', 'execution'] });
    remember({ kind: 'profile', id: agent.id, name: agent.display_name });
    const members: number[] = [];
    for (const profile of [person, agent]) {
        const intent = { profile_id: profile.id, name: `Sample: ${profile.display_name}` };
        const observed = await planningInputService.readInitial('member', iteration.id, true, intent);
        const member = await teamService.create(iteration.id, { ...intent, position: 'Sample', availability_percent: 100,
            professionalism_coefficient: 1, operational_utilization: 1 }, observed.expected_revisions);
        members.push(remember({ kind: 'member', id: member.id, name: member.name, parentId: iteration.id }));
        // Creating a linked row uses the profile's name; rename only this allocation, never the person's profile.
        await teamService.update(member.id, { name: intent.name }, await revisions('member', member.id));
        manifest.records.find(record => record.kind === 'member' && record.id === member.id)!.name = intent.name;
        save({ ...manifest, records: [...manifest.records] });
    }
    const tasks: number[] = [];
    for (const data of fixture.tasks) {
        const current = await iterationService.getById(iteration.id);
        const task = await taskService.create(iteration.id, {
            title: data.title, description: data.brief.scope, brief: data.brief, effort_hours: data.effort_hours,
            effort_days: data.effort_hours / (current.nominal_day_hours ?? 8), estimate_provenance: 'estimated',
            project_id: project.id, assignee_id: members[data.assignee], milestone_id: milestones[data.milestone],
            depends_on: data.dependencies.map(index => tasks[index]), tags: ['sample'], expected_revision: current.revision,
        });
        tasks.push(remember({ kind: 'task', id: task.id, name: task.title, parentId: iteration.id }));
    }
    const current = await iterationService.getById(iteration.id);
    const preview = await ganttService.previewSchedule(iteration.id, [], current.revision);
    const result = await ganttService.schedule(iteration.id, preview.input_revision, preview.input_planning_revision);
    if (!result.success) throw new Error('Sample schedule could not be applied.');
    const readiness = await iterationService.getPlanningReadiness(iteration.id);
    if (readiness.checkpoints_done !== 6) throw new Error('Sample schedule is not ready.');
    manifest.complete = true;
    save({ ...manifest, records: [...manifest.records] });
    return { projectId: project.id, iterationId: iteration.id };
};

const notFound = (error: unknown) => (error as { response?: { status?: number } })?.response?.status === 404;

/** Delete only recorded IDs, children first. Stop if a container acquired other work. */
export const removeSampleProject = async (manifest: SampleManifest, save: SaveSample) => {
    for (const record of [...manifest.records].reverse()) {
        try {
            switch (record.kind) {
                case 'task': {
                    const initial = await taskService.getDetail(record.id);
                    const iteration = initial.task.iteration_id ? await iterationService.getById(initial.task.iteration_id) : null;
                    const detail = await taskService.getDetail(record.id);
                    if (detail.children.items.length || detail.children.has_more || detail.task.iteration_id !== initial.task.iteration_id) {
                        throw new Error('Sample task has additional work.');
                    }
                    const task = detail.task;
                    await taskService.delete(record.id, task.version, iteration?.revision);
                    break;
                }
                case 'member': {
                    const observed = await revisions('member', record.id);
                    if ((await taskService.getByIteration(record.parentId!)).some(task => task.assignee?.id === record.id)
                        || (await teamService.getByIteration(record.parentId!)).some(member => member.id === record.id && member.vacations?.length)) {
                        throw new Error('Sample capacity has additional work.');
                    }
                    if ((await teamService.getWorkload(record.id)).allocated_days > 0) throw new Error('Sample capacity is in use.');
                    await teamService.delete(record.id, observed);
                    break;
                }
                case 'profile': {
                    const observed = await revisions('profile', record.id);
                    if (Object.keys(observed).length) throw new Error('Sample profile is used by other capacity rows.');
                    await teamService.deleteProfile(record.id, observed);
                    break;
                }
                case 'iteration': {
                    const observed = await revisions('iteration', record.id);
                    if ((await taskService.getByIteration(record.id)).length || (await teamService.getByIteration(record.id)).length) {
                        throw new Error('Sample iteration has additional work.');
                    }
                    await iterationService.delete(record.id, observed);
                    break;
                }
                case 'milestone':
                    if ((await projectService.getTasks(record.parentId!)).length) throw new Error('Sample project has additional work.');
                    await projectService.deleteMilestone(record.parentId!, record.id);
                    break;
                case 'project': {
                    const observed = await revisions('project', record.id);
                    if ((await projectService.getIterations(record.id)).length || (await projectService.getMilestones(record.id)).length
                        || (await projectService.getTasks(record.id)).length) throw new Error('Sample project has additional work.');
                    await projectService.delete(record.id, observed);
                    break;
                }
            }
        } catch (error) {
            if (!notFound(error)) throw error;
        }
        manifest.records = manifest.records.filter(item => item.kind !== record.kind || item.id !== record.id);
        manifest.complete = false;
        save({ ...manifest, records: [...manifest.records] });
    }
};
