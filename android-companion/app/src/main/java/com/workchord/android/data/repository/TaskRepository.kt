package com.workchord.android.data.repository

import com.workchord.android.data.api.TokenManager
import com.workchord.android.data.api.WorkChordApi
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Identity
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.data.models.TaskStatusChangeRequest
import com.workchord.android.data.models.TaskUpdateRequest
import com.workchord.android.data.models.TaskCommandRequest
import com.workchord.android.data.models.ApiProblem
import com.workchord.android.data.models.ProblemDetail
import com.workchord.android.data.models.*
import com.workchord.android.data.api.WorkSelection
import kotlinx.coroutines.flow.emptyFlow
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.withContext

interface TaskRepository {
    val cachedTasks: Flow<List<Task>>
    suspend fun getWhoAmI(): Result<Session>
    suspend fun getIdentity(): Result<Identity>
    suspend fun fetchTasks(iterationId: Int): Result<List<Task>>
    suspend fun getTaskById(taskId: Int): Result<Task>
    suspend fun updateTaskStatus(
        taskId: Int,
        newStatus: TaskStatus,
        reason: String? = null,
        expectedVersion: Int? = null
    ): Result<Task>
    suspend fun updateTask(
        taskId: Int,
        request: TaskUpdateRequest
    ): Result<Task>
    fun observeTask(taskId: Int): Flow<Task?>
    suspend fun executeCommand(taskId: Int, request: TaskCommandRequest): Result<Task>
    val workChanges: Flow<Long> get() = emptyFlow()
    var workSelection: WorkSelection
    suspend fun fetchMyWork(selection: WorkSelection, afterId: Int = 0): Result<HumanWork>
    suspend fun fetchReviewQueue(selection: WorkSelection, afterId: Int = 0): Result<TaskReferencePage>
    suspend fun getProjects(): Result<List<Project>>
    suspend fun getIterations(): Result<List<Iteration>>
    suspend fun getCapabilities(): Result<DomainCapabilities>
    suspend fun getTaskDetail(taskId: Int): Result<TaskDetail>
    suspend fun getTaskActions(taskId: Int): Result<TaskActions>
    suspend fun getReviews(taskId: Int): Result<List<TaskReview>>
    suspend fun getCurrentReview(taskId: Int): Result<CurrentTaskReview>
    suspend fun recordProgress(taskId: Int, request: ProgressRequest): Result<Task>
    suspend fun reviewTask(taskId: Int, request: ReviewRequest): Result<Task>
}

class TaskRepositoryImpl(
    private val api: WorkChordApi,
    private val tokenManager: TokenManager,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO
) : TaskRepository {

    private val _tasksFlow = MutableStateFlow<List<Task>>(emptyList())
    override val cachedTasks: Flow<List<Task>> = _tasksFlow.asStateFlow()
    private val cacheLock = Any()
    private var cacheGeneration = 0L
    private var verifiedPrincipal: Int? = null
    private var verifiedServer: String? = null
    private val changes = MutableStateFlow(0L)
    override val workChanges: Flow<Long> = changes.asStateFlow()
    override var workSelection: WorkSelection
        get() = tokenManager.workSelection
        set(value) { tokenManager.workSelection = value }

    private suspend fun <T> read(response: suspend () -> retrofit2.Response<T>): Result<T> = withContext(ioDispatcher) {
        try {
            val result = response()
            if (result.isSuccessful && result.body() != null) Result.success(result.body()!!)
            else Result.failure(ApiProblem.parse(result.code(), result.errorBody()?.string()))
        } catch (error: CancellationException) { throw error }
        catch (error: Exception) { Result.failure(error) }
    }

    override suspend fun fetchMyWork(selection: WorkSelection, afterId: Int): Result<HumanWork> = read {
        api.getMyWork(selection.projectId, selection.iterationId, selection.backlogOnly, afterId)
    }
    override suspend fun fetchReviewQueue(selection: WorkSelection, afterId: Int): Result<TaskReferencePage> = read {
        api.getReviewQueue(selection.projectId, selection.iterationId, selection.backlogOnly, afterId)
    }
    override suspend fun getProjects(): Result<List<Project>> = read { api.getProjects() }
    override suspend fun getIterations(): Result<List<Iteration>> = read { api.getIterations() }
    override suspend fun getCapabilities(): Result<DomainCapabilities> = read { api.getCapabilities() }
    override suspend fun getTaskActions(taskId: Int): Result<TaskActions> = read { api.getTaskActions(taskId) }
    override suspend fun getReviews(taskId: Int): Result<List<TaskReview>> = read { api.getReviews(taskId) }
    override suspend fun getCurrentReview(taskId: Int): Result<CurrentTaskReview> = read { api.getCurrentReview(taskId) }
    override suspend fun recordProgress(taskId: Int, request: ProgressRequest): Result<Task> = mutation(taskId, request.expectedVersion) { api.recordProgress(taskId, request) }
    override suspend fun reviewTask(taskId: Int, request: ReviewRequest): Result<Task> = mutation(taskId, request.expectedVersion) { api.reviewTask(taskId, request) }
    private suspend fun mutation(taskId: Int, expectedVersion: Int, call: suspend () -> retrofit2.Response<Task>): Result<Task> {
        val result = read(call)
        result.getOrNull()?.let { task ->
            if (task.id != taskId || task.authoritativeVersion == null || task.authoritativeVersion!! < expectedVersion) {
                return Result.failure(ApiProblem(502, ProblemDetail("unverified_write_response", "The write response could not be verified. Reload and compare before submitting again.")))
            }
        }
        result.getOrNull()?.let { updateLocalTask(it); changes.value++ }
        return result
    }
    override suspend fun getTaskDetail(taskId: Int): Result<TaskDetail> {
        val result = read { api.getTaskDetail(taskId) }
        result.getOrNull()?.task?.let { updateLocalTask(it) }
        return result
    }

    override suspend fun executeCommand(taskId: Int, request: TaskCommandRequest): Result<Task> =
        mutation(taskId, request.expectedVersion) { api.executeTaskCommand(taskId, request) }

    override suspend fun getIdentity(): Result<Identity> = withContext(ioDispatcher) {
        try {
            val response = api.getIdentity()
            val identity = response.body()
            if (response.isSuccessful && identity != null) {
                synchronized(cacheLock) {
                    val principal = identity.principal?.id?.takeIf { identity.authenticated }
                    if (verifiedPrincipal != principal || verifiedServer != tokenManager.baseUrl || !identity.authenticated) {
                        cacheGeneration++
                        _tasksFlow.value = emptyList()
                    }
                    verifiedPrincipal = principal
                    verifiedServer = tokenManager.baseUrl
                }
                Result.success(identity)
            } else Result.failure(ApiProblem.parse(response.code(), response.errorBody()?.string()))
        } catch (e: CancellationException) {
            throw e
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getWhoAmI(): Result<Session> = withContext(ioDispatcher) {
        try {
            val response = api.getSessionWhoami()
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to get session: ${response.code()} ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun fetchTasks(iterationId: Int): Result<List<Task>> = withContext(ioDispatcher) {
        val generation = synchronized(cacheLock) { cacheGeneration }
        try {
            val response = api.getIterationTasks(iterationId)
            if (response.isSuccessful && response.body() != null) {
                val tasks = response.body()!!
                synchronized(cacheLock) {
                    if (generation != cacheGeneration) {
                        Result.failure(Exception("Identity changed. Reload your work."))
                    } else {
                        _tasksFlow.value = tasks
                        Result.success(tasks)
                    }
                }
            } else {
                Result.failure(Exception("Failed to fetch tasks: ${response.code()} ${response.message()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getTaskById(taskId: Int): Result<Task> = withContext(ioDispatcher) {
        try {
            // First check local cache
            val cached = _tasksFlow.value.firstOrNull { it.id == taskId }
            val response = api.getTaskById(taskId)
            if (response.isSuccessful && response.body() != null) {
                val remoteTask = response.body()!!
                updateLocalTask(remoteTask)
                Result.success(remoteTask)
            } else if (cached != null) {
                Result.success(cached)
            } else {
                Result.failure(Exception("Task $taskId not found: ${response.code()}"))
            }
        } catch (e: Exception) {
            val cached = _tasksFlow.value.firstOrNull { it.id == taskId }
            if (cached != null) {
                Result.success(cached)
            } else {
                Result.failure(e)
            }
        }
    }

    override suspend fun updateTaskStatus(
        taskId: Int,
        newStatus: TaskStatus,
        reason: String?,
        expectedVersion: Int?
    ): Result<Task> = withContext(ioDispatcher) {
        try {
            val currentTask = _tasksFlow.value.firstOrNull { it.id == taskId }
            val versionToUse = expectedVersion ?: currentTask?.version
            if (newStatus == TaskStatus.UNKNOWN || currentTask?.status == TaskStatus.UNKNOWN) {
                return@withContext Result.failure(ApiProblem(422, ProblemDetail("unsupported_task_status", "This lifecycle state is unsupported. Refresh before taking action.")))
            }
            if (versionToUse == null || versionToUse < 1) {
                return@withContext Result.failure(ApiProblem(428, ProblemDetail("task_version_required", "Reload authoritative task state before changing it.")))
            }

            val request = TaskStatusChangeRequest(
                status = newStatus.value,
                reason = reason,
                expectedVersion = versionToUse
            )
            val response = api.changeTaskStatus(taskId, request)
            if (response.isSuccessful && response.body() != null) {
                val updatedTask = response.body()!!.task
                updateLocalTask(updatedTask)
                changes.value++
                Result.success(updatedTask)
            } else {
                val errorBody = response.errorBody()?.string() ?: response.message()
                Result.failure(Exception("Failed to update status: $errorBody"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun updateTask(
        taskId: Int,
        request: TaskUpdateRequest
    ): Result<Task> = withContext(ioDispatcher) {
        try {
            if (request.expectedVersion == null || request.expectedVersion < 1) {
                return@withContext Result.failure(ApiProblem(428, ProblemDetail("task_version_required", "Reload authoritative task state before changing it.")))
            }
            val response = api.updateTask(taskId, request)
            if (response.isSuccessful && response.body() != null) {
                val updatedTask = response.body()!!
                updateLocalTask(updatedTask)
                changes.value++
                Result.success(updatedTask)
            } else {
                val errorBody = response.errorBody()?.string() ?: response.message()
                Result.failure(Exception("Failed to update task: $errorBody"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override fun observeTask(taskId: Int): Flow<Task?> = flow {
        _tasksFlow.collect { tasks ->
            emit(tasks.firstOrNull { it.id == taskId })
        }
    }.flowOn(ioDispatcher)

    private fun updateLocalTask(task: Task) {
        val currentList = _tasksFlow.value.toMutableList()
        val index = currentList.indexOfFirst { it.id == task.id }
        if (index >= 0) {
            currentList[index] = task
        } else {
            currentList.add(task)
        }
        _tasksFlow.value = currentList
    }
}
