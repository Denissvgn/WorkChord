package com.workchord.android.ui.viewmodels

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.workchord.android.data.models.Session
import com.workchord.android.data.models.Task
import com.workchord.android.data.models.TaskStatus
import com.workchord.android.data.repository.TaskRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class MyWorkUiState(
    val isLoading: Boolean = false,
    val isRefreshing: Boolean = false,
    val session: Session? = null,
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

    fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }

            // 1. Fetch Session WhoAmI
            val sessionResult = repository.getWhoAmI()
            val session = sessionResult.getOrNull()

            // 2. Fetch Tasks for Iteration 1
            val tasksResult = repository.fetchTasks(iterationId = 1)
            tasksResult.fold(
                onSuccess = { tasks ->
                    _uiState.update { state ->
                        state.copy(
                            isLoading = false,
                            session = session ?: state.session,
                            errorMessage = null
                        )
                    }
                    updateTaskLists(tasks)
                },
                onFailure = { exception ->
                    _uiState.update { state ->
                        state.copy(
                            isLoading = false,
                            session = session ?: state.session,
                            errorMessage = exception.localizedMessage ?: "Failed to connect to WorkChord server"
                        )
                    }
                }
            )
        }
    }

    fun refresh() {
        viewModelScope.launch {
            _uiState.update { it.copy(isRefreshing = true, errorMessage = null) }
            val tasksResult = repository.fetchTasks(iterationId = 1)
            tasksResult.fold(
                onSuccess = { tasks ->
                    _uiState.update { it.copy(isRefreshing = false, errorMessage = null) }
                    updateTaskLists(tasks)
                },
                onFailure = { exception ->
                    _uiState.update {
                        it.copy(
                            isRefreshing = false,
                            errorMessage = exception.localizedMessage ?: "Failed to refresh tasks"
                        )
                    }
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

    private fun updateTaskLists(tasks: List<Task>) {
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
