package com.workchord.android.fakes

import com.workchord.android.data.models.Identity
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.data.models.TaskUpdateRequest
import com.workchord.android.data.models.TaskCommandRequest
import com.workchord.android.data.models.*
import com.workchord.android.data.api.WorkSelection
import com.workchord.android.data.repository.TaskRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.flow

class FakeTaskRepository(
    initialTasks: List<Task> = emptyList(),
    initialSession: Session? = Session(id = 3, publicId = "usr_3", displayName = "Dmitry QA")
) : TaskRepository {

    private val _tasksFlow = MutableStateFlow(initialTasks)
    override val cachedTasks: Flow<List<Task>> = _tasksFlow.asStateFlow()

    var whoAmIResult: Result<Session> = if (initialSession != null) {
        Result.success(initialSession)
    } else {
        Result.failure(Exception("Not logged in"))
    }

    var identityResult: Result<Identity> = Result.success(Identity())

    override suspend fun getIdentity(): Result<Identity> = identityResult

    var fetchTasksResult: Result<List<Task>>? = null
    var getTaskByIdResult: Result<Task>? = null
    var updateTaskStatusResult: Result<Task>? = null
    var updateTaskResult: Result<Task>? = null

    // Call tracking
    var fetchTasksCallCount = 0
    var lastFetchIterationId: Int? = null
    var lastUpdatedTaskId: Int? = null
    var lastUpdatedStatus: TaskStatus? = null
    var lastReason: String? = null
    var lastExpectedVersion: Int? = null
    var lastCommand: String? = null
    override var workSelection = WorkSelection()
    var myWorkResult: Result<HumanWork> = Result.success(HumanWork("ready", emptyMap(), false, null))
    var reviewQueueResult: Result<TaskReferencePage> = Result.success(TaskReferencePage(emptyList(), false, null))
    var projectsResult: Result<List<Project>> = Result.success(listOf(Project(1, "Shared delivery"), Project(9, "Other delivery")))
    var iterationsResult: Result<List<Iteration>> = Result.success(listOf(Iteration(12, "Current iteration", projectId = 1)))
    var capabilitiesResult: Result<DomainCapabilities> = Result.success(DomainCapabilities(1, true,
        listOf("human-my-work-v1", "human-my-work-filters-v1", "task-actions-v1"), currentReviewProjection = true))
    var lastSelection: WorkSelection? = null
    var lastAfterId: Int? = null
    var actionsResult: Result<TaskActions>? = null
    var progressResult: Result<Task>? = null
    var reviewResult: Result<Task>? = null
    var lastProgress: ProgressRequest? = null
    var lastReview: ReviewRequest? = null
    var commandCalls = 0
    private val reviews = mutableListOf<TaskReview>()
    override val draftScope = "fixture-scope"
    private val saved = mutableMapOf<Int, SavedTaskDraft>()
    var cachedDetail: TaskReadState? = null
    override fun cachedReadState(taskId: Int) = cachedDetail?.takeIf { it.detail.task.id == taskId }
    override fun savedDraft(taskId: Int) = saved[taskId]
    override fun saveDraft(taskId: Int, draft: SavedTaskDraft?, expectedScope: String?) {
        check(expectedScope == draftScope)
        if (draft == null) saved.remove(taskId) else saved[taskId] = draft
    }
    override suspend fun getTaskActions(taskId: Int): Result<TaskActions> = actionsResult ?: getTaskById(taskId).map { task ->
        TaskActions(taskId, requireNotNull(task.version), listOf("start_manual", "resolve_manual", "block", "unblock", "cancel", "reopen", "record_progress", "review", "accept_review")
            .map { AllowedAction(it, true, emptyList()) }, 0, emptyList(), emptyList())
    }
    override suspend fun getReviews(taskId: Int): Result<List<TaskReview>> = Result.success(reviews.toList())
    override suspend fun getCurrentReview(taskId: Int): Result<CurrentTaskReview> = getTaskById(taskId).map { task ->
        CurrentTaskReview(requireNotNull(task.version), reviews.lastOrNull { it.taskVersion == task.version })
    }
    override suspend fun recordProgress(taskId: Int, request: ProgressRequest): Result<Task> {
        lastProgress = request
        progressResult?.let { return it }
        val task = getTaskById(taskId).getOrThrow()
        val next = (task.artifactRevision ?: 0) + 1
        val updated = task.copy(version = request.expectedVersion + 1, artifactRevision = next,
            progress = TaskProgress(request.criteria, request.artifacts, task.briefRevision, next))
        setTasks(_tasksFlow.value.map { if (it.id == taskId) updated else it })
        return Result.success(updated)
    }
    override suspend fun reviewTask(taskId: Int, request: ReviewRequest): Result<Task> {
        lastReview = request
        reviewResult?.let { return it }
        val task = getTaskById(taskId).getOrThrow()
        val updated = task.copy(version = request.expectedVersion + 1, statusRaw = if (request.verdict == "accept") "closed" else "active")
        reviews.add(TaskReview(reviews.size + 1, requireNotNull(updated.version), request.briefRevision, request.artifactRevision,
            20, request.verdict, request.reason, request.evidence, "2026-10-03T12:00:00Z"))
        setTasks(_tasksFlow.value.map { if (it.id == taskId) updated else it })
        return Result.success(updated)
    }
    override suspend fun fetchMyWork(selection: WorkSelection, afterId: Int): Result<HumanWork> {
        lastSelection = selection; lastAfterId = afterId; fetchTasksCallCount++
        return myWorkResult
    }
    override suspend fun fetchReviewQueue(selection: WorkSelection, afterId: Int): Result<TaskReferencePage> {
        lastSelection = selection; lastAfterId = afterId
        return reviewQueueResult
    }
    override suspend fun getProjects() = projectsResult
    override suspend fun getIterations() = iterationsResult
    override suspend fun getCapabilities() = capabilitiesResult
    override suspend fun getTaskDetail(taskId: Int): Result<TaskDetail> {
        return getTaskById(taskId).map { TaskDetail(it, emptyList(), true,
            TaskReferencePage(emptyList(), false, null), TaskReferencePage(emptyList(), false, null), false) }
    }

    override suspend fun executeCommand(taskId: Int, request: TaskCommandRequest): Result<Task> {
        commandCalls++
        lastCommand = request.action
        lastReason = request.reason
        lastExpectedVersion = request.expectedVersion
        val task = _tasksFlow.value.firstOrNull { it.id == taskId } ?: return Result.failure(Exception("Task unavailable"))
        val updated = task.copy(blockedReason = if (request.action == "block") request.reason else null,
            canceledAt = if (request.action == "cancel") "2026-10-03T12:00:00Z" else null,
            statusRaw = when (request.action) { "start_manual" -> "active"; "resolve_manual" -> "resolved"; "reopen" -> "planned"; else -> task.statusRaw },
            version = request.expectedVersion + 1)
        _tasksFlow.value = _tasksFlow.value.map { if (it.id == taskId) updated else it }
        return Result.success(updated)
    }

    fun setTasks(tasks: List<Task>) {
        _tasksFlow.value = tasks
    }

    override suspend fun getWhoAmI(): Result<Session> {
        return whoAmIResult
    }

    override suspend fun fetchTasks(iterationId: Int): Result<List<Task>> {
        fetchTasksCallCount++
        lastFetchIterationId = iterationId
        val customResult = fetchTasksResult
        return if (customResult != null) {
            if (customResult.isSuccess) {
                _tasksFlow.value = customResult.getOrNull() ?: emptyList()
            }
            customResult
        } else {
            Result.success(_tasksFlow.value)
        }
    }

    override suspend fun getTaskById(taskId: Int): Result<Task> {
        val custom = getTaskByIdResult
        if (custom != null) return custom

        val found = _tasksFlow.value.firstOrNull { it.id == taskId }
        return if (found != null) {
            Result.success(found)
        } else {
            Result.failure(Exception("Task $taskId not found in fake repository"))
        }
    }

    override suspend fun updateTaskStatus(
        taskId: Int,
        newStatus: TaskStatus,
        reason: String?,
        expectedVersion: Int?
    ): Result<Task> {
        lastUpdatedTaskId = taskId
        lastUpdatedStatus = newStatus
        lastReason = reason
        lastExpectedVersion = expectedVersion

        val custom = updateTaskStatusResult
        if (custom != null) return custom

        val currentList = _tasksFlow.value.toMutableList()
        val index = currentList.indexOfFirst { it.id == taskId }
        if (index >= 0) {
            val oldTask = currentList[index]
            if (expectedVersion != null && oldTask.version != expectedVersion) {
                return Result.failure(Exception("Version conflict: expected $expectedVersion but task is at ${oldTask.version}"))
            }
            val updatedTask = oldTask.copy(
                statusRaw = newStatus.value,
                version = requireNotNull(oldTask.version) + 1
            )
            currentList[index] = updatedTask
            _tasksFlow.value = currentList
            return Result.success(updatedTask)
        }
        return Result.failure(Exception("Task $taskId not found"))
    }

    override suspend fun updateTask(
        taskId: Int,
        request: TaskUpdateRequest
    ): Result<Task> {
        val custom = updateTaskResult
        if (custom != null) return custom

        val currentList = _tasksFlow.value.toMutableList()
        val index = currentList.indexOfFirst { it.id == taskId }
        if (index >= 0) {
            val old = currentList[index]
            val updated = old.copy(
                title = request.title ?: old.title,
                description = request.description ?: old.description,
                priority = request.priority ?: old.priority,
                effortHours = request.effortHours ?: old.effortHours,
                version = requireNotNull(old.version) + 1
            )
            currentList[index] = updated
            _tasksFlow.value = currentList
            return Result.success(updated)
        }
        return Result.failure(Exception("Task $taskId not found"))
    }

    override fun observeTask(taskId: Int): Flow<Task?> = flow {
        _tasksFlow.collect { tasks ->
            emit(tasks.firstOrNull { it.id == taskId })
        }
    }
}
