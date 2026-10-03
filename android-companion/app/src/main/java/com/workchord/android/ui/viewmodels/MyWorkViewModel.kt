package com.workchord.android.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.workchord.android.data.api.WorkSelection
import com.workchord.android.data.models.*
import com.workchord.android.data.repository.TaskRepository
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Job
import kotlinx.coroutines.ensureActive
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.drop
import kotlinx.coroutines.launch
import kotlin.coroutines.coroutineContext

enum class TaskFilter(val title: String, val queue: String) {
    ALL("All work", "all"), ACTIVE("Active", "active"), QUEUED("Queued", "queued"),
    BLOCKED("Blocked", "blocked"), RESOLVED("Awaiting review", "awaiting_review"), REVIEW("Review work", "review")
}

data class MyWorkUiState(val isLoading: Boolean = true, val isRefreshing: Boolean = false,
    val identity: Identity? = null, val projects: List<Project> = emptyList(), val iterations: List<Iteration> = emptyList(),
    val queues: Map<String, List<TaskReference>> = emptyMap(), val workState: String? = null,
    val selection: WorkSelection = WorkSelection(), val hasMore: Boolean = false, val nextAfterId: Int? = null,
    val filtersSupported: Boolean = false, val errorMessage: String? = null,
    val source: String = "unknown", val fetchedAt: Long? = null) {
    val selectedFilter get() = TaskFilter.entries.firstOrNull { it.queue == selection.queue } ?: TaskFilter.ALL
    val visibleWork get() = if (selectedFilter == TaskFilter.ALL) queues.values.flatten().distinctBy { it.id }
        else queues[selection.queue].orEmpty()
}

class MyWorkViewModel(private val repository: TaskRepository) : ViewModel() {
    private val state = MutableStateFlow(MyWorkUiState(selection = repository.workSelection))
    val uiState = state.asStateFlow()
    private var loadJob: Job? = null
    private var generation = 0L
    private var cached: MyWorkUiState? = null
    private var cachedScope: String? = null

    init {
        loadData()
        viewModelScope.launch { repository.workChanges.drop(1).collect { refresh() } }
    }

    fun loadData() = reload(false)
    fun refresh() = reload(true)
    fun loadMore() {
        if (!state.value.isLoading && state.value.hasMore && state.value.nextAfterId != null) reload(true, true)
    }
    fun setFilter(filter: TaskFilter) = select(state.value.selection.copy(queue = filter.queue))
    fun selectProject(id: Int?) = select(state.value.selection.copy(projectId = id, iterationId = null))
    fun selectIteration(id: Int?) = select(state.value.selection.copy(iterationId = id, backlogOnly = false))
    fun selectBacklog() = select(state.value.selection.copy(iterationId = null, backlogOnly = true))
    fun clearScope() = select(WorkSelection(queue = state.value.selection.queue))
    private fun select(selection: WorkSelection) {
        cached = null
        repository.workSelection = selection
        state.value = state.value.copy(selection = selection, queues = emptyMap(), nextAfterId = null, hasMore = false)
        reload(false)
    }

    private fun reload(refreshing: Boolean, append: Boolean = false) {
        val current = ++generation
        loadJob?.cancel()
        val selection = state.value.selection
        val cursor = if (append) state.value.nextAfterId ?: 0 else 0
        state.value = state.value.copy(isLoading = !refreshing, isRefreshing = refreshing, errorMessage = null)
        loadJob = viewModelScope.launch {
            try {
                val identity = repository.getIdentity().getOrThrow()
                coroutineContext.ensureActive()
                if (!identity.authenticated || identity.principal?.kind != "human" || identity.principal.id < 1) {
                    throw ApiProblem(401, ProblemDetail("authentication_required", "Sign in with a human account to load your work."))
                }
                val capabilities = repository.getCapabilities().getOrThrow()
                require(capabilities.supports("human-my-work-v1")) { "This server cannot provide canonical human work queues. Ask its operator to complete the domain setup." }
                val filters = capabilities.supports("human-my-work-filters-v1")
                val projects = repository.getProjects().getOrThrow()
                val iterations = repository.getIterations().getOrThrow()
                coroutineContext.ensureActive()
                if (current != generation) return@launch
                state.value = state.value.copy(identity = identity, projects = projects, iterations = iterations, filtersSupported = filters)
                require(filters || selection.projectId == null && selection.iterationId == null && !selection.backlogOnly) {
                    "This server cannot apply the saved work filters. Clear the selection or upgrade the server."
                }
                require(selection.projectId == null || projects.any { it.id == selection.projectId }) {
                    "The selected project is no longer accessible. Choose another project."
                }
                require(selection.iterationId == null || iterations.any { it.id == selection.iterationId }) {
                    "The selected iteration is no longer accessible. Choose another scope."
                }
                val work = if (selection.queue == "review") {
                    val page = repository.fetchReviewQueue(selection, cursor).getOrThrow()
                    HumanWork("ready", mapOf("review" to page.items.orEmpty()), page.hasMore, page.nextAfterId)
                } else repository.fetchMyWork(selection, cursor).getOrThrow()
                coroutineContext.ensureActive()
                if (current != generation) return@launch
                require(work.state in setOf("ready", "profile_unlinked", "membership_required")) { "The server returned an unsupported work state." }
                val queues = if (append) (state.value.queues.keys + work.queues.orEmpty().keys).associateWith { key ->
                    (state.value.queues[key].orEmpty() + work.queues.orEmpty()[key].orEmpty()).groupBy { it.id }
                        .map { (_, rows) -> rows.maxByOrNull { it.version ?: -1 }!! }
                } else work.queues.orEmpty()
                state.value = state.value.copy(isLoading = false, isRefreshing = false, identity = identity,
                    projects = projects, iterations = iterations, queues = queues, workState = work.state,
                    hasMore = work.hasMore != false, nextAfterId = work.nextAfterId, filtersSupported = filters,
                    source = "remote", fetchedAt = System.currentTimeMillis())
                cached = state.value
                cachedScope = repository.draftScope
            } catch (error: CancellationException) { throw error }
            catch (error: Exception) {
                if (current == generation) {
                    val temporary = error is java.io.IOException || error is ApiProblem && error.statusCode >= 500
                    val snapshot = cached?.takeIf { temporary && cachedScope == repository.draftScope }
                    if (snapshot != null) state.value = snapshot.copy(isLoading = false, isRefreshing = false, source = "cache",
                        errorMessage = "Cached read-only work. Current access and acceptance are unverified until refresh.")
                    else {
                        cached = null
                        state.value = state.value.copy(isLoading = false, isRefreshing = false,
                            identity = null, projects = emptyList(), iterations = emptyList(), filtersSupported = false,
                            queues = emptyMap(), hasMore = false, nextAfterId = null, source = "unavailable",
                            errorMessage = error.localizedMessage ?: "Could not refresh your work.")
                    }
                }
            }
        }
    }
}
