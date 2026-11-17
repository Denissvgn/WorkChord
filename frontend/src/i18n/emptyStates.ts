/**
 * Copy for the empty states of each destination and view. Each state says what appears there in
 * one sentence; its one button comes from the first-run order (see useNextSetupAction).
 */
export const emptyStatesEnglish = {
    filtered: {
        title: 'Nothing matches the filters',
        body: 'Clear the filters to see everything in this view.',
        clear: 'Clear filters',
    },
    overview: {
        iterationTitle: 'No iteration yet',
        iterationBody: 'Iterations hold the capacity, tasks and schedule for one period of work.',
    },
    myWork: {
        queueBody: 'Tasks assigned to you, and reviews you owe, appear here.',
        inboxBody: 'Notifications about your work appear here as they happen.',
    },
    triage: {
        emptyTitle: 'No requests yet',
        emptyBody: 'Requests you capture appear here until you review them.',
        action: 'New request',
    },
    projects: {
        title: 'No projects yet',
        body: 'Projects group the iterations and tasks of one piece of work.',
        action: 'New project',
    },
    plan: {
        title: 'No iteration selected',
        body: 'Plan shows one iteration at a time, and its capacity, work and schedule follow once it exists.',
    },
    gantt: {
        title: 'No iteration to show',
        body: 'The saved schedule of an iteration appears here once it is applied.',
    },
    tasks: {
        title: 'No tasks yet',
        body: 'Tasks in this iteration appear here in every view once they are added.',
        action: 'New task',
        backlogTitle: 'No backlog tasks yet',
        backlogBody: 'Tasks captured without an iteration appear here until one is planned.',
    },
    pipeline: {
        body: 'Agent tasks appear here once work is assigned to an agent.',
    },
    analytics: {
        title: 'No iteration to analyse',
        body: 'Analytics shows the delivery and capacity of one iteration.',
    },
    team: {
        membersBody: 'Add a person to start; connected agents appear here too.',
        modelsTitle: 'Models need the admin key',
        modelsBody: 'This tab holds the model catalog and the bindings, and viewing or editing them needs the admin key.',
        connectTitle: 'Connecting an agent needs the admin key',
        connectBody: 'Connecting and editing agents needs the admin key in this browser tab.',
        catalogTitle: 'No models in the catalog yet',
        catalogBody: 'The catalog lists the models agents can run on; add one, then bind agents to it.',
        bindingsTitle: 'No model bindings yet',
        bindingsBody: 'A binding connects an agent to a model from the catalog.',
        unlock: 'Unlock editing',
    },
} as const;

export const emptyStatesRussian = {
    filtered: {
        title: 'Ничего не подходит под фильтры',
        body: 'Сбросьте фильтры, чтобы увидеть всё в этом виде.',
        clear: 'Сбросить фильтры',
    },
    overview: {
        iterationTitle: 'Итераций пока нет',
        iterationBody: 'Итерации содержат мощность, задачи и расписание одного отрезка работы.',
    },
    myWork: {
        queueBody: 'Здесь появятся назначенные вам задачи и проверки, которые вы должны выполнить.',
        inboxBody: 'Здесь появятся уведомления о вашей работе по мере её изменения.',
    },
    triage: {
        emptyTitle: 'Запросов пока нет',
        emptyBody: 'Запросы, которые вы зафиксировали, остаются здесь до проверки.',
        action: 'Новый запрос',
    },
    projects: {
        title: 'Проектов пока нет',
        body: 'Проекты объединяют итерации и задачи одной работы.',
        action: 'Новый проект',
    },
    plan: {
        title: 'Итерация не выбрана',
        body: 'План показывает одну итерацию за раз; её мощность, работа и расписание появятся после создания.',
    },
    gantt: {
        title: 'Нет итерации для показа',
        body: 'Сохранённое расписание итерации появится здесь после его применения.',
    },
    tasks: {
        title: 'Задач пока нет',
        body: 'Задачи этой итерации появятся здесь во всех видах, как только их добавят.',
        action: 'Новая задача',
        backlogTitle: 'В бэклоге задач пока нет',
        backlogBody: 'Задачи, созданные без итерации, появляются здесь, пока их не запланируют.',
    },
    pipeline: {
        body: 'Задачи агентов появятся здесь, когда работа будет назначена агенту.',
    },
    analytics: {
        title: 'Нет итерации для анализа',
        body: 'Аналитика показывает поставку и мощность одной итерации.',
    },
    team: {
        membersBody: 'Добавьте человека, чтобы начать; подключённые агенты тоже появятся здесь.',
        modelsTitle: 'Для моделей нужен ключ администратора',
        modelsBody: 'На этой вкладке хранятся каталог моделей и привязки; просмотр и изменение требуют ключа администратора.',
        connectTitle: 'Для подключения агента нужен ключ администратора',
        connectBody: 'Подключение и изменение агентов требует ключа администратора в этой вкладке браузера.',
        catalogTitle: 'В каталоге пока нет моделей',
        catalogBody: 'В каталоге перечислены модели, на которых могут работать агенты; добавьте модель и привяжите к ней агентов.',
        bindingsTitle: 'Привязок моделей пока нет',
        bindingsBody: 'Привязка связывает агента с моделью из каталога.',
        unlock: 'Открыть редактирование',
    },
} as const;
