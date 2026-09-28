package com.workchord.android.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.workchord.android.data.models.Identity
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.data.repository.TaskRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.Job
import java.util.ArrayDeque

data class MyWorkUiState(
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val session: Session? = null,
    val identity: Identity? = null,
    val allTasks: List<Task> = emptyList(),
    val activeTasks: List<Task> = emptyList(),
    val assignedQueue: List<Task> = emptyList(),
    val resolvedTasks: List<Task> = emptyList(),
    val errorMessage: String? = null,
    val selectedFilter: TaskFilter = TaskFilter.ALL
)

enum class TaskFilter(val title: String) {
    ALL("All Tasks"),
    ACTIVE("Active"),
    QUEUED("Assigned"),
    RESOLVED("Resolved")
}

class MyWorkViewModel(
    private val repository: TaskRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(MyWorkUiState(isLoading = true))
    val uiState: StateFlow<MyWorkUiState> = _uiState.asStateFlow()

    private var loadJob: Job? = null
    private var loadGeneration = 0L

    init {
        loadData()
        observeRepositoryTasks()
    }

    private fun observeRepositoryTasks() {
        viewModelScope.launch {
            repository.cachedTasks.collect { tasks ->
                updateTaskLists(tasks)
            }
        }
    }

    fun loadData() = reload(refreshing = false)

    fun refresh() = reload(refreshing = true)

    private fun reload(refreshing: Boolean) {
        val generation = ++loadGeneration
        loadJob?.cancel()
        _uiState.update { it.copy(isLoading = !refreshing, isRefreshing = refreshing,
            identity = null, session = null, allTasks = emptyList(), activeTasks = emptyList(),
            assignedQueue = emptyList(), resolvedTasks = emptyList(), errorMessage = null) }
        loadJob = viewModelScope.launch {
            val identityResult = repository.getIdentity()
            if (generation != loadGeneration) return@launch
            val identity = identityResult.getOrNull()
            if (identity?.humanOwnerProfileId == null) {
                _uiState.update { it.copy(isLoading = false, isRefreshing = false,
                    errorMessage = identityResult.exceptionOrNull()?.localizedMessage
                        ?: "My Work requires an authenticated human identity with a linked profile.") }
                return@launch
            }
            val session = repository.getWhoAmI().getOrNull()
            if (generation != loadGeneration) return@launch
            _uiState.update { it.copy(identity = identity, session = session) }
            val result = repository.fetchTasks(iterationId = 1)
            if (generation != loadGeneration) return@launch
            result.fold(
                onSuccess = { tasks ->
                    _uiState.update { it.copy(isLoading = false, isRefreshing = false, errorMessage = null) }
                    updateTaskLists(tasks)
                },
                onFailure = { failure ->
                    _uiState.update { it.copy(isLoading = false, isRefreshing = false, identity = null, session = null,
                        allTasks = emptyList(), activeTasks = emptyList(), assignedQueue = emptyList(), resolvedTasks = emptyList(),
                        errorMessage = failure.localizedMessage ?: "Failed to refresh your work") }
                }
            )
        }
    }

    fun setFilter(filter: TaskFilter) {
        _uiState.update { it.copy(selectedFilter = filter) }
    }

    fun clearError() {
        _uiState.update { it.copy(errorMessage = null) }
    }

    private fun updateTaskLists(incoming: List<Task>) {
        val owner = _uiState.value.identity?.humanOwnerProfileId
        val pending = ArrayDeque(incoming)
        val byId = linkedMapOf<Int, Task>()
        val expanded = mutableSetOf<Int>()
        while (pending.isNotEmpty()) {
            val task = pending.removeFirst()
            val existing = byId[task.id]
            if (existing == null || task.version >= existing.version) byId[task.id] = task
            if (expanded.add(task.id)) pending.addAll(task.children.orEmpty())
        }
        val tasks = if (owner == null) emptyList() else byId.values.filter {
            it.ownerProfileId == owner && !it.isComposite && it.children.isNullOrEmpty() && it.canceledAt == null
        }
        val active = tasks.filter { it.status == TaskStatus.ACTIVE }
        val queued = tasks.filter { it.status == TaskStatus.PLANNED || it.status == TaskStatus.BLOCKED }
        val resolved = tasks.filter { it.status == TaskStatus.RESOLVED || it.status == TaskStatus.CLOSED }

        _uiState.update { state ->
            state.copy(
                allTasks = tasks,
                activeTasks = active,
                assignedQueue = queued,
                resolvedTasks = resolved
            )
        }
    }
}
