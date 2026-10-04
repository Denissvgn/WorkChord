package com.workchord.android.data.repository

import com.workchord.android.data.api.TokenManager
import com.workchord.android.data.api.WorkChordApi
import com.workchord.android.data.api.WorkSelection
import com.workchord.android.data.models.*
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.withContext
import kotlin.coroutines.coroutineContext

interface TaskRepository {
    val cachedTasks: Flow<List<Task>>
    fun cachedReadState(taskId: Int): TaskReadState?
    fun savedDraft(taskId: Int): SavedTaskDraft?
    val draftScope: String?
    fun saveDraft(taskId: Int, draft: SavedTaskDraft?, expectedScope: String?)
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


class TaskRepositoryImpl(private val api: WorkChordApi, private val tokenManager: TokenManager,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO) : TaskRepository {
    private data class Scope(val server: String, val principal: Int?, val generation: Long)
    private fun scope() = Scope(tokenManager.baseUrl, tokenManager.principalId, tokenManager.scopeGeneration)
    private val lock = Any()
    private var boundScope = scope()
    private var epoch = 0L
    private var identityFingerprint: String? = null
    private val tasks = MutableStateFlow<List<Task>>(emptyList())
    private val changes = MutableStateFlow(0L)
    private val details = mutableMapOf<Int, TaskReadState>()
    private val memoryDrafts = mutableMapOf<String, SavedTaskDraft>()
    private val gson = com.google.gson.Gson()
    override val cachedTasks: Flow<List<Task>> = tasks.asStateFlow()
    override val workChanges: Flow<Long> = changes.asStateFlow()
    override var workSelection: WorkSelection
        get() = tokenManager.workSelection
        set(value) { tokenManager.workSelection = value }

    private fun syncScope() {
        if (boundScope != scope()) { epoch++; tasks.value = emptyList(); details.clear(); boundScope = scope(); identityFingerprint = null }
    }
    private fun guard() = synchronized(lock) { syncScope(); scope() to epoch }
    private fun forget(taskId: Int?) = synchronized(lock) {
        epoch++
        if (taskId == null) { tasks.value = emptyList(); details.clear() }
        else { tasks.value = tasks.value.filter { it.id != taskId }; details.remove(taskId) }
    }
    private suspend fun <T> request(taskId: Int? = null, call: suspend () -> retrofit2.Response<T>): Result<T> = withContext(ioDispatcher) {
        val captured = synchronized(lock) { syncScope(); scope() to epoch }
        try {
            val response = call()
            coroutineContext.ensureActive()
            synchronized(lock) {
                if (captured.first != scope() || captured.second != epoch) {
                    syncScope()
                    return@synchronized Result.failure(ApiProblem(409, ProblemDetail("identity_scope_changed", "Account or access changed. Reload current work.")))
                }
                if (!response.isSuccessful || response.body() == null) {
                    val problem = if (response.isSuccessful) ApiProblem(502, ProblemDetail("incomplete_response", "The server returned an incomplete response."))
                        else ApiProblem.parse(response.code(), response.errorBody()?.string())
                    if (response.code() in setOf(401, 403, 404)) forget(taskId)
                    if (response.code() == 401) { tokenManager.invalidateSession(); syncScope() }
                    return@synchronized Result.failure(problem)
                }
                Result.success(response.body()!!)
            }
        } catch (error: CancellationException) { throw error }
        catch (error: Exception) {
            synchronized(lock) {
                if (captured.first != scope() || captured.second != epoch) {
                    syncScope(); Result.failure(ApiProblem(409, ProblemDetail("identity_scope_changed", "Account or access changed. Reload current work.")))
                } else Result.failure(error)
            }
        }
    }
    private fun cache(task: Task, captured: Pair<Scope, Long>): Result<Task> = synchronized(lock) {
        syncScope()
        if (captured.first != scope() || captured.second != epoch) return@synchronized Result.failure(ApiProblem(409,
            ProblemDetail("identity_scope_changed", "Account or access changed. Reload current work.")))
        val prior = tasks.value.firstOrNull { it.id == task.id }
        if (prior?.authoritativeVersion != null && (task.authoritativeVersion == null || task.authoritativeVersion!! < prior.authoritativeVersion!!)) {
            return@synchronized Result.failure(ApiProblem(409, ProblemDetail("stale_read", "An older response was ignored. Reload current work.")))
        }
        tasks.value = tasks.value.filter { it.id != task.id } + task
        Result.success(task)
    }
    private suspend fun mutate(taskId: Int, version: Int, call: suspend () -> retrofit2.Response<Task>): Result<Task> {
        val captured = guard()
        val result = request(taskId, call)
        val task = result.getOrNull() ?: return result
        if (task.id != taskId || task.authoritativeVersion == null || task.authoritativeVersion!! < version) {
            return Result.failure(ApiProblem(502, ProblemDetail("unverified_write_response", "The write response could not be verified. Reload and compare before submitting again.")))
        }
        val stored = cache(task, captured)
        if (stored.isSuccess) changes.value++
        return stored
    }

    override suspend fun getIdentity(): Result<Identity> {
        val captured = guard()
        val result = request { api.getIdentity() }
        result.getOrNull()?.let { identity ->
            synchronized(lock) {
                if (captured.first != scope() || captured.second != epoch) return Result.failure(ApiProblem(409,
                    ProblemDetail("identity_scope_changed", "Account or access changed. Reload current work.")))
                val fingerprint = gson.toJson(listOf(identity.principal?.id, identity.profile?.id, identity.workspaceRole, identity.projects))
                if (identity.authenticated && tokenManager.principalId != null && tokenManager.principalId != identity.principal?.id) {
                    tokenManager.invalidateSession(); syncScope()
                    return Result.failure(ApiProblem(409, ProblemDetail("identity_scope_changed", "Account identity changed. Sign in again.")))
                }
                if (!identity.authenticated || fingerprint != identityFingerprint) forget(null)
                identityFingerprint = fingerprint
                if (!identity.authenticated && (tokenManager.nativeAccessToken != null || tokenManager.principalId != null || tokenManager.cookies.isNotEmpty())) { tokenManager.invalidateSession(); syncScope() }
            }
        }
        return result
    }
    override suspend fun getWhoAmI(): Result<Session> = request { api.getSessionWhoami() }
    override suspend fun getProjects(): Result<List<Project>> = request { api.getProjects() }
    override suspend fun getIterations(): Result<List<Iteration>> = request { api.getIterations() }
    override suspend fun getCapabilities(): Result<DomainCapabilities> = request { api.getCapabilities() }
    override suspend fun fetchMyWork(selection: WorkSelection, afterId: Int): Result<HumanWork> = request {
        api.getMyWork(selection.projectId, selection.iterationId, selection.backlogOnly, afterId)
    }
    override suspend fun fetchReviewQueue(selection: WorkSelection, afterId: Int): Result<TaskReferencePage> = request {
        api.getReviewQueue(selection.projectId, selection.iterationId, selection.backlogOnly, afterId)
    }
    override suspend fun fetchTasks(iterationId: Int): Result<List<Task>> {
        val captured = guard()
        val result = request { api.getIterationTasks(iterationId) }
        result.getOrNull()?.forEach { task ->
            val stored = cache(task, captured)
            if (stored.isFailure) return Result.failure(stored.exceptionOrNull()!!)
        }
        return result
    }
    override suspend fun getTaskById(taskId: Int): Result<Task> {
        val captured = guard()
        val result = request(taskId) { api.getTaskById(taskId) }
        return result.getOrNull()?.let { cache(it, captured) } ?: result
    }
    override suspend fun getTaskDetail(taskId: Int): Result<TaskDetail> {
        val captured = guard()
        val result = request(taskId) { api.getTaskDetail(taskId) }
        val detail = result.getOrNull()
        if (detail != null) {
            if (detail.task.id != taskId || detail.task.authoritativeVersion == null) return Result.failure(ApiProblem(502,
                ProblemDetail("incomplete_task_response", "The server returned incomplete task identity or version information.")))
            val stored = cache(detail.task, captured)
            if (stored.isFailure) return Result.failure(stored.exceptionOrNull()!!)
            synchronized(lock) {
                if (captured.first != scope() || captured.second != epoch) return Result.failure(ApiProblem(409,
                    ProblemDetail("identity_scope_changed", "Account or access changed. Reload current work.")))
                if (tasks.value.firstOrNull { it.id == taskId }?.authoritativeVersion != detail.task.authoritativeVersion) {
                    return Result.failure(ApiProblem(409, ProblemDetail("stale_read", "A newer task response has already been received.")))
                }
                details[taskId] = TaskReadState(detail, System.currentTimeMillis())
            }
        } else if (result.exceptionOrNull() !is ApiProblem) synchronized(lock) {
            details[taskId]?.let { details[taskId] = it.copy(source = "cache", authoritative = false) }
        }
        return result
    }
    override fun cachedReadState(taskId: Int): TaskReadState? = synchronized(lock) {
        syncScope()
        val saved = details[taskId] ?: return@synchronized null
        val latest = tasks.value.firstOrNull { it.id == taskId }
        if (latest?.authoritativeVersion != null && latest.authoritativeVersion!! > (saved.detail.task.authoritativeVersion ?: 0)) {
            saved.copy(detail = saved.detail.copy(task = latest), source = "cache", authoritative = false)
        } else saved
    }
    override suspend fun getTaskActions(taskId: Int): Result<TaskActions> = request(taskId) { api.getTaskActions(taskId) }
    override suspend fun getReviews(taskId: Int): Result<List<TaskReview>> = request(taskId) { api.getReviews(taskId) }
    override suspend fun getCurrentReview(taskId: Int): Result<CurrentTaskReview> = request(taskId) { api.getCurrentReview(taskId) }
    override suspend fun executeCommand(taskId: Int, request: TaskCommandRequest) = mutate(taskId, request.expectedVersion) { api.executeTaskCommand(taskId, request) }
    override suspend fun recordProgress(taskId: Int, request: ProgressRequest) = mutate(taskId, request.expectedVersion) { api.recordProgress(taskId, request) }
    override suspend fun reviewTask(taskId: Int, request: ReviewRequest) = mutate(taskId, request.expectedVersion) { api.reviewTask(taskId, request) }
    override suspend fun updateTask(taskId: Int, request: TaskUpdateRequest): Result<Task> {
        val version = request.expectedVersion?.takeIf { it > 0 } ?: return Result.failure(ApiProblem(428,
            ProblemDetail("task_version_required", "Reload authoritative task state before changing it.")))
        return mutate(taskId, version) { api.updateTask(taskId, request) }
    }
    override suspend fun updateTaskStatus(taskId: Int, newStatus: TaskStatus, reason: String?, expectedVersion: Int?): Result<Task> {
        val captured = guard()
        val current = synchronized(lock) { syncScope(); tasks.value.firstOrNull { it.id == taskId } }
        if (newStatus == TaskStatus.UNKNOWN || current?.status == TaskStatus.UNKNOWN) return Result.failure(ApiProblem(422,
            ProblemDetail("unsupported_task_status", "This lifecycle state is unsupported. Refresh before taking action.")))
        val version = (expectedVersion ?: current?.authoritativeVersion)?.takeIf { it > 0 } ?: return Result.failure(ApiProblem(428,
            ProblemDetail("task_version_required", "Reload authoritative task state before changing it.")))
        val response = request(taskId) { api.changeTaskStatus(taskId, TaskStatusChangeRequest(newStatus.value, reason, version)) }
        val task = response.getOrNull()?.task ?: return Result.failure(response.exceptionOrNull() ?: IllegalStateException("Incomplete write response"))
        if (task.id != taskId || task.authoritativeVersion == null || task.authoritativeVersion!! < version) return Result.failure(ApiProblem(502,
            ProblemDetail("unverified_write_response", "Reload current work before submitting again.")))
        val stored = cache(task, captured)
        if (stored.isSuccess) changes.value++
        return stored
    }
    override fun observeTask(taskId: Int): Flow<Task?> = tasks.map { rows -> rows.firstOrNull { it.id == taskId } }
    override fun savedDraft(taskId: Int): SavedTaskDraft? {
        val key = tokenManager.draftScope() ?: return null
        val raw = tokenManager.draftStorage?.read(key, taskId)
        if (key != tokenManager.draftScope()) return null
        return if (raw != null) runCatching { gson.fromJson(raw, SavedTaskDraft::class.java) }.getOrNull()
            ?.takeIf { it.schemaVersion == 1 && it.savedAt > 0 && (it.evidence == null || it.evidence.base.id == taskId) }
        else memoryDrafts["$key:$taskId"]
    }
    override val draftScope get() = tokenManager.draftScope()
    override fun saveDraft(taskId: Int, draft: SavedTaskDraft?, expectedScope: String?) {
        val key = tokenManager.draftScope() ?: throw IllegalStateException("Verify your account before saving a private draft.")
        check(key == expectedScope) { "Account or server changed. This draft remains quarantined." }
        if (tokenManager.draftStorage != null) tokenManager.draftStorage.write(key, taskId, draft?.let { gson.toJson(it) })
        else if (draft == null) memoryDrafts.remove("$key:$taskId") else memoryDrafts["$key:$taskId"] = draft
    }
}
