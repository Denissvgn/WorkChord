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
    suspend fun fetchTasks(iterationId: Int = 1): Result<List<Task>>
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

    override suspend fun executeCommand(taskId: Int, request: TaskCommandRequest): Result<Task> = withContext(ioDispatcher) {
        try {
            val response = api.executeTaskCommand(taskId, request)
            if (response.isSuccessful && response.body() != null) {
                val updated = response.body()!!
                updateLocalTask(updated)
                Result.success(updated)
            } else Result.failure(ApiProblem.parse(response.code(), response.errorBody()?.string()))
        } catch (error: CancellationException) { throw error }
        catch (error: Exception) { Result.failure(error) }
    }

    override suspend fun getIdentity(): Result<Identity> = withContext(ioDispatcher) {
        synchronized(cacheLock) {
            cacheGeneration++
            _tasksFlow.value = emptyList()
        }
        try {
            val response = api.getIdentity()
            val identity = response.body()
            if (response.isSuccessful && identity != null) Result.success(identity)
            else Result.failure(Exception("Failed to verify identity: ${response.code()}"))
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
