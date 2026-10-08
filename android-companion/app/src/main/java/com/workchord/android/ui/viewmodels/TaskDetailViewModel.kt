package com.workchord.android.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.workchord.android.data.models.*
import com.workchord.android.data.repository.TaskRepository
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Job
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.withContext
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlin.coroutines.coroutineContext

data class TaskDetailUiState(val isLoading: Boolean = true, val isUpdatingStatus: Boolean = false,
    val task: Task? = null, val detail: TaskDetail? = null, val actions: TaskActions? = null,
    val reviews: List<TaskReview> = emptyList(), val reviewSnapshot: CurrentTaskReview? = null, val draft: EvidenceDraft? = null,
    val reason: String = "", val reviewEvidence: String = "", val errorMessage: String? = null,
    val isLoadingRelations: Boolean = false, val relationError: String? = null,
    val successMessage: String? = null, val conflict: Task? = null, val authoritative: Boolean = false,
    val pendingWriteVersion: Int? = null) {
    val acceptanceCriteria get() = task?.extractAcceptanceCriteria().orEmpty()
    val hasUnsavedInputs get() = draft != null || reason.isNotBlank() || reviewEvidence.isNotBlank() || pendingWriteVersion != null
    val currentReview get() = reviewSnapshot?.review?.takeIf { reviewSnapshot?.taskVersion == task?.version &&
        it.taskVersion == task?.version && it.briefRevision == task?.briefRevision && it.artifactRevision == task?.artifactRevision }
    fun allowed(action: String) = authoritative && pendingWriteVersion == null && !isLoading && !isUpdatingStatus && !isLoadingRelations && actions?.version == task?.version &&
        actions?.actions.orEmpty().any { it.action == action && it.allowed }
    fun blockers(action: String) = actions?.actions.orEmpty().firstOrNull { it.action == action }?.blockers.orEmpty()
}

class TaskDetailViewModel(private val taskId: Int, private val repository: TaskRepository,
    private val ioDispatcher: CoroutineDispatcher = Dispatchers.IO) : ViewModel() {
    private val state = MutableStateFlow(TaskDetailUiState())
    val uiState = state.asStateFlow()
    private var load: Job? = null
    private var relations: Job? = null
    private var generation = 0L
    private var restored = false
    private var scopeAtRead: String? = null
    init { loadTask() }

    fun loadTask() {
        val current = ++generation
        load?.cancel()
        relations?.cancel()
        state.value = state.value.copy(isLoadingRelations = false, relationError = null, isLoading = true, authoritative = false, errorMessage = null)
        load = viewModelScope.launch {
            try {
                val capabilities = repository.getCapabilities().getOrThrow()
                require(capabilities.supports("task-actions-v1") && capabilities.currentReviewProjection == true) {
                    "Upgrade or reconcile the server to provide current action and review projections."
                }
                val detail = repository.getTaskDetail(taskId).getOrThrow()
                val actions = repository.getTaskActions(taskId).getOrThrow()
                val reviews = repository.getReviews(taskId).getOrThrow()
                val currentReview = repository.getCurrentReview(taskId).getOrThrow()
                coroutineContext.ensureActive()
                if (current != generation) return@launch
                require(detail.task.authoritativeVersion != null && actions.taskId == taskId && actions.version == detail.task.version && currentReview.taskVersion == detail.task.version) {
                    "Task state changed while loading. Refresh before taking action."
                }
                state.value = state.value.copy(isLoading = false, task = detail.task, detail = detail,
                    actions = actions, reviews = reviews, reviewSnapshot = currentReview,
                    authoritative = detail.task.status != TaskStatus.UNKNOWN,
                    errorMessage = if (detail.task.status == TaskStatus.UNKNOWN) "This lifecycle state is unsupported. Upgrade the client before executing or reviewing." else null)
                scopeAtRead = repository.draftScope
                if (!restored) {
                    restored = true
                    val saved = withContext(ioDispatcher) { repository.savedDraft(taskId) }
                    coroutineContext.ensureActive()
                    if (current != generation || scopeAtRead != repository.draftScope) return@launch
                    if (saved != null) state.value = state.value.copy(draft = saved.evidence,
                        reason = saved.reason, reviewEvidence = saved.reviewEvidence, pendingWriteVersion = saved.pendingWriteVersion,
                        successMessage = "Saved local draft restored. Compare its version before submitting.")
                }
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) {
                if (current == generation) {
                    val forbidden = error is ApiProblem && error.statusCode in setOf(401, 403, 404)
                    val temporary = error is java.io.IOException || (error is ApiProblem && error.statusCode >= 500)
                    val cached = if (temporary) repository.cachedReadState(taskId) else null
                    state.value = state.value.copy(isLoading = false, authoritative = false,
                        task = cached?.detail?.task, detail = cached?.detail, actions = null, reviewSnapshot = null,
                        reviews = if (forbidden) emptyList() else state.value.reviews,
                        draft = if (forbidden) null else state.value.draft,
                        reason = if (forbidden) "" else state.value.reason,
                        reviewEvidence = if (forbidden) "" else state.value.reviewEvidence,
                        errorMessage = if (cached != null) "Cached read-only data from ${java.time.Instant.ofEpochMilli(cached.fetchedAt)}. Access and acceptance are not verified until a successful refresh."
                            else error.localizedMessage ?: "Could not load current work.")
                }
            }
        }
    }

    fun loadMoreRelations(children: Boolean) {
        val detail = state.value.detail ?: return
        val page = if (children) detail.children else detail.dependencies
        val cursor = page.nextAfterId ?: return
        if (page.hasMore != true || state.value.isLoadingRelations || !state.value.authoritative) return
        if (cursor <= 0 || page.items.orEmpty().lastOrNull()?.id != cursor) {
            state.value = state.value.copy(relationError = "Invalid relation cursor. Reload current work.")
            return
        }
        val current = generation
        val scope = repository.draftScope
        state.value = state.value.copy(isLoadingRelations = true, relationError = null)
        relations?.cancel()
        relations = viewModelScope.launch {
            try {
                val next = repository.getTaskDetailPage(taskId, if (children) cursor else 0, if (children) 0 else cursor).getOrThrow()
                coroutineContext.ensureActive()
                if (current != generation) return@launch
                if (scope != repository.draftScope) {
                    state.value = TaskDetailUiState(isLoading = false, errorMessage = "Account changed. Reload current work.")
                    return@launch
                }
                require(next.task.authoritativeVersion == detail.task.authoritativeVersion) { "Task changed while paging. Reload current work." }
                val received = if (children) next.children else next.dependencies
                require(received.items != null && received.items.orEmpty().all { it.id > cursor } && received.hasMore != null && (received.hasMore != true || (received.nextAfterId ?: 0) > cursor)) {
                    "The relation page is incomplete. Reload current work."
                }
                val combined = received.copy(items = (page.items.orEmpty() + received.items.orEmpty()).distinctBy { it.id })
                val updated = if (children) detail.copy(children = combined) else detail.copy(dependencies = combined)
                state.value = state.value.copy(detail = updated, isLoadingRelations = false)
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) {
                if (current == generation) {
                    if (scope != repository.draftScope || (error is ApiProblem && error.statusCode in setOf(401, 403, 404))) {
                        state.value = TaskDetailUiState(isLoading = false, errorMessage = error.message)
                    } else state.value = state.value.copy(isLoadingRelations = false, relationError = error.message,
                        authoritative = state.value.authoritative && error !is IllegalArgumentException)
                }
            }
        }
    }

    fun setReason(value: String) { state.value = state.value.copy(reason = value) }
    fun setReviewEvidence(value: String) { state.value = state.value.copy(reviewEvidence = value) }
    fun execute(action: String) {
        val before = state.value
        val task = before.task ?: return
        val actions = before.actions ?: return
        if (!before.allowed(action) || before.reason.isBlank()) {
            state.value = before.copy(errorMessage = "Choose an available action and explain the reason.")
            return
        }
        if (actions.claimGeneration == null || actions.runningRunIds == null || actions.liveAssignmentIds == null) {
            state.value = before.copy(errorMessage = "Ownership evidence is incomplete. Refresh before changing this work.")
            return
        }
        mutate(clearInputs = true) { repository.executeCommand(task.id, TaskCommandRequest(action, requireNotNull(task.authoritativeVersion),
            before.reason, actions.claimGeneration, actions.runningRunIds, actions.liveAssignmentIds)) }
    }

    fun beginEvidenceEdit() {
        val before = state.value
        val task = before.task ?: return
        if (!before.allowed("record_progress") || task.brief?.schemaVersion != 1) {
            state.value = before.copy(errorMessage = "A canonical brief and evidence permission are required. Convert legacy text in the web editor first.")
            return
        }
        val criteria = task.extractAcceptanceCriteria().map { CriterionProgress(requireNotNull(it.id), requireNotNull(it.revision), it.state, it.evidence.orEmpty()) }
        state.value = before.copy(draft = EvidenceDraft(task, criteria, task.progress?.artifacts.orEmpty().joinToString("\n")))
    }
    fun setCriterion(id: String, progress: String? = null, evidence: String? = null) {
        val draft = state.value.draft ?: return
        state.value = state.value.copy(draft = draft.copy(criteria = draft.criteria.map {
            if (it.criterionId == id) it.copy(state = progress ?: it.state, evidence = evidence ?: it.evidence) else it
        }))
    }
    fun setArtifacts(value: String) { state.value.draft?.let { state.value = state.value.copy(draft = it.copy(artifacts = value)) } }
    fun discardDraft() {
        if (state.value.isUpdatingStatus) return
        val before = state.value
        val scope = scopeAtRead
        viewModelScope.launch {
            try {
                withContext(ioDispatcher) { repository.saveDraft(taskId,
                    if (before.reason.isNotBlank() || before.reviewEvidence.isNotBlank()) SavedTaskDraft(
                        reason = before.reason, reviewEvidence = before.reviewEvidence, savedAt = System.currentTimeMillis()) else null, scope) }
                state.value = state.value.copy(draft = null, conflict = null, errorMessage = null)
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) { state.value = state.value.copy(errorMessage = error.localizedMessage ?: "Could not discard the saved evidence.") }
        }
    }
    fun discardInputs(onComplete: () -> Unit = {}) {
        if (state.value.isUpdatingStatus) return
        val scope = scopeAtRead
        viewModelScope.launch {
            try {
                withContext(ioDispatcher) { repository.saveDraft(taskId, null, scope) }
                state.value = state.value.copy(draft = null, reason = "", reviewEvidence = "", conflict = null, pendingWriteVersion = null)
                onComplete()
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) { state.value = state.value.copy(errorMessage = error.localizedMessage ?: "Could not discard the saved draft.") }
        }
    }
    fun saveLocalDraft() {
        if (state.value.isUpdatingStatus) return
        val before = state.value
        val scope = scopeAtRead
        viewModelScope.launch {
            try {
                withContext(ioDispatcher) { repository.saveDraft(taskId, SavedTaskDraft(evidence = before.draft,
                    reason = before.reason, reviewEvidence = before.reviewEvidence, savedAt = System.currentTimeMillis(),
                    pendingWriteVersion = before.pendingWriteVersion), scope) }
                state.value = state.value.copy(successMessage = "Draft saved only on this device. It has not changed server progress or acceptance.")
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) { state.value = state.value.copy(errorMessage = error.localizedMessage ?: "Could not save the local draft.") }
        }
    }
    fun saveProgress() {
        val before = state.value
        val draft = before.draft ?: return
        if (!before.allowed("record_progress")) return
        if (draft.criteria.any { it.state == "completed" && it.evidence.isNullOrBlank() }) {
            state.value = before.copy(errorMessage = "Completed criteria require evidence. Your draft is retained.")
            return
        }
        mutate(clearDraft = true) { repository.recordProgress(taskId, ProgressRequest(requireNotNull(draft.base.authoritativeVersion),
            draft.criteria, draft.artifacts.lines().map { it.trim() }.filter { it.isNotBlank() })) }
    }
    fun reconcileDraft() {
        val before = state.value
        val draft = before.draft ?: return
        val task = before.task ?: return
        if (!before.authoritative || task.brief?.schemaVersion != 1) return
        val current = task.brief.acceptanceCriteria.orEmpty().associate { it.id to it.revision }
        if (draft.criteria.any { current[it.criterionId] != it.criterionRevision } || current.size != draft.criteria.size) {
            state.value = before.copy(errorMessage = "Criteria changed. Compare your retained draft with the current brief before starting a new evidence draft.")
            return
        }
        state.value = before.copy(draft = draft.copy(base = task), conflict = null, errorMessage = null)
    }
    fun submitReview(verdict: String) {
        val before = state.value
        val task = before.task ?: return
        val action = if (verdict == "accept") "accept_review" else "review"
        if (verdict !in setOf("accept", "reject") || !before.allowed(action) || before.reason.isBlank() || task.briefRevision == null || task.artifactRevision == null) {
            state.value = before.copy(errorMessage = "Review requires current revisions, an available independent verdict, and a reason.")
            return
        }
        mutate(clearInputs = true) { repository.reviewTask(taskId, ReviewRequest(requireNotNull(task.authoritativeVersion), task.briefRevision,
            task.artifactRevision, verdict, before.reason, before.reviewEvidence)) }
    }

    fun comparePendingWrite() {
        val before = state.value
        if (!before.authoritative || before.isLoading || before.isUpdatingStatus || before.pendingWriteVersion == null) return
        val scope = scopeAtRead
        viewModelScope.launch {
            try {
                withContext(ioDispatcher) { repository.saveDraft(taskId, SavedTaskDraft(evidence = before.draft,
                    reason = before.reason, reviewEvidence = before.reviewEvidence, savedAt = System.currentTimeMillis()), scope) }
                state.value = state.value.copy(pendingWriteVersion = null,
                    successMessage = "Current server work compared. Retained evidence still needs its own version reconciliation.")
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) { state.value = state.value.copy(errorMessage = error.localizedMessage) }
        }
    }

    private fun mutate(clearDraft: Boolean = false, clearInputs: Boolean = false, call: suspend () -> Result<Task>) {
        if (state.value.isUpdatingStatus) return
        val before = state.value
        val version = before.task?.authoritativeVersion ?: return
        val scope = scopeAtRead
        state.value = state.value.copy(isUpdatingStatus = true, errorMessage = null, successMessage = null, pendingWriteVersion = version)
        viewModelScope.launch {
            var sent = false
            try {
                withContext(ioDispatcher) { repository.saveDraft(taskId, SavedTaskDraft(evidence = before.draft,
                    reason = before.reason, reviewEvidence = before.reviewEvidence, savedAt = System.currentTimeMillis(),
                    pendingWriteVersion = version), scope) }
                sent = true
                call().fold(onSuccess = { task ->
                    state.value = state.value.copy(task = task, isUpdatingStatus = false, authoritative = false,
                        draft = if (clearDraft) null else state.value.draft, conflict = null,
                        reason = if (clearInputs) "" else state.value.reason,
                        reviewEvidence = if (clearInputs) "" else state.value.reviewEvidence,
                        pendingWriteVersion = null, successMessage = "Saved on the server. Reloading current work.")
                    val remaining = state.value
                    withContext(ioDispatcher) {
                        repository.saveDraft(taskId, if (remaining.hasUnsavedInputs) SavedTaskDraft(evidence = remaining.draft,
                            reason = remaining.reason, reviewEvidence = remaining.reviewEvidence, savedAt = System.currentTimeMillis()) else null, scope)
                    }
                    loadTask()
                }, onFailure = { error ->
                    val rejected = error is ApiProblem && error.statusCode in 400..499
                    state.value = state.value.copy(isUpdatingStatus = false, authoritative = false,
                        pendingWriteVersion = if (rejected) null else version,
                        conflict = (error as? ApiProblem)?.problem?.currentTask,
                        errorMessage = error.localizedMessage ?: "Save failed. Your inputs are retained.")
                    if (rejected) withContext(ioDispatcher) { repository.saveDraft(taskId, SavedTaskDraft(evidence = before.draft,
                        reason = before.reason, reviewEvidence = before.reviewEvidence, savedAt = System.currentTimeMillis()), scope) }
                })
            } catch (error: CancellationException) { state.value = state.value.copy(isUpdatingStatus = false, authoritative = false); throw error }
            catch (error: Exception) { state.value = state.value.copy(isUpdatingStatus = false, authoritative = false,
                pendingWriteVersion = if (sent) version else null,
                errorMessage = error.localizedMessage ?: "Save could not be verified. Reload before submitting again.") }
        }
    }
    fun clearMessages() { state.value = state.value.copy(errorMessage = null, successMessage = null) }
}
