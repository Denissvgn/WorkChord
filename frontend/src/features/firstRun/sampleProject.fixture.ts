import type { TaskBrief } from '../../types/task';

const english = {
    project: 'Sample welcome guide', iteration: 'Sample first iteration',
    milestones: ['Sample draft ready', 'Sample guide published'],
    tasks: [
        ['Agree on the audience', 'Describe who will read the welcome guide and the three questions it must answer.'],
        ['Collect useful links', 'Gather the team contacts, setup instructions and workspace links for a new teammate.'],
        ['Outline the guide', 'Arrange the welcome guide into a short introduction, setup checklist and help section.'],
        ['Write the introduction', 'Write a friendly introduction that explains the team and its shared purpose.'],
        ['Draft the setup checklist', 'Turn the collected links into an ordered checklist a new teammate can follow.'],
        ['Review the draft', 'Read the introduction and checklist together and resolve unclear instructions.'],
        ['Publish the guide', 'Prepare the reviewed guide for sharing and check that every link opens.'],
        ['Try the welcome journey', 'Follow the published guide from start to finish and record any remaining questions.'],
    ],
    context: 'A small team is preparing a welcome guide for a new teammate.',
    exclusions: 'No external services or real invitations.',
    criterion: 'The result answers the brief and is ready for the next task.',
    verification: 'Read the result and check it against the brief.',
    artifact: 'A short document or checklist with the result.',
};
const russian: typeof english = {
    project: 'Sample: руководство для новичка', iteration: 'Sample: первая итерация',
    milestones: ['Sample: черновик готов', 'Sample: руководство опубликовано'],
    tasks: [
        ['Определить аудиторию', 'Опишите читателя руководства и три вопроса, на которые оно должно ответить.'],
        ['Собрать полезные ссылки', 'Соберите контакты команды, инструкции по настройке и ссылки для нового коллеги.'],
        ['Составить структуру', 'Разделите руководство на введение, список настройки и раздел помощи.'],
        ['Написать введение', 'Напишите дружелюбное введение о команде и её общей цели.'],
        ['Подготовить список настройки', 'Превратите собранные ссылки в последовательный список действий для нового коллеги.'],
        ['Проверить черновик', 'Прочитайте введение и список действий и уточните непонятные инструкции.'],
        ['Опубликовать руководство', 'Подготовьте проверенное руководство к публикации и проверьте все ссылки.'],
        ['Пройти путь новичка', 'Пройдите опубликованное руководство от начала до конца и запишите оставшиеся вопросы.'],
    ],
    context: 'Небольшая команда готовит руководство для нового коллеги.',
    exclusions: 'Без внешних сервисов и настоящих приглашений.',
    criterion: 'Результат отвечает заданию и готов для следующей задачи.',
    verification: 'Прочитайте результат и сверьте его с заданием.',
    artifact: 'Короткий документ или список действий с результатом.',
};

export const sampleProjectFixture = (language: string, now = new Date()) => {
    const copy = language.startsWith('ru') ? russian : english;
    const start = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    // Begin on the next Monday, leaving a generous window for the small example.
    start.setDate(start.getDate() + ((8 - start.getDay()) % 7 || 7));
    const date = (offset: number) => {
        const value = new Date(start);
        value.setDate(value.getDate() + offset);
        return `${value.getFullYear()}-${String(value.getMonth() + 1).padStart(2, '0')}-${String(value.getDate()).padStart(2, '0')}`;
    };
    const dependencies = [[], [], [0, 1], [2], [2], [3, 4], [5], [6]];
    return {
        project: copy.project, iteration: copy.iteration, start: date(0), end: date(25),
        milestones: copy.milestones.map((name, index) => ({ name, target_date: date(index === 0 ? 11 : 25) })),
        tasks: copy.tasks.map(([title, scope], index) => ({
            title: `Sample: ${title}`, effort_hours: 2, milestone: index < 6 ? 0 : 1,
            assignee: index % 2, dependencies: dependencies[index],
            brief: {
                schema_version: 1, goal: scope, scope, context: copy.context, exclusions: copy.exclusions,
                acceptance_criteria: [{ id: 'result', revision: 1, text: copy.criterion, verification: copy.verification }],
                verification: copy.verification, artifact_expectations: copy.artifact,
            } satisfies TaskBrief,
        })),
    };
};
